import discord, gnupg, os, pymongo, datetime
from discord import app_commands, Button, client, Embed, Intents, Interaction
from discord.ext import commands
from discord.ui import View
from pymongo import MongoClient
from typing import Optional

MONGO_URI = os.getenv("MONGO_URI")
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

mongo_client = MongoClient(MONGO_URI)
database = mongo_client["AutoKicker"]
guild_collection = database.guild_collection


def insert_into_db(guild_entry: dict) -> bool or Exception:
    try:
        guild_collection.update_one({guild_entry}, {"$set": guild_entry}, upsert=True)
        return True
    except pymongo.errors.ServerSelectionTimeoutError:
        insert_into_db(guild_entry)

    except pymongo.errors.BulkWriteError:
        insert_into_db(guild_entry)

    except pymongo.errors.DuplicateKeyError:
        insert_into_db(guild_entry)

    except Exception as e:
        print(e)


class InviteButton(View):
    def __init__(self, support_invite: str):
        super().__init__()

        self.support_invite = support_invite
        self.add_item(
            discord.ui.Button(
                label="🖥️ Source code",
                style=discord.ButtonStyle.green,url="https://github.com/ibnaleem/AutoKicker/blob/main/src/autokicker.py"))

    @discord.ui.button(label="📨 Support Server", style=discord.ButtonStyle.blurple)
    async def support_invite_btn(
        self, interaction: Interaction, button: Button
    ) -> None:
        await interaction.response.send_message(self.support_invite, ephemeral=True)


class AutoKicker(client):
    def __init__(
        self,
        bot_id: int = 1174796137862021190,
        guild_id: int = 1174803169168085132,
        synced: bool = False,
    ) -> None:
        super().__init__(
            command_prefix="!", intents=Intents.default(), owner_id=1110526906106904626
        )

        self.bot_id = bot_id
        self.guild_id = guild_id
        self.guild = discord.Client().fetch_guild(guild_id)
        self.error_channel = discord.Client().fetch_channel(1174862833398333511)
        self.synced = synced
        self.yellow = 0xFFFF00

        def __len__(self) -> int:
            return len(self.guilds)

        def __str__(self) -> str:
            return f"Running with Bot ID: {self.bot_id}\nIgnoring auto kick feature for {self.guild_id}\nRunning in {self} servers"

    async def on_ready(self) -> None:
        try:
            await tree.sync()
            self.synced = True
            await self.change_presence(
                activity=discord.Streaming(
                    name="/help", url="https://twitch.tv/gothamchess"
                )
            )

            print(self)

        except Exception as e:
            print(Exception)

    async def channel_perms_check(self, guild: discord.Guild, message: str) -> bool:
        support_server = self.guild.channel.create_invite(
            reason=f"Support server requested by {guild.owner.name}", max_uses=1
        )
        for channel in guild.channels:
            if (
                isinstance(channel, discord.TextChannel)
                and channel.permissions_for(guild.me).send_messages
            ):
                await channel.send(
                    message,
                    view=InviteButton(str(support_server)),
                )
                return True
            else:
                return False

    async def message_guild_owner(
        self, owner: discord.Member, guild: discord.Guild, message: str
    ) -> None:
        if message == "success":
            message = "✅ **{guild.name} ({guild.id})** was successfully added to my database. Thank you for inviting AutoKick"
        else:
            pass

        try:
            await owner.send(message)
        except discord.Forbidden:
            if (
                self.channel_perms_check(
                    guild,
                    message="success",
                )
                is None
            ):
                if message == "warn":
                    title = "⚠️ Guild Owner Not Informed About Guild Configuration"
                    description = f"Could not inform {guild.owner.mention} **({guild.owner.name})** that their server {guild.name} ({guild.id}) has been configured for auto kicking"
                else:
                    title = "❌ Could Not Configure Guild"
                    description = f"Could not inform {guild.owner.mention} **({guild.owner.name})** that their server {guild.name} ({guild.id}) has **not been configured** for auto kicking"

                em = Embed(title=title, description=description, color=self.yellow)
                em.timestamp = datetime.datetime.utcnow()

                await self.error_channel.send(embed=em)
            else:
                pass

    async def on_guild_join(self, guild) -> None:
        support_server = self.guild.channel.create_invite(
            reason=f"Support server requested by {guild.owner.name}", max_uses=1
        )

        if guild.id != self.guild_id:
            insert_into_db({"guild_id": guild.id, "settings": "true"})

            if insert_into_db:
                await self.message_guild_owner(
                    owner=guild.owner,
                    guild=guild,
                    message=f"✅ **{guild.name} ({guild.id})** was successfully added to my database. Thank you for inviting AutoKick",
                    view=InviteButton(str(support_server)),
                )

                await self.message_guild_owner("warn")

            else:
                await self.message_guild_owner("error")

    async def on_member_join(self, member: discord.Member) -> None:
        def check(member: discord.Member) -> bool:
            if not guild_collection.find_one({"member_id": member.id}):
                if not guild_collection.find_one({"settings": "true"}):
                    return False

                return True

            return False

        if check:
            try:
                await member.kick(
                    reason="Autokicking feature on: member is not whitelisted"
                )
            except commands.BotMissingPermissions:
                guild = member.guild

                await self.message_guild_owner(
                    owner=guild.owner,
                    guild=guild,
                    message=f"❌ Auto-kicking feature not enabled: I am missing permissions to kick members. Please update my role or grant me `MODERATE_MEMBERS` and `KICK_MEMBERS` permissions.",
                )

            except commands.MemberNotFound:
                pass

            except Exception as e:
                print(e)

        else:
            pass


client = AutoKicker() 
tree = app_commands.CommandTree(client)

@tree.command(description="Whitelist a member from auto-kicking")
@app_commands.has_permissions(kick_members=True)
async def whitelist(interaction: Interaction, member: Optional[discord.Member] = None, member_id: Optional[int or str] = None):
    
    command_user = interaction.user

    if (member and not member_id):  
        member_id = member.id

    insert_into_db({"member_id": member_id})

    if insert_into_db:
        await command_user.send_message(f"✅ **{member_id}** has been whitelisted")
    
    else:
        # handle error
        pass
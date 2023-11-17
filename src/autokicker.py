import discord, gnupg, os, pymongo, datetime
from discord import app_commands, Button, Client, Embed, Intents, Interaction
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
        guild_collection.insert_one(guild_entry)
        return True
    except pymongo.errors.ServerSelectionTimeoutError as e:
        print(f"ServerSelectionTimeoutError: {e}")
    except pymongo.errors.BulkWriteError as e:
        print(f"BulkWriteError: {e}")
    except pymongo.errors.DuplicateKeyError as e:
        print(f"DuplicateKeyError: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return False


class InviteButton(View):
    def __init__(self, support_invite: str):
        super().__init__()

        self.support_invite = support_invite
        self.add_item(
            discord.ui.Button(
                label="🖥️ Source code",
                style=discord.ButtonStyle.green,
                url="https://github.com/ibnaleem/AutoKicker/blob/main/src/autokicker.py",
            )
        )

    @discord.ui.button(label="📨 Support Server", style=discord.ButtonStyle.blurple)
    async def support_invite_btn(
        self, interaction: Interaction, button: Button
    ) -> None:
        await interaction.response.send_message(self.support_invite, ephemeral=True)


class AutoKicker(Client):
    def __init__(
        self,
        bot_id: int = 1174796137862021190,
        guild_id: int = 1174803169168085132,
        synced: bool = False,
    ) -> None:
        super().__init__(
            command_prefix="!", intents=Intents.all(), owner_id=1110526906106904626
        )

        self.bot_id = bot_id
        self.guild_id = guild_id
        self.synced = synced
        self.yellow = 0xFFFF00
        self.green = 0x00FF02
        self.support_server = "https://discord.gg/Z38zqxHRFQ"

        @property
        async def guild(self) -> discord.Guild:
            return await self.fetch_guild(self.guild_id)

        @property
        async def error_channel(self) -> discord.TextChannel:
            return await self.fetch_channel(1174862833398333511)

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
                await channel.send(message, view=InviteButton(str(support_server)))
                return True
            else:
                return False

    async def message_guild_owner(
        self, owner: discord.Member, guild: discord.Guild, message: str
    ) -> None:
        if message == "success":
            message = f"✅ **{guild.name}** was successfully added to my database. Thank you for inviting <@{self.bot_id}>"
        else:
            pass

        embed = Embed(description=message, color=self.green)
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text="run /whitelist for whitelisting members")

        try:
            await owner.send(embed=embed, view=InviteButton(str(self.support_server)))
        except discord.Forbidden:
            self.channel_perms_check(guild, message="success")

    async def on_guild_join(self, guild: discord.Guild) -> None:
        if guild.id != self.guild_id:
            insert_into_db({"guild_id": guild.id, "settings": "true"})

            if insert_into_db:
                owner = await guild.fetch_member(guild.owner_id)

                if owner:
                    await self.message_guild_owner(
                        owner=owner,
                        guild=guild,
                        message=f"✅ | **{guild.name}** was successfully added to my database. Thank you for inviting <@{self.bot_id}>",
                    )
                else:
                    print("Owner not found")
            else:
                print("handle error")

    async def on_member_join(self, member: discord.Member) -> None:
        def should_kick(member: discord.Member) -> bool:
            return not guild_collection.find_one(
                {"member_id": member.id}
            ) and guild_collection.find_one({"settings": "true"})

        if should_kick(member):
            try:
                await member.kick(
                    reason="Autokicking feature on: member is not whitelisted"
                )
            except discord.errors.Forbidden:
                guild = member.guild
                await self.message_guild_owner(
                    owner=guild.owner,
                    guild=guild,
                    message="❌ Auto-kicking feature not enabled: I am missing permissions to kick members. "
                    "Please update my role or grant me `KICK_MEMBERS` permission.",
                )
            except Exception as e:
                print(f"An error occurred while kicking member: {e}")
        else:
            pass


client = AutoKicker()
tree = app_commands.CommandTree(client)


@tree.command(description="Whitelist a member from auto-kicking")
@app_commands.checks.has_permissions(kick_members=True)
async def whitelist(
    interaction: Interaction,
    member: Optional[discord.Member] = None,
    member_id: Optional[str] = None,
):
    command_user = interaction.user

    if member and not member_id:
        member_id = str(member.id)

    if member_id is not None:
        try:
            member_id = int(member_id)
        except ValueError:
            await command_user.send("❌ Please provide a valid integer member ID.")
            return

        insert_into_db({"member_id": member_id})

        if insert_into_db:
            try:
                await interaction.response.send_message(
                    f"✅ **{member_id}** has been whitelisted"
                )
            except:
                try:
                    command_user.send(f"✅ **{member_id}** has been whitelisted")

                except discord.Forbidden:
                    pass

        else:
            # handle error
            pass
    else:
        await command_user.send("❌ Please provide a valid member or member ID.")


@tree.command(description="Enable auto-kicking")
@app_commands.checks.has_permissions(kick_members=True)
async def enable(interaction: Interaction):
    command_user = interaction.user
    guild_id = interaction.guild.id

    current_settings = guild_collection.find_one({"settings": {"$exists": True}})

    if current_settings:
        guild_collection.update_one(
            {"settings": {"$exists": True}}, {"$set": {"settings": "true"}}
        )

        try:
            await interaction.response.send_message("✅ Auto-kicking has been enabled.")
        except:
            try:
                await command_user.send_message("✅ Auto-kicking has been enabled.")
            except discord.errors.Forbidden:
                pass
    else:
        guild_collection.insert_one({"guild_id": guild_id, "settings": "true"})

        current_guild = guild_collection.find_one({"guild_id": guild_id})

        if not current_guild:
            guild_collection.insert_one({"guild_id": guild_id, "settings": "true"})

        try:
            await interaction.response.send_message("✅ Auto-kicking has been enabled.")
        except:
            try:
                await command_user.send_message("✅ Auto-kicking has been enabled.")
            except discord.errors.Forbidden:
                pass


@tree.command(description="Disable auto-kicking")
@app_commands.checks.has_permissions(kick_members=True)
async def disable(interaction: Interaction):
    command_user = interaction.user
    guild_id = interaction.guild.id

    current_settings = guild_collection.find_one({"settings": {"$exists": True}})

    if current_settings:
        guild_collection.update_one(
            {"settings": {"$exists": True}}, {"$set": {"settings": "false"}}
        )

        try:
            await interaction.response.send_message("✅ Auto-kicking has been disabled.")
        except:
            try:
                await command_user.send_message("✅ Auto-kicking has been disabled.")
            except discord.errors.Forbidden:
                pass
    else:
        guild_collection.insert_one({"guild_id": guild_id, "settings": "false"})

        current_guild = guild_collection.find_one({"guild_id": guild_id})

        if not current_guild:
            guild_collection.insert_one({"guild_id": guild_id, "settings": "false"})

        try:
            await interaction.response.send_message("✅ Auto-kicking has been disabled.")
        except:
            try:
                await command_user.send_message("✅ Auto-kicking has been disabled.")
            except discord.errors.Forbidden:
                pass


@tree.command(description="Displays help command")
async def help(interaction: Interaction):
    embed = Embed(
        title="AutoKicker Help",
        description="Auto kicks new members until a member is whitelisted via **/whitelist** command.\n\nThere are 3 methods to whitelisting a member\n\n**1. Default using Member ID**\n```/whitelist [member-id]```\n\n**2. Mention**\nIf a member has joined the server *before* AutoKicker (or during the time autokick was disabled), you can mention the member to **/whitelist** them:\n```/whitelist @member-mention```\n\n **3. Risky (Disable AutoKick)\n```/disable```\n\nRemember that you must run **/enable** to re-enable auto-kicking. You check this using **/status**.\n\n**Errors & Support** You can click the button below to join my support server, or **[open an issue on my GitHub](https://github.com/ibnaleem/AutoKicker/issues)**",
        color=client.green,
    )

    embed.set_footer(text="/help", icon_url=client.user.avatar)
    embed.set_thumbnail(url=client.user.avatar)

    await interaction.response.send_message(
        embed=embed, view=InviteButton(str(client.support_server))
    )


client.run(DISCORD_BOT_TOKEN)

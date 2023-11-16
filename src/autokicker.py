import discord, gnupg, os, pymongo
from discord import app_commands, Button, client, Embeds, Intents, Interaction
from discord.ext import commands
from discord.ui import View
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI")
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

mongo_client = MongoClient(MONGO_URI)
database = mongo_client["AutoKicker"]
guild_collection = database.guild_collection

def insert_into_db(guild_entry: dict) -> bool:
    try:
        guild_collection.update_one({guild_entry}, {"$set": guild_entry}, upsert=True)
        return True
    except pymongo.errors.ServerSelectionTimeoutError:
        insert_into_db(guild_entry)

    except pymongo.errors.BulkWriteError:
        insert_into_db(guild_entry)
    
    except pymongo.errors.DuplicateKeyError:
        insert_into_db(guild_entry)

class InviteButton(View):
    def __init__(self, support_invite: str):
        super().__init__()

        self.support_invite = support_invite
        self.add_item(discord.ui.Button(label="🖥️ Source code", style=discord.ButtonStyle.green, url="https://github.com/ibnaleem/AutoKicker/blob/main/src/autokicker.py"))

    @discord.ui.button(label="📨 Support Server", style=discord.ButtonStyle.blurple)
    async def support_invite_btn(self, interaction: Interaction, button: Button) -> None:
        await interaction.response.send_message(self.support_invite, ephemeral=True)

class AutoKicker(client):
    def __init__(self, bot_id:int = 1174796137862021190, guild_id:int = 1174803169168085132, synced:bool = False) -> None:
        super().__init__(command_prefix="!", intents=Intents.default(), owner_id=1110526906106904626)
        
        self.bot_id = bot_id
        self.guild_id = guild_id
        self.guild = self.fetch_guild(guild_id)
        self.synced = synced

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
                    name="/help", url="https://twitch.tv/gothamchess")
            )

            print(self)

        except Exception as e:
            print(Exception)

    async def on_guild_join(self, guild) -> None:

        support_server = self.guild.channel.create_invite(reason=f"Support server requested by {guild.owner.name}", max_uses=1)

        if guild.id != self.guild_id:

            insert_into_db({"guild_id": guild.id})

            if insert_into_db:
                try:
                    await guild.owner.send(f"✅ **{guild.name} ({guild.id})** was successfully added to my database. Thank you for inviting AutoKick", view=InviteButton(str(support_server)))
                except discord.Forbidden:
                    # add more
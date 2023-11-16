from typing import Optional
import discord, gnupg, os
from discord import app_commands, Button, client, Embeds, Intents, Interaction
from discord.ext import commands
from discord.ui import View
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI")
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

mongo_client = MongoClient(MONGO_URI)
database = mongo_client["AutoKicker"]
guild_collection = database.guild_collection

class InviteButton(View):
    def __init__(self, support_invite: str):
        super().__init__()

        self.support_invite = support_invite

    @discord.ui.button(label="📨 Support Server", style=discord.ButtonStyle.blurple)
    async def support_invite_btn(self, interaction: Interaction, button: Button) -> None:
        await interaction.response.send_message(self.support_invite, ephemeral=True)

class AutoKicker(client):
    def __init__(self, bot_id:int = 1174796137862021190, guild_id:int = 1174803169168085132, synced:bool = False) -> None:
        super().__init__(command_prefix="!", intents=Intents.default(), owner_id=1110526906106904626)
        
        self.bot_id = bot_id
        self.guild_id = guild_id
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

import discord, gnupg, os
from discord import app_commands, client, Embeds, Intents, Interaction
from discord.ext import commands
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI")
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")


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

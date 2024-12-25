import discord
import discord.ext.commands as commands
from dotenv import load_dotenv
import os
import structlog

# Setting up logging
logger = structlog.getLogger(__name__)

# Declare intents -- requires message content to be enabled
logger.debug("Declaring bot intents")
intents = discord.Intents.default()
intents.message_content = True

# Creating bot with intents
logger.debug("Creating bot")
bot = commands.Bot(intents=intents, command_prefix='/')

@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user}")

# Getting Discord token
logger.debug("Loading environment variables")
load_dotenv()

if "DISCORD_TOKEN" not in os.environ:
    logger.critical("Discord token not found, please place it at 'DISCORD_TOKEN' environment variable")
    exit(1)

token = os.environ["DISCORD_TOKEN"]

# Start bot
logger.debug("Bot starting")
bot.run(token)
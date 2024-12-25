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

@bot.command(name="track")
async def track_command(ctx, *args):
    logger.info(f"Track command called by user {ctx.message.author}")

@bot.command(name="report")
async def report_command(ctx, *args):
    logger.info(f"Report command called by user {ctx.message.author}")

@bot.command(name="reset")
async def reset_command(ctx, *args):
    logger.info(f"Report command called by user {ctx.message.author}")

@bot.command(name="remove")
async def remove_command(ctx, *args):
    logger.info(f"Remove command called by user {ctx.message.author}")

@bot.command(name="list")
async def list_command(ctx):
    logger.info(f"List command called by user {ctx.message.author}")

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
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
@commands.guild_only()
async def track_command(ctx, *args):
    logger.info(f"Track command called by user {ctx.author}")

@bot.command(name="report")
@commands.guild_only()
async def report_command(ctx, *args):
    logger.info(f"Report command called by user {ctx.author}")

@bot.command(name="reset")
@commands.guild_only()
async def reset_command(ctx, *args):
    logger.info(f"Report command called by user {ctx.author}")

@bot.command(name="remove")
@commands.guild_only()
async def remove_command(ctx, *args):
    logger.info(f"Remove command called by user {ctx.author}")

@bot.command(name="list")
@commands.guild_only()
async def list_command(ctx):
    logger.info(f"List command called by user {ctx.author}")

@bot.event
async def on_command_error(ctx, error):
    logger.debug(f"{error} received from command {ctx.command}")

    # Handle private message errors
    if isinstance(error, commands.errors.NoPrivateMessage):
        logger.info(f"Command '{ctx.command}' incorrectly used in private message by user '{ctx.author}'")
        await ctx.send("Sorry! This command can only be used in servers.")

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
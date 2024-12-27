import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import structlog
import database
from custom_exceptions import *
import datetime
from CustomHelpCommand import CustomHelpCommand

# Setting up logging
logger = structlog.getLogger(__name__)

# Declare intents -- requires message content to be enabled
logger.debug("Declaring bot intents")
intents = discord.Intents.default()
intents.message_content = True

# Creating bot with intents
logger.debug("Creating bot")
bot = commands.Bot(intents=intents, command_prefix='/', help_command=CustomHelpCommand())
# bot = commands.Bot(intents=intents, command_prefix='/')

@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user}")

@bot.command(name="track",
             description = "Add an incident to track, the incident will begin being tracked from the time the command "
                           "is called",
             brief="Add an incident to track",
             usage=f"{bot.command_prefix}track <name>"
             )
@commands.guild_only()
async def track_command(ctx, name: str = commands.parameter(description="Name of the incident to be tracked")):
    logger.info(f"Track command called by user {ctx.author}")
    try:
        logger.debug(f"Adding incident '{name}' to guild '{ctx.guild.id}")
        database.add_incident(ctx.guild.id, name)
    except IncidentAlreadyExistsException:
        logger.info(f"Incident '{name}' already exists in guild '{ctx.guild.id}, nothing done")
        await ctx.send(f"Oops! It looks like incident `{name}` already exists, please use `{bot.command_prefix}reset"
                       f" {name}` to reset it, `{bot.command_prefix}remove {name}` to remove it, or choose another"
                       f" name.")
        return

    logger.debug("Successfully added incident")
    await ctx.send(f"Incident `{name}` successfully created! Use `{bot.command_prefix}report {name}` to see time since"
                   f" last incident or use `{bot.command_prefix}reset {name}` to reset the counter.")

@bot.command(name="report",
             description="Get the time since the last reported incident, will report the time in days, hours, minutes, "
                         "and seconds",
             brief="Get the time since the last reported incident",
             usage=f"{bot.command_prefix}report <name>")
@commands.guild_only()
async def report_command(ctx, arg):
    logger.info(f"Report command called by user {ctx.author}")

    try:
        logger.debug(f"Getting incident '{arg}' from guild '{ctx.guild.id}'")
        incident_time = database.get_incident(ctx.guild.id, arg)
    except NoSuchIncidentException:
        logger.info(f"Incident '{arg}' not found in guild '{ctx.guild.id}'")
        await ctx.send(f"Oops! It looks like incident `{arg}` doesn't exist, use `{bot.command_prefix}track {arg}` to create it.")
        return

    logger.debug("Successfully got incident")

    current_time = datetime.datetime.now()
    delta_time = current_time - incident_time

    time_str = (f"Time since last incident: {delta_time.days} days, {delta_time.seconds / 60 / 60:.0f} hours, "
                f"{delta_time.seconds / 60 % 60:.0f} minutes, {delta_time.seconds % 60 % 60:.0f} seconds")

    await ctx.send(time_str)

@bot.command(
    name="reset",
    description="Reset the counter of the incident, the time will be set to the time the command is run",
    brief="Reset the counter of the incident",
    usage=f"{bot.command_prefix}reset <name>"
    )
@commands.guild_only()
async def reset_command(ctx, *args):
    logger.info(f"Report command called by user {ctx.author}")

@bot.command(name="remove",
             description="Remove the incident from being tracked",
             brief="Remove the incident",
             usage=f"{bot.command_prefix}remove <name>")
@commands.guild_only()
async def remove_command(ctx, *args):
    logger.info(f"Remove command called by user {ctx.author}")

@bot.command(name="list",
             description="List all incidents being tracked in the server",
             brief="List all incidents being tracked",
             usag=f"{bot.command_prefix}list <name>")
@commands.guild_only()
async def list_command(ctx):
    logger.info(f"List command called by user {ctx.author}")

@bot.event
async def on_command_error(ctx, error):
    logger.debug(f"'{error}' received from command '{ctx.command}'")

    # Handle private message errors
    if isinstance(error, commands.errors.NoPrivateMessage):
        logger.info(f"Command '{ctx.command}' incorrectly used in private message by user '{ctx.author}'")
        await ctx.send("Sorry! This command can only be used in servers.")
        return

    if isinstance(error, commands.errors.MissingRequiredArgument):
        logger.info(f"Command '{ctx.command}' used with too few arguments")
        await ctx.send(f"Oops! It looks like you used a command with too few arguments, use `{bot.command_prefix}help`"
                       f" to see syntax for all commands.")
        return

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
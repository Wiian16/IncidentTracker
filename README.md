# Incident Tracker Discord Bot

The Incident Tracker Discord Bot, or just "Incident Tracker", for short, is a discord bot that aims to add a little more
fun to your servers. By tracking "incidents" in your server, whether they're the last time your roommate clogged the 
toilet, the last time someone got lost, or whatever else, this bot want to help you have fun! Continue reading below to
learn more about how to add the bot and begin tracking your "incidents"!

## Adding Incident Tracker to Your Server

Adding Incident Tracker to your sever is easy, simply paste the 
[invite link](https://discord.com/oauth2/authorize?client_id=1322635647470801070) into your browser, and follow the 
discord prompts to add it to your sever.

## Using Incident Tracker

By default, Incident Tracker has no incidents for your server, to add one, use `/track <name>` to start tracking. when
you begin tracking an incident, it begins counting from when the command is first run. 

## Commands

### /help

Displays the help text.

### /list

Lists all incidents being tracked in the server.

### /remove

Remove the incident from being tracked.

Usage: `/remove <name>`

### /report

Get the time since the last reported incident, will report the time in days, hours, minutes, and seconds.

Usage: `/remove <name>`

### /reset

Reset the counter of the incident, the time will be set to the time the command is run.

Usage: `/reset <name>`

### /track

Add an incident to track, the incident will begin being tracked from the time the command is called

Usage: `/track <name>`

## Hosting Your own

If you would like to host your own follow these steps:

1. Download the [repository](https://github.com/Wiian16/IncidentTracker)

    `git clone https://github.com/Wiian16/IncidentTracker`

2. Install dependencies

    `pip install requirements.txt` 

    or your system's package manager

3. Create a discord bot at the [Discord Developer Portal](https://discord.com/developers/applications)

4. Set the following permissions:
    
    - "Bot" > "Privileged Gateway Intents" > "Message Content Intent"

    - "Installation" > "Default Install Settings" > "Guild Install" > "Scopes" > "applicatiopns.commands" and "bot"

    - "Installation" > "Default Install Settings" > "Guild Install" > "Permissions" > "Send Messages"

5. Get you bot's token:

    1. Navigate to "Bot" > "Token" and click "Reset Token"

    2. Copy this token and store it somewhere secure

6. Set `DISCORD_TOKEN` environment variable or place it in a .env file in your project directory

7. Run your bot

    `python3 /path/to/repo/incident_tracker.py`

8. Add your bot to servers using the install link in the Developer Portal under "Installation"

9. The Incident Tracker bot will create a database.json file that holds incidents for all servers it is in, do not
modify this file or remove it unless you want to change the tracked incidents directly

## Important Note

This discord bot is a passion project and a hobby. Because of this, it is self hosted and may not always be available. 
Please be patient if it is not available. Additionally, if you find any bugs, please report them at 
https://github.com/Wiian16/IncidentTracker/issues

## Contributors

[Ian McGillivary](https://github.com/wiian16) -- Creator

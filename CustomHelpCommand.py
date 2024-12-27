import discord
from discord.ext import commands


class CustomHelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__()

    def get_command_signature(self, command: commands.Command, /) -> str:
        return f"/{command.qualified_name} -- {command.short_doc or 'No description provided'}"

    async def send_bot_help(self, mapping, /) -> None:
        embed = discord.Embed(title="Incident Bot Commands", color=discord.Color.blue())
        for cog, commands in mapping.items():
            filtered = await self.filter_commands(commands, sort=True)
            if filtered:
                cog_name = cog.qualified_name if cog else "General Commands"
                embed.add_field(
                    name=cog_name,
                    value="\n".join(self.get_command_signature(c) for c in filtered),
                    inline=False
                )

            embed.set_footer(text="Type `/help command` for more info on a command.")

            await self.get_destination().send(embed=embed)

    async def send_command_help(self, command: commands.Command, /) -> None:
        embed = discord.Embed(title=command.qualified_name, color=discord.Color.blue())

        field_value = (f"Usage: {command.usage or 'Not provided'}"
                       f"\n{command.description or 'No description available'}")

        embed.add_field(
            name="General",
            value=field_value,
            inline=False
        )

        arguments = command.clean_params.values()

        field_value = "\n".join(f"{argument.name} -- {argument.description}" for argument in arguments)

        embed.add_field(
            name="Arguments",
            value=field_value,
            inline=False
        )

        await self.get_destination().send(embed=embed)
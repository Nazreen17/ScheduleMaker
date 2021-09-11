#!/usr/bin/env python

# discord.py Documentation: https://discordpy.readthedocs.io/en/stable/
import os
import discord
from discord.ext import commands
from datetime import datetime

from redacted import CLIENT_TOKEN
from constants import CURRENT_TERM, GITHUB_REPO
from DiscordBotStuff.BotConstants import PREFIX, DEV_IDS

# CLIENT_TOKEN = STR Discord dev bot token


start_datetime = datetime.now()


class CustomHelpCommand(commands.MinimalHelpCommand):
    def __init__(self):
        super().__init__()

    async def send_bot_help(self, mapping):
        beta_help = (f"__**Step 1: Make an ICS file**__"
                     f"```{PREFIX}display <CRN_1> <CRN_2> <CRN_3> ...```\n"
                     f"> Find your CRN codes on MyCampus -> Student Schedule -> Banner Website (Same site you "
                     f"registered for your classes)\n"
                     f"\n"
                     f"__**Step 2: Import ICS to Google Calendar (Or wherever you prefer)**__\n"
                     f"Google it or check the quick documentation:\n"
                     f"https://docs.google.com/document/d/1zgVHCSHJoIqeGINdOmOBZsoW-tphYWR38JG_btiSBpA/"
                     f"edit#heading=h.1kjb12kquobi\n"
                     f"\n"
                     f"**__Note: CRN Not found__**\n"
                     f"If your CRN codes are not being recognised, you may need to send a course update request for "
                     f"that CRN's parent course:\n"
                     f"```{PREFIX}request <Course_1> <Course_2> <Course_3> ...```\n"
                     f"After a request is submitted please wait as the database updates, after which you can use the "
                     f"bot normally.\n")
        await self.get_destination().send(beta_help)

    # Using default discord.ext.commands.MinimalHelpCommand

    """
    async def send_cog_help(self, cog):
        await self.get_destination().send(f"{cog.qualified_name}: {[command.name for command in cog.get_commands()]}")

    async def send_group_help(self, group):
        await self.get_destination().send(f"{group.name}: "
                                          f"{[command.name for index, command in enumerate(group.commands)]}")

    async def send_command_help(self, command):
        await self.get_destination().send(command.name)
    """


client = commands.Bot(command_prefix=PREFIX, owner_ids=DEV_IDS, help_command=CustomHelpCommand())


@client.event
async def on_ready():
    global start_datetime
    start_datetime = datetime.now()

    print(f"Logged in: {client.user.name} ({client.user.id}) @ {start_datetime}")
    await client.change_presence(activity=discord.Game(f"{PREFIX}help"))  # Bot activity status


@client.command(aliases=["shutdown", "goodbye"])
@commands.is_owner()
async def dev_shutdown_bot(ctx):  # "ctx" is required to be called in all commands
    shutdown_datetime = datetime.now()

    print_str = (f"Shutdown: {client.user.name} ({client.user.id}) @ {shutdown_datetime}\n"
                 f"Uptime = {shutdown_datetime - start_datetime}")

    await ctx.reply(f"```{print_str}```", mention_author=True)
    await client.close()

    print(print_str)


@client.command()
async def about(ctx):
    global start_datetime

    await ctx.reply(f"__**Program Status**__\n"
                    f"Current Term = `{CURRENT_TERM}`\n"
                    f"Prefix = `{PREFIX}`\n"
                    f"Uptime Start = `{start_datetime}`\n"
                    f"Uptime = `{datetime.now() - start_datetime}`\n"
                    f"Ping = `{round(client.latency * 1000)} ms`", mention_author=False)


@client.command()
async def github(ctx):
    await ctx.reply(f"__**Github**__\n{GITHUB_REPO}", mention_author=False)


@client.command()
async def ping(ctx):
    await ctx.reply(f"Kinda useless stuff, but ok... `{round(client.latency * 1000)} ms`", mention_author=False)


if __name__ == "__main__":
    # Must run under if __name__ == "__main__": in order to use multi-processing for max template generation

    # Add all cogs in the specified directory
    for filename in os.listdir("DiscordBotStuff/cogs"):
        if filename.endswith(".py"):
            client.load_extension(f"DiscordBotStuff.cogs.{filename[:-3]}")

    client.run(CLIENT_TOKEN)

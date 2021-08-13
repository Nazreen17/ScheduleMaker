#!/usr/bin/env python

# discord.py Documentation: https://discordpy.readthedocs.io/en/stable/
import os

import discord
from discord.ext import commands
from datetime import datetime

from redacted import CLIENT_TOKEN

from DiscordBotStuff.BotConstants import PREFIX, DEV_IDS


# CLIENT_TOKEN = STR Discord dev bot token


class CustomHelpCommand(commands.MinimalHelpCommand):
    def __init__(self):
        super().__init__()

    async def send_bot_help(self, mapping):
        for cog in mapping:
            await self.get_destination().send(f"{cog.qualified_name}: {[command.name for command in mapping[cog]]}")

    async def send_cog_help(self, cog):
        await self.get_destination().send(f"{cog.qualified_name}: {[command.name for command in cog.get_commands()]}")

    async def send_group_help(self, group):
        await self.get_destination().send(f"{group.name}: "
                                          f"{[command.name for index, command in enumerate(group.commands)]}")

    async def send_command_help(self, command):
        await self.get_destination().send(command.name)


# client = commands.Bot(command_prefix=PREFIX, owner_ids=DEV_IDS, help_command=CustomHelpCommand())
client = commands.Bot(command_prefix=PREFIX, owner_ids=DEV_IDS, help_command=commands.MinimalHelpCommand())


@client.event
async def on_ready():
    print(f"Logged in: {client.user.name} ({client.user.id}) @ {datetime.now()} UTC")
    await client.change_presence(activity=discord.Game(f"{PREFIX}help"))  # Bot activity status


@client.command(aliases=["shutdown", "goodbye"])
@commands.is_owner()
async def dev_shutdown_bot(ctx):  # "ctx" is required to be called in all commands
    await ctx.reply(f"```Shutdown: {client.user.name} @ {datetime.now()} UTC```", mention_author=True)
    print(f"Shutdown called via command by: {ctx.message.author.name} ({ctx.message.author.id})")
    await client.close()
    print(f"Shutdown: {client.user.name} ({client.user.id}) @ {datetime.now()} UTC")


@client.command()
async def ping(ctx):
    await ctx.reply(f"Kinda useless stuff, but ok... {round(client.latency * 1000)} ms", mention_author=False)


if __name__ == "__main__":
    # Must run under if __name__ == "__main__": in order to use multi-processing for max template generation
    for filename in os.listdir("DiscordBotStuff/cogs"):
        if filename.endswith(".py"):
            client.load_extension(f"DiscordBotStuff.cogs.{filename[:-3]}")

    client.run(CLIENT_TOKEN)

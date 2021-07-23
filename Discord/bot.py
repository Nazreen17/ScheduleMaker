#!/usr/bin/env python

import discord
from discord.ext import commands

from redacted import CLIENT_TOKEN
from BotConstants import PREFIX


# CLIENT_TOKEN = STR Discord dev bot token


client = commands.Bot(command_prefix=PREFIX)


@client.event
async def on_ready():
    print("Logged in: %s, %s" % (client.user.name, client.user.id))


@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')


# draw_schedule(TermSchedule(list(map(int, crn_codes.split()))))


@client.command(aliases=["image", "picture"])
async def make_image(ctx, *, crn_codes):
    with open("..//PNGMaker/schedule.png", "rb") as f:
        f = discord.File(f, filename="schedule.png")
    await ctx.send(file=f)


client.run(CLIENT_TOKEN)

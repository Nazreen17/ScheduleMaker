#!/usr/bin/env python

import discord
from discord.ext import commands

from redacted import CLIENT_TOKEN
from BotConstants import PREFIX
from DiscordBotStuff.BotExtraProcessing import get_clean_courses_list
from JSONMaxTemplates.MaxTemplateGeneration import generate

# CLIENT_TOKEN = STR Discord dev bot token


client = commands.Bot(command_prefix=PREFIX)


@client.event
async def on_ready():
    print(f"Logged in: {client.user.name} {client.user.id}")


@client.command()
async def ping(ctx):
    await ctx.send(f"Kinda useless stuff, but ok... {round(client.latency * 1000)} ms")


@client.command(aliases=["new", "generate"])
async def make_schedule(ctx, *, course_inputs):
    all_courses_list = get_clean_courses_list(course_inputs)
    max_schedules = generate(all_courses_list)
    ctx.send(f"First: {max_schedules[0]}")


client.run(CLIENT_TOKEN)

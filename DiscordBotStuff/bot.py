#!/usr/bin/env python

from discord.ext import commands

from redacted import CLIENT_TOKEN
from BotConstants import PREFIX
from DiscordBotStuff.BotExtraProcessing import get_clean_courses_list
from MaxScheduleTemplates.MaxTemplateGeneration import generate
from DiscordBotStuff.PNGMaker.Pillow import get_discord_file_png_schedule
from DB.SQLCoursePullController import pull_class
from ClassStructure.TermScheduleStructure import TermSchedule

# CLIENT_TOKEN = STR Discord dev bot token


client = commands.Bot(command_prefix=PREFIX)


@client.event
async def on_ready():
    print(f"Logged in: {client.user.name} {client.user.id}")


@client.command()
async def ping(ctx):
    await ctx.send(f"Kinda useless stuff, but ok... {round(client.latency * 1000)} ms")


@client.command(aliases=["max"])
async def make_max_schedule(ctx, *, course_inputs):
    all_courses_list = get_clean_courses_list(course_inputs)
    max_schedules = generate(all_courses_list)

    await ctx.send(f"Generated {len(max_schedules)} schedules")
    if len(max_schedules) > 0:
        await ctx.send(f"Index 0: {max_schedules[0]}")  # TODO testing use case only

    class_objects_list = []
    for crn in max_schedules[0]:
        for course in all_courses_list:
            class_objects_list += pull_class(fac=course.fac, uid=course.uid, crn=crn)

    temp = TermSchedule()
    temp.add_class(class_objects_list)

    file = get_discord_file_png_schedule(temp)

    await ctx.send(file=file)


client.run(CLIENT_TOKEN)

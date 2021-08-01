#!/usr/bin/env python

# discord.py Documentation: https://discordpy.readthedocs.io/en/stable/

import discord
from discord.ext import commands
from datetime import datetime

from redacted import CLIENT_TOKEN
from constants import ENABLED_OPTIMIZER_OBJECT_LIST
from DiscordBotStuff.BotConstants import PREFIX, DEV_IDS
from DiscordBotStuff.BotExtraProcessing import get_clean_courses_list, is_valid_optimizer
from DiscordBotStuff.BotCallOptimizers import get_optimizer
from MaxSchedule.MaxScheduleGeneration import generate
from COREDB.MaxTemplatePrivateUpdate import update_private_max_template
from COREDB.MaxTemplatePrivatePull import pull_private_max_schedule_crn_2d_list
from COREDB.MaxTemplatePublicUpdate import update_public_max_template
from COREDB.MaxTemplatePublicPull import get_public_id_from_private_course_manifest, \
    pull_public_max_schedule_crn_2d_list
from DiscordBotStuff.PNGMaker.Pillow import draw_png_schedule

# CLIENT_TOKEN = STR Discord dev bot token


client = commands.Bot(command_prefix=PREFIX, owner_ids=DEV_IDS)


# async def command_example(ctx, arg) means send arguments via position after command declaration
# (https://discordpy.readthedocs.io/en/latest/ext/commands/commands.html#positional)
# async def command_example(ctx, *arg) means send all arguments
# (https://discordpy.readthedocs.io/en/latest/ext/commands/commands.html#variable)
# async def command_example(ctx, *, arg) means send all arguments as single arg
# (https://discordpy.readthedocs.io/en/latest/ext/commands/commands.html#keyword-only-arguments)


@client.event
async def on_ready():
    print(f"Logged in: {client.user.name} {client.user.id} @ {datetime.now()} UTC")


@client.command(aliases=["goodbye"])
@commands.is_owner()
async def shutdown_bot(ctx):  # "ctx" is required to be called in all commands
    await ctx.reply(f"```Shutdown: {client.user.name} @ {datetime.now()} UTC```", mention_author=True)
    await client.close()
    print(f"Shutdown: {client.user.name} {client.user.id} @ {datetime.now()} UTC")


@client.command()
async def ping(ctx):
    await ctx.send(f"Kinda useless stuff, but ok... {round(client.latency * 1000)} ms")


@client.command(aliases=["personal"])
async def generate_private_max_template(ctx, *, course_inputs):
    all_courses_list = get_clean_courses_list(course_inputs)

    course_raw_str_list = []
    for course in all_courses_list:
        course_raw_str_list.append(course.get_raw_str())

    public_id_num = get_public_id_from_private_course_manifest(course_raw_str_list=course_raw_str_list)

    if public_id_num < 0:  # No public match, save this private custom max schedule template
        max_schedules = generate(all_courses_list)

        await ctx.reply(f"Generated {len(max_schedules)} schedules", mention_author=False)
        if len(max_schedules) > 0:
            update_private_max_template(max_schedule=max_schedules, discord_user_id=ctx.message.author.id)
    else:  # Public match found
        await ctx.reply("Matching public template already exists. "
                        f"\nPlease use the public template `id = {public_id_num}`", mention_author=False)


@client.command(aliases=["wpublic", "writepublic", "write_public"])
@commands.is_owner()  # Only bot devs and labeled owners can request a public template creation
async def generate_public_max_template(ctx, *, course_inputs):
    all_courses_list = get_clean_courses_list(course_inputs)
    max_schedules = generate(all_courses_list)

    await ctx.reply(f"Generated {len(max_schedules)} schedules", mention_author=False)
    if len(max_schedules) > 0:
        course_raw_str_list = []
        for course in all_courses_list:
            course_raw_str_list.append(course.get_raw_str())

        update_public_max_template(max_schedule=max_schedules, course_raw_str_list=course_raw_str_list)


@client.command(aliases=["templates", "public"])
async def view_public_templates(ctx, public_template_id=None):
    pass


@client.command(aliases=["vprivate", "viewprivate", "view_private"])
@commands.is_owner()
async def view_private_templates(ctx, user_id=None):
    pass


@client.command(aliases=["optimizers"])
async def show_all_optimizers(ctx):
    optimizer_text = ""
    for optimizer in ENABLED_OPTIMIZER_OBJECT_LIST:
        optimizer_text += f"\nName: **{optimizer.name}**\nDescription: {optimizer.description}"
        if ENABLED_OPTIMIZER_OBJECT_LIST.index(optimizer) != len(ENABLED_OPTIMIZER_OBJECT_LIST) - 1:
            optimizer_text += "\n"

    await ctx.reply(f"**Optimizers ({len(ENABLED_OPTIMIZER_OBJECT_LIST)})**\n{optimizer_text}", mention_author=False)


@client.command(aliases=["make"])
async def optimize_max(ctx, template_id, optimizer_name, *additional_optimizer_values):
    if not is_valid_optimizer(optimizer_name):
        raise commands.errors.BadArgument()

    if template_id == "personal":
        max_schedules = pull_private_max_schedule_crn_2d_list(ctx.message.author.id)
    else:
        max_schedules = pull_public_max_schedule_crn_2d_list(template_id)

    completed_optimizer = get_optimizer(max_schedules=max_schedules, optimizer_name=optimizer_name,
                                        optimizer_values=additional_optimizer_values)

    # Generate schedule.png
    single_term_schedule = completed_optimizer.optimal

    # Discord send schedule.png
    draw_png_schedule(single_term_schedule)
    with open("DiscordBotStuff/PNGMaker/schedule.png", "rb") as png_file:
        await ctx.reply(file=discord.File(png_file, "schedule.png"), mention_author=True)

    # Generate results.txt
    results = completed_optimizer.result
    result_txt = f"OPTIMIZER.result =\n{results}\n------------------------------\n"

    with open("DiscordBotStuff/result.txt", "w") as file:
        file.write(result_txt + single_term_schedule.get_raw_str())

    # Discord send results.txt
    with open("DiscordBotStuff/result.txt", "rb") as file:
        await ctx.reply(file=discord.File(file, "result.txt"), mention_author=True)


client.run(CLIENT_TOKEN)

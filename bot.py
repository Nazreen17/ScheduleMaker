#!/usr/bin/env python

# discord.py Documentation: https://discordpy.readthedocs.io/en/stable/

import discord
from discord.ext import commands
from datetime import datetime

from redacted import CLIENT_TOKEN
from enabledOptimizers import ENABLED_OPTIMIZER_OBJECT_LIST
from DiscordBotStuff.BotConstants import PREFIX, DEV_IDS
from FullProcess.GeneralProcessing import get_clean_courses_list, generate_png_and_txt
from FullProcess.CallMaxTemplateProcessing import generate_and_update_db_private_template, \
    generate_and_update_db_public_template, pull_public_details_str, pull_private_details_str
from FullProcess.CallOptimizers import request_optimizer
from FullProcess.GeneralProcessing import make_term_schedule_from_crn_no_overhead
from FullProcess.CallCourseRequester import add_course_requests_via_list, drop_course_requests_via_list

# CLIENT_TOKEN = STR Discord dev bot token


client = commands.Bot(command_prefix=PREFIX, owner_ids=DEV_IDS)


@client.event
async def on_ready():
    print(f"Logged in: {client.user.name} ({client.user.id}) @ {datetime.now()} UTC")
    await client.change_presence(activity=discord.Game(f"{PREFIX}help"))  # Bot activity status


@client.command(aliases=["goodbye"])
@commands.is_owner()
async def dev_shutdown_bot(ctx):  # "ctx" is required to be called in all commands
    await ctx.reply(f"```Shutdown: {client.user.name} @ {datetime.now()} UTC```", mention_author=True)
    print(f"Shutdown called via command by: {ctx.message.author.name} ({ctx.message.author.id})")
    await client.close()
    print(f"Shutdown: {client.user.name} ({client.user.id}) @ {datetime.now()} UTC")


@client.command()
async def ping(ctx):
    await ctx.reply(f"Kinda useless stuff, but ok... {round(client.latency * 1000)} ms", mention_author=False)


@client.command(aliases=["request"])
async def user_course_request(ctx, *course_inputs):
    course_object_list = get_clean_courses_list("".join(course_inputs))

    try:
        add_course_requests_via_list(courses_list=course_object_list)
        await ctx.reply(f"Successfully submitted course update request(s)", mention_author=False)
    except Exception as e:
        raise e


@client.command(aliases=["drop"])
@commands.is_owner()
async def dev_drop_course_request(ctx, *course_inputs):
    course_object_list = get_clean_courses_list("".join(course_inputs))

    try:
        drop_course_requests_via_list(courses_list=course_object_list)
        await ctx.reply(f"Successfully removed course update request(s)", mention_author=False)
    except Exception as e:
        raise e


@client.command(aliases=["personal"])
async def generate_private_max_template(ctx, *course_inputs):
    course_object_list = get_clean_courses_list("".join(course_inputs))

    generate_and_update = generate_and_update_db_private_template(course_object_list=course_object_list,
                                                                  discord_user_id=ctx.message.author.id)

    if generate_and_update:
        await ctx.reply(f"Successfully generated your personal template", mention_author=False)
    else:
        await ctx.reply("ERROR! A public template with the same course manifest exists!\nPlease use `id = {call}`",
                        mention_author=False)


@client.command(aliases=["private"])
async def view_private_templates(ctx):
    printing_str = pull_private_details_str(ctx.message.author.id)
    await ctx.reply(printing_str, mention_author=False)


@client.command(aliases=["vprivate", "viewprivate", "view_private"])
@commands.is_owner()
async def dev_view_private_templates(ctx, user_id):
    printing_str = pull_private_details_str(user_id)
    await ctx.reply(printing_str, mention_author=False)


@client.command(aliases=["wpublic", "writepublic", "write_public"])
@commands.is_owner()
async def dev_generate_public_max_template(ctx, description, *course_inputs):
    course_object_list = get_clean_courses_list("".join(course_inputs))

    try:
        generate_and_update_db_public_template(course_object_list=course_object_list, description=description)
        await ctx.reply(f"Successfully generated public template", mention_author=False)
    except Exception as e:
        raise e


@client.command(aliases=["templates", "public"])
async def view_public_templates(ctx, public_template_id=None):
    printing_str = pull_public_details_str(public_template_id)
    await ctx.reply(printing_str, mention_author=False)


@client.command(aliases=["optimizers"])
async def show_all_optimizers(ctx):
    optimizer_text = ""
    for optimizer in ENABLED_OPTIMIZER_OBJECT_LIST:
        optimizer_text += f"\nName: **{optimizer.name}**\nDescription: {optimizer.description}"
        if ENABLED_OPTIMIZER_OBJECT_LIST.index(optimizer) != len(ENABLED_OPTIMIZER_OBJECT_LIST) - 1:
            optimizer_text += "\n"

    await ctx.reply(f"**Optimizers ({len(ENABLED_OPTIMIZER_OBJECT_LIST)})**\n{optimizer_text}", mention_author=False)


@client.command(aliases=["make"])
async def optimize_max(ctx, template_id, *optimization_requests):
    # Complete command: $ <PublicTemplateId / 'personal'> "<SINGLE_REQUEST#1>" "<SINGLE_REQUEST#1>"
    # <SINGLE_REQUEST#1> format: <OptimizerName>, <ExtraValue#n>, <ExtraValue#n+1>

    request_optimizer(template_id=template_id, request_list=list(optimization_requests),
                      user_discord_id=ctx.message.author.id)

    # Discord send schedule.png
    with open("DiscordBotStuff/PNGMaker/schedule.png", "rb") as png_file:
        await ctx.reply(file=discord.File(png_file, "schedule.png"), mention_author=True)

    # Discord send results.txt
    with open("DiscordBotStuff/result.txt", "rb") as file:
        await ctx.reply(file=discord.File(file, "result.txt"), mention_author=True)


@client.command(aliases=["display"])
async def display_from_crn(ctx, *crn_codes):
    single_term_schedule = make_term_schedule_from_crn_no_overhead(crn_list=crn_codes)

    result_txt = f"Display Source CRNs =\n{crn_codes}\n"

    generate_png_and_txt(single_term_schedule=single_term_schedule, result_txt_header_str=result_txt)

    # Discord send schedule.png
    with open("DiscordBotStuff/PNGMaker/schedule.png", "rb") as png_file:
        await ctx.reply(file=discord.File(png_file, "schedule.png"), mention_author=True)

    # Discord send results.txt
    with open("DiscordBotStuff/result.txt", "rb") as file:
        await ctx.reply(file=discord.File(file, "result.txt"), mention_author=True)


client.run(CLIENT_TOKEN)

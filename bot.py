#!/usr/bin/env python

from discord.ext import commands

from redacted import CLIENT_TOKEN
from DiscordBotStuff.BotConstants import PREFIX, DEV_IDS
from DiscordBotStuff.BotExtraProcessing import get_clean_courses_list
from MaxSchedule.MaxScheduleGeneration import generate
from COREDB.MaxTemplatePrivateUpdate import update_private_max_template

# CLIENT_TOKEN = STR Discord dev bot token


client = commands.Bot(command_prefix=PREFIX, owner_ids=DEV_IDS)


@client.event
async def on_ready():
    print(f"Logged in: {client.user.name} {client.user.id}")


@client.command(aliases=["shutdown"])
@commands.is_owner()
async def shutdown(ctx):
    await ctx.bot.logout()


@client.command()
async def ping(ctx):
    await ctx.send(f"Kinda useless stuff, but ok... {round(client.latency * 1000)} ms")


"""
@client.command(aliases=["wpublic", "writepublic"])
@commands.is_owner()
async def generate_public_max_template(ctx):
    await ctx.bot.logout()
"""

"""
@client.command(aliases=["templates", "public"])
async def view_public_templates(ctx, public_template_id=None):
    pass
"""


@client.command(aliases=["max"])
async def generate_private_max_template(ctx, *, course_inputs):
    all_courses_list = get_clean_courses_list(course_inputs)
    max_schedules = generate(all_courses_list)

    await ctx.reply(f"Generated {len(max_schedules)} schedules", mention_author=False)
    if len(max_schedules) > 0:
        update_private_max_template(max_schedule=max_schedules, discord_user_id=ctx.message.author.id)


"""
@client.command(aliases=["vprivate", "viewprivate"])
@commands.is_owner()
async def view_private_templates(ctx):
    pass
"""

"""
@client.command(aliases=["optimize"])
async def optimize(ctx, template_id=None):
    template_id = ctx.message.author.id if template_id is None else template_id
"""

client.run(CLIENT_TOKEN)

import discord
from discord.ext import commands

from enabledOptimizers import ENABLED_OPTIMIZER_OBJECT_LIST
from FullProcess.CallOptimizers import request_optimizer


class OptimizationCog(commands.Cog):

    @commands.command(aliases=["optimizers", "voptimizers", "viewoptimizers"])
    async def show_all_optimizers(self, ctx):
        optimizer_text = ""
        for optimizer in ENABLED_OPTIMIZER_OBJECT_LIST:
            optimizer_text += f"\nName: **{optimizer.name}**\nDescription: {optimizer.description}"
            if ENABLED_OPTIMIZER_OBJECT_LIST.index(optimizer) != len(ENABLED_OPTIMIZER_OBJECT_LIST) - 1:
                optimizer_text += "\n"

        await ctx.reply(f"**Optimizers ({len(ENABLED_OPTIMIZER_OBJECT_LIST)})**\n{optimizer_text}",
                        mention_author=False)

    @commands.command(aliases=["make"])
    async def optimize_max(self, ctx, template_id, *optimization_requests):
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


def setup(client):
    client.add_cog(OptimizationCog(client))

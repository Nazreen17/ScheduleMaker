import discord
from discord.ext import commands

from enabledOptimizers import ENABLED_OPTIMIZER_OBJECT_LIST
from FullProcess.CallPngAndTextGenerate import generate_png_and_txt
from FullProcess.CallOptimizers import get_requested_optimizer


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

        last_optimizer_obj = get_requested_optimizer(template_id=template_id,
                                                     request_list=list(optimization_requests),
                                                     user_discord_id=ctx.message.author.id)

        optimal_term_schedule = last_optimizer_obj.ties[0]  # Set first optimizer TermSchedule as the best optimal
        result_txt = f"OPTIMIZER.result =\n{last_optimizer_obj.result}\n"  # Set the result text for results.txt

        generate_png_and_txt(single_term_schedule=optimal_term_schedule, result_txt_header_str=result_txt)

        # Discord send schedule.png
        with open("DiscordBotStuff/PNGMaker/schedule.png", "rb") as png_file:
            await ctx.reply(file=discord.File(png_file, "schedule.png"), mention_author=True)

        # Discord send results.txt
        with open("DiscordBotStuff/result.txt", "rb") as file:
            await ctx.reply(file=discord.File(file, "result.txt"), mention_author=True)


def setup(client):
    client.add_cog(OptimizationCog(client))

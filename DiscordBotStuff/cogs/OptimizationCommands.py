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

        try:
            last_optimizer_obj = get_requested_optimizer(template_id=template_id,
                                                         request_list=list(optimization_requests),
                                                         user_discord_id=ctx.message.author.id)

            optimal_term_schedule = last_optimizer_obj.ties[0]  # Set first optimizer TermSchedule as the best optimal
            result_txt = f"OPTIMIZER.result =\n{last_optimizer_obj.result}\n"  # Set the result text for results.txt

            # Generate a png and txt
            generate_png_and_txt(single_term_schedule=optimal_term_schedule, result_txt_header_str=result_txt)

            # Discord send schedule.png
            with open("DiscordBotStuff/PNGMaker/schedule.png", "rb") as png_file:
                await ctx.message.author.send(file=discord.File(png_file, "schedule.png"))

            # Discord send results.txt
            with open("DiscordBotStuff/result.txt", "rb") as file:
                await ctx.message.author.send(file=discord.File(file, "result.txt"))

        except ValueError as e:
            await ctx.reply(f"ValueError -> {e}", mention_author=False)
        except TypeError as e:
            await ctx.reply(f"TypeError -> {e}", mention_author=False)
        except RuntimeError as e:
            await ctx.reply(f"RuntimeError -> {e}", mention_author=False)
        except Exception as e:
            raise e


def setup(client):
    client.add_cog(OptimizationCog(client))

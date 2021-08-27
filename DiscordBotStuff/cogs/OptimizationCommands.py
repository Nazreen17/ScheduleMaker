import discord
from discord.ext import commands

from constants import SCHEDULE_PNG_FILENAME, RESULT_TXT_FILENAME
from CacheFilePathManipulation import get_cache_path
from Optimizations.EnabledOptimizers import ENABLED_OPTIMIZER_OBJECT_LIST
from FullProcess.CallPngAndTextGenerate import generate_png_and_txt
from FullProcess.CallOptimizers import get_requested_optimizer
from CacheFilePathManipulation import remove_file_path


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
            result_text = self.__result_text(last_optimizer_obj)

            # Generate a png and txt
            generate_png_and_txt(single_term_schedule=optimal_term_schedule, result_txt_header_str=result_text,
                                 user_id=ctx.message.author.id)

            # Discord send schedule.png
            path1 = get_cache_path(SCHEDULE_PNG_FILENAME, ctx.message.author.id)
            with open(path1, "rb") as png_file:
                await ctx.message.author.send(file=discord.File(png_file, SCHEDULE_PNG_FILENAME))
            remove_file_path(path1)

            # Discord send results.txt
            path2 = get_cache_path(RESULT_TXT_FILENAME, ctx.message.author.id)
            with open(path2, "rb") as file:
                await ctx.message.author.send(file=discord.File(file, RESULT_TXT_FILENAME))
            remove_file_path(path2)

        except ValueError as e:
            await ctx.reply(f"ValueError -> {e}", mention_author=False)
        except TypeError as e:
            await ctx.reply(f"TypeError -> {e}", mention_author=False)
        except RuntimeError as e:
            await ctx.reply(f"RuntimeError -> {e}", mention_author=False)
        except Exception as e:
            await ctx.reply(f"Something went wrong", mention_author=False)
            raise e

    @staticmethod
    def __result_text(last_optimizer_obj):
        result_txt = ""

        # Ties Count
        result_txt += f"OPTIMIZER.result =\n{last_optimizer_obj.result}\n"  # Set the result text for results.txt

        # Combine all Ties as CRN codes if there are less than or equal to 50
        if len(last_optimizer_obj.ties) <= 50:
            crn_code_str = ""

            for term_schedule in last_optimizer_obj.ties:
                crn_code_str += "\n" + (" ".join([str(class_obj.crn) for class_obj in term_schedule.classes]))

            result_txt += f"\nTies as CRN Codes:{crn_code_str}"

        return result_txt


def setup(client):
    client.add_cog(OptimizationCog(client))

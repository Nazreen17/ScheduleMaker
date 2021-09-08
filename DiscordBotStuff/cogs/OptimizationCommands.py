import discord
from discord.ext import commands

from constants import SCHEDULE_PNG_FILENAME, RESULT_TXT_FILENAME, CALENDAR_ICS_FILENAME
from CacheFilePathManipulation import get_cache_path
from Optimizations.enabledOptimizers import ENABLED_OPTIMIZER_OBJECT_LIST
from FullProcess.CallPngTxtCsvGenerate import generate_triple_png_txt_csv
from FullProcess.CallOptimizers import get_requested_optimizer
from FullProcess.CallResultTextGenerate import full_result_text
from FullProcess.CallGeneralProcesses import remove_dupes
from CacheFilePathManipulation import remove_file_path


class OptimizationCog(commands.Cog):

    @commands.command(aliases=["optimizers", "voptimizers", "viewoptimizers"])
    async def show_all_optimizers(self, ctx):
        optimizer_text = ""
        for optimizer in ENABLED_OPTIMIZER_OBJECT_LIST:
            optimizer_text += f"\nName: **{optimizer.name}**\nDescription: {optimizer.description}"
            if ENABLED_OPTIMIZER_OBJECT_LIST.index(optimizer) != len(ENABLED_OPTIMIZER_OBJECT_LIST) - 1:
                optimizer_text += "\n"

        await ctx.send(f"**Optimizers ({len(ENABLED_OPTIMIZER_OBJECT_LIST)})**\n{optimizer_text}",
                       mention_author=False)

    @commands.command(aliases=["make"])
    async def optimize_max(self, ctx, template_id, *optimization_requests):
        # Complete command: $ <PublicTemplateId / 'personal'> "<SINGLE_REQUEST#1>" "<SINGLE_REQUEST#1>"
        # <SINGLE_REQUEST#1> format: <OptimizerName>, <ExtraValue#n>, <ExtraValue#n+1>

        try:
            optimization_requests = remove_dupes(optimization_requests)

            # Don't call clean() for optimization_requests since it uses "," in the command
            last_optimizer_obj = get_requested_optimizer(template_id=template_id,
                                                         request_list=list(optimization_requests),
                                                         user_discord_id=ctx.message.author.id)

            optimal_term_schedule = last_optimizer_obj.ties[0]  # Set first optimizer TermSchedule as the best optimal
            result_text = self.__result_text(last_optimizer_obj, optimal_term_schedule)

            # Generate a png and txt
            generate_triple_png_txt_csv(single_term_schedule=optimal_term_schedule, result_txt_header_str=result_text,
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

            # Discord send calendar.csv
            path3 = get_cache_path(CALENDAR_ICS_FILENAME, ctx.message.author.id)
            with open(path3, "rb") as csv_file:
                await ctx.message.author.send(file=discord.File(csv_file, CALENDAR_ICS_FILENAME))
            remove_file_path(path3)

        except ValueError as e:
            await ctx.send(f"ValueError -> {e}")
        except TypeError as e:
            await ctx.send(f"TypeError -> {e}")
        except RuntimeError as e:
            await ctx.send(f"RuntimeError -> {e}")
        except Exception as e:
            await ctx.send(f"Something went wrong")
            raise e

        await ctx.message.delete()  # Delete original message

    @staticmethod
    def __result_text(last_optimizer_obj, result_term_schedule):
        result_txt = ""

        # Ties Count
        result_txt += f"Optimizer Result Data:\n{last_optimizer_obj.result}\n\n"  # Set the result text for results.txt

        # Generate result text
        result_txt += full_result_text(term_schedule=result_term_schedule)

        # Combine all Ties as CRN codes if there are less than or equal to 50
        crn_code_str = ""
        max_show_results = 10

        for i, term_schedule in enumerate(last_optimizer_obj.ties[:max_show_results]):
            crn_code_str += f"\n{i + 1}) " + (", ".join([str(class_obj.crn) for class_obj in term_schedule.classes]))

        result_txt += f"\nTop {max_show_results} results:{crn_code_str}"

        return result_txt


def setup(client):
    client.add_cog(OptimizationCog(client))

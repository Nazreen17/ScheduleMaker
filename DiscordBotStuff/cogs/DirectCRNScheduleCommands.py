import discord
from discord.ext import commands

from constants import SCHEDULE_PNG_FILENAME, RESULT_TXT_FILENAME, CALENDAR_ICS_FILENAME
from CacheFilePathManipulation import get_cache_path
from FullProcess.CallGeneralProcesses import clean, remove_dupes
from FullProcess.CallPngTxtCsvGenerate import generate_triple_png_txt_csv
from FullProcess.CallDirectScheduleFromCRNs import generate_term_schedule_from_crn_list
from FullProcess.CallResultTextGenerate import full_result_text
from FullProcess.CallStatRecord import call_add_stat
from CacheFilePathManipulation import remove_file_path


class DirectCRNScheduleCog(commands.Cog):

    @commands.command(aliases=["display"])
    async def display_from_crn(self, ctx, *crn_codes):
        try:
            crn_codes = remove_dupes(crn_codes)
            crn_codes = clean(crn_codes)
            single_term_schedule = generate_term_schedule_from_crn_list(crn_codes)

            # Generate result text
            result_txt = full_result_text(term_schedule=single_term_schedule, search_crn_codes=crn_codes)

            # Generate a png and txt
            generate_triple_png_txt_csv(single_term_schedule=single_term_schedule, result_txt_header_str=result_txt,
                                        user_id=ctx.message.author.id)

            call_add_stat("display")  # Add new display stat record

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


def setup(client):
    client.add_cog(DirectCRNScheduleCog(client))

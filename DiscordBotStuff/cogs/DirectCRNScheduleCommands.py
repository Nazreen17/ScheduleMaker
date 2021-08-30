import discord
from discord.ext import commands

from constants import SCHEDULE_PNG_FILENAME, RESULT_TXT_FILENAME, CALENDAR_CVS_FILENAME
from CacheFilePathManipulation import get_cache_path
from FullProcess.CallPngTxtCvsGenerate import generate_triple_png_txt_cvs
from FullProcess.CallDirectScheduleFromCRNs import generate_term_schedule_from_crn_list
from CacheFilePathManipulation import remove_file_path


class DirectCRNScheduleCog(commands.Cog):

    @commands.command(aliases=["display"])
    async def display_from_crn(self, ctx, *crn_codes):
        try:
            single_term_schedule = generate_term_schedule_from_crn_list(crn_codes)

            warning_message = ""

            # Check for possible bad crn codes
            if len(single_term_schedule.classes) != len(crn_codes):
                warning_message += f"WARNING! Could not find all originally specified CRN codes.\n"

            # Check for possible time conflict
            if not single_term_schedule.is_time_valid():
                warning_message += "WARNING! Time conflict detected.\n"

            # Check for link satisfaction
            if not single_term_schedule.all_links_satisfied():
                warning_message += "WARNING! Class links are unsatisfied.\n"

            # Check for open seats
            if not single_term_schedule.all_open_seats():
                warning_message += "WARNING! Some classes may have no seats left.\n"

            # Send possible error messages
            if len(warning_message) > 0:
                await ctx.message.author.send(warning_message)

            # Generate Result text
            found_crn_code_matches = []
            for class_object in single_term_schedule.classes:
                found_crn_code_matches.append(str(class_object.crn))  # Cast as str to ensure .join works

            crn_codes_str = ", ".join(found_crn_code_matches)  # Join as a string
            result_txt = f"Display Source CRNs =\n{crn_codes_str}\n{warning_message}"

            # Generate a png and txt
            generate_triple_png_txt_cvs(single_term_schedule=single_term_schedule, result_txt_header_str=result_txt,
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

            # Discord send calendar.cvs
            path3 = get_cache_path(CALENDAR_CVS_FILENAME, ctx.message.author.id)
            with open(path3, "rb") as cvs_file:
                await ctx.message.author.send(file=discord.File(cvs_file, CALENDAR_CVS_FILENAME))
            remove_file_path(path3)

        except ValueError as e:
            await ctx.reply(f"ValueError -> {e}", mention_author=False)
        except TypeError as e:
            await ctx.reply(f"TypeError -> {e}", mention_author=False)
        except RuntimeError as e:
            await ctx.reply(f"RuntimeError -> {e}", mention_author=False)
        except Exception as e:
            await ctx.reply(f"Something went wrong", mention_author=False)
            raise e


def setup(client):
    client.add_cog(DirectCRNScheduleCog(client))

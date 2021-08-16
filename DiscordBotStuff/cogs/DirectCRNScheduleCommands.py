import discord
from discord.ext import commands

from FullProcess.CallPngAndTextGenerate import generate_png_and_txt
from FullProcess.CallDirectScheduleFromCRNs import generate_term_schedule_from_crn_list


class DirectCRNScheduleCog(commands.Cog):

    @commands.command(aliases=["display"])
    async def display_from_crn(self, ctx, *crn_codes):
        try:
            single_term_schedule = generate_term_schedule_from_crn_list(crn_codes)

            # Check for possible bad crn codes
            if len(single_term_schedule.classes) != len(crn_codes):
                await ctx.reply("Warning! Some CRN codes specified could not be found", mention_author=False)

            # Generate Result text
            found_crn_code_matches = []
            for class_object in single_term_schedule.classes:
                found_crn_code_matches.append(str(class_object.crn))  # Cast as str to ensure .join works

            crn_codes_str = ", ".join(found_crn_code_matches)  # Join as a string
            result_txt = f"Display Source CRNs =\n{crn_codes_str}\n"

            # Generate a png and txt
            generate_png_and_txt(single_term_schedule=single_term_schedule, result_txt_header_str=result_txt)

            # Discord send schedule.png
            with open("DiscordBotStuff/PNGMaker/schedule.png", "rb") as png_file:
                await ctx.reply(file=discord.File(png_file, "schedule.png"), mention_author=True)

            # Discord send results.txt
            with open("DiscordBotStuff/result.txt", "rb") as file:
                await ctx.reply(file=discord.File(file, "result.txt"), mention_author=True)

        except ValueError as e:
            await ctx.reply(f"ValueError -> {e}", mention_author=False)
        except TypeError as e:
            await ctx.reply(f"TypeError -> {e}", mention_author=False)
        except RuntimeError as e:
            await ctx.reply(f"RuntimeError -> {e}", mention_author=False)
        except Exception as e:
            raise e


def setup(client):
    client.add_cog(DirectCRNScheduleCog(client))

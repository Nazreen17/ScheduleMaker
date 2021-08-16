import discord
from discord.ext import commands

from FullProcess.CallPngAndTextGenerate import generate_png_and_txt
from FullProcess.CallGeneralProcesses import make_term_schedule_from_crn_no_overhead


class DirectCRNScheduleCog(commands.Cog):

    @commands.command(aliases=["display"])
    async def display_from_crn(self, ctx, *crn_codes):
        single_term_schedule = make_term_schedule_from_crn_no_overhead(crn_list=crn_codes)

        result_txt = f"Display Source CRNs =\n{crn_codes}\n"

        generate_png_and_txt(single_term_schedule=single_term_schedule, result_txt_header_str=result_txt)

        # Discord send schedule.png
        with open("DiscordBotStuff/PNGMaker/schedule.png", "rb") as png_file:
            await ctx.reply(file=discord.File(png_file, "schedule.png"), mention_author=True)

        # Discord send results.txt
        with open("DiscordBotStuff/result.txt", "rb") as file:
            await ctx.reply(file=discord.File(file, "result.txt"), mention_author=True)


def setup(client):
    client.add_cog(DirectCRNScheduleCog(client))

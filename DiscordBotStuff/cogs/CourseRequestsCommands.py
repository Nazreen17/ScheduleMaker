from discord.ext import commands

from FullProcess.CallCourseRequester import add_course_requests_via_list, drop_course_requests_via_list, \
    pull_course_requests_as_str
from FullProcess.GeneralProcessing import get_clean_courses_list


class CourseRequestCog(commands.Cog):

    @commands.command(aliases=["request"])
    async def add_course_requests(self, ctx, *course_inputs):
        course_object_list = get_clean_courses_list("".join(course_inputs))

        try:
            add_course_requests_via_list(courses_list=course_object_list)
            await ctx.reply(f"Successfully submitted course update request(s)", mention_author=False)
        except ValueError as e:
            await ctx.reply(f"ValueError -> {e}", mention_author=False)
        except TypeError as e:
            await ctx.reply(f"TypeError -> {e}", mention_author=False)
        except RuntimeError as e:
            await ctx.reply(f"RuntimeError -> {e}", mention_author=False)
        except Exception as e:
            raise e

    @commands.command(aliases=["vrequest", "viewrequest", "vrequests", "viewrequests"])
    async def view_all_course_requests(self, ctx):
        printing_str = pull_course_requests_as_str()
        await ctx.reply(printing_str, mention_author=False)

    @commands.command(aliases=["droprequest", "droprequests"])
    @commands.is_owner()
    async def drop_course_requests(self, ctx, *course_inputs):
        course_object_list = get_clean_courses_list("".join(course_inputs))

        drop_course_requests_via_list(courses_list=course_object_list)
        await ctx.reply(f"Successfully removed course update request(s)", mention_author=False)


def setup(client):
    client.add_cog(CourseRequestCog(client))

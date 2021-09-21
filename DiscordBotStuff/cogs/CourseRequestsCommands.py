from discord.ext import commands

from FullProcess.CallCourseRequester import add_course_requests_via_list, drop_course_requests_via_list, \
    pull_course_requests_as_str
from FullProcess.CallGeneralProcesses import get_clean_courses_list, remove_dupes


class CourseRequestCog(commands.Cog):

    @commands.command(aliases=["update"])
    async def add_course_update_requests(self, ctx, *course_inputs):
        try:
            if len(course_inputs) > 0:
                course_inputs = remove_dupes(course_inputs)

                course_object_list = get_clean_courses_list("".join(course_inputs))
                add_course_requests_via_list(courses_list=course_object_list)

                await ctx.send(f"Successfully submitted course(s) update request")
            else:
                raise ValueError("Missing course input arguments")

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

    @commands.command(aliases=["vupdate", "viewupdate", "vupdates", "viewupdates"])
    async def view_all_course_update_requests(self, ctx):
        printing_str = pull_course_requests_as_str()
        await ctx.reply(f"```{printing_str}```", mention_author=True)

    @commands.command(aliases=["dropupdate", "dropupdates"])
    @commands.is_owner()
    async def drop_course_update_requests(self, ctx, *course_inputs):
        try:
            course_object_list = get_clean_courses_list("".join(course_inputs))
            drop_course_requests_via_list(courses_list=course_object_list)

            await ctx.reply(f"Successfully removed course update request(s)", mention_author=True)

        except ValueError as e:
            await ctx.reply(f"ValueError -> {e}", mention_author=True)
        except TypeError as e:
            await ctx.reply(f"TypeError -> {e}", mention_author=True)
        except RuntimeError as e:
            await ctx.reply(f"RuntimeError -> {e}", mention_author=True)
        except Exception as e:
            await ctx.reply(f"Something went wrong", mention_author=True)
            raise e


def setup(client):
    client.add_cog(CourseRequestCog(client))

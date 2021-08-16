from discord.ext import commands

from FullProcess.CallMaxTemplateProcessing import generate_and_update_db_private_template, \
    pull_private_details_str
from FullProcess.CallGeneralProcesses import get_clean_courses_list, raise_value_error_for_unknown_course_on_db


class PrivateMaxScheduleCog(commands.Cog):

    @commands.command(aliases=["personal"])
    async def generate_private_max_template(self, ctx, *course_inputs):
        try:
            course_object_list = get_clean_courses_list("".join(course_inputs))
            raise_value_error_for_unknown_course_on_db(course_object_list)

            generate_and_update_db_private_template(course_object_list=course_object_list,
                                                    discord_user_id=ctx.message.author.id)

            await ctx.reply(f"Successfully generated your personal template", mention_author=False)

        except ValueError as e:
            await ctx.reply(f"ValueError -> {e}", mention_author=False)
        except TypeError as e:
            await ctx.reply(f"TypeError -> {e}", mention_author=False)
        except RuntimeError as e:
            await ctx.reply(f"RuntimeError -> {e}", mention_author=False)
        except Exception as e:
            raise e

    @commands.command(aliases=["vpersonal", "viewpersonal"])
    async def view_private_templates(self, ctx):
        printing_str = pull_private_details_str(ctx.message.author.id)
        await ctx.reply(printing_str, mention_author=False)

    @commands.command(aliases=["vprivate", "viewprivate"])
    @commands.is_owner()
    async def dev_view_private_templates(self, ctx, user_id=None):
        user_id = ctx.message.author.id if user_id is None else user_id

        printing_str = pull_private_details_str(user_id)
        await ctx.reply(printing_str, mention_author=False)


def setup(client):
    client.add_cog(PrivateMaxScheduleCog(client))

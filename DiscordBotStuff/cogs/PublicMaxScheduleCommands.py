from discord.ext import commands

from FullProcess.CallGeneralProcesses import get_clean_courses_list, clean, remove_dupes, \
    raise_value_error_for_unknown_course_on_db
from FullProcess.CallMaxTemplateProcessing import generate_and_update_db_public_template, pull_public_details_str, \
    drop_public_templates


class PublicMaxScheduleCog(commands.Cog):

    @commands.command(aliases=["wpublic", "writepublic"])
    @commands.is_owner()
    async def dev_generate_public_max_template(self, ctx, description, *course_inputs):
        try:
            course_inputs = remove_dupes(course_inputs)

            course_object_list = get_clean_courses_list("".join(course_inputs))
            raise_value_error_for_unknown_course_on_db(course_object_list)

            generate_and_update_db_public_template(course_object_list=course_object_list, description=description)

            await ctx.reply(f"Successfully generated public template", mention_author=False)

        except ValueError as e:
            await ctx.reply(f"ValueError -> {e}", mention_author=False)
        except TypeError as e:
            await ctx.reply(f"TypeError -> {e}", mention_author=False)
        except RuntimeError as e:
            await ctx.reply(f"RuntimeError -> {e}", mention_author=False)
        except Exception as e:
            await ctx.reply(f"Something went wrong", mention_author=False)
            raise e

    @commands.command(aliases=["templates", "public", "vpublic", "viewpublic"])
    async def view_public_templates(self, ctx, public_template_id=None):
        try:
            printing_str = pull_public_details_str(public_template_id)
            await ctx.reply(printing_str, mention_author=False)

        except ValueError as e:
            await ctx.reply(f"ValueError -> {e}", mention_author=False)
        except TypeError as e:
            await ctx.reply(f"TypeError -> {e}", mention_author=False)
        except RuntimeError as e:
            await ctx.reply(f"RuntimeError -> {e}", mention_author=False)
        except Exception as e:
            await ctx.reply(f"Something went wrong", mention_author=False)
            raise e

    @commands.command(aliases=["droppublic", "droppublics"])
    @commands.is_owner()
    async def dev_drop_public_template(self, ctx, *id_nums):
        try:
            id_nums = clean(id_nums)
            drop_public_templates(id_nums)

            await ctx.reply(f"Successfully dropped public template(s) id = {', '.join(id_nums)}", mention_author=False)

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
    client.add_cog(PublicMaxScheduleCog(client))

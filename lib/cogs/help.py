"""
Help cog contains the help page command
"""
from typing import Optional
from discord.utils import get
from discord.ext.commands import Cog, command
from discord import Embed
from discord.ext.menus import MenuPages, ListPageSource


def syntax(command):  # pylint: disable=W0621
    """Function to return the help content"""
    cmd_and_aliases = " | ".join([str(command), *command.aliases])
    params = []

    for key, value in command.params.items():
        if key not in ("self", "ctx"):
            params.append(f"[{key}]" if "NoneType" in str(value) else f"<{key}>")

    params = " ".join(params)

    return f"```{cmd_and_aliases} {params}```"


class HelpMenu(ListPageSource):
    """Help menu pages class"""

    def __init__(self, ctx, data):
        self.ctx = ctx

        super().__init__(data, per_page=5)

    async def write_page(self, menu, fields=[]):  # pylint: disable=W0102
        """This parses through the commands and writes the pages"""
        offset = (menu.current_page * self.per_page) + 1

        len_data = len(self.entries)

        embed = Embed(title="Help",
                      description="This is the Correct_skill Bot help.",
                      colour=self.ctx.author.colour)
        embed.set_thumbnail(url=self.ctx.guild.me.avatar_url)
        embed.set_footer(text=f"{offset:,}"
                              f" - {min(len_data, offset + self.per_page - 1):,}"
                              f" of {len_data:,} commands.")

        for name, value in fields:
            embed.add_field(name=name, value=value, inline=False)

        return embed

    async def format_page(self, menu, entries):  # pylint: disable=W0221
        fields = []

        for entry in entries:
            fields.append((entry.brief or "No Description.", syntax(entry)))

        return await self.write_page(menu, fields)


class Help(Cog):
    """"Help cog class"""

    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command("help")
        self.bot.remove_cog('jishaku')

    async def cmd_help(self, ctx, command):  # pylint: disable=W0621
        """specific command help"""
        embed = Embed(title=f"Help with `{command}`",
                      description=syntax(command),
                      colour=ctx.author.colour)
        embed.add_field(name="Command Description", value=command.brief)
        await ctx.send(embed=embed)

    @command(name="help", aliases=['Help', 'h'], brief="Shows this message")
    async def show_help(self, ctx, cmd: Optional[str]):
        """help command"""
        if cmd is None:
            menu = MenuPages(source=HelpMenu(ctx, list(self.bot.commands)),
                             # delete_message_after=True,
                             clear_reactions_after=True,
                             timeout=60.0)
            await menu.start(ctx)

        else:
            if (command := get(self.bot.commands, name=cmd)):  # pylint: disable=W0621
                await self.cmd_help(ctx, command)
            else:
                await ctx.send("That command does not exist.")

    @Cog.listener()
    async def on_ready(self):
        """Ready up the cog calling the ready_up function in ./lib/bot/__init__.py"""
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("help")


def setup(bot):
    """Cog setup"""
    bot.add_cog(Help(bot))

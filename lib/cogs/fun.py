"""
Fun cog of the bot
contains various fun commands like say, slap, etc.
"""
import json
import random
from typing import Optional
import requests
import discord
from discord.ext.commands import Cog, BucketType
from discord.ext.commands import command, cooldown
from discord import Member
from discord.ext.commands import BadArgument
from config import TENOR_API_KEY  # pylint: disable=E0401


class Fun(Cog):
    """Fun cog various fun commands"""

    def __init__(self, bot):
        self.bot = bot

    @command(name="slap", aliases=["hit"],
             brief="Returns a random Gif with the reason for you slapping")
    @cooldown(1, 10, BucketType.user)
    async def slap_member(self, ctx, member: Member, *, reason: Optional[str] = "for no reason"):
        """Returns a random Gif with the reason for you slapping"""
        apikey = TENOR_API_KEY
        lmt = 20
        search_term = "slap"
        gif = requests.get(
            "https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (search_term, apikey, lmt)
        )
        if gif.status_code == 200:
            top_gifs = json.loads(gif.content)
            uri = random.choice(random.choice(top_gifs['results'])['media'])["gif"]["url"]
        embed = discord.Embed(
            title=f"{ctx.author.display_name} slapped {member.display_name} {reason}!",
            colour=discord.Colour.blurple()
        )

        embed.set_image(url=uri)
        embed.set_footer(text="Powered by Tenor")
        await ctx.send(embed=embed)

    @slap_member.error
    async def slap_member_error(self, ctx, exc):
        """error handler for slap func"""
        if isinstance(exc, BadArgument):
            await ctx.send("I can't find that member")

    @command(name="say", aliases=["echo"], brief="Repeats what you sent and deletes your message")
    async def echo(self, ctx, *, message: str):
        """repeates whatever you want to say"""
        await ctx.message.delete()
        await ctx.send(f"{message}")

    @Cog.listener()
    async def on_ready(self):
        """when bot is ready this is performed"""
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("fun")


def setup(bot):
    """cog init procedure"""
    bot.add_cog(Fun(bot))

from discord.ext.commands import Cog, BucketType
from discord.ext.commands import command,cooldown
from discord.ext.commands import check
from discord.ext import commands
from discord import Member
from typing import Optional
from discord.ext.commands import (CommandNotFound, BadArgument, MissingRequiredArgument)
import os
from discord.ext.commands import Bot
import requests
import json
import random
import discord
from config import *


class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="slap", aliases=["hit"], brief="Returns a random Gif with the reason for you slapping")
    @cooldown(1, 10, BucketType.user)
    #fun command to slap someone like pancake
    async def slap_member(self, ctx, member: Member, *, reason: Optional[str] = "for no reason"):
        apikey = TENOR_API_KEY #os.environ["TENOR_API_KEY"]
        lmt = 20
        search_term = "slap"
        r = requests.get(
            "https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (search_term, apikey, lmt)
            )
        if r.status_code == 200:  
            top_gifs = json.loads(r.content)
            uri = random.choice(random.choice(top_gifs['results'])['media'])["gif"]["url"]
            #print(uri)
        embed = discord.Embed(
            title = f"{ctx.author.display_name} slapped {member.display_name} {reason}!",
            colour = discord.Colour.blurple()
            )

        #await ctx.send(f"{ctx.author.display_name} slapped {member.mention} {reason}!")
        embed.set_image(url=uri)
        embed.set_footer(text="Powered by Tenor")
        await ctx.send(embed=embed)
        #TODO: ERROR HANDLING

    @slap_member.error
    async def slap_member_error(self, ctx, exc):
        if isinstance(exc, BadArgument):
            await ctx.send("I can't find that member")

    @command(name="say", aliases=["echo"], brief="Repeats what you sent and deletes your message")
    #repeates whatever you want to say
    async def echo(self, ctx, *, message: str):
        await ctx.message.delete()
        await ctx.send(f"{message}")

    @Cog.listener()
    #when bot is ready this is performed
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("fun")
        #print("fun cog ready")
    

def setup(bot):
    bot.add_cog(Fun(bot))

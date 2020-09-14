from discord.ext.commands import Cog, command
import discord
from typing import Optional
from datetime import datetime

class Info(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @command(name="userinfo", aliases=["memberinfo", 'ui', "mi", "whois"], brief="")
    async def userinfo(self, ctx, member: Optional[discord.Member]):
        target = member or ctx.author

        embed = discord.Embed(title=f"User Info for {target.display_name}",
                              color=discord.Colour.blurple(),
                              timestamp=datetime.now())
        embed.set_thumbnail(url=target.avatar_url)
        #fields = [()]
        await ctx.send(embed=embed)        

    @command(name="serverinfo", aliases=["guildinfo", "si", "gi"], brief="")
    async def serverinfo(self, ctx):
        pass
    

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("info")  
            #print("info cog ready")

def setup(bot):
    bot.add_cog(Info(bot))

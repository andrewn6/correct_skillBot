from discord.ext.commands import Cog, command
import discord


class Youtube(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("youtube")
            #print("youtube cog ready")

def setup(bot):
    bot.add_cog(Youtube(bot))

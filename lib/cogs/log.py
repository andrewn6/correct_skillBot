"""
discord bot cog that logs message edits and deletes
"""
from datetime import datetime
import discord
from discord.ext.commands import Cog
from config import STAFF_LOGS_CHANNEL_ID  # pylint: disable=E0401


class Log(Cog):
    """Log cog class"""

    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        """called to ready the cog"""
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("log")
            self.log_channel = self.bot.get_channel(STAFF_LOGS_CHANNEL_ID)  # pylint: disable=W0201
        # print("log cog ready")

    @Cog.listener()
    async def on_user_update(self, before, after):
        """to listen to user changes"""
        if before.name != after.name:
            embed = discord.Embed(title="Member Update",
                                  description="Name changed",
                                  colour=discord.Colour.blurple(),
                                  timestamp=datetime.now())
            fields = [("Before", before.name, False),
                      ("After", after.name, False)]
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await self.log_channel.send(embed=embed)

        elif before.avatar_url != after.avatar_url:
            embed = discord.Embed(title="Member Update",
                                  description="Avatar changed Below is the new one",
                                  colour=discord.Colour.blurple(),
                                  timestamp=datetime.now())
            embed.set_thumbnail(url=before.avatar_url)
            embed.set_image(url=after.avatar_url)
            await self.log_channel.send(embed=embed)

    @Cog.listener()
    async def on_member_update(self, before, after):
        """listen to member updates"""
        if before.display_name != after.display_name:
            embed = discord.Embed(title="Member Update",
                                  description="Nickname changed",
                                  colour=discord.Colour.blurple(),
                                  timestamp=datetime.now())
            fields = [("Before", before.display_name, False),
                      ("After", after.display_name, False)]
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await self.log_channel.send(embed=embed)

    @Cog.listener()
    async def on_message_edit(self, before, after):
        """listens to message edits"""
        if not after.author.bot:
            if before.content != after.content:
                embed = discord.Embed(title="Message Update",
                                      description=f"Action By {after.author.display_name}",
                                      colour=discord.Colour.blurple(),
                                      timestamp=datetime.now())

                fields = [("Before", before.content, False),
                          ("After", after.content, False)]
                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)

                await self.log_channel.send(embed=embed)

    @Cog.listener()
    async def on_message_delete(self, message):
        """listens to message deletes"""
        if not message.author.bot:
            embed = discord.Embed(title="Message Deleted",
                                  description=f"Action By {message.author.display_name}",
                                  colour=discord.Colour.blurple(),
                                  timestamp=datetime.now())
            fields = [("Content", message.content, False),
                      ("In", message.channel, False)]
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await self.log_channel.send(embed=embed)


def setup(bot):
    """COG SETUP"""
    bot.add_cog(Log(bot))

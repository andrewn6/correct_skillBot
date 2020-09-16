from discord.ext.commands import Cog, command
import discord
from discord import Forbidden
from datetime import datetime
from config import STAFF_LOGS_CHANNEL_ID

class Log(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("log")
            self.log_channel = self.bot.get_channel(STAFF_LOGS_CHANNEL_ID) #753121567755599892
        #print("log cog ready")

    @Cog.listener()
    async def on_user_update(self, before, after):
        if before.name != after.name:
            embed = discord.Embed(title="Member Update",
                                  description=f"Name changed",
                                  colour=after.colour,
                                  timestamp=datetime.now())
            fields = [("Before", before.name, False),
                      ("After", after.name, False)]
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await self.log_channel.send(embed=embed)

        elif before.avatar_url != after.avatar_url:
            embed = discord.Embed(title="Member Update",
                                  description="Avatar changed Below is the new one",
                                  colour=after.avatar.colour,
                                  timestamp=datetime.now())
            embed.set_thumbnail(url=before.avatar_url)
            embed.set_image(url=after.avatar_url)
            await self.log_channel.send(embed=embed)    

    @Cog.listener()
    async def on_member_update(self, before, after):
        if before.display_name != after.display_name:
            embed = discord.Embed(title="Member Update",
                                  description=f"Nickname changed",
                                  colour=after.colour,
                                  timestamp=datetime.now())
            fields = [("Before", before.display_name, False),
                      ("After", after.display_name, False)]
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await self.log_channel.send(embed=embed)
        
    @Cog.listener()
    async def on_message_edit(self, before, after):
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
    bot.add_cog(Log(bot))

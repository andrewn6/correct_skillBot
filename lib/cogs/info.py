"""
Cog that gives server info and user info
"""
from typing import Optional
from datetime import datetime
import discord
from discord.ext.commands import (Cog, command, MemberConverter)


class Info(Cog):
    """Info cog class"""
    def __init__(self, bot):
        self.bot = bot

    @command(name="av", aliases=["pfp", "pic"], brief="Sends a users pfp default is you")
    async def av(self, ctx, *, member: Optional[MemberConverter]):  # pylint: disable=C0103
        """sends a users pfp"""
        target = member or ctx.author

        embed = discord.Embed(title=f"{target.display_name}",
                              color=discord.Colour.blurple(),
                              timestamp=datetime.utcnow())
        embed.set_image(url=target.avatar_url)
        await ctx.send(embed=embed)

    @command(name="userinfo", aliases=["memberinfo", 'ui', "mi", "whois"],
             brief="Returns Basic user info like pfp name id and date of joining")
    async def userinfo(self, ctx, *, member: Optional[MemberConverter]):
        """returns user info"""
        target = member or ctx.author

        embed = discord.Embed(title=f"User Info for {target.display_name}",
                              color=discord.Colour.blurple(),
                              timestamp=datetime.utcnow())
        embed.set_thumbnail(url=target.avatar_url)
        fields = [("Name", str(target), True),
                  ("ID", target.id, True),
                  ("Bot?", target.bot, True),
                  ("Top Role", target.top_role.mention, True),
                  ("Status", str(target.status).title(), True),
                  ("Activity",
                   f"{str(target.activity.type).split('.')[-1].title() if target.activity else 'N/A'} {target.activity.name if target.activity else ''}", # pylint: disable=C0301
                   True),
                  ("Created on", target.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
                  ("Joined on", target.joined_at.strftime("%d/%m/%Y %H:%M:%S"), True),
                  ("Boosted", bool(target.premium_since), True)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        await ctx.send(embed=embed)

    @command(name="serverinfo", aliases=["guildinfo", "si", "gi"],
             brief="Returns server info like member count owner and many more try to find out...")
    async def serverinfo(self, ctx):
        """returns server info"""
        embed = discord.Embed(title="Server information",
                              colour=discord.Colour.blurple(),
                              timestamp=datetime.utcnow())

        embed.set_thumbnail(url=ctx.guild.icon_url)

        statuses = [len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members)))]

        fields = [("ID", ctx.guild.id, True),
                  ("Owner", ctx.guild.owner, True),
                  ("Region", ctx.guild.region, True),
                  ("Created at", ctx.guild.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
                  ("Members", len(ctx.guild.members), True),
                  ("Humans", len(list(filter(lambda m: not m.bot, ctx.guild.members))), True),
                  ("Bots", len(list(filter(lambda m: m.bot, ctx.guild.members))), True),
                  ("Banned members", len(await ctx.guild.bans()), True),
                  ("Statuses",
                   f"🟢 {statuses[0]} 🟠 {statuses[1]} 🔴 {statuses[2]} ⚪ {statuses[3]}",
                   True),
                  ("Text channels", len(ctx.guild.text_channels), True),
                  ("Voice channels", len(ctx.guild.voice_channels), True),
                  ("Categories", len(ctx.guild.categories), True),
                  ("Roles", len(ctx.guild.roles), True),
                  ("Invites", len(await ctx.guild.invites()), True),
                  ("\u200b", "\u200b", True)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)

    @Cog.listener()
    async def on_ready(self):
        """readies the cog"""
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("info")


def setup(bot):
    """sets the cog"""
    bot.add_cog(Info(bot))

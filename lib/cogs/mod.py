import discord 
from discord import Member
from typing import Optional
from datetime import datetime
from config import *
from discord.ext.commands import (Cog, MemberConverter,
                                  command, has_permissions, 
                                  bot_has_permissions, 
                                  CheckFailure, Greedy)
from ..db import db

                                  
class Mod(Cog):
    def __init__(self, bot):
        self.bot = bot
        
    
    @command(name="kick",brief='kicks member')
    @bot_has_permissions(kick_members=True)
    @has_permissions(kick_members=True)
    async def kick_members(self, ctx, targets : Greedy[Member], *, reason : Optional[str] = "no reason provied."):
        if not len(targets):
            await ctx.send("One or more required arguments are missing")
        else:
            for target in targets:
    
                if (ctx.guild.me.top_role.position > target.top_role.position 
                    and not target.guild_permissions.administrator):
    
                    await target.kick(reason=reason)
                    embed = discord.Embed(title=f"kicked {target.display_name} {reason}",
                                        colour=discord.Color.blurple(),
                                        timestamp=datetime.utcnow())
                    fields = [("Actioned By", ctx.author.display_name, False)]
                    for name, value, inline in fields:
                        embed.add_field(name=name, value=value, inline=inline)
                    await self.log_channel.send(embed=embed)
                else:
                    await ctx.send(f"{target.display_name} could not be kicked.")
            await self.log_channel.send("Action completed.")
    
    @kick_members.error
    async def kick_members_error(self, ctx, exc):
        if isinstance(exc, CheckFailure):
            await ctx.send("You dont have the permission to do this. -_-")

    @command(name="ban", brief="bans member")
    @bot_has_permissions(ban_members=True)
    @has_permissions(ban_members=True)
    async def ban_members(self, ctx, targets : Greedy[Member], *, reason : Optional[str] = "no reason provied."):
        if not len(targets):
            await ctx.send("One or more required arguments are missing")
    
        else:
    
            for target in targets:
    
                if (ctx.guild.me.top_role.position > target.top_role.position 
                    and not target.guild_permissions.administrator):
    
                    await target.ban(reason=reason)
                    embed = discord.Embed(title=f"banned {target.display_name} {reason}",
                                        colour=discord.Color.blurple(),
                                        timestamp=datetime.utcnow())
                    fields = [("Actioned By", ctx.author.display_name, False)]
                    for name, value, inline in fields:
                        embed.add_field(name=name, value=value, inline=inline)
                    await self.log_channel.send(embed=embed)
                else:
                     await ctx.send(f"{target.display_name} could not be banned.")
            await self.log_channel.send("Action completed.")
   
    @ban_members.error
    async def ban_members_error(self, ctx, exc):
        if isinstance(exc, CheckFailure):
            await ctx.send("You dont have the permission to do this. -_-")

    @command(name="purge", aliases=["clear"], brief="deletes some amount of messages")
    @bot_has_permissions(manage_messages=True)
    @has_permissions(manage_messages=True)
    async def clear_messages(self, ctx, limit:Optional[int] = 1):
        if 0 < limit <= 100:
            with ctx.channel.typing():
                await ctx.message.delete()
                deleted = await ctx.channel.purge(limit=limit)
                await ctx.send(f"Deleted {len(deleted):,} messages.", delete_after=5)
        else:
            await ctx.send("These are too many messages to delete")

    @command(name="mute", brief="mutes a member for some amount of time and remove all other roles")
    @bot_has_permissions(manage_roles=True)
    @has_permissions(manage_roles=True)
    async def mute(self, ctx, targets: Greedy[Member], hours: Optional[int], *,
                   reason: Optional[str] = "No reason Provided."):
        if not len(targets):
            await ctx.send("One or more required arguments are missing")
        else:
            unmutes = []
            for target in targets:
                if not self.mute_role in target.roles:
                    if ctx.guild.me.top_role.position > target.top_role.position:
                        role_ids = ",".join([str(r.id) for r in target.roles])
                        end_time = datetime.utcnow() + datetime.timedelta(seconds = hours) if hours else None
                        #db.execute("INSERT INTO mutes VALUES (%s,%s,%s)",
                         #          target.id, role_ids, getattr(end_time, "isoformat", lambda: None)())
                        #await target.edit(roles=[self.mute_role,target.guild.get_role(VERIFIED_ROLE_ID)])
                        await target.add_roles(self.mute_role)
                        embed = discord.Embed(title=f"Muted {target.display_name} {reason}",
                                              colour=discord.Color.blurple(),
                                              timestamp=datetime.utcnow())
                        fields = [("Actioned By", ctx.author.display_name, False),
                                  ("Duration", f"{hours:,} hour(s)" if hours else "Indefinite", False)]
                        for name, value, inline in fields:
                            embed.add_field(name=name, value=value, inline=inline)
                        await self.log_channel.send(embed=embed)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("mod")
            self.log_channel = self.bot.get_channel(STAFF_LOGS_CHANNEL_ID)
            for i in self.bot.guild.roles:
                if i.name == "Muted":
                    self.mute_role = i


def setup(bot):
    bot.add_cog(Mod(bot))

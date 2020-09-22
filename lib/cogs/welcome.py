from discord.ext.commands import Cog, command
import discord
from ..db import db
import os
from config import *


class Welcome(Cog):
    def __init__(self, bot):
        self.bot = bot
  
    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("welcome")   #for example if the file name is fun.py then the cog name would be fun please insert the cog name here that is the file name without the extension
        #print("welcome cog ready")

    @Cog.listener()
    async def on_member_join(self, member):
        db.execute("INSERT INTO exp (UserId) VALUES (%s)", (member.id))
        await self.bot.get_channel(WELCOME_CHANNEL_ID).send(f"Welcome to {member.guild.name} {member.mention} Please go to <#{SERVER_RULES_CHANNEL_ID}> and react to the message to send messages.")
    
    @Cog.listener()
    async def on_raw_reaction_add(self, payload):
        #print("reaction")
        if payload.message_id == SERVER_RULES_MESSAGE_ID and payload.emoji.name == '✅':            
            print("added")
            await payload.member.add_roles(payload.member.guild.get_role(VERIFIED_ROLE_ID))

    @Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        print("reaction removed")
        if payload.message_id == SERVER_RULES_MESSAGE_ID and payload.emoji.name == '✅':            
            print("removed")
            guild = self.bot.get_guild(int(os.environ["GUILD_ID"]))
            member = guild.get_member(payload.user_id)
            await member.remove_roles(member.guild.get_role(VERIFIED_ROLE_ID))

    
    @Cog.listener()
    async def on_member_remove(self, member):
        db.execute("DELETE FROM exp WHERE UserID = %s", (member.id))
        await self.bot.get_channel(STAFF_LOGS_CHANNEL_ID).send(f"{member.display_name} has left {member.guild.name}.")


def setup(bot):
    bot.add_cog(Welcome(bot))

from asyncio import sleep
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from discord.ext.commands import Bot as BotBase
import discord
from glob import glob
#from discord.ext.commands import (CommandNotFound, BadArgument, MissingRequiredArgument, CommandOnCooldown)
from discord.ext.commands.errors import *
from discord.ext.commands import when_mentioned_or
from ..db import db
import os
from apscheduler.triggers.cron import CronTrigger
from config import *
#Config (PREFIX, BOT_TOKEN, BOT_CHANNEL, OWNER_ID, GUILD_ID, SUGGESTION_CHANNEL_ID)

OWNER_IDS = [OWNER_ID]
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ["JISHAKU_HIDE"] = "True"
COGS = ['jishaku']

for file in os.listdir('./lib/cogs'):
    if file.endswith('.py'):
        COGS.append(file[:-3])
IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument)

def get_prefix(bot, message):
    return when_mentioned_or(PREFIX)(bot, message)


class Ready(object):
    def __init__(self):
        for cog in COGS:
            if cog == "jishaku":
                setattr(self, cog, True)
            else:
                setattr(self, cog, False)

    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f" {cog} cog ready")

    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])

class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.guild = None
        self.cogs_ready = Ready()
        self.scheduler = AsyncIOScheduler()
        db.autosave(self.scheduler)
        super().__init__(command_prefix=get_prefix, owner_ids=OWNER_IDS)

    def setup(self):
        for cog in COGS:
            if cog == 'jishaku':
                self.load_extension('jishaku')
            else:
                self.load_extension(f'lib.cogs.{cog}')
            print(f'{cog} cog loaded')
        print("setup complete")

    def run(self, version):
        self.VERSION = version
        print("running setup")
        self.setup()

        self.TOKEN = BOT_TOKEN
        print("running bot...")
        super().run(self.TOKEN,reconnect=True)

    async def print_message(self):
        self.stdout.send(embed = discord.Embed(title = "Good Morning!",colour = discord.Colour.orange()))

    async def on_connect(self):
        print("Bot connected")

    async def on_disconnect(self):
        print("bot disconnected")

    async def on_error(self, err, *args, **kwargs,):
        if err == "on_command_error":
            await args[0].send("something went wrong")

        embed = discord.Embed(title = "An error occured", colour = discord.Colour.red(),timestamp = datetime.utcnow())
        await self.stdout.send(embed = embed)
        raise

    async def on_command_error(self,ctx,exc):
        error = getattr(exc, 'original', exc)

        if isinstance(exc,CommandNotFound):
            await ctx.send(embed = discord.Embed(title="Wrong Command", colour=discord.Colour.red()))
        #elif isinstance(exc, BadArgument):
            #pass
        elif isinstance(exc,CommandOnCooldown):
            await ctx.send(embed = discord.Embed(title=f"That command is on {str(exc.cooldown.type).split('.')[-1]} cooldown. Try again in {exc.retry_after:,.2f}", colour = discord.Colour.red()))
        elif isinstance(exc, MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(title="One or two required arguments are missing", colour=discord.Colour.red()))
        #elif isinstance(error, CheckFailure):
           # return
        elif isinstance(exc, TooManyArguments):
            await ctx.send(embed=discord.Embed(title="This command does not have this many arguments", colour=discord.Colour.red()))
        else:
            raise exc

    async def on_ready(self):
        if not self.ready:
            self.guild = self.get_guild(GUILD_ID)
            self.scheduler.add_job(self.print_message,CronTrigger(day_of_week = 0, hour=12,minute = 0, second=0))
            self.scheduler.start()
            self.stdout = self.get_channel(BOT_CHANNEL)
            embed = discord.Embed(title = "Bot is Online", colour = discord.Colour.purple(),timestamp = datetime.utcnow())
            embed.set_author(name=self.guild.name,icon_url=self.guild.icon_url)

            while not self.cogs_ready.all_ready():
                await sleep(0.5)
            self.ready = True
            await self.stdout.send(embed = embed)
            await self.change_presence(activity=discord.Game("f.help"))
            print("Bot ready")
        else:
            print("Bot reconnected")
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.channel.id == PROJECT_DISPLAY_CHANNEL_ID:
            await message.add_reaction('👍')
        await self.process_commands(message)


bot = Bot()

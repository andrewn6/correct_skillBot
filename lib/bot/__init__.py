"""
This module is called from the root folder
launcher.py this module overwrites the discord bot class
"""
import os
from asyncio import sleep
import asyncio
from datetime import datetime
import discord
from discord.ext.commands import Bot as BotBase
from discord.ext.commands.errors import *
from discord.ext.commands import when_mentioned_or
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from config import (OWNER_ID, BOT_PREFIX, BOT_TOKEN,  # pylint: disable=E0401
                    GUILD_ID, BOT_CHANNEL, PROJECT_DISPLAY_CHANNEL_ID)
from ..db import db  # pylint: disable=E0401


OWNER_IDS = [OWNER_ID]
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ["JISHAKU_HIDE"] = "True"
COGS = ['jishaku']

for file in os.listdir('./lib/cogs'):
    if file.endswith('.py'):
        COGS.append(file[:-3])
IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument)


def get_prefix(bot, message):  # pylint: disable=W0621
    """PREFIX OF BOT"""
    return when_mentioned_or(BOT_PREFIX)(bot, message)


class Ready(object):  # pylint: disable=R0205
    """Ready class called when Bot gets ready On_ready function"""
    def __init__(self):
        for cog in COGS:
            if cog == "jishaku":
                setattr(self, cog, True)
            else:
                setattr(self, cog, False)

    def ready_up(self, cog):
        """ready_up function called in a cog to ready that cog up for usage"""
        setattr(self, cog, True)
        print(f" {cog} cog ready")

    def all_ready(self):
        """Check to determine if all cogs are ready"""
        return all([getattr(self, cog) for cog in COGS])


class Bot(BotBase):  # pylint: disable=R0902
    """Discord bot class overwrite"""
    def __init__(self):
        self.PREFIX = BOT_PREFIX  # pylint: disable=C0103
        self.ready = False
        self.guild = None
        self.cogs_ready = Ready()
        self.scheduler = AsyncIOScheduler()
        db.autosave(self.scheduler)
        super().__init__(command_prefix=get_prefix, owner_ids=OWNER_IDS)

    def setup(self):
        """To Set up the bot and load all the cogs called while bot starts"""
        for cog in COGS:
            if cog == 'jishaku':
                self.load_extension('jishaku')
            else:
                self.load_extension(f'lib.cogs.{cog}')
            print(f'{cog} cog loaded')
        print("setup complete")

    def run(self, version):  # pylint: disable=W0221
        self.VERSION = version  # pylint: disable=W0201, C0103
        print("running setup")
        self.setup()

        self.TOKEN = BOT_TOKEN  # pylint: disable=W0201, C0103
        print("running bot...")
        super().run(
            self.TOKEN,
            reconnect=True
        )

    async def print_message(self):
        """Scheduled to send every 24 hours"""
        self.stdout.send(embed=discord.Embed(
            title="Good Morning!",
            colour=discord.Colour.orange()))

    async def on_connect(self):
        """Debug message when bot connects"""
        print("Bot connected")

    async def on_disconnect(self):
        """Debug message when bot disconnects"""
        print("bot disconnected")

    async def on_error(self, err, *args, **kwargs, ):  # pylint: disable=W0221
        if err == "on_command_error":
            await args[0].send("something went wrong")

        embed = discord.Embed(title="An error occured",
                              colour=discord.Colour.red(),
                              timestamp=datetime.utcnow())
        await self.stdout.send(embed=embed)
        raise  # pylint: disable=E0704

    async def on_command_error(self, ctx, exc):  # pylint: disable=W0221
        error = getattr(exc, 'original', exc)
        if isinstance(exc, CommandNotFound):
            await ctx.send(embed=discord.Embed(
                title="Wrong Command",
                colour=discord.Colour.red()))
        elif isinstance(exc, BadArgument):
            print(exc)
            # pass
        elif isinstance(exc, CommandOnCooldown):
            await ctx.send(embed=discord.Embed(
                title=(f"That command is on {str(exc.cooldown.type).split('.')[-1]} "
                       f"cooldown. Try again in {exc.retry_after:,.2f}"),
                colour=discord.Colour.red()))
        elif isinstance(exc, MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(title="One or two required arguments are missing",
                                               colour=discord.Colour.red()))
        elif isinstance(error, CheckFailure):
            return
        elif isinstance(exc, TooManyArguments):
            await ctx.send(embed=discord.Embed(title=("This command does not "
                                                      "have this many arguments"),
                                               colour=discord.Colour.red()))
        else:
            raise exc

    async def on_ready(self):
        """Called when bot is starting and when bot is ready if not then it readies the bot"""
        if not self.ready:
            self.guild = self.get_guild(GUILD_ID)
            self.scheduler.add_job(self.print_message,
                                   CronTrigger(day_of_week=0,
                                               hour=12,
                                               minute=0,
                                               second=0))
            self.scheduler.start()
            self.stdout = self.get_channel(BOT_CHANNEL)  # pylint: disable=W0201
            embed = discord.Embed(title="Bot is Online",
                                  colour=discord.Colour.purple(),
                                  timestamp=datetime.utcnow())
            embed.set_author(name=self.guild.name,
                             icon_url=self.guild.icon_url)

            while not self.cogs_ready.all_ready():
                # print("cog not ready")
                await sleep(0.5)
            self.ready = True
            await self.stdout.send(embed=embed)
            await self.change_presence(activity=discord.Game("f.help"))
            print("Bot ready")
        else:
            print("Bot reconnected")

    async def on_message(self, message):
        """Function that listens to every message and sends them to their respective cogs"""
        if message.author.bot:
            return
        if message.channel.id == PROJECT_DISPLAY_CHANNEL_ID:
            await message.add_reaction('👍')
        if not message.guild:
            return
        await self.process_commands(message)


bot = Bot()

from asyncio import sleep
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from discord.ext.commands import Bot as BotBase
import discord
from glob import glob
from discord.ext.commands import (CommandNotFound, BadArgument, MissingRequiredArgument, CommandOnCooldown)
from ..db import db
import os 
from apscheduler.triggers.cron import CronTrigger


PREFIX = os.environ["PREFIX"] #"c."
OWNER_IDS = [int(os.environ["OWNER_ID"])] #735376244656308274
COGS = [path.split("\\")[-1][:-3] for path in glob("./lib/cogs/*.py")]
IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument)
print(COGS)

class Ready(object):
    def __init__(self):
        for cog in COGS:
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
        super().__init__(command_prefix = PREFIX, owner_ids = OWNER_IDS)
    
    def setup(self):
        for cog in COGS:
            self.load_extension(f'lib.cogs.{cog}')
            print(f'{cog} cog loaded')
        print("setup complete")

    def run(self, version):
        self.VERSION = version
        #with open("./lib/bot/token.0","r",encoding="utf-8") as tf:
            #self.TOKEN = tf.read()
        print("running setup")
        self.setup()

        self.TOKEN = os.environ['BOT_TOKEN']
        print("running bot...")
        super().run(self.TOKEN,reconnect=True)
    
    async def print_message(self):
        #channel = self.get_channel(int(os.environ["BOT_CHANNEL"])) #753138246187352094 
        self.stdout.send(embed = discord.Embed(title = "Good Morning!",colour = discord.Colour.orange()))

    async def on_connect(self):
        print("Bot connected")
    
    async def on_disconnect(self):
        print("bot disconnected")
    
    async def on_error(self, err, *args, **kwargs,):
        if err == "on_command_error":
            await args[0].send("something went wrong")
        
        #channel = self.get_channel(int(os.environ["BOT_CHANNEL"])) 
        embed = discord.Embed(title = "An error occured", colour = discord.Colour.red(),timestamp = datetime.utcnow())
        #await channel.send("@Correct_Skill")
        await self.stdout.send(embed = embed)
        raise

    async def on_command_error(self,ctx,exc):
        if isinstance(exc,CommandNotFound):
            await ctx.send(embed = discord.Embed(title = "Wrong Command", colour = discord.Colour.red()))
        elif isinstance(exc, BadArgument):
            pass
        elif isinstance(exc,CommandOnCooldown):
            await ctx.send(embed = discord.Embed(title = f"That command is on {str(exc.cooldown.type).split('.')[-1]} cooldown. Try again in {exc.retry_after:,.2f}", colour = discord.Colour.red()))
        elif isinstance(exc, MissingRequiredArgument):
            await ctx.send("One or two required arguments are missing")
        else:
            raise exc.original
    
    async def on_ready(self):
        if not self.ready:
            self.guild = self.get_guild(int(os.environ["GUILD_ID"])) #742283065694617611
            self.scheduler.add_job(self.print_message,CronTrigger(day_of_week = 0, hour=12,minute = 0, second=0))
            self.scheduler.start()
            self.stdout = self.get_channel(int(os.environ["BOT_CHANNEL"]))
            embed = discord.Embed(title = "Bot is Online", colour = discord.Colour.purple(),timestamp = datetime.utcnow())
            embed.set_author(name=self.guild.name,icon_url=self.guild.icon_url)
           
            while not self.cogs_ready.all_ready():
                await sleep(0.5)
            self.ready = True
            await self.stdout.send(embed = embed)
            print("Bot ready")
        else:
            print("Bot reconnected")
    async def on_message(self, message):
        if not message.author.bot:
            await self.process_commands(message)

bot = Bot()
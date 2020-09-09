from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from discord.ext.commands import Bot as BotBase
import discord
from discord.ext.commands import CommandNotFound
from ..db import db
import os 
from apscheduler.triggers.cron import CronTrigger

PREFIX = os.environ["PREFIX"] #"c."
OWNER_IDS = [int(os.environ["OWNER_ID"])] #735376244656308274

class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.guild = None
        self.scheduler = AsyncIOScheduler()

        db.autosave(self.scheduler)
        super().__init__(command_prefix = PREFIX, owner_ids = OWNER_IDS)
    
    def run(self, version):
        self.VERSION = version
        #TODO:get token from env
        #with open("./lib/bot/token.0","r",encoding="utf-8") as tf:
            #self.TOKEN = tf.read()
        self.TOKEN = os.environ['BOT_TOKEN']
        print("running bot...")
        super().run(self.TOKEN,reconnect=True)
    
    async def print_message(self):
        channel = self.get_channel(int(os.environ["BOT_CHANNEL"])) #753138246187352094 
        channel.send(embed = discord.Embed(title = "Good Morning!",colour = discord.Colour.orange()))

    async def on_connect(self):
        print("Bot connected")
    
    async def on_disconnect(self):
        print("bot disconnected")
    
    async def on_error(self, err, *args, **kwargs,):
        if err == "on_command_error":
            await args[0].send("something went wrong")
        
        channel = self.get_channel(int(os.environ["BOT_CHANNEL"])) 
        embed = discord.Embed(title = "An error occured", colour = discord.Colour.red(),timestamp = datetime.utcnow())
        #await channel.send("@Correct_Skill")
        await channel.send(embed = embed)
        raise

    async def on_command_error(self,ctx,exc):
        if isinstance(exc,CommandNotFound):
            await ctx.send(embed = discord.Embed(title = "Wrong Command",colour = discord.Colour.red()))
        else:
            raise exc.original
    
    async def on_ready(self):
        if not self.ready:
            self.ready = True
            self.guild = self.get_guild(int(os.environ["GUILD_ID"])) #742283065694617611
            self.scheduler.add_job(self.print_message,CronTrigger(day_of_week = 0, hour=12,minute = 0, second=0))
            self.scheduler.start()
            channel = self.get_channel(int(os.environ["BOT_CHANNEL"]))
            embed = discord.Embed(title = "Bot is Online", colour = discord.Colour.purple(),timestamp = datetime.utcnow())
            embed.set_author(name=self.guild.name,icon_url=self.guild.icon_url)
            await channel.send(embed = embed)
            print("Bot ready")
        else:
            print("Bot reconnected")
    async def on_message(self, message):
        pass

bot = Bot()
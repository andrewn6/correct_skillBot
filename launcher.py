from lib.bot import bot
import os

VERSION = "0.0.6"
try:
    if os.environ["HEROKU"]=='True':
        print("Creating config file")
        os.system("python create-config.py")
except:
    pass

bot.run(VERSION)
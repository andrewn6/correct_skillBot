import os

VERSION = "0.0.6"
if 'config.py' not in os.listdir('.'):
    print("Creating config file")
    os.system("python create-config.py")

from lib.bot import bot
bot.run(VERSION)

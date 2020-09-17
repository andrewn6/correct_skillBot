import io

config=(
"""import os

BOT_TOKEN = os.environ['BOT_TOKEN'] #replace this with bot token or set BOT_TOKEN env var
DATABASE_URL = os.environ['DATABASE_URL'] #replace this with DATABASE_URL or set env_var
BOT_CHANNEL = int(os.environ['BOT_CHANNEL'])#753138246187352094 #this is where bot status is being showed
OWNER_ID = os.environ["OWNER_ID"]#735376244656308274 #server owner id
PREFIX = os.environ["PREFIX"]#"f."
GUILD_ID = int(os.environ["GUILD_ID"])#742283065694617611 
TENOR_API_KEY = os.environ["TENOR_API_KEY"] #tenor api key for slap command
PROJECT_DISPLAY_CHANNEL_ID = int(os.environ["PROJECT_DISPLAY_CHANNEL_ID"]) #753121781987934298 #suggestions are reacted with :thumbsup:
STAFF_LOGS_CHANNEL_ID = int(os.environ["STAFF_LOGS_CHANNEL_ID"]) #753121567755599892 #all logs like message edits etc show up here
WELCOME_CHANNEL_ID = int(os.environ["WELCOME_CHANNEL_ID"]) #753130960266068058 #welcome msgs go here
SERVER_RULES_MESSAGE_ID = int(os.environ["SERVER_RULES_MESSAGE_ID"]) #753135467645501440 #msg id of a server rule msg which is to be reacted with ✅ to gain access to the server
VERIFIED_ROLE_ID = int(os.environ["VERIFIED_ROLE_ID"]) #753133700455333958   #the role given to user after he/she clicks ✅ on the rules
"""
)
with io.open("config.py", "w",encoding="utf-8") as f:
    f.write(config)



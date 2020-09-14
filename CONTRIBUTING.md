# Contributing to this Repositry 
### You can contribute to this repositry in three ways:
#### 1.By reviewing code and implementing pep8 standards where it is missing
#### 2.By adding commands and functions in lib/cogs
#### 3.By resolving the issues that are open

### Below is the way you can add a command:
##### Go to lib/cogs
#### Add a cog file if you are creating a new cog... if you are not creating a new cog and are just adding commands to existing cog then you can do it easily
#### to add a new cog i have given a basic shell so that you have someplace to start with
#### Please try to adhere to pep8 standards i am not a stickler for rules but it is important if you find someplace where i am not adhering to them please point them out or correct them

```python
from discord.ext.commands import Cog, command
import discord


class ClassName(Cog):
    def __init__(self, bot):
        self.bot = bot
  
    #To add commands just do
    @command(name="name", aliases=["alias"], brief="Please write the description of the command here or nothing will show up in the description of the help")
    #repeates whatever you want to say
    async def name(self, ctx, *args):
        await ctx.send(f"{message}")
  
    #Please handle all the command errors here
    @name.error
    async def name_error(self, ctx, error): #name is the command name
      if isinstance(error, ERRORNAME ): #import the error name
        await ctx.send("error message")
    
    @Cog.listener()
      #when bot is ready this is performed
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("filename")   #for example if the file name is fun.py then the cog name would be fun please insert the cog name here that is the file name without the extension
            

def setup(bot):
    bot.add_cog(ClassName(bot))

```

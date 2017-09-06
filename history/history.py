import os
from discord.ext import commands
from .utils.dataIO import fileIO
import datetime

class History:
    def __init__(self, bot):
        self.bot = bot

    async def listener(self, before, after):
        server = after.server

    @commands.command(pass_context=True, no_pm=True, name='show')
    async def _show(self, context):
        """Nein."""
        server = context.message.server
        for m in server.members:
            await self.bot.say(str(m.status))

def CheckFolder():
    if not os.path.exists('data/history'):
        print('Creating data/history folder...')
        os.makedirs('data/history')

def CreateDayFile():
    data = {}

    year = str(datetime.datetime.today().date().year)
    month = str(datetime.datetime.today().date().month)
    day = str(datetime.datetime.today().date().day)

    file = 'data/history/' + day + '-' + month + '-' + year + '.json'

    if not fileIO(file, 'check'):
        print('Json file for today not found, creating')
        fileIO(file, 'save', data)

def setup(bot):
    CheckFolder()
    CreateDayFile()
    n = History(bot)
    bot.add_listener(n.listener, 'on_member_update')
    bot.add_cog(n)

import os
from discord.ext import commands
from .utils.dataIO import fileIO
import datetime

class History:
    def __init__(self, bot):
        self.bot = bot

    async def listener(self, member):
        await self.bot.say(str(member.status))

def CheckFolder():
    if not os.path.exists('data/history'):
        print('Creating data/history folder...')
        os.makedirs('data/history')

def CreateDayFile():
    data = {}

    year = datetime.datetime.today().date().year
    month = datetime.datetime.today().date().month
    day = datetime.datetime.today().date().day

    file = 'data/history/' + day + '-' + month + '-' + year + '.json'

    if not fileIO(file, 'check'):
        print('Json file for today not found, creating')
        fileIO(file, 'save', data)

def setup(bot):
    CheckFolder()
    CreateDayFile()
    n = History(bot)
    bot.add_listener(n.listener(), 'on_member_join')
    bot.add_cog(n)

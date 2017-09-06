import os
from discord.ext import commands
from .utils.dataIO import fileIO
import datetime

class History:
    def __init__(self, bot):
        self.bot = bot

    async def listener(self, before, after):
        #before_game = str(before.game)
        before_status = str(before.status)
        try:
            #after_game = str(after.game)
            after_status = str(before.status)
        except TypeError:
            #after_game = 'None'
            after_status = 'None'
        server = after.server

        if not after.bot:
            data = fileIO('data/history/' + GetCurrentDate() + '.json', 'load')
            if server.id not in data:
                data[server.id] = {}
                if after.id not in data[server.id]:
                    data[server.id][after.id] = {}
                else:
                    if after_status is member.status.online:
                        hour_minute = '{}:{}'.format(datetime.datetime.today().hour, datetime.datetime.today().minute)
                        data[server.id][after.id]['ONLINE'] = str(hour_minute)
                    if after_status is member.status.offline:
                        hour_minute = '{}:{}'.format(datetime.datetime.today().hour, datetime.datetime.today().minute)
                        data[server.id][after.id]['OFFLINE'] = str(hour_minute)

            fileIO('data/history/' + GetCurrentDate() + '.json', 'save', data)



    @commands.command(pass_context=True, no_pm=True, name='show')
    async def _show(self, context):
        """Nein."""
        server = context.message.server

        for member in server.members:
            msg = 'Member {} is {} on {} server'.format(member.name, member.status, server.name)

            await self.bot.say(msg)

def CheckFolder():
    if not os.path.exists('data/history'):
        print('Creating data/history folder...')
        os.makedirs('data/history')

def GetCurrentDate():
    year = str(datetime.datetime.today().date().year)
    month = str(datetime.datetime.today().date().month)
    day = str(datetime.datetime.today().date().day)

    formated = day + '-' + month + '-' + year
    return formated

def CreateDayFile():
    data = {}
    file = 'data/history/' + GetCurrentDate() + '.json'

    if not fileIO(file, 'check'):
        print('Json file for today not found, creating')
        fileIO(file, 'save', data)

def setup(bot):
    CheckFolder()
    CreateDayFile()
    n = History(bot)
    bot.add_listener(n.listener, 'on_member_update')
    bot.add_cog(n)

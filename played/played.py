import os
import asyncio
from discord.ext import commands
from .utils.dataIO import fileIO
import time


class Played:

    def __init__(self, bot):
        self.bot = bot
        self.data_file = 'data/played/played.json'

    @commands.command(name="played")
    async def _cookie(self):
        time.sleep(1)
        return await self.bot.say("teste")


def check_folder():
    if not os.path.exists('data/played'):
        print('Creating data/played folder...')
        os.makedirs('data/played')

def check_file():
    data = {}
    f = 'data/played/played.json'
    if not fileIO(f, 'check'):
        print('Creating default played.json...')
        fileIO(f, 'save', data)

def setup(bot):
    check_folder()
    check_file()
    bot.add_cog(Played(bot))
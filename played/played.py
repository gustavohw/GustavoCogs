import os
from discord.ext import commands
from .utils.dataIO import fileIO
from difflib import SequenceMatcher
import asyncio

class Played:
    def __init__(self, bot):
        self.bot = bot
        self.data_file = 'data/played/played.json'

    def match(self, a, b):
        return SequenceMatcher(None, a, b).ratio()

    @commands.command(pass_context=True, no_pm=True, name='played')
    async def _played(self, context):
        """Shows top 10 most popular games on this server."""
        server = context.message.server
        for member in server.members:
            if member.game is not None:
                await self.bot.say(member.name + ' está jogando: ' + member.game)


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
    n = Played(bot)
    """bot.add_listener(n.listener, 'on_member_update')"""
    bot.add_cog(n)

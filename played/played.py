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

    @commands.command(pass_context=True, no_pm=True, name='getPlayTime')
    async def _getPlayTime(self, context):
        """Schedule this per 1 minute basis."""
        server = context.message.server

        for member in server.members:
            if member.game is not None:
                after_game = str(member.game)


        data = fileIO(self.data_file, 'load')
        if server.id not in data:
            data[server.id] = {}
            data[server.id]['GAMES'] = {}
        game_match = ''
        for game in data[server.id]['GAMES']:
            if self.match(str(game).upper(), after_game.upper()) > 0.89 and self.match(str(game).upper(),after_game.upper()) < 1.0:
                game_match = game

        if game_match in data[server.id]['GAMES']:
            data[server.id]['GAMES'][game_match]['MINUTES'] += 1
        elif after_game not in data[server.id]['GAMES']:
            data[server.id]['GAMES'][after_game] = {}
            data[server.id]['GAMES'][after_game]['MINUTES'] = 1
            data[server.id]['GAMES'][after_game]['GAME'] = after_game
        else:
            data[server.id]['GAMES'][after_game]['MINUTES'] += 1
        fileIO(self.data_file, 'save', data)

    @commands.command(pass_context=True, no_pm=True, name='played')
    async def _played(self, context):
        """Shows playtime per game."""
        server = context.message.server
        message = '```Jogos sendo jogados atualmente {}\n\n'.format(server.name)
        for member in server.members:
            if member.game is not None:
                message += '**' + member.name + '**'
                message += ' está jogando: '
                message += member.game.name
                message += '\n'

        message += '```'
        await self.bot.say(message)


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
    bot.add_cog(n)

import os
import json
import discord
from discord.ext import commands
from .utils.dataIO import fileIO
from difflib import SequenceMatcher

class Played2:
    def __init__(self, bot):
        self.bot = bot
        self.data_file = 'data/played2/played.json'

    def match(self, a, b):
        return SequenceMatcher(None, a, b).ratio()

    # TODO: Adicionar hook pra pegar @menção e fazer mais uma key em baixo do Game pra conter Nome : Tempo
    @commands.command(pass_context=True, no_pm=True, name='getTime')
    async def _getTime(self, context):
        """Schedule this per 1 minute basis."""

        server = context.message.server
        data = fileIO(self.data_file, 'load')
        for member in server.members:
            if member.status is not member.status.idle:
                if member.game is not None:
                    after_game = str(member.game)
                    member_id = str(member.id)
                    game_match = ''

                    if server.id not in data:
                        data[server.id] = {}

                    if member_id not in data[server.id]:
                        data[server.id][member_id] = {}
                        data[server.id][member_id]['INFO'] = {}
                        data[server.id][member_id]['INFO']['NAME'] = member.name
                        data[server.id][member_id]['GAMES'] = {}
                        data[server.id][member_id]['GAMES'][after_game] = {}
                        data[server.id][member_id]['GAMES'][after_game]['GAME'] = after_game
                        data[server.id][member_id]['GAMES'][after_game]['MINUTES'] = 1
                        data[server.id][member_id]['GAMES'][after_game]['LASTPLAY'] = 1
                    elif member_id in data[server.id]:
                        if after_game not in data[server.id][member_id]['GAMES']:
                            data[server.id][member_id]['GAMES'][after_game] = {}
                            data[server.id][member_id]['GAMES'][after_game]['GAME'] = after_game
                            data[server.id][member_id]['GAMES'][after_game]['MINUTES'] = 1
                            data[server.id][member_id]['GAMES'][after_game]['LASTPLAY'] = 1
                        else:
                            data[server.id][member_id]['INFO']['NAME'] = member.name
                            data[server.id][member_id]['GAMES'][after_game]['MINUTES'] += 1

        fileIO(self.data_file, 'save', data)

    @commands.command(pass_context=True, no_pm=True, name='played2')
    async def _played2(self, context, username: discord.Member):
        """Shows playtime per game."""
        server = context.message.server
        data = fileIO(self.data_file, 'load')
        author = username
        finalMsg = '```Jogos mais jogados por {} no servidor: {}\n\n'.format(username.display_name, server.name)

        if server.id in data:
            if username.id in data[server.id]:
                data = data[server.id][username.id]['GAMES']

                games_played = sorted(data, key=lambda x: (data[x]['MINUTES']), reverse=True)
                i = 0
                for game in games_played:
                    if i < 10:
                        gamestr = str(game)

                        time = data[game]['MINUTES']
                        timeLast = data[game]['LASTPLAY']
                        if time > 60:
                            hours = int(time/60)
                            minutes = time % 60
                            msg = '{:<5}{}: {} horas e {} minutos.'.format(i+1, gamestr, str(hours), str(minutes))

                            diff = get_change(time, timeLast)
                            if diff > 0.05:
                                msg += ' (+{}%)'.format(str(format(get_change(time, timeLast), '.2f')))
                        else:
                            minutes = time
                            msg = '{:<5}{}: {} minutos.'.format(i+1, gamestr, str(minutes))

                            diff = get_change(time, timeLast)
                            if diff > 0.05:
                                msg += ' (+{}%)'.format(str(format(get_change(time, timeLast), '.2f')))

                        msg += '\n'
                        finalMsg += msg
                        i += 1
                finalMsg += ' ```'
                self.save_last(server, username.id)
                await self.bot.say(finalMsg)
            else:
                finalMsg = '``{} no servidor: {} ainda não está no banco de dados.``'.format(author.display_name, server.name)
                await self.bot.say(finalMsg)

    def save_last(self, server, player_id):
        data = fileIO(self.data_file, 'load')

        if server.id in data:
            if player_id in data[server.id]:
                for game in data[server.id][player_id]['GAMES']:
                    data[server.id][player_id]['GAMES'][game]['LASTPLAY'] = data[server.id][player_id]['GAMES'][game]['MINUTES']

                fileIO(self.data_file, 'save', data)


def sort_games(data):
    games_sorted = {}
    for member in data:
        games_played = sorted(member['GAMES'], key=lambda x: (member[x]['MINUTES']), reverse=True)
        for game in games_played:
            gamestr = str(game)
            games_sorted[gamestr] = {}
            games_sorted[gamestr]['GAMENAME'] = game['GAME']
            games_sorted[gamestr]['LASTPLAY'] = game['LASTPLAY']
            games_sorted[gamestr]['MINUTES'] = game['MINUTES']
    return games_sorted

def get_change(current, previous):
    if current == previous:
        return 0
    try:
       return ((current-previous)/previous)*100
    except ZeroDivisionError:
        return 0

def check_folder():
    if not os.path.exists('data/played2'):
        print('Creating data/played2 folder...')
        os.makedirs('data/played2')

def check_file():
    data = {}
    f = 'data/played2/played.json'
    if not fileIO(f, 'check'):
        print('Creating default played.json...')
        fileIO(f, 'save', data)

def setup(bot):
    check_folder()
    check_file()
    n = Played2(bot)
    bot.add_cog(n)

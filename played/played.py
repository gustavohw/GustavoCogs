import os
from discord.ext import commands
from .utils.dataIO import fileIO
from difflib import SequenceMatcher

class Played:
    def __init__(self, bot):
        self.bot = bot
        self.data_file = 'data/played/played.json'

    def match(self, a, b):
        return SequenceMatcher(None, a, b).ratio()

    # TODO: Adicionar hook pra pegar @menção e fazer mais uma key em baixo do Game pra conter Nome : Tempo
    @commands.command(pass_context=True, no_pm=True, name='getPlayTime')
    async def _getPlayTime(self, context):
        """Schedule this per 1 minute basis."""
        server = context.message.server
        data = fileIO(self.data_file, 'load')
        for member in server.members:
            if member.status is not member.status.idle:
                if member.game is not None:
                    after_game = str(member.game)

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
                        data[server.id]['GAMES'][after_game]['LASTPLAY'] = 1
                    else:
                        data[server.id]['GAMES'][after_game]['MINUTES'] += 1

        fileIO(self.data_file, 'save', data)

    @commands.command(pass_context=True, no_pm=True, name='played')
    async def _played(self, context):
        """Shows playtime per game."""
        server = context.message.server
        data = fileIO(self.data_file, 'load')
        await self.ctx.send(context.message)
        if context.message is not None:
            ar = context.message
            if ar == "all":
                limit = 30
                finalMsg = '```30 Jogos mais jogados no servidor: {}\n\n'.format(server.name)
            else:
                limit = 10
                finalMsg = '```10 Jogos mais jogados no servidor: {}\n\n'.format(server.name)
        if server.id in data:
            data = data[server.id]['GAMES']

            games_played = sorted(data, key=lambda x: (data[x]['MINUTES']), reverse=True)
            i = 0
            for game in games_played:
                if i < limit:
                    gamestr = str(game)

                    msg = gamestr
                    msg += ': '
                    time = data[game]['MINUTES']
                    timeLast = data[game]['LASTPLAY']
                    if time > 60:
                        hours = int(time/60)
                        minutes = time % 60
                        msg += str(hours)
                        msg += ' horas e '
                        msg += str(minutes)
                        msg += ' minutos.'
                        diff = get_change(time, timeLast)
                        if diff > 0.05:
                            msg += ' (+'
                            msg += str(format(get_change(time, timeLast), '.2f'))
                            msg += '%)'
                    else:
                        minutes = time
                        msg += str(minutes)
                        if time is 1:
                            msg += ' minuto.'
                        else:
                            msg += ' minutos.'
                            diff = get_change(time, timeLast)
                            if diff > 0.05:
                                msg += ' (+'
                                msg += str(format(get_change(time, timeLast), '.2f'))
                                msg += '%)'

                    msg += '\n'
                    finalMsg += msg
                    i += 1
            finalMsg += ' ```'
            self.save_last(server)
            await self.bot.say(finalMsg)

    def save_last(self, server):
        data = fileIO(self.data_file, 'load')

        if server.id in data:
            for game in data[server.id]['GAMES']:
                data[server.id]['GAMES'][game]['LASTPLAY'] = data[server.id]['GAMES'][game]['MINUTES']

        fileIO(self.data_file, 'save', data)

def get_change(current, previous):
    if current == previous:
        return 0
    try:
       return ((current-previous)/previous)*100
    except ZeroDivisionError:
        return 0

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

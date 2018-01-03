import os
from discord.ext import commands
from .utils.dataIO import fileIO
from difflib import SequenceMatcher
import time


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
        saved_epoch = data['INFO']['EPOCH']
        mes = str(context.message.content)[1:]
        prefix = '```Markdown\n'
        if mes == "played all":
            limit = 30
            finalMsg = prefix + '30 Jogos mais jogados no servidor: {} desde {}\n\n'.format(server.name, epoch_converter(saved_epoch))
        else:
            limit = 10
            finalMsg = prefix + '10 Jogos mais jogados no servidor: {} desde {}\n\n'.format(server.name, epoch_converter(saved_epoch))

        if server.id in data:
            data = data[server.id]['GAMES']

            games_played = sorted(data, key=lambda x: (data[x]['MINUTES']), reverse=True)
            i = 1
            total_played_hours = 0
            total_played_minutes = 0
            for game in games_played:
                if i < limit:
                    gamestr = str(game)
                    index = str(i) + '.'
                    time = data[game]['MINUTES']
                    timeLast = data[game]['LASTPLAY']
                    if time > 60:
                        hours = int(time/60)
                        minutes = time % 60

                        hoursLast = int(timeLast / 60)
                        minutesLast = timeLast % 60

                        final_sum_hours = hours - hoursLast
                        final_sum_minutes = ((time - timeLast) % 60)
                        total_played_hours += final_sum_hours
                        total_played_minutes += final_sum_minutes

                        msg = '{:<5}{}: {} horas e {} minutos.'.format(index, gamestr, str(hours), str(minutes))

                        diff = get_change(time, timeLast)
                        if diff > 0.05:
                            msg += ' <+{}h:{}m/+{}%>'.format(str(final_sum_hours), str(final_sum_minutes), str(format(get_change(time, timeLast), '.2f')))
                    else:
                        minutes = time
                        minutesLast = timeLast
                        final_sum_minutes = ((time - timeLast) % 60)
                        total_played_minutes += final_sum_minutes

                        msg = '{:<5}{}: {} minutos.'.format(index, gamestr, str(minutes))

                        diff = get_change(time, timeLast)
                        if diff > 0.05:
                            msg += ' <+{} minutos/+{}%>'.format(str(final_sum_minutes), str(format(get_change(time, timeLast), '.2f')))

                    msg += '\n'
                    finalMsg += msg
                    i += 1
            finalMsg += '\nForam jogados totais de <{} horas> e <{} minutos> nessa semana!'.format(str(total_played_hours), str(total_played_minutes))
            finalMsg += ' ```'
            self.save_last(server)
            await self.bot.say(finalMsg)

    def save_last(self, server):
        data = fileIO(self.data_file, 'load')
        saved_epoch = data['INFO']['EPOCH']
        if check_weekly(saved_epoch):
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

def epoch_converter(epoch):
    return time.strftime('%d-%m-%Y', time.localtime(epoch))

def check_weekly(epoch):
    epoch_week = 604800
    if int(time.time()) > (epoch + epoch_week):
        return True
    else:
        return False

def save_weekly_epoch():
    data_file = 'data/played/played.json'
    data = fileIO(data_file, 'load')
    epoch = data['INFO']['EPOCH']
    if check_weekly(epoch) is True:
        data['INFO']['EPOCH'] = int(time.time())

def fix_modulo(value):
    if value < 0:
        return value*-1

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

import os
from discord.ext import commands
from .utils.dataIO import fileIO
from difflib import SequenceMatcher

class Played:
    def __init__(self, bot):
        self.bot = bot
        self.data_file = 'data/played/played2.json'

    def match(self, a, b):
        return SequenceMatcher(None, a, b).ratio()

    # TODO: Adicionar hook pra pegar @menção e fazer mais uma key em baixo do Game pra conter Nome : Tempo
    @commands.command(pass_context=True, no_pm=True, name='getPlayTime')
    async def _getPlayTime(self, context):
        """Schedule this per 1 minute basis."""
        server = context.message.server
        data = fileIO(self.data_file, 'load')

        if server.id not in data:
            data[server.id] = {}
            data[server.id]['MEMBERS'] = {}
            for member in server.members:
                if member.id not in data[server.id]['MEMBERS']:
                    data[server.id]['MEMBERS']['ID'] = member.id
                else:
                    data[server.id]['MEMBERS']['ID'] = {}
                    data[server.id]['MEMBERS']['ID'] = member.id
                    if member.status is not member.status.idle:
                        if member.game is not None:
                            after_game = str(member.game)
                            game_match = ''
                            for game in data[server.id]['MEMBERS'][member.id]['GAMES']:
                                if self.match(str(game).upper(), after_game.upper()) > 0.89 and self.match(str(game).upper(),after_game.upper()) < 1.0:
                                    game_match = game
                            if game_match in data[server.id]['MEMBERS'][member.id]['GAMES']:
                                data[server.id]['MEMBERS'][member.id]['GAMES'][game_match]['MINUTES'] += 1
                            elif after_game not in data[server.id]['MEMBERS'][member.id]['GAMES']:
                                data[server.id]['MEMBERS'][member.id]['GAMES'][after_game] = {}
                                data[server.id]['MEMBERS'][member.id]['GAMES'][after_game]['MINUTES'] = 1
                                data[server.id]['MEMBERS'][member.id]['GAMES'][after_game]['GAME'] = after_game
                            else:
                                data[server.id]['MEMBERS'][member.id]['GAMES'][after_game]['MINUTES'] += 1

        fileIO(self.data_file, 'save', data)

    @commands.command(pass_context=True, no_pm=True, name='played')
    async def _played(self, context):
        """Shows playtime per game."""
        server = context.message.server
        data = fileIO(self.data_file, 'load')
        if server.id in data:
            data = data[server.id]['GAMES']

            #games_played = sorted(data, key=lambda x: (data[x]['MINUTES']), reverse=True)
            finalMsg = '```Jogos mais jogados no servidor: {}\n\n'.format(server.name)

            for game in data:
                gamestr = str(game)

                #if len(gamestr) < 31:
                    #msg = gamestr.ljust(31 - len(gamestr))
                #else:
                msg = gamestr

                msg += ': '
                time = (data[game]['MINUTES'])
                if time > 60:
                    hours = int(time/60)
                    minutes = time % 60
                    msg += str(hours)
                    msg += ' horas e '
                    msg += str(minutes)
                    msg += ' minutos.'
                else:
                    minutes = time
                    msg += str(minutes)
                    if time is 1:
                        msg += ' minuto.'
                    else:
                        msg += ' minutos.'

                msg += '\n'
                finalMsg += msg
            finalMsg += ' ```'
            await self.bot.say(finalMsg)


            #games_played = sorted(data, key=lambda x: (data[x]['MINUTES']), reverse=True)
            """message = '```Jogos mais jogados no servidor:  {}\n\n'.format(server.name)
            for i, game in enumerate(games_played, 1):
                if i > 10:
                    break
                gameMessage = ''
                message += '{:<5}{:<10}\n'.format(game, game)
            message += '```'
            await self.bot.say(message)"""


def check_folder():
    if not os.path.exists('data/played2'):
        print('Creating data/played folder...')
        os.makedirs('data/played')

def check_file():
    data = {}
    f = 'data/played/played2.json'
    if not fileIO(f, 'check'):
        print('Creating default played2.json...')
        fileIO(f, 'save', data)

def setup(bot):
    check_folder()
    check_file()
    n = Played(bot)
    bot.add_cog(n)

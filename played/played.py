import os
import asyncio
from discord.ext import commands
from .utils.dataIO import fileIO
import time

client = discord.Client()

class Played:

    def __init__(self, bot):
        self.bot = bot
        self.data_file = 'data/played/played.json'



    asyncdef my_background_task():
        await client.wait_until_ready()
        counter = 0
        channel = discord.Object(id='channel_id_here')
        while not client.is_closed:
            counter += 1
            await client.send_message(channel, counter)
            await asyncio.sleep(60)  # task runs every 60 seconds

    @client.event
    async def on_ready():
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('------')

    client.loop.create_task(my_background_task())
    client.run('token')


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
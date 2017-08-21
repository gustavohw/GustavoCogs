# Developed by Redjumpman for Redbot
from discord.ext import commands
from random import choice as randchoice


class Quinta:

    def __init__(self, bot):
        self.bot = bot
        self.fortune = "https://www.youtube.com/watch?v=OZpx3loLxg8"

    @commands.command(name="quinta")
    async def _cookie(self):
        return await self.bot.say(self.fortune)


def setup(bot):
    bot.add_cog(Quinta(bot))
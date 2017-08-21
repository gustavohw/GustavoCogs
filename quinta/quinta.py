# Developed by Redjumpman for Redbot
from discord.ext import commands
from random import choice as randchoice


class Quinta:
    """Fortune Cookie Commands."""

    def __init__(self, bot):
        self.bot = bot
        self.fortune = ["https://www.youtube.com/watch?v=OZpx3loLxg8"]

    @commands.command(name="fortune")
    async def _cookie(self):
        """Ask for your fortune
        And look deeply into my scales
        """
        return await self.bot.say("`" + randchoice(self.fortune) + "`")


def setup(bot):
    bot.add_cog(Quinta(bot))
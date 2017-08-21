from discord.ext import commands

class Quinta:
    def __init__(self, bot):
        self.bot = bot

    @commands.command (no_pm=True)
    async def quinta(self, *, text):
        await self.bot.say("https://www.youtube.com/watch?v=OZpx3loLxg8")


def setup(bot):
    n = Quinta(bot)
    bot.add_cog(n)


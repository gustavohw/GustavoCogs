# Developed by Redjumpman for Redbot
from discord.ext import commands
import time


class Quinta:

    def __init__(self, bot):
        self.bot = bot
        self.fortune = "CHEGAMOS NA QUINTA FEIRA, ÚLTIMO GÁS " \
                       "https://www.youtube.com/watch?v=OZpx3loLxg8"

    @commands.command(name="quinta")
    async def _cookie(self):
        time.sleep(5)
        return await self.bot.say(self.fortune)


def setup(bot):
    bot.add_cog(Quinta(bot))
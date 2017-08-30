from discord.ext import commands

class Quinta:

    def __init__(self, bot):
        self.bot = bot
        self.message = "CHEGAMOS NA QUINTA FEIRA, ÚLTIMO GÁS " \
                       "https://www.youtube.com/watch?v=OZpx3loLxg8"

    @commands.command(name="quinta")
    async def _cookie(self):
        return await self.bot.say(self.message)

def setup(bot):
    bot.add_cog(Quinta(bot))
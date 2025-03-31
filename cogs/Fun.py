from discord.ext import commands
import random

class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.hybrid_command()
    async def airfryer(self, ctx: commands.Context):
        texts = [
            "*whirrrrrrrrrrr*",
            "🌡️ *bzzzzzzzzzt*",
            "❌ BEEP! BEEP! BEEP!",
            "*angry air fryer noises*"
            "*click*",
            "*whoooosh*",
            "*clunk*",
            "🌡️ *ding!*",
            "*steady whirring*",
            "📳 *ding ding*",
            "SHAKE SHAKE SHAKE",
            "*brrrrrrrrr continues*"
        ] # thx ai

        await ctx.reply(random.choice(texts))

async def setup(bot):
    await bot.add_cog(Fun(bot))
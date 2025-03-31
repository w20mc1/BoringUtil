from discord.ext import commands
from firebase_admin import firestore_async
import discord

class General(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.db = firestore_async.client()
        self.servers = self.db.collection("servers")
    
    @commands.command()
    async def prefix(self, ctx: commands.Context, prefix: str):
        srv_document = self.servers.document(str(ctx.guild.id))

        await srv_document.set({
            "prefix": prefix
        })
        
        await ctx.reply(embed = discord.Embed(
            color = 0x00FB00,
            title = f"Changed prefix to {prefix}"
        ))
    
    @commands.hybrid_command()
    async def ping(self, ctx: commands.Context):
        await ctx.reply(f"Ping: {round(self.bot.latency * 1000)}ms")

async def setup(bot):
    await bot.add_cog(General(bot))
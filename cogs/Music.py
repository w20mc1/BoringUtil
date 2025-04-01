from discord.ext import commands
from dotenv import load_dotenv
import discord
import yt_dlp
import os
load_dotenv()

class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._queue = {}
        self.cursong = {}

        self._YDL_OPTS = {
            "cookiefile": "config/cookies.txt" if os.environ["USE_YTDLP_COOKIES"] == "true" else "",
            "format": "bestaudio/best",
            "default_search": "ytsearch"
        }

        self._FFMPEG_OPTS = {
            "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", 
            "options": "-vn"
        }
    
    async def get_vc_client(self, ctx: commands.Context):
        if ctx.author.voice != None:
            if ctx.guild.voice_client in self.bot.voice_clients:
                vc_client = ctx.guild.voice_client
            else:
                vc = ctx.author.voice.channel
                vc_client = await vc.connect()
            return vc_client
        else:
            await ctx.reply(embed = discord.Embed(
                color = 0xFF0000,
                title = "Error", 
                description = "You must be in a voice channel to use this function."
            ))
            return False
    
    def play_song(self, server_id, vc_client):
        if server_id not in self.cursong:
            self.cursong[server_id] = {}
        
        if self._queue:
            if len(self.cursong) > 0:
                self.cursong[server_id] = self._queue[server_id].pop(0)
            
            vc_client.play(
                discord.FFmpegOpusAudio(self.cursong[server_id]["url"], **self._FFMPEG_OPTS),
                after = lambda _: self.play_song(server_id, vc_client)
            )
        else:
            self.cursong[server_id] = {}
  
    @commands.hybrid_command()
    async def play(self, ctx: commands.Context, *, song_name):
        vc_client = await self.get_vc_client(ctx)
        if ctx.guild.id not in self._queue:
            self._queue[ctx.guild.id] = []

        if vc_client != False:
            with yt_dlp.YoutubeDL(self._YDL_OPTS) as ydl:
                yt_info = ydl.extract_info(song_name, False)
            
            if "entries" in yt_info:
                entries = yt_info["entries"]
                song = {
                    "url": entries[0]["url"],
                    "name": entries[0]["title"],
                    "thumb": entries[0]["thumbnails"]
                }
            else:
                song = {
                    "url": yt_info["url"],
                    "name": yt_info["title"],
                    "thumb": yt_info["thumbnails"]
                }
            
            self._queue[ctx.guild.id].append(song)
            
            if not vc_client.is_playing():
                self.play_song(ctx.guild.id, vc_client)
                song_embed = discord.Embed(
                    color = 0x00FF00,
                    title = f"Playing {song['name']}"
                )
                print(song["thumb"])
                thumbnail = song["thumb"][-2] if len(song["thumb"]) >= 2 else song["thumb"][0]
                song_embed.set_image(url = thumbnail["url"])
                
                await ctx.reply(embed = song_embed)
            else:
                await ctx.reply(f"Added to queue {song['name']}")
    
    @commands.hybrid_command()
    async def queue(self, ctx: commands.Context, *, cmd):
        if cmd.lower() == "":
            cmd_embed = discord.Embed(
                title = "Queue",
                color = 0x7024bd,
                description = f"""
                {await self.bot.command_prefix(None, ctx)}queue skip - Skips the queue
                {await self.bot.command_prefix(None, ctx)}queue list - Lists the queue
                """
            )
            await ctx.reply(embed = cmd_embed)
        elif cmd.lower() == "skip":
            vc_client = await self.get_vc_client(ctx)

            if vc_client != False and vc_client.is_playing():
                vc_client.stop()
        elif cmd.lower() == "list":
            if len(self._queue[ctx.guild.id]) > 0:
                songs = ""
                for i in range(len(self._queue[ctx.guild.id])):
                    songs += f"{self._queue[ctx.guild.id][i]['name']}\n"

                await ctx.reply(f"(PLAYING) {self.cursong[ctx.guild.id]['name']}\n{songs}")
            elif ctx.guild.id in self.cursong:
                await ctx.reply(f"(PLAYING) {self.cursong[ctx.guild.id]['name']}")
            else:
                await ctx.reply("There are no songs in the queue.")
    
    @commands.hybrid_command()
    async def stop(self, ctx: commands.Context):
        vc_client = await self.get_vc_client(ctx)
        if vc_client != False:
            self._queue[ctx.guild.id].clear()
            vc_client.stop()

async def setup(bot):
    await bot.add_cog(Music(bot))
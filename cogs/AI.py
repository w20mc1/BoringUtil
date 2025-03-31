import base64
from io import BytesIO
import os
from PIL import Image
import discord
from discord.ext import commands
from firebase_admin import firestore_async
import google.generativeai as genai
from google.generativeai import protos
import requests

class AI(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.db = firestore_async.client()
        self.servers = self.db.collection("servers")
        self.model = genai.GenerativeModel("gemini-2.0-flash-exp")
    
    def serialize_history(self, gemini_history: list[protos.Content]):
        return [
            {
                "role": msg.role,
                "parts": [
                    {
                        "type": "text",
                        "content": part.text 
                    } for part in msg.parts
                ]
            } for msg in gemini_history
        ]
    
    def unserialize_history(self, serialized: dict[str]):
        return [
            protos.Content(
                role=msg["role"],
                parts=[
                    {"text": part["content"]} if part["type"] == "text" else {"image_data": part["content"]}
                    for part in msg["parts"]
                ]
            ) for msg in serialized
        ]
    
    async def fetch_data(self, ctx: commands.Context):
        server_document = self.servers.document(str(ctx.guild.id))
        user_document = server_document.collection("users").document(str(ctx.author.id))
        data = (await user_document.get()).to_dict()
        if data is None:
            data = {"messages": []}
        return data, user_document
    
    @commands.hybrid_command()
    async def ai(self, ctx: commands.Context, *, ai_input: str):
        ai_content = []

        if len(ctx.message.attachments) > 0:
            for att in ctx.message.attachments:
                if "image" in att.content_type:
                    ai_content.append(Image.open(BytesIO(requests.get(att.url, stream = True).content)))
                elif att.content_type in ["video/mp4", "audio/mpeg"]:
                    await ctx.send("WIP")
                    
            ai_content.append(ai_input)
        else:
            ai_content.append(ai_input)

        if not ai_input:
            return
        
        user_data, user_document = (await self.fetch_data(ctx))
        
        chat = self.model.start_chat(history = self.unserialize_history(user_data["messages"]))
        resp = (await chat.send_message_async(ai_content))
        ai_resp = resp.text
    
        await user_document.set({"messages": self.serialize_history(chat.history)})
        if len(ai_resp) > 2000:
            ext_result = f"{ctx.message.id}_extended.md"
            with open(ext_result, "w") as ext:
                ext.write(ai_resp)
            await ctx.reply(file = discord.File(ext_result))
            os.remove(ext_result)
        else:
            await ctx.reply(ai_resp)

async def setup(bot):
    await bot.add_cog(AI(bot))
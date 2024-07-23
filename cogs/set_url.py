import os
import deepl
from discord.ext import commands
from googletrans import Translator
import re
import yaml
import requests
import emoji
import discord
from dotenv import load_dotenv
load_dotenv(".env")        

class SetUrl(commands.Cog):    
    def __init__(self, bot):
        self.bot = bot
        self.path = "config/set_url.yaml"
        self.read()


    # 読み込み
    def read(self):
        if not os.path.exists(self.path):
            return

        with open(self.path, encoding="utf-8") as yml:
            self.config = yaml.safe_load(yml)

    # 書き出し
    def write(self):
        with open(self.path, 'w', encoding="utf-8") as f:
            yaml.dump(self.config, f, default_flow_style=False, allow_unicode=True)


    # 起動時
    @commands.Cog.listener()
    async def on_ready(self):
        print("[SetURL] OK")

    # メッセージ送信
    @commands.Cog.listener(name='on_message')
    async def on_message(self, message):
        if (
            message.author.bot or                      # 自身を除外
            message.content == "" or
            message.channel.id != int(self.config['channel_id']) # 指定チャンネル以外を除外
        ):
            return  
                 
        if "http" in message.content:
            f = open("url.txt", "w")
            f.write(message.content)
            f.close()
            await message.channel.send("OK")


def setup(bot):
    return bot.add_cog(SetUrl(bot), guilds=[discord.Object(id=os.getenv("DISCORD_SERVER_ID"))])

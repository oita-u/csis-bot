import os
from discord.ext import commands
import requests
import discord
from dotenv import load_dotenv
import yaml
load_dotenv(".env")

class AddRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.path = "config/add_role.yaml"
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
        print("[AddRole] OK")
        channel_id = self.config['channel_id']
        message = self.config['message']
        channel = self.bot.get_channel(channel_id)

        if 'message_id' in self.config and self.config['message_id'] is not None:
            message_id = self.config['message_id']
            msg = await channel.fetch_message(message_id)
            await msg.edit(content=message)
        else:
            msg = await channel.send(message)
            self.config['message_id'] = msg.id
            self.write()

        # Add reactions for all emojis in the config
        for emoji in self.config['roles']:
            await msg.add_reaction(emoji)

    @commands.Cog.listener(name='on_raw_reaction_add')
    async def on_raw_reaction_add(self, payload):
        if payload.member.bot or payload.message_id != self.config['message_id']:
            return

        emoji = str(payload.emoji)
        if emoji not in self.config['roles']:
            return
        
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)

        role_id = self.config['roles'][emoji]
        role = payload.member.guild.get_role(role_id)
        if role:
            await payload.member.add_roles(role)
            
        # それ以外のroleを外す
        for emoji in self.config['roles']:
            if emoji == str(payload.emoji): continue
            
            role_id = self.config['roles'][emoji]
            role = payload.member.guild.get_role(role_id)
            
            await message.remove_reaction(emoji, payload.member)
            await payload.member.remove_roles(role)
                
                                    

def setup(bot):
    return bot.add_cog(AddRole(bot), guilds=[discord.Object(id=os.getenv("DISCORD_SERVER_ID"))])


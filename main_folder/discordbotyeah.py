
import discord
from discord.ext import commands, tasks
import sys

fspeech = open('C:\\Users\\hiton\\OneDrive\\文件\\GenAICode\\speech1.txt', 'r')
fres = open('C:\\Users\\hiton\\OneDrive\\文件\\GenAICode\\res1.txt', 'r')

# 替换为你的Bot Token
TOKEN = ''
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
# 创建一个命令前缀为 '!' 的bot实例
bot = commands.Bot(command_prefix='!',intents=intents)
# 替换为你想要发送消息的频道ID
CHANNEL_ID = 1259176236173885612

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')
    print('------')
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(f"\n\nspeech:\n{fspeech.read()}")
        await channel.send(f"\n\nres:\n{fres.read()}")
    # 启动自动发送消息的任务
        sys.exit()  # 終止當前腳本

# 运行bot
bot.run(TOKEN)










#---------------------------------------------------------------------------------



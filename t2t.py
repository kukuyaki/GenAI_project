import requests
from dotenv import load_dotenv
from dotenv import dotenv_values
from googlesearch import search
import webbrowser
import queue
import datetime
import discord
import re
from multiprocessing import Process
from threading import Thread
from os import getpid
import signal
import os
from random import randint
from time import time, sleep
# from screen_brightness_control import set_brightness, get_brightness
load_dotenv()
config = dotenv_values(".env")
# print(config["openaiTOKEN"])
API_KEY = config["openaiTOKEN"]
botToken = config["BOT_TOKEN"]
intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.message_content = True
client = discord.Client(intents = intents)
MEMORY = 5
RUNNING = True

class Joiner(Thread):
    def __init__(self, q, r):
        super(Joiner, self).__init__()
        self.__q = q
        self._is_running = r
    def run(self):
        while self._is_running:
            child = self.__q.get()
            print("Joiner: get", child)
            if child == None:
                return
            child.join()
    def stop(self):
        print("Joiner stop")
        self._is_running = False

# def reminder(timeStamp):
#     print("reminder starting, will be awaken at", timeStamp, ", pid:", getpid())
#     stop = False
#     while stop == False:
#         rn = str(datetime.datetime.now().time())
#         secc = " "
#         for t in rn:
#             num = re.findall(r'\d+', t)
#             if num:
#                 secc += t
#         rn = int(secc)
#
#         if rn == timeStamp:
#             stop = True
#     print("reminder done, pid:", getpid())

def timer(seconds):
    print("timer starting, pid:", getpid())
    sleep(seconds)
    print("timer done, pid:", getpid())

# def isReminder(prompt):
#     response = requests.post(
#         'https://api.openai.com/v1/chat/completions',
#         headers={
#             'Content-Type': 'application/json',
#             'Authorization': f'Bearer {API_KEY}'
#         },
#         json={
#             'model': 'gpt-4o',
#             'messages': [{"role": "user", "content": "output only True or False if the incoming prompting trying to set a reminder on a specific time: " + prompt}]
#         }
#     )
#     output = response.json()
#     if output["usage"]["total_tokens"] < 10:
#         print("提醒: 您的quota即將用完。", "quota剩餘:", output["usage"]["total_tokens"])
#     return (output["choices"][0]["message"]["content"][0] == 'T')

def isTiming(prompt):
    response = requests.post(
        'https://api.openai.com/v1/chat/completions',
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {API_KEY}'
        },
        json={
            'model': 'gpt-4o',
            'messages': [{"role": "user", "content": "output only True or False if the incoming prompting trying to set an alerm" + prompt}]
        }
    )
    output = response.json()
    if output["usage"]["total_tokens"] < 10:
        print("提醒: 您的quota即將用完。", "quota剩餘:", output["usage"]["total_tokens"])
    return (output["choices"][0]["message"]["content"][0] == 'T')

def getTime(prompt):
    response = requests.post(
        'https://api.openai.com/v1/chat/completions',
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {API_KEY}'
        },
        json={
            'model': 'gpt-4o',
            'messages': [{"role": "user", "content": "output only the desired time in the prompt, you only need to output hh:mm:ss:" + prompt}]
        }
    )
    output = response.json()
    if output["usage"]["total_tokens"] < 10:
        print("提醒: 您的quota即將用完。", "quota剩餘:", output["usage"]["total_tokens"])
    secc = " "
    for t in output["choices"][0]["message"]["content"]:
        num = re.findall(r'\d+', t)
        if num:
            secc += t
    return int(secc)

def getSeconds(prompt):
    response = requests.post(
        'https://api.openai.com/v1/chat/completions',
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {API_KEY}'
        },
        json={
            'model': 'gpt-4o',
            'messages': [{"role": "user", "content": "output only number of seconds in the prompt:" + prompt}]
        }
    )
    output = response.json()
    if output["usage"]["total_tokens"] < 10:
        print("提醒: 您的quota即將用完。", "quota剩餘:", output["usage"]["total_tokens"])
    secc = " "
    for t in output["choices"][0]["message"]["content"]:
        num = re.findall(r'\d+', t)
        if num:
            secc += t
    return int(secc)


def generateRes(prompt, prev): 
    tmp = "previous conversation:\n"
    for i in range(prev.qsize()):
        tmp += prev.get()
        prev.put(tmp)
    # print(prompt)
    response = requests.post(
        'https://api.openai.com/v1/chat/completions',
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {API_KEY}'
        },
        json={
            'model': 'gpt-4o',
            'messages': [{"role": "user", "content": tmp + "\nThe current prompt is: " + prompt}],
        }
    )
    output = response.json()
    if output["usage"]["total_tokens"] < 10:
        print("提醒: 您的quota即將用完。", "quota剩餘:", output["usage"]["total_tokens"])
    return output["choices"][0]["message"]["content"]

def searchNOpen(query):
    targetURL = ""
    for j in search(query, tld="co.in", num=1, stop=1, pause=2):
        targetURL = j
    webbrowser.open(targetURL)

def speechRes(prompt): 
    response = requests.post(
        'https://api.openai.com/v1/chat/completions',
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {API_KEY}'
        },
        json={
            'model': 'gpt-4o',
            'messages': [{"role": "user", "content": "I want to make a speech based on data of the incoming prompt. Please summarize it within 50 words:" + prompt}],
        }
    )
    output = response.json()
    if output["usage"]["total_tokens"] < 10:
        print("提醒: 您的quota即將用完。", "quota剩餘:", output["usage"]["total_tokens"])
    return output["choices"][0]["message"]["content"]

async def enter(member):
    if member.voice is None:
        print("請先進入語音頻道")
        return
    channel = member.voice.channel
    await channel.connect()


@client.event
async def on_ready():
    print(f"目前登入身份 --> {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == "Hello":
        await message.channel.send("Hello, world!")

# pbot = Process (target = client.run, args = (botToken,))
# pbot.start()
tmp = ""
# userId = ""
# if userId == "":
#     userId = input("請輸入使用者id:")
# User = client.get_user(int(userId))
# print(User)
# if User is None:
#     print("請輸入正確的使用者id")
#     exit()
# guildId = "457174952731475987"
# if guildId == "":
#     guildId = input("請輸入目標Discord伺服器id:")
# Guild = client.get_guild(int(guildId))
# print(Guild)
# if Guild is None:
#     print("請輸入正確的伺服器id")
#     exit()
# if Guild.get_member(int(userId)) is None:
#     print("你必須要加入該伺服器")
#     exit()
# Member = Guild.get_member(int(userId))
prev = queue.Queue()
joinq = queue.Queue()
p1 = Joiner(joinq, True)
p1.start()
# joinq.put(pbot)
while True:
    inputstr = input("輸入內容:")
    # if "enter" in inputstr or "進入" in inputstr:
    #     status = enter(Member)
    #     continue
    if "end" in inputstr or "終止" in inputstr or "結束" in inputstr:
        print("結束程式....")
        joinq.put(None)
        p1.stop()
        # p1.join()
        break
    if "現在幾點" in inputstr or "現在時間" in inputstr or "current time" in inputstr:
        print("現在時間:", datetime.datetime.now().strftime("%H:%M:%S"))
        continue
    if "search" in inputstr or "查詢" in inputstr:
        searchNOpen(inputstr)
        continue
    if isTiming(inputstr):
        sec = 300 if "閃現" in inputstr else int(getSeconds(inputstr))
        p = Process (target = timer, args = (sec,))
        p.start()
        joinq.put(p)
        continue 
    tmp += ("user: " + inputstr + "\n")
    res = generateRes(inputstr, prev)
    tmp += ("AI: " + res + "\n")
    if prev.qsize() < MEMORY:
        prev.put(tmp)
    else:
        prev.get()
        prev.put(tmp)
    # print(tmp)
    print(res)
    print("speech res:", speechRes(res))
print("程式結束")
exit(0)

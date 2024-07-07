import assemblyai as aai
import requests
from pydub import AudioSegment
from pydub import AudioSegment            # 載入 pydub 的 AudioSegment 模組
from pydub.playback import play           # 載入 pydub.playback 的 play 模組
#---------------------------------
import requests
from dotenv import load_dotenv
from dotenv import dotenv_values
import queue
from multiprocessing import Process
from threading import Thread
from os import getpid
from random import randint
from time import time, sleep, ctime
import os
import keyboard
import sys
from discord.ext import commands, tasks
import discord
t = time()
load_dotenv()
config = dotenv_values("C:\\Users\\hiton\\OneDrive\\文件\\GenAICode\\main_folder\\.env")
print(config["openaiTOKEN"])
API_KEY = config["openaiTOKEN"]
MEMORY = 5

class Joiner(Thread):
    def __init__(self, q):
        super(Joiner, self).__init__()
        self.__q = q
    def run(self):
        while True:
            child = self.__q.get()
            if child == None:
                return
            child.join()

def timer(seconds):
    print("timer starting, pid:", getpid())
    sleep(seconds)
    print("timer done, pid:", getpid())

def getSeconds(prompt):
    response = requests.post(
        'https://api.openai.com/v1/chat/completions',
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {API_KEY}'
        },
        json={
            'model': 'gpt-4o',
            'messages': [{"role": "user", "content": "output only number of seconds in the promptd:" + prompt}]
        }
    )
    output = response.json()
    if output["usage"]["total_tokens"] < 10:
        print("提醒: 您的quota即將用完。", "quota剩餘:", output["usage"]["total_tokens"])
    return output["choices"][0]["message"]["content"]



def generateRes(prompt, prev):
    tmp = "previous conversation:\n"
    for i in range(prev.qsize()):
        tmp += prev.get()
        prev.put(tmp)
    response = requests.post(
        'https://api.openai.com/v1/chat/completions',
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {API_KEY}'
        },
        json={
            'model': 'gpt-4o',
            'messages': [{"role": "user", "content": tmp + "\nThe current prompt is: " + prompt +"curren time is: "+ctime()}],
        }
    )
    output = response.json()
    if output["usage"]["total_tokens"] < 10:
        print("提醒: 您的quota即將用完。", "quota剩餘:", output["usage"]["total_tokens"])
    return output["choices"][0]["message"]["content"]
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
#stt-------------------------------------------------------------------------------
print("stt start-----------------------------------------------------------------------")
def wav_to_mp3(wav_file, mp3_file):
    try:
        audio = AudioSegment.from_wav(wav_file)
        audio.export(mp3_file, format="mp3")
        # print(f"Successfully converted {wav_file} to {mp3_file}")
    except Exception as e:
        print(f"Failed to convert {wav_file} to {mp3_file}: {e}")
# Replace with your API key
aai.settings.api_key = "145dd5ef3120436da62b2c7a7bf9eae9"

# URL of the file to transcribe
FILE_URL = "C:\\Users\\hiton\\OneDrive\\文件\\GenAICode\\input.mp3"

# You can also transcribe a local file by passing in a file path
# FILE_URL = './path/to/file.mp3'

transcriber = aai.Transcriber()
transcript = transcriber.transcribe(FILE_URL)

if transcript.status == aai.TranscriptStatus.error:
    print(transcript.error)
else:
    pass
    print(f"text:\n{transcript.text}")
    print("stt finish-----------------------------------------------------------------------")
#openAI--------------------------------------------------------------------------------------------
print("openAI start--------------------------------------------------------------------------------")
prev = queue.Queue()
joinq = queue.Queue()
p1 = Joiner(joinq)
p1.start()
tmp = ""
# while True:
str = transcript.text+" do not waste my time, only answer."
# if "計時" in str:
#     sec = 180 if "閃現" in str else int(getSeconds(str))
#     p = Process (target = timer, args = (sec,))
#     p.start()
#     joinq.put(p)
#     continue
tmp += ("user: " + str + "\n")
res = generateRes(str, prev)
tmp += ("AI: " + res + "\n")
if prev.qsize() < MEMORY:
    prev.put(tmp)
else:
    prev.get()
    prev.put(tmp)
print(f"\n\nres:\n{res}")
speech = speechRes(res)
print(f"\n\nspeech:\n{speech}")

#discord--------------------------------------------------------------------------

path = 'speech1.txt'
f = open(path, 'w')
f.write(speech)
f.close()
path = 'res1.txt'
f = open(path, 'w')
f.write(res)
f.close()
os.system("python C:\\Users\\hiton\\OneDrive\\文件\\GenAICode\\main_folder\\discordbotyeah.py")



# print("openAI finish--------------------------------------------------------------------------------")


#tts-------------------------------------------------------------------------------
# print("tts start-----------------------------------------------------------------------")
# textW=transcript.text
textW=res
wav_name="output.wav"
mp3_name="output.mp3"
def text_to_speech(text, wav_file):
    effects = "Rate(2.0)"
    response = requests.get(
        "http://localhost:59125/process",
        params={
            "INPUT_TEXT": text,
            "INPUT_TYPE": "TEXT",
            "OUTPUT_TYPE": "AUDIO",
            "AUDIO": "WAVE_FILE",
            "LOCALE": "en_US",
            "effect_F0Add_selected":"on",
            "effect_Stadium_parameters":"f0Add:50.0",
            "effect_Rate_selected":"on",
            "effect_Stadium_parameters":"durScale:3.0",
        }
    )
    print(response)
    # print("Response Headers:", response.headers)
    # print("Response Content Type:", response.headers['Content-Type'])

    with open(wav_file, 'wb') as f:
        f.write(response.content)

    # print("WAV file created:", wav_file)

    # 將文本轉換為語音並保存為 WAV 文件

text_to_speech(textW, wav_name)
# 檢查 WAV 文件是否成功創建並嘗試轉換為 MP3
wav_to_mp3(wav_name, mp3_name)
print("tts finish-----------------------------------------------------------------------")
#play mp3 start---------------------------------------------------------------------------
os.system("python C:\\Users\\hiton\\OneDrive\\文件\\GenAICode\\main_folder\\playmp3.py")
sys.exit()  # 終止當前腳本
#play mp3 finish--------------------------------------------------------------------------

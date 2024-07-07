import requests
from dotenv import load_dotenv
from dotenv import dotenv_values
import queue
from multiprocessing import Process
from threading import Thread
from os import getpid
from random import randint
from time import time, sleep
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
            'messages': [{"role": "user", "content": tmp + "\nThe current prompt is: " + prompt}],
        }
    )
    output = response.json()
    if output["usage"]["total_tokens"] < 10:
        print("提醒: 您的quota即將用完。", "quota剩餘:", output["usage"]["total_tokens"])
    return output["choices"][0]["message"]["content"]

prev = queue.Queue()
joinq = queue.Queue()
p1 = Joiner(joinq)
p1.start()
tmp = ""
while True:
    str = input("輸入內容:")
    if "計時" in str:
        sec = 180 if "閃現" in str else int(getSeconds(str))
        p = Process (target = timer, args = (sec,))
        p.start()
        joinq.put(p)
        continue
    tmp += ("user: " + str + "\n")
    if str == "q":
        p1.join()
        break
    res = generateRes(str, prev)
    tmp += ("AI: " + res + "\n")
    if prev.qsize() < MEMORY:
        prev.put(tmp)
    else:
        prev.get()
        prev.put(tmp)
    # print(tmp)
    print(res)
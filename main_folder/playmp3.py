import pygame
import keyboard
import os
import sys
import subprocess
# 初始化 pygame 混音器
pygame.mixer.init()

# 初始化 pygame 的事件模組
pygame.init()
# 加載 MP3 文件
pygame.mixer.music.load("C:\\Users\\hiton\\OneDrive\\文件\\GenAICode\\output.mp3")
def on_music_end():
    print("Music ended, stopping audio...")
    pygame.mixer.music.stop()
    pygame.mixer.quit()  # 終止混音器
    # os.system("python C:\\Users\\hiton\\OneDrive\\文件\\GenAICode\\main_folder\\s2t2t2s.py")
    subprocess.Popen(["python", "C:\\Users\\hiton\\OneDrive\\文件\\GenAICode\\main_folder\\s2t2t2s.py"])
    sys.exit()  # 終止當前腳本
# 播放音檔
pygame.mixer.music.play()
pygame.mixer.music.set_endevent(pygame.USEREVENT)
# 定義一個終止播放的函數
# def stop_audio():
#     # print("Stopping audio...")
#     pygame.mixer.music.stop()
#     pygame.mixer.quit()  # 終止混音器
#     # os.system("python C:\\Users\\hiton\\OneDrive\\文件\\GenAICode\\main_folder\\s2t2t2s.py")
#     subprocess.Popen(["python", "C:\\Users\\hiton\\OneDrive\\文件\\GenAICode\\main_folder\\s2t2t2s.py"])
#     sys.exit()  # 終止當前腳本
###
# 設定按鍵 T 的事件監聽
keyboard.add_hotkey('u', on_music_end)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.USEREVENT:
            on_music_end()
            running = False
        elif event.type == pygame.QUIT:
            running = False

# 保持程式運行，等待按鍵事件
keyboard.wait('esc')  # 按下 Esc 鍵退出程式

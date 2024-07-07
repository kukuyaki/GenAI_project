import assemblyai as aai
from pydub import AudioSegment
import pyaudio
import wave
import keyboard
import threading

chunk = 1024                     # 記錄聲音的樣本區塊大小
sample_format = pyaudio.paInt16  # 樣本格式
channels = 2                     # 聲道數量
fs = 44100                       # 取樣頻率
filename = "myrecord1.wav"      # 錄音檔名
filenamemp3 = "myrecord1.mp3"      # 錄音檔名

p = pyaudio.PyAudio()            # 建立 pyaudio 物件
recording = False
frames = []
stream = None
recording_thread = None
def wav_to_mp3(wav_file, mp3_file):
    try:
        audio = AudioSegment.from_wav(wav_file)
        audio.export(mp3_file, format="mp3")
        print(f"Successfully converted {wav_file} to {mp3_file}")
    except Exception as e:
        print(f"Failed to convert {wav_file} to {mp3_file}: {e}")
def start_recording():
    global recording, frames, stream, recording_thread
    if recording:
        return
    print("開始錄音...")
    recording = True
    frames = []
    stream = p.open(format=sample_format, channels=channels, rate=fs, frames_per_buffer=chunk, input=True)
    recording_thread = threading.Thread(target=record_audio)
    recording_thread.start()

def record_audio():
    global frames, stream
    while recording:
        data = stream.read(chunk)
        frames.append(data)

def stop_recording(e=None):
    global recording, stream
    if not recording:
        return
    print("錄音結束...")
    recording = False
    recording_thread.join()
    stream.stop_stream()
    stream.close()
    
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wav_to_mp3(filename, filenamemp3)
    wf.close()


# 設定按鍵事件

keyboard.on_press_key("u", lambda e: start_recording())
keyboard.on_release_key("u", lambda e: stop_recording())

print("按下U鍵開始錄音，放開U鍵結束錄音")
print("aa")
# 保持程式運行，直到手動終止
keyboard.wait("esc")
print("addddddda")

p.terminate()  # 終止 pyaudio 物件，釋放資源

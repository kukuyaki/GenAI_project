
import requests
from pydub import AudioSegment
textW="Hello, how are you my friend? you are so funny?"
wav_name="output7.wav"
def text_to_speech(text, wav_file):
    response = requests.get(
        "http://localhost:59125/process",
        params={
            "INPUT_TEXT": text,
            "INPUT_TYPE": "TEXT",
            "OUTPUT_TYPE": "AUDIO",
            "AUDIO": "WAVE_FILE",
            "LOCALE": "en_US",
            "VOICE": "cmu-slt-hsmm",
            "effect_F0Add_selected":"on",
            "effect_Stadium_parameters":"f0Add:50.0",
            "effect_Rate_selected":"on",
            "effect_Stadium_parameters":"durScale:3.0",
        }
    )
    print("Response Headers:", response.headers)
    print("Response Content Type:", response.headers['Content-Type'])

    with open(wav_file, 'wb') as f:
        f.write(response.content)

    print("WAV file created:", wav_file)

def wav_to_mp3(wav_file, mp3_file):
    try:
        audio = AudioSegment.from_wav(wav_file)
        audio.export(mp3_file, format="mp3")
        print(f"Successfully converted {wav_file} to {mp3_file}")
    except Exception as e:
        print(f"Failed to convert {wav_file} to {mp3_file}: {e}")

# 將文本轉換為語音並保存為 WAV 文件

text_to_speech(textW, wav_name)
# 檢查 WAV 文件是否成功創建並嘗試轉換為 MP3
wav_to_mp3(wav_name, "output7.mp3")

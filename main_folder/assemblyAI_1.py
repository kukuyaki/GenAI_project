# Start by making sure the `assemblyai` package is installed.
# If not, you can install it by running the following command:
# pip install -U assemblyai
#
# Note: Some macOS users may need to use `pip3` instead of `pip`.

import assemblyai as aai
import requests
from pydub import AudioSegment
#stt-------------------------------------------------------------------------------

print("stt start-----------------------------------------------------------------------")

# Replace with your API key
aai.settings.api_key = "145dd5ef3120436da62b2c7a7bf9eae9"

# URL of the file to transcribe
FILE_URL = "C:\\Users\\hiton\\Downloads\\5 TIMELAPSE tips in 30 seconds! (320).mp3"

# You can also transcribe a local file by passing in a file path
# FILE_URL = './path/to/file.mp3'

transcriber = aai.Transcriber()
transcript = transcriber.transcribe(FILE_URL)

if transcript.status == aai.TranscriptStatus.error:
    print(transcript.error)
else:
    print(transcript.text)

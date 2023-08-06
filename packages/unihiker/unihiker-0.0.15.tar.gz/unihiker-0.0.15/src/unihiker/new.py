"""PyAudio Example: Play a wave file (callback version)"""

import pyaudio
import wave
import time
import sys
from pydub import AudioSegment, effects  
from math import ceil


if len(sys.argv) < 2:
    print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    sys.exit(-1)


sound = AudioSegment.from_file(sys.argv[1])

chunk = 1024

number_of_chunks = ceil(len(sound.raw_data) / float(chunk))
frames = [sound.raw_data[i * chunk:(i + 1) * chunk] for i in range(int(number_of_chunks))]


wf = wave.open(sys.argv[1], 'rb')

p = pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
    data = wf.readframes(frame_count)
    # print(data)
    # print(len(data))
    # data = frames.pop(0)
    # print(data)
    # print(len(data))
    return (data, pyaudio.paContinue)

print(wf.getsampwidth())

stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True,
                stream_callback=callback)

stream.start_stream()

while stream.is_active():
    time.sleep(0.1)

stream.stop_stream()
stream.close()
wf.close()

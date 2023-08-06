"""
PyAudio Example: Make a wire between input and output (i.e., record a
few samples and play them back immediately).

This is the callback (non-blocking) version.
"""

import pyaudio
import time
from pydub import AudioSegment, effects  

WIDTH = 2
CHANNELS = 1
RATE = 16000

p = pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):

    def auto_level(sound, target_dBFS):
        change_in_dBFS = target_dBFS - sound.dBFS
        return sound.apply_gain(change_in_dBFS)

    sound = AudioSegment(in_data, sample_width=WIDTH, channels=CHANNELS, frame_rate=RATE)
    sound = auto_level(sound, -20.0) 

    return (sound.raw_data, pyaudio.paContinue)

stream = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                stream_callback=callback, frames_per_buffer=4096)

stream.start_stream()

while stream.is_active():
    time.sleep(0.1)

stream.stop_stream()
stream.close()

p.terminate()
import time
import pyaudio
from pydub import AudioSegment  
from math import ceil

#Mute alsa
import ctypes

ERROR_HANDLER_FUNC = ctypes.CFUNCTYPE(None, ctypes.c_char_p, ctypes.c_int,
                                      ctypes.c_char_p, ctypes.c_int,
                                      ctypes.c_char_p)

def py_error_handler(filename, line, function, err, fmt):
    pass

c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

try:
    asound = ctypes.cdll.LoadLibrary('libasound.so.2')
    asound.snd_lib_error_set_handler(c_error_handler)
except OSError:
    pass
#End mute alsa

class Audio():
    def __init__(self, rate=16000, chunk=1024, format=pyaudio.paInt16):
        self.rate = rate
        self.chunk = chunk
        self.format = format
        self.channels = 1
        self.frame = None
        self.frames = []
        self.stream = None
        self.duration = None
        self.recording = False
        self.target_volume = -20
        self.sound = None
        self.player = None

        self.p = pyaudio.PyAudio()
        
        def callback(in_data, frame_count, time_info, status):
            if self.recording:
                self.frames.append(in_data)
                if self.duration is not None and len(self.frames) >= int(self.rate / self.chunk * self.duration):
                    self.recording = False
            self.frame = in_data
            return (in_data, pyaudio.paContinue)

        self.stream = self.p.open(format=self.format,
                        channels=self.channels,
                        rate=self.rate,
                        input=True,
                        frames_per_buffer=self.chunk,
                        stream_callback = callback)

    def auto_volume(self, sound, target_dBFS):
        change_in_dBFS = target_dBFS - sound.dBFS
        return sound.apply_gain(change_in_dBFS)

    def start_record(self, target_volume=-20):
        self.recording = False
        self.frames = []
        self.duration = None
        self.recording = True
        self.target_volume = target_volume
    
    def stop_record(self):
        self.recording = False
        self.sound = AudioSegment(b''.join(self.frames), sample_width=self.p.get_sample_size(pyaudio.paInt16), channels=self.channels, frame_rate=self.rate)
        if self.target_volume is not None:
            self.sound = self.auto_volume(self.sound, self.target_volume) 

    def record(self, duration, target_volume=-20):
        self.recording = False
        self.frames = []
        self.duration = duration
        self.recording = True
        self.target_volume = target_volume
        while self.recording:
            time.sleep(0.05)
        self.stop_record()

    def sound_level(self):
        def mapping( x,  in_min,  in_max,  out_min,  out_max):
            result = (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
            result = max(min(result, 100), 0)
            return result

        return round( mapping(self.sound_dBFS(), -50, -20, 0, 100), 2)

    def sound_dBFS(self):
        if self.frame is None:
            return -96.00
        else:
            return AudioSegment(self.frame, sample_width=self.p.get_sample_size(pyaudio.paInt16), channels=self.channels, frame_rate=self.rate).dBFS

    def save(self, file_path="output.wav"):
        self.sound.export(file_path, format='wav')

    def load(self, file_path):
        self.sound = AudioSegment.from_file(file_path)

    def play(self):
        self.start_play()
        while self.player.is_active():
            time.sleep(0.05)
        self.stop_play()

    def start_play(self):
        def callback(in_data, frame_count, time_info, status):
            if not self.frames:
                return (b'', pyaudio.paComplete)
            data = self.frames.pop(0)
            return (data, pyaudio.paContinue)

        chunk_size = self.chunk * self.sound.sample_width * self.sound.channels

        number_of_chunks = ceil(len(self.sound.raw_data) / float(chunk_size))
        self.frames = [self.sound.raw_data[i * chunk_size:(i + 1) * chunk_size] for i in range(int(number_of_chunks))]

        self.player = self.p.open(format = self.p.get_format_from_width(self.sound.sample_width), 
            channels = self.sound.channels, 
            rate = self.sound.frame_rate,
            output = True,
            frames_per_buffer=self.chunk,
            stream_callback = callback)
    
        self.player.start_stream()
    
    def stop_play(self):
        self.player.stop_stream()
        self.frames = []
        self.player.close()

    def pause_play(self):
        self.player.stop_stream()

    def resume_play(self):
        self.player.start_stream()


if __name__ == "__main__":
    audio = Audio()

    for i in range(30):
        print(audio.sound_level())
        time.sleep(0.1)

    print("start record")
    audio.start_record()
    time.sleep(10)

    print("stop record")
    audio.stop_record()

    print("start play")
    audio.start_play()
    time.sleep(3)

    print("pause play")
    audio.pause_play()
    time.sleep(3)

    print("resume play")
    audio.resume_play()
    time.sleep(3)

    print("stop play")
    audio.stop_play()

    print("save to 10s.wav")
    audio.save('10s.wav')

    print("start record 5s")
    audio.record(5)
    print("end record 5s")

    print("play whole sound")
    audio.play()
    print("play finished")
    audio.save('5s.wav')

    audio.load("test.mp3")

    audio.start_play()
    time.sleep(5.5)
    audio.stop_play()

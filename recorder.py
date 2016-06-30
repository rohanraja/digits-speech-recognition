import pyaudio
import wave
import numpy as np

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024 
RECORD_SECONDS = 2

audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)

    
# for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#     data = stream.read(CHUNK)
#     numpydata = np.fromstring(data, dtype=np.int16)
#     print numpydata.max()
#     frames.append(data)

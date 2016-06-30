import pyaudio
import wave
 
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024 
RECORD_SECONDS = 2

import sys

WAVE_OUTPUT_FILENAME = "file.wav"

 
audio = pyaudio.PyAudio()
 
# start Recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)
print "recording...\n"
frames = []
 
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    print i
    frames.append(data)
print "finished recording"
 
 
# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()
 
waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()

import scipy.io.wavfile as w
import numpy as np
import matplotlib.pyplot as plt
import os


# outPath = "/mnt/2tb/datasets/spoken_spects"
outPath = "."

def saveSpect(fname):
    samp, data = w.read(fname)
    data = data[1::2]
    samp /= 2
    #plt.plot(data)
    plt.clf()
    frame1 = plt.gca()
    frame1.axes.get_xaxis().set_visible(False)
    frame1.axes.get_yaxis().set_visible(False)
    frame1.spines['top'].set_visible(False)
    frame1.spines['bottom'].set_visible(False)
    frame1.spines['left'].set_visible(False)
    frame1.spines['right'].set_visible(False)

    S, freqs, bins, im = plt.specgram(data, NFFT=1024, Fs=samp, noverlap=512)

    plt.tight_layout()
    plt.axis('tight')
    
    fileName = fname.split("/")[-1]
    fpath = os.path.join(outPath, "%s.png"%fileName)
    plt.savefig(fpath, bbox_inches='tight', pad_inches=0)

# saveSpect(WAVE_OUTPUT_FILENAME)

from processWav import writeMFCC


samp, data = w.read(WAVE_OUTPUT_FILENAME)
data = data[1::2]
samp /= 2
writeMFCC(data, samp, "file.wav.png")

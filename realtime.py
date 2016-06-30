from threading import Thread
import time
import random
from Queue import Queue
import numpy as np
import sys
import pyaudio
import wave
import cv2
from processWav import writeMFCC
from classifier import Classifier

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024 
RECORD_SECONDS = 2
RECORD_FRAMES = RECORD_SECONDS * RATE

queue = Queue()
worksqueue = Queue()
spectImg = np.array([[1,2]], np.uint8)

class ProducerThread(Thread):
    def run(self):
        global queue

        audio = pyaudio.PyAudio()
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)

        while True:

            data = stream.read(CHUNK)
            npFrame = np.fromstring(data, dtype=np.int16)
            queue.put(npFrame)

        stream.stop_stream()
        stream.close()
        audio.terminate()

class ConsumerThread(Thread):
    
    def check_spoken(self, frame):
        return frame.max() > 400

    def run(self):
        global queue, spectImg
        
        numChunks = int(RATE / CHUNK * RECORD_SECONDS)
        self.allFrames = np.array([], np.int16)
        started = -1
        ended = -1

        while True:

            frame = queue.get()
            queue.task_done()
            self.allFrames = np.hstack([self.allFrames, frame])

            if self.check_spoken(frame):
                if started == -1:
                    started = self.allFrames.shape[0] - CHUNK
            else:
                if started != -1:
                    ended = self.allFrames.shape[0] - CHUNK 
                    self.processSpokenPart(started, ended)
                    started = -1

            # spectImg = writeMFCC(currFrame, RATE)


    def processSpokenPart(self, st, end): 
        global queue, spectImg
        

        N = end - st
        if N <= 3*CHUNK: # Discard accidental noise
            return
        padd = int((RECORD_FRAMES - N)/2)
        print "Processing spoken part"
        
        actualStart = st - padd
        actualEnd = end + padd


        while(self.allFrames.shape[0] < actualEnd):
            frame = queue.get()
            queue.task_done()
            self.allFrames = np.hstack([self.allFrames, frame])

        SPOKEN_SAMPLE = self.allFrames[actualStart:actualEnd]
        self.processSample(SPOKEN_SAMPLE)

    def processSample(self, sample):
        global worksqueue
        worksqueue.put(sample)




class ProcessorThread(Thread):

    def run(self):
        global worksqueue, spectImg

        classifier = Classifier()

        while True:
            sample = worksqueue.get()
            worksqueue.task_done()

            result = classifier.classify(sample)

            print "\nPreciction: %s\n" % result
        
            spectImg = writeMFCC(sample, RATE)


ProducerThread().start()
ConsumerThread().start()
ProcessorThread().start()


import imutils

while True:
    outp = imutils.resize(spectImg.T,width=712)
    cv2.imshow("out", outp)
    cv2.waitKey(1)

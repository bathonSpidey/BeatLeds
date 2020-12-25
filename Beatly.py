# -*- coding: utf-8 -*-
"""
Created on Thu Dec 24 09:31:41 2020

@author: batho
"""

import pyaudio
import numpy as np
import requests as req
from time import sleep
np.set_printoptions(suppress=True) # don't use scientific notation

CHUNK = 1024*2 # number of data points to read at a time
RATE = 44100 # time resolution of the recording device (Hz)
TARGET = 2100 # show only this one frequency
p=pyaudio.PyAudio() # start the PyAudio class
stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
              frames_per_buffer=CHUNK) #uses default input device

# create a numpy array holding a single read of audio data
change=0
red=np.random.randint(255)
green=np.random.randint(255)
blue=np.random.randint(255)
prevPeak=0
try:
    for i in range(8000):
        if change%500:
            red=np.random.randint(255)
            green=np.random.randint(255)
            blue=np.random.randint(255)
        change+=1
        data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
        peak=np.average(np.abs(data))*2
        fft = abs(np.fft.fft(data).real)
        fft = fft[:int(len(fft)/2)] # keep only first half
        freq = np.fft.fftfreq(CHUNK,1.0/RATE)
        freq = freq[:int(len(freq)/2)] # keep only first half
        assert freq[-1]>TARGET, "ERROR: increase chunk size"
        val = fft[np.where(freq>TARGET)[0][0]]
        if val>10000:
            val/=10
        ledNumbers=int(np.interp(val/10,[0,1024], [0,30]))
        
        if ledNumbers < 2 and (5<= peak <60) and 10<(prevPeak-peak)<30:
            print("I am here yay")
            try:
                req.get("http://192.168.8.107/rainbow")
                sleep(0.030)
            except ConnectionResetError:
                pass
        else:
            try:
                req.get("http://192.168.8.107/setStrip?total={}&r={}&g={}&b={}".format(
                    ledNumbers,red, green, blue))
                sleep(0.02)
            except ConnectionResetError:
                 pass
        prevPeak=peak
    #print(str(ledNumbers)+":"+str(val/10)+":"+ int(val/10)*"*")
   
except KeyboardInterrupt:
# close the stream gracefully
    stream.stop_stream()
    stream.close()
    p.terminate()
stream.stop_stream()
stream.close()
p.terminate()
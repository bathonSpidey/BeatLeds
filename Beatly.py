# -*- coding: utf-8 -*-
"""
Created on Thu Dec 24 09:31:41 2020
@author: spidey
"""

import pyaudio
import numpy as np
import requests as req
from time import sleep
import threading


CHUNK = 1024*2 
RATE = 44100 
TARGET = 2100 
REST=.03
p=pyaudio.PyAudio() # start the PyAudio class
stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
              frames_per_buffer=CHUNK) 
change=0
red=np.random.randint(255)
green=np.random.randint(255)
blue=np.random.randint(255)
prevPeak=0

def callRainbow():
    req.get("http://192.168.8.107/rainbow")
def callStrip(ledNumbers,red, green, blue):
    req.get("http://192.168.8.107/setStrip?total={}&r={}&g={}&b={}".format(
                ledNumbers,red, green, blue))
def threadRainbow():
    t = threading.Thread(target=callRainbow)
    t.daemon = True
    t.start()
def threadStrip(ledNumbers,red, green, blue):
    t = threading.Thread(target=callStrip, args=(ledNumbers,red, green, blue))
    t.daemon = True
    t.start()
def getTriggerParameters(stream):
    data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
    peak=np.average(np.abs(data))*2
    fft = abs(np.fft.fft(data).real)
    fft = fft[:int(len(fft)/2)] # keep only first half
    freq = np.fft.fftfreq(CHUNK,1.0/RATE)
    freq = freq[:int(len(freq)/2)] # keep only first half
    assert freq[-1]>TARGET, "ERROR: increase chunk size"
    val = fft[np.where(freq>TARGET)[0][0]]/25
    return val, peak
def getColors():
    return np.random.randint(255),np.random.randint(255),np.random.randint(255)
def changeNeoPixel(ledNumbers, peak, prevPeak):
    if ledNumbers < 2 and (5<= peak <60) and 10<(prevPeak-peak)<25:
        threadRainbow()
        sleep(REST)
    else:
        threadStrip(ledNumbers,red, green, blue)
        sleep(REST)
    
if __name__=="__main__":
    try:
        while True:
            if change%500:
                red, green, blue = getColors()
            change+=1
            val, peak=getTriggerParameters(stream)
            ledNumbers=int(np.interp(val,[0,1250], [0,30])*1.2)
            changeNeoPixel(ledNumbers, peak, prevPeak)
            prevPeak=peak
            #print(str(ledNumbers)+":"+str(val/10)+":"+ int(val/10)*"*") 
    except KeyboardInterrupt:
    # close the stream gracefully
        stream.stop_stream()
        stream.close()
        p.terminate()
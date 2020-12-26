# BeatLeds

We have all used Winamp at some point of time if you were a 90s kid. If you would have used the visualizer liked me, ou must have wondered that the visualizer was preety cool to adjust to the music and change its pattern. In a an attempt to create it physically I ended up making the BeatLeds over the christmas vacation! 

## Components
- NeoPixels: The standard 60led neopixel strip working on 5V
- Esp32: I used both ttgo and nodemcu. It might also work with Arduino Mkr or plain arduino with wifi module.
- Pi/Laptop/Desktop with microphone: This os where you run the python script to process the audio.

## Working 

You must be wondering why esp32. The point of the project is to use IoT to control the Led's. 
For this the python  file processes the audio coming in and calls the esp32 to control the led light pattern.

At the moment it can easily detect beat and beat drops. just run the script in the background upload the ino file to the esp32 done!

## Results 
[Link to sample](https://www.instagram.com/p/CJNCmLrnnXW/?utm_source=ig_web_copy_link)

## Future updates

If anyone interested to  develop it further. I would like to use different frequency and extract guitar, drums frequency and write a different control loop for each.
At the moment it uses simple numpy fft thanks to [Scott W Harden](https://swharden.com/blog/2016-07-19-realtime-audio-visualization-in-python/)

Hope you enjoy it! 

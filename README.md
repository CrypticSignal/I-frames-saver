# I-frames-saver
A command-line program that takes a video file as input and saves the I-frames (or keyframes only by using the `-k` argument) as PNG files. 

Using this program is very simple, simply specify the path of the video using the `-f` argument, e.g. `python3 main.py -f video.mp4`. Include the `-k` argument if you are only interested in keyframes, e.g. `python3 main.py -f video.mp4 -k`

*Note: with H.264, "keyframes" refers to Instantaneous Decoder Refresh (IDR) frames, which is a special type of I-frame. Where there is an IDR frame, subsequent frames cannot reference any frames before the IDR frame. Because of this, video segments that begin with an IDR frame can be independently decoded.*
# Usage
```
usage: main.py [-h] -f FILE_PATH [-k]

optional arguments:
  -h, --help            show this help message and exit
  -f FILE_PATH, --file-path FILE_PATH
                        Enter the path of the file that you want to analyse.
                        If the path contains a space, it must be surrounded in double quotes.
                        Example: -f "C:/Users/H/Desktop/my file.mp4"
  -k, --key-frames-only
                        Only process keyframes.
```
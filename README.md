# I-frames Saver
A command-line program that takes a video file as input and saves each I-frame as a PNG file. The filename of each PNG file is in the format `HH-MM-SS.ms`. As an example, if the first I-frame is present at 10.427 seconds into the video, the I-frame will be saved as `00-00-10.427.png`.

Using this program is very simple, simply specify the path of the video with the `-f` argument, e.g. `python main.py -f video.mp4`
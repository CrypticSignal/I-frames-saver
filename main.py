from argparse import ArgumentParser
import os
from pathlib import Path
import subprocess
import sys

parser = ArgumentParser()

parser.add_argument(
    '-f', '--file-path', 
    type=str, 
    required=True,
    help='Enter the path of the file that you want to analyse. '
         'If the path contains a space, it must be surrounded in double quotes. '
         'Example: -f "C:/Users/H/Desktop/my file.mp4"'
)

args = parser.parse_args()
filename = Path(args.file_path).name
output_folder = filename
os.makedirs(output_folder, exist_ok=True)
timestamps_path = os.path.join(output_folder, "Timestamps.txt")

if len(os.listdir(output_folder)) > 0:
    print(f'I-frames-saver has already been run for {filename}')
    sys.exit()

cmd = [
    'ffmpeg', '-loglevel', 'warning', '-stats', '-i', args.file_path, '-threads', str(os.cpu_count()), 
    '-vf', 'select=eq(pict_type\, I)',
    '-r', '1000',
    '-vsync', '2',
    '-frame_pts', 'true',
    os.path.join(output_folder, '%d.png')
]

print('Saving the I-frames as PNG files...')
subprocess.run(cmd)
print(f'Done! {filename} has {len(os.listdir(output_folder)) - 1} I-frames.')

print('Attempting to rename the PNG files to adhere to the HH-MM-SS.ms format...')

for file in os.listdir(output_folder):
    if file == "Timestamps.txt":
        continue

    if "-" in file:
        print("It seems like the PNG files are already in the HH-MM-SS.ms format.")
        break

    ms = int(Path(file).stem)
    seconds, ms = divmod(ms,1000) 
    minutes, seconds = divmod(seconds, 60) 
    hours, minutes = divmod(minutes, 60)
    timestamp_formatted = f'{hours:02d}-{minutes:02d}-{seconds:02d}.{ms:03d}'
    new_filename = f'{timestamp_formatted}.png'
    os.rename(os.path.join(output_folder, file), os.path.join(output_folder, new_filename))

# Create a list, where the timestamps are sorted in ascending order.
timestamps_sorted = sorted(os.listdir(output_folder))
# -1 because Timestamps.txt is not an I-frame.

i_frame_number = 0
with open(timestamps_path, "w"): pass
print("Populating Timestamps.txt using the format <I-frame number> --> <timestamp>...")

for timestamp in timestamps_sorted:
    if timestamp == "Timestamps.txt":
        continue

    i_frame_number += 1

    with open(timestamps_path, "a") as f:
        f.write(f'{i_frame_number} --> {timestamp}\n')

print(f'Done! Check out the "{output_folder}" folder.')

from argparse import ArgumentParser
import os
from pathlib import Path
import subprocess

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
output_folder = f'[{filename}] I-frames'
os.makedirs(output_folder, exist_ok=True)

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
print('Done!')
print('Re-naming the PNG files to adhere to the HH-MM-SS.ms format...')

for file in os.listdir(output_folder):
    ms = int(Path(file).stem)
    seconds, ms = divmod(ms,1000) 
    minutes, seconds = divmod(seconds, 60) 
    hours, minutes = divmod(minutes, 60) 
    new_filename = f'{hours:02d}-{minutes:02d}-{seconds:02d}.{ms:03d}.png'
    os.rename(os.path.join(output_folder, file), os.path.join(output_folder, new_filename))

print(f'Done! Check out the "{output_folder}" folder.')

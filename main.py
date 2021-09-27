from argparse import ArgumentParser, RawTextHelpFormatter
import os
from pathlib import Path
import subprocess
import sys


def line():
    print("---------------------------------------------------------------------------------------")


parser = ArgumentParser(formatter_class=RawTextHelpFormatter)

parser.add_argument(
    "-f",
    "--file-path",
    type=str,
    required=True,
    help="Enter the path of the file that you want to analyse.\n"
    "If the path contains a space, it must be surrounded in double quotes.\n"
    'Example: -f "C:/Users/H/Desktop/my file.mp4"',
)

parser.add_argument("-k", "--key-frames-only", action="store_true", help="Only process keyframes.")

args = parser.parse_args()

filename = Path(args.file_path).name
output_folder = f"{filename} [I-frames]"

# Defaults.
skip_frame_value = "nointra"
i_frames_or_keyframes = "I-frames"

if args.key_frames_only:
    line()
    print("Keyframes only mode activated.")
    output_folder = f"{filename} [keyframes]"
    skip_frame_value = "nokey"
    i_frames_or_keyframes = "keyframes"

os.makedirs(output_folder, exist_ok=True)
timestamps_path = os.path.join(output_folder, "Timestamps.txt")
with open(timestamps_path, "w"):
    pass

if "http://" not in args.file_path and "https://" not in args.file_path:
    if not os.path.exists(args.file_path):
        print(f"{args.file_path} does not exist. Exiting.")
        sys.exit()

cmd = [
    "ffmpeg", "-loglevel", "warning",
    "-copyts",
    "-skip_frame", skip_frame_value,
    "-stats",
    "-i", args.file_path,
    "-vsync", "0",
    # "-frame_pts sets the numeral portion of the output image filename to represent the timestamp"
    # See https://superuser.com/a/1421195/1272956
    "-frame_pts", "true",
    # Setting -r 1000 means that the timestamp in the filename will be in ms.
    "-r", "1000",
    os.path.join(output_folder, "%d.png"),
]

line()
print(f"Saving the {i_frames_or_keyframes} as PNG files...")
subprocess.run(cmd)
print("Done!")
line()

get_timestamps_cmd = [
    "ffprobe", "-loglevel", "warning",
    "-skip_frame", skip_frame_value,
    "-select_streams", "V:0",
    "-show_entries", "frame=pkt_pts_time",
    "-of", "csv=print_section=0",
    args.file_path,
]

process = subprocess.Popen(
    get_timestamps_cmd,
    stdout=subprocess.PIPE,
)

print(f"The {i_frames_or_keyframes} will be printed along with their timestamp in seconds.")
print(f"This data will also be stored in {output_folder}/Timestamps.txt")

count = 0
while process.poll() is None:
    output = process.stdout.readline().decode("utf-8").strip()
    if output != "":
        count += 1
        print(f"{i_frames_or_keyframes[:-1]} #{count} --> {output}")
        with open(timestamps_path, "a") as f:
            f.write(output + "\n")

if args.key_frames_only:
    timestamps_ms = []

    with open(timestamps_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            timestamps_ms.append(int(float(line.strip()) * 1000))

    print(timestamps_ms)

    print("Deleting any PNG files that are not keyframes...")
    for file in os.listdir(output_folder):
        if file != "Timestamps.txt":
            if int(Path(file).stem) not in timestamps_ms:
                os.remove(os.path.join(output_folder, file))
                print(f"{file} deleted")


print(f"{filename} has {len(os.listdir(output_folder)) - 1} {i_frames_or_keyframes}.")
print(f'All done. Check out the "{output_folder}" folder.')

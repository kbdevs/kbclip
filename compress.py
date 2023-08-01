import os
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

def get_creation_time(file_path):
    return os.path.getctime(file_path)

def compress_video(input_file, output_file):
    command = (
        f'ffmpeg -i "{input_file}" -c:v h264_nvenc -rc constqp -qp 23 "{output_file}"'
    )
    subprocess.run(command, shell=True)
    print(f"Compressed {input_file} to {output_file}")
    os.remove(input_file)
    print(f"Deleted original file: {input_file}")

def compress_videos(directory):
    with ThreadPoolExecutor(max_workers=4) as executor:
        video_files = []
        for root, _, files in os.walk(directory):
            for filename in files:
                if filename.lower().endswith(".mp4"):
                    input_file = os.path.join(root, filename)
                    video_files.append(input_file)

        # Sort the video files by their creation time in descending order (most recent first)
        video_files.sort(key=get_creation_time, reverse=True)

        for input_file in video_files:
            output_file = os.path.join(os.path.dirname(input_file), f"compressed_{os.path.basename(input_file)}")
            executor.submit(compress_video, input_file, output_file)

if __name__ == "__main__":
    directory_path = input("What directory?: \n")  # Replace this with the actual directory path
    compress_videos(directory_path)

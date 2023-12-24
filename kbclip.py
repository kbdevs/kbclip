import os
import subprocess
import tkinter as tk
from tkinter import filedialog
from concurrent.futures import ThreadPoolExecutor

def get_creation_time(file_path):
    return os.path.getctime(file_path)

def should_compress(input_file):
    metadata_command = f'ffprobe -v error -show_entries format_tags=description -of default=noprint_wrappers=1:nokey=1 "{input_file}"'
    existing_metadata = subprocess.check_output(metadata_command, shell=True, text=True).strip()
    return existing_metadata.lower() != "kbclip"

def compress_video(input_file, output_file, prefix):
    command = f'ffmpeg -i "{input_file}" -c:v h264_nvenc -rc constqp -qp 23 -metadata description="kbclip" "{output_file}"'
    subprocess.run(command, shell=True)
    print(f"Compressed {input_file} to {output_file}")
    os.remove(input_file)
    print(f"Deleted original file: {input_file}")

def get_video_files(directory):
    video_files = []
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.lower().endswith(".mp4"):
                input_file = os.path.join(root, filename)
                video_files.append(input_file)
    return video_files

def compress_videos(directory, num_concurrent_tasks, prefix):
    with ThreadPoolExecutor(max_workers=num_concurrent_tasks) as executor:
        video_files = get_video_files(directory)

        # Sort the video files by their creation time in ascending order (oldest first)
        video_files.sort(key=get_creation_time)

        for input_file in video_files:
            output_file = os.path.join(os.path.dirname(input_file), f"{prefix}{os.path.basename(input_file)}")
            if should_compress(input_file):
                if not os.path.exists(output_file):  # Check if the output file already exists
                    executor.submit(compress_video, input_file, output_file, prefix)
                else:
                    print(f"Skipped compression for {input_file} because {output_file} already exists")
            else:
                print(f"Skipped compression for {input_file} because it already has the 'kbclip' metadata")

def remove_compressed_prefix(directory):
    # Check if the provided directory exists

    prefix = prefix_entry.get()
    # Iterate through all items (files and subdirectories) in the current directory
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)

        # If the item is a file and its name starts with "compressed_", rename it
        if os.path.isfile(item_path) and item.startswith(prefix):
            new_filename = item.replace(prefix, "", 1)
            new_path = os.path.join(directory, new_filename)

            # Rename the file
            os.rename(item_path, new_path)
            print(f"Renamed '{item}' to '{new_filename}'")

        # If the item is a subdirectory, call the function recursively to process its contents
        elif os.path.isdir(item_path):
            remove_compressed_prefix(item_path)

def validate_prefix():
    prefix = prefix_entry.get().strip()  # Get the entered prefix and remove leading/trailing spaces
    if not prefix:
        tk.messagebox.showerror("Error", "Please enter a prefix for the compressed files.")
        return False
    return True

def start_compression():
    directory = directory_entry.get()
    num_concurrent_tasks = concurrent_slider.get()
    if not validate_prefix():  # Validate the prefix before proceeding
        return
    prefix = prefix_entry.get().strip()  # Get the chosen prefix
    compress_videos(directory, num_concurrent_tasks, prefix)  # Pass the chosen prefix to compress_videos


def browse_directory():
    selected_directory = filedialog.askdirectory()
    if selected_directory:
        directory_entry.delete(0, tk.END)
        directory_entry.insert(0, selected_directory)

def remove_prefix_button_clicked():
    directory = directory_entry.get()
    remove_compressed_prefix(directory)

# Create the main application window
root = tk.Tk()
root.title("kbclip")

# Define the dark mode lavender color scheme
background_color = "#211d2e"
foreground_color = "#f2e9e4"
button_color = "#8a89a6"
slider_color = "#4f4d68"

# Set the background color for the root window
root.configure(bg=background_color)

# Create and place widgets with the dark mode lavender color scheme
label = tk.Label(root, text="Enter directory with clips:", bg=background_color, fg=foreground_color)
label.pack(pady=10)

directory_entry = tk.Entry(root, width=50, bg=background_color, fg=foreground_color)
directory_entry.pack(pady=5)

browse_button = tk.Button(root, text="Browse", command=browse_directory, bg=button_color, fg=foreground_color)
browse_button.pack(pady=5)

concurrent_slider = tk.Scale(root, from_=1, to=10, orient=tk.HORIZONTAL, label="Concurrent Tasks", bg=background_color, fg=foreground_color, troughcolor=slider_color, highlightbackground=background_color)
concurrent_slider.pack(pady=5)

# Add a new label and entry field for the prefix
prefix_label = tk.Label(root, text="Enter file prefix:", bg=background_color, fg=foreground_color)
prefix_label.pack(pady=5)

prefix_entry = tk.Entry(root, width=20, bg=background_color, fg=foreground_color)
prefix_entry.pack(pady=5)

compress_button = tk.Button(root, text="Start Compression", command=start_compression, bg=button_color, fg=foreground_color)
compress_button.pack(pady=10)

remove_prefix_button = tk.Button(root, text="Remove Compressed Prefix", command=remove_prefix_button_clicked, bg=button_color, fg=foreground_color)
remove_prefix_button.pack(pady=5)

root.mainloop()

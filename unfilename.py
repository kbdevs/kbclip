import os

def remove_compressed_prefix(directory):
    # Check if the provided directory exists
    if not os.path.isdir(directory):
        print(f"Error: The directory '{directory}' does not exist.")
        return

    # List all files in the directory
    files = os.listdir(directory)

    # Iterate through the files and rename those that start with "compressed_"
    for filename in files:
        if filename.startswith("compressed_"):
            new_filename = filename.replace("compressed_", "", 1)
            old_path = os.path.join(directory, filename)
            new_path = os.path.join(directory, new_filename)

            # Rename the file
            os.rename(old_path, new_path)
            print(f"Renamed '{filename}' to '{new_filename}'")

if __name__ == "__main__":
    directory_path = input("What directory?: \n")
    remove_compressed_prefix(directory_path)

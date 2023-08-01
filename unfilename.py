import os

def remove_compressed_prefix(directory):
    # Check if the provided directory exists
    if not os.path.isdir(directory):
        print(f"Error: The directory '{directory}' does not exist.")
        return

    # Iterate through all items (files and subdirectories) in the current directory
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)

        # If the item is a file and its name starts with "compressed_", rename it
        if os.path.isfile(item_path) and item.startswith("compressed_"):
            new_filename = item.replace("compressed_", "", 1)
            new_path = os.path.join(directory, new_filename)

            # Rename the file
            os.rename(item_path, new_path)
            print(f"Renamed '{item}' to '{new_filename}'")

        # If the item is a subdirectory, call the function recursively to process its contents
        elif os.path.isdir(item_path):
            remove_compressed_prefix(item_path)

if __name__ == "__main__":
    directory_path = input("What directory?: \n")
    remove_compressed_prefix(directory_path)

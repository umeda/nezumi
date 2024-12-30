# initial design by "Gemini, a large language model by Google AI".


import os
from PIL import Image
from datetime import datetime

def rename_files_with_exif_date(directory):
    """
    Renames files in a directory based on their EXIF creation date, appending a sequential letter for duplicates.

    Args:
        directory: The path to the directory containing the images.
    """

    file_names = set()
    for filename in os.listdir(directory):
        if filename.endswith('.jpg'):
            file_path = os.path.join(directory, filename)
            try:
                with Image.open(file_path) as img:
                    exif_data = img._getexif()
                    if exif_data:
                        date_taken = exif_data.get(36867)  # Tag for Date/Time Original
                        if date_taken:
                            date_obj = datetime.strptime(date_taken, '%Y:%m:%d %H:%M:%S')
                            new_filename = directory + date_obj.strftime('%Y%m%d%H%M%S') + '.jpg'
                            if new_filename in file_names:
                                letter = 'a'
                                while new_filename + letter in file_names:
                                    letter = chr(ord(letter) + 1)
                                new_filename += letter
                            file_names.add(new_filename)
                            os.rename(file_path, new_filename)
                            print(f"Renamed {filename} to {new_filename}")
            except (OSError, ValueError, KeyError) as e:
                print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    directory_path = "path/to/your/directory"  # Replace with your directory path
    rename_files_with_exif_date(directory_path))

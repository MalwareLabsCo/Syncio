import os
import shutil
import zipfile
import tempfile
import string
import random

def generateRandName(length=16):
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for _ in range(length))
    return password


def zip_folder_contents(source_folder, zip_filename):
    # Create a temporary directory to store the contents of the source folder
    temp_dir = tempfile.gettempdir()
    temp_source_folder = os.path.join(temp_dir, 'temp_source_folder_contents')

    # Create the temporary folder
    os.makedirs(temp_source_folder, exist_ok=True)

    # Copy the contents of the source folder to the temporary folder
    for item in os.listdir(source_folder):
        source_item = os.path.join(source_folder, item)
        temp_item = os.path.join(temp_source_folder, item)

        if os.path.isdir(source_item):
            shutil.copytree(source_item, temp_item)
        else:
            shutil.copy2(source_item, temp_item)

    # Create a zip file in the temporary directory
    zip_filepath = os.path.join(temp_dir, zip_filename)
    with zipfile.ZipFile(zip_filepath, 'w') as zipf:
        # Walk through the temporary source folder and add each file to the zip file
        for foldername, subfolders, filenames in os.walk(temp_source_folder):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                arcname = os.path.relpath(file_path, temp_source_folder)
                zipf.write(file_path, arcname)

    # Clean up: remove the temporary source folder
    try:
        shutil.rmtree(temp_source_folder)
    except PermissionError:
        os.rename(temp_source_folder, tempfile.gettempdir()+"\\"+generateRandName())

# EXAMPLE:
#folder_to_be_copied = '/path/to/your/source/folder'
#zip_filename = 'zipped_contents.zip'

#zip_folder_contents(folder_to_be_copied, zip_filename)
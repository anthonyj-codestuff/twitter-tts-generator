import os
import datetime
import shutil
import constants as c

def find_file(file_dir, base_name, ext):
    image_path = os.path.join(file_dir, f"{base_name}{ext}")
    if os.path.exists(image_path):
        return image_path
    return None

def find_image_file(file_dir, base_name):
    image_extensions = ['.jpg', '.jpeg', '.png']
    for ext in image_extensions:
        image_path = os.path.join(file_dir, f"{base_name}{ext}")
        if os.path.exists(image_path):
            return image_path
    return None

def erase_file_contents(file_path):
    try:
        with open(file_path, "w") as file:
            file.truncate()
    except Exception as e:
        addLogToFile(f"Error erasing '{file_path}': {str(e)}", c.LOG_FILE)

def delete_file(file_path):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        addLogToFile(f"Error deleting '{file_path}': {str(e)}", c.LOG_FILE)

def addLogToFile(text, filepath):
    with open(filepath, "a", encoding="utf-8") as file:
        file.write(f"{datetime.datetime.now()}: {text}\n")

def moveFilesToDestination(sourceDir, logFilepath, destinationDir):
    if not os.path.exists(sourceDir):
        print(f"Source directory '{sourceDir}' does not exist.")
        return
    if not os.path.exists(destinationDir):
        print(f"Destination directory '{destinationDir}' does not exist.")
        return

    for filename in os.listdir(sourceDir):
        sourceFilePath = os.path.join(sourceDir, filename)
        if not os.path.exists(sourceFilePath):
            destinationFilePath = os.path.join(destinationDir, filename)
            print(f"Moving {filename}")
            try:
                shutil.copy(sourceFilePath, destinationFilePath)
            except FileExistsError as err:
                addLogToFile(f"{err}", logFilepath)
            except FileNotFoundError as err:
                addLogToFile(f"{err}", logFilepath)
        else:
            addLogToFile(f"WARN: File {filename} already exists", logFilepath)
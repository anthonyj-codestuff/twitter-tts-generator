import os
import re
import datetime
import shutil
import constants as c

def findFile(file_dir, base_name, ext):
    image_path = os.path.join(file_dir, f"{base_name}{ext}")
    if os.path.exists(image_path):
        return image_path
    return None

def findImageFile(file_dir, base_name):
    image_extensions = ['.jpg', '.jpeg', '.png']
    for ext in image_extensions:
        image_path = os.path.join(file_dir, f"{base_name}{ext}")
        if os.path.exists(image_path):
            return [image_path, ext]
    return None

def findVideoFile(file_dir, base_name):
    image_extensions = [".mp4"]
    for ext in image_extensions:
        image_path = os.path.join(file_dir, f"{base_name}{ext}")
        if os.path.exists(image_path):
            return [image_path, ext]
    return None

def eraseFileContents(filepath):
    try:
        with open(filepath, "w") as file:
            file.truncate()
    except Exception as e:
        addLogToFile(f"Error erasing '{filepath}': {str(e)}", c.LOG_FILE)

def deleteFile(filepath):
    if c.WRITE_COMMANDS:
        addCommandToFile(f"IF EXIST {filepath} DEL /F {filepath}")
    else:
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
        except Exception as e:
            addLogToFile(f"Error deleting '{filepath}': {str(e)}", c.LOG_FILE)

def addLogToFile(text, filepath):
    with open(filepath, "a", encoding="utf-8") as file:
        file.write(f"{datetime.datetime.now()}: {text}\n")

def addCommandToFile(text):
    with open(c.COMMANDS_FILEPATH, "a", encoding="utf-8") as file:
        file.write(f"{text}\n")

def findParentTweetById(id):
    for filename in os.listdir(c.TWEETS_DIR):
        matchesPattern =  re.match(r'^' + str(id) + '-[a-zA-Z0-9_]+_pd_\d{8}.json', filename)
        if matchesPattern:
            return filename

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
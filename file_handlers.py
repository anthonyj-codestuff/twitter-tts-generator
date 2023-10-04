import os
import re
import datetime
import shutil
import constants as c
import file_handlers as fileUtils

extract_video_frame_template = (
    c.FFMPEG_PATH + ' -i {video_filepath} -vf "scale=iw*sar:ih,setsar=1" -vframes 1 ' + c.TWEETS_DIR + '\{filename}.png'
)

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
    video_extensions = [".mp4"]
    for ext in video_extensions:
        video_path = os.path.join(file_dir, f"{base_name}{ext}")
        if os.path.exists(video_path):
            return [video_path, ext]
    return None

def extractVideoFrameToAssets(input):
    file = os.path.basename(input)
    filename = os.path.splitext(file)[0]
    
    extractCommand = extract_video_frame_template.format(video_filepath=input, filename=filename)
    if c.WRITE_COMMANDS:
        fileUtils.addCommandToFile(extractCommand)
        return os.path.join(c.TWEETS_DIR, f"{filename}.png")
    else:
        # TODO: Run extract script immediately
        return

def eraseFileContents(filepath):
    try:
        with open(filepath, "w") as file:
            file.truncate()
    except Exception as e:
        addLogToFile(f"Error erasing '{filepath}': {str(e)}")

def deleteFile(filepath):
    if c.WRITE_COMMANDS:
        addCommandToFile(f"IF EXIST {filepath} DEL /F {filepath}")
    else:
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
        except Exception as e:
            addLogToFile(f"Error deleting '{filepath}': {str(e)}")

def addLogToFile(text):
    if not c.USE_LOGS:
        return
    with open(c.LOG_FILEPATH, "a", encoding="utf-8") as file:
        file.write(f"{datetime.datetime.now()}: {text}\n")

def addTweetToArchive(filename):
    if not c.USE_ARCHIVE:
        return
    with open(c.ARCHIVE_FILEPATH, "a", encoding="utf-8") as file:
        file.write(f"{filename}\n")

def existsInArchive(target):
    if not c.USE_ARCHIVE:
        return False
    try:
        with open(c.ARCHIVE_FILEPATH, 'r', encoding="utf-8") as file:
            for line in file:
                line = line.rstrip()
                if line == target:
                    return True
        return False
    except FileNotFoundError:
        error = f"File '{c.ARCHIVE_FILEPATH}' not found."
        addLogToFile(error)
        print(error)
        return False
    except Exception as e:
        addLogToFile(f"An error occurred: {str(e)}")
        return False

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
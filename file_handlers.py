import os
import re
import datetime
import shutil
import constants as c
import file_handlers as fileUtils
import subprocess
import json

extract_video_frame_template = (
    c.FFMPEG_PATH + ' -i {video_filepath} -vf "scale=iw*sar:ih,setsar=1" -vframes 1 -y ' + c.TWEETS_DIR + '\{filename}.png'
)

move_file_template = (
    'MOVE /Y "{file}" "{destination_dir}"'
)

def loadJSONData(filepath, keys=None):
    data = {}
    try:
        with open(filepath, 'r', encoding="utf-8") as json_file:
            rawData = json.load(json_file)

            if keys is not None:
                for key in keys:
                    if key in rawData:
                        data[key] = rawData[key]
            else:
                data = rawData
            return data
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}")
        return None

def findImageFile(file_dir, base_name): # Expecting: "ID-USERNAME_pd_DATE" for base_name
    image_extensions = ['.jpg', '.jpeg', '.png']
    for ext in image_extensions:
        image_path = os.path.join(file_dir, f"{base_name}{ext}")
        if os.path.exists(image_path):
            return [image_path, ext]
    return None

def findVideoFile(file_dir, base_name): # Expecting: "ID-USERNAME_pd_DATE" for base_name
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

def deleteFile(filepath, override=False):
    # If override is true, this will on-demand delete a file even if WRITE_COMMANDS is set
    if c.WRITE_COMMANDS and not override:
        addCommandToFile(f"IF EXIST \"{filepath}\" DEL /F \"{filepath}\"")
    else:
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
        except Exception as e:
            addLogToFile(f"Error deleting '{filepath}': {str(e)}")

def addLogToFile(text, printLog=False):
    if printLog:
        print(text)
    if not c.USE_LOGS:
        return
    with open(c.ERRORLOG_FILEPATH, "a", encoding="utf-8") as file:
        file.write(f"{datetime.datetime.now()}: {text}\n")

def addTweetToArchive(filename):
    if not c.USE_ARCHIVE:
        return
    with open(c.ARCHIVE_FILEPATH, "a", encoding="utf-8") as file:
        file.write(f"{filename}\n")

def existsInArchive(target):
    if not c.USE_ARCHIVE or c.CUSTOM_TWEET_LIST:
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
    #TODO this name does not accurately describe the behavior of this function
    for filename in os.listdir(c.TWEETS_DIR):
        matchesPattern =  re.match(r'^' + str(id) + '-[a-zA-Z0-9_]+_pd_\d{8}.json', filename)
        if matchesPattern:
            return filename

def getListOfFilesForTweet(tweetFile): # Expecting: "ID-USERNAME_pd_DATE.json"
    fileList = []
    childTweet = None
    childImage = None
    childVideo = None
    parentTweet = None
    parentImage = None
    parentVideo = None

    childTweet = os.path.join(c.TWEETS_DIR, tweetFile)
    childName = os.path.splitext(tweetFile)[0]
    childImageData = findImageFile(c.TWEETS_DIR, childName)
    if childImageData:
        childImage = childImageData[0]
    childVideoData = findVideoFile(c.TWEETS_DIR, childName)
    if childVideoData:
        childVideo = childVideoData[0]

    parentData = loadJSONData(os.path.join(c.TWEETS_DIR, tweetFile), ["reply_id"])
    parentFilename = findParentTweetById(parentData["reply_id"]) if parentData["reply_id"] else None
    if parentFilename:
        parentName = os.path.splitext(parentFilename)[0]
        parentImageData = findImageFile(c.TWEETS_DIR, parentName)
        if parentImageData:
            parentImage = parentImageData[0]
        parentVideoData = findVideoFile(c.TWEETS_DIR, parentName)
        if parentVideoData:
            parentVideo = parentVideoData[0]
        parentTweet = os.path.join(c.TWEETS_DIR, parentFilename)
        

    if childTweet:
        fileList.append(childTweet)
    if childImage:
        fileList.append(childImage)
    if childVideo:
        fileList.append(childVideo)
    if parentTweet:
        fileList.append(parentTweet)
    if parentImage:
        fileList.append(parentImage)
    if parentVideo:
        fileList.append(parentVideo)
    return fileList

def moveFileToDestination(sourceFile, destinationDir):
    filename = os.path.basename(sourceFile)
    if not os.path.isfile(sourceFile) and not c.WRITE_COMMANDS:
        # this is a bit risky if writing commands
        addLogToFile(f"Error moving file to destination: Source file '{sourceFile}' does not exist.", True)
        return
    if not os.path.exists(destinationDir):
        print(f"Error moving file to destination: Destination directory '{destinationDir}' does not exist.", True)
        return
    if os.path.isfile(os.path.join(destinationDir, filename)):
        print(f"Error moving file to destination: File '{filename}' already exists at {destinationDir}.", True)
        return

    if c.WRITE_COMMANDS:
        moveCommand = move_file_template.format(file=sourceFile, destination_dir=destinationDir)
        addCommandToFile(moveCommand)
        return os.path.join(destinationDir, filename)
    else:
        print(f"Moving {filename}")
        try:
            shutil.move(sourceFile, destinationDir)
        except FileExistsError as err:
            addLogToFile(f"{err}")
        except FileNotFoundError as err:
            addLogToFile(f"{err}")

def echo(input):
    if c.WRITE_COMMANDS:
        fileUtils.addCommandToFile(f"echo {input}")
        print(input)
    else:
        subprocess.run(f"echo {input}")

def genlog(input):
    with open(c.GENLOG_FILEPATH, "a", encoding="utf-8") as file:
        file.write(f"{input}\n")

def deleteAssets(fileList):
    dedupedFiles = []
    for i in fileList:
        if i not in dedupedFiles:
            dedupedFiles.append(i)
    for file in dedupedFiles:
        fileUtils.deleteFile(file, False)

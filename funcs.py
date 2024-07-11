import re
import os
import json
import audio
import text_handlers as textUtils
import file_handlers as fileUtils
import constants as c

def pickTweetsByUser(twitterName):
  tweets = []
  for filename in os.listdir(c.TWEETS_DIR):
    matchesPattern = re.match(r'^\d{17,20}-' + twitterName + '_pd_\d{8}.json', filename)
    # bail if name mismatch
    if not matchesPattern:
      continue
    # if picking all tweets, accept this one
    if not c.REPLIES_ONLY:
      tweets.append(filename)
      continue
    # open file and check for replyId
    data = fileUtils.loadJSONData(os.path.join(c.TWEETS_DIR, filename))
    replyId = int(data["reply_id"])
    if replyId and replyId > 0:
      tweets.append(filename)
  fileUtils.addLogToFile(f"found {len(tweets)} eligible tweets")
  return tweets

def loadCustomTweetList():
  fileUtils.addLogToFile(f"Loading custom tweet list")
  try:
    with open(c.CUSTOM_TWEET_LIST_FILEPATH, "r") as file:
      lines = file.readlines()

    validFiles = []
    foundError = False

    for line in lines:
      # check if it's a string of 17-20 numerals
      line = line.strip()
      # just skip it if it's a whitespace-only line
      if not line:
        continue
      if len(line) >= 17 and len(line) <= 20 and line.isdigit():
        # Check if a corresponding JSON file already exists
        pattern = f"{line}-{c.MAIN_ACCOUNT}_pd_" + r"\d{8}\.json"
        jsonFilenames = [f for f in os.listdir(c.TWEETS_DIR) if re.match(pattern, f)]
        if any(json_filename for json_filename in jsonFilenames):
          # print(f"found file {jsonFilenames[0]} for id {line}")
          if not c.REPLIES_ONLY:
            validFiles.append(jsonFilenames[0])
            continue
          # open file and check for replyId
          with open(os.path.join(c.TWEETS_DIR, jsonFilenames[0]), "r", encoding="utf-8") as json_file:
            replyId = 0
            try:
              data = json.load(json_file)
              replyId = int(data["reply_id"])
            except json.JSONDecodeError:
              print(f"Error decoding JSON in file: {jsonFilenames[0]}")
            if replyId > 0:
              validFiles.append(jsonFilenames[0])


        else:
          fileUtils.addLogToFile(f"ERROR: JSON for tweet {line} does not exist")
          foundError = True
      else:
        fileUtils.addLogToFile(f"ERROR: Invalid line in tweet list: {line}\n")
        foundError = True
    if not foundError:
      return validFiles
    else:
      return []
  except FileNotFoundError:
    fileUtils.addLogToFile(f"ERROR: Custom tweet file not found\n")
    return []
  except Exception as e:
    fileUtils.addLogToFile(f"ERROR: Error processing custom tweet file: {str(e)}\n")
    return []

def loadJSONData(filepath):
  with open(filepath, "r", encoding="utf-8") as json_file:
    try:
      print(f"loading {filepath}")
      return json.load(json_file)
    except json.JSONDecodeError:
      print(f"ERROR: Error decoding JSON in file: {filepath}")

def checkTweetForParent(filename):
  replyId = 0
  data = loadJSONData(os.path.join(c.TWEETS_DIR, filename))
  replyId = int(data["reply_id"])
  if replyId > 0:
    return replyId

def checkTweetForQuoted(filename):
  data = loadJSONData(os.path.join(c.TWEETS_DIR, filename))
  originalId = data["tweet_id"]
  for file in os.listdir(c.TWEETS_DIR):
    if file.endswith(".json"):
      data = loadJSONData(os.path.join(c.TWEETS_DIR, file))
      quoteId = data["quote_id"]
      if quoteId == originalId:
        return data["tweet_id"]

def tweetToSanitizedContent(filepath):
  with open(filepath, "r", encoding="utf-8") as json_file:
    try:
      data = json.load(json_file)
      if "content" in data and len(data["content"]) > 0:
        content = data["content"]
        contentOneline = content.replace("\r", "").replace("\n", "")
        fileUtils.genlog(f"Tweet before sanitizing: {contentOneline}")
        content = textUtils.sanitize(content)
        return content
    except json.JSONDecodeError:
      log = f"ERROR: Error decoding JSON in file: {filepath}"
      print(log)
      fileUtils.addLogToFile(log)

# This should do a bunch of things. It should result in an audio file that contains:
# TODO the quoted tweet (and any audio it might contain)
# DONE main tweet body, regardless of length
# DONE Any audio contained in the attached media
# TODO An OCR of the image attached
def tweetFileToAudioPath(directory, file, mode=c.TweetModes.CHILD):
  # Check for video and extract audio
  filename = os.path.splitext(file)[0]
  videoAudioPath = retrieveVideoAudioForTweet(directory, filename)

  filepath = os.path.join(directory, file)
  print(f"Parsing file: {file}")
  content = tweetToSanitizedContent(filepath)
  if not content:
    # there is no text content for this tweet. Check if there is video and return that instead
    if videoAudioPath:
      # in the case that there is ONLY video for a given tweet, this will assign a voice to it so that files can be named correctly
      # if the child and the parent are both from the same account, they will have different voices, but it's fine because TTS is not done
      voiceForVideoOnly = c.VOICE_NORMAL if mode == c.TweetModes.CHILD else c.VOICE_GENERIC
      convertedAudio = audio.convertAudioFile(videoAudioPath, voiceForVideoOnly)
      # if a file does not go through TTS, it is not moved to the TTS folder. Do that before returning the file
      movedFile = fileUtils.moveFileToDestination(convertedAudio, c.TTS_DIR)
      return [movedFile, voiceForVideoOnly]
    fileUtils.genlog(f"Tweet after sanitizing:  {content}")
    print(f"empty tweet {file}")
  elif mode == c.TweetModes.CHILD:
    voice = c.VOICE_MAD if textUtils.stringHasMostlyCaps(content) else c.VOICE_NORMAL
    # text is prepped, send it to tortoise
    file = audio.generateAudio(content, voice)
    if videoAudioPath:
      # video exists. merge with tweet before returning
      file = audio.mergeAudioFilesToWav(file, videoAudioPath, voice)
    fileUtils.genlog(f"Tweet after sanitizing:  {content}")
    return [file, voice]
  else:
    twitterHandle = re.search(r'-(\w+)_pd_\d+\.json$', file).group(1)
    sanitizedHandle = textUtils.sanitize(f"@{twitterHandle}", False)
    if mode == c.TweetModes.QUOTE:
      contentWithIntro = f"quoted from {sanitizedHandle}, {content}"
    else:
      contentWithIntro = f"from {sanitizedHandle}, {content}"

    voice = findCustomVoice(twitterHandle)
    file = audio.generateAudio(contentWithIntro, voice)
    if videoAudioPath:
      # video exists. merge with tweet before returning
      file = audio.mergeAudioFilesToWav(file, videoAudioPath, voice)
    fileUtils.genlog(f"Tweet after sanitizing:  {contentWithIntro}")
    return [file, voice]
  
def retrieveVideoAudioForTweet(directory, filename):
  tweetVideoVars = fileUtils.findVideoFile(directory, filename)
  if not tweetVideoVars:
    return None
  videoPath = tweetVideoVars[0]
  audioPath = audio.extractAudioFromVideo(videoPath)
  return audioPath
  
def findCustomVoice(name):
  # retrieve the assigned voice for the given username or use the default
  return c.USER_DICT.get(name, c.VOICE_GENERIC)
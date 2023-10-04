import re
import os
import json
import audio
import text_handlers as textUtils
import file_handlers as fileUtils
import constants as c

def pickTweetsByUser(twitterName, repliesOnly=False):
  tweets = []
  for filename in os.listdir(c.TWEETS_DIR):
    print(f"picking file {filename}")
    matchesPattern = re.match(r'^\d{19}-' + twitterName + '_pd_\d{8}.json', filename)
    # bail if name mismatch
    if not matchesPattern:
      continue
    # if picking all tweets, accept this one
    if not repliesOnly:
      tweets.append(filename)
      continue
    # open file and check for replyId
    with open(os.path.join(c.TWEETS_DIR, filename), "r", encoding="utf-8") as json_file:
      replyId = 0
      try:
        print(f"loading {os.path.join(c.TWEETS_DIR, filename)}")
        data = json.load(json_file)
        replyId = int(data["reply_id"])
      except json.JSONDecodeError:
        print(f"Error decoding JSON in file: {filename}")
      if replyId > 0:
        tweets.append(filename)
  return tweets

def checkTweetForParent(filename):
  with open(os.path.join(c.TWEETS_DIR, filename), "r", encoding="utf-8") as json_file:
    replyId = 0
    try:
      print(f"loading {os.path.join(c.TWEETS_DIR, filename)}")
      data = json.load(json_file)
      replyId = int(data["reply_id"])
    except json.JSONDecodeError:
      print(f"Error decoding JSON in file: {filename}")
    if replyId > 0:
      return replyId

def tweetToSanitizedContent(filepath):
  with open(filepath, "r", encoding="utf-8") as json_file:
    try:
      data = json.load(json_file)
      if "content" in data and len(data["content"]) > 0:
        content = data["content"]
        content = textUtils.sanitize(content)
        return content
    except json.JSONDecodeError:
      log = f"Error decoding JSON in file: {filepath}"
      print(log)
      fileUtils.addLogToFile(log, c.LOG_FILEPATH)

def tweetFileToAudioPath(directory, file, isChild=True):
  # Check for video and extract audio
  filename = os.path.splitext(file)[0]
  videoAudioPath = retrieveVideoAudioForTweet(directory, filename)

  filepath = os.path.join(directory, file)
  print(f"Parsing file: {file}")
  content = tweetToSanitizedContent(filepath)
  if not content:
    # there is no text content for this tweet. Check if there is video and return that instead
    if videoAudioPath:
      # name the file as though it has the generic voice
      convertedAudio = audio.convertAudioFile(videoAudioPath, c.VOICE_GENERIC)
      return [convertedAudio, c.VOICE_GENERIC]
    print(f"empty tweet {file}")
  elif isChild:
    voice = c.VOICE_MAD if textUtils.stringHasMostlyCaps(content) else c.VOICE_NORMAL
    # text is prepped, send it to tortoise
    file = audio.generateAudio(content, voice)
    if videoAudioPath:
      # video exists. merge with tweet before returning
      file = audio.mergeAudioFilesToWav(videoAudioPath, file, voice)
    return [file, voice]
  else:
    twitterHandle = re.search(r'-(\w+)_pd_\d+\.json$', file).group(1)
    contentWithIntro = f"from {twitterHandle}. {content}"

    voice = findCustomVoice(twitterHandle)
    file = audio.generateAudio(contentWithIntro, voice)
    if videoAudioPath:
      # video exists. merge with tweet before returning
      file = audio.mergeAudioFilesToWav(videoAudioPath, file, voice)
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
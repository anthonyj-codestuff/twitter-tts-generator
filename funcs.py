import re
import os
import json
import tortoise
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

def tweetFileToAudioPath(directory, filename):
  filepath = os.path.join(directory, filename)
  print(f"Parsing file: {filename}")
  content = tweetToSanitizedContent(filepath)
  if content:
    # text is prepped, send it to tortoise
    print(f"{content}\n")
  else:
    print(f"empty tweet {filename}")
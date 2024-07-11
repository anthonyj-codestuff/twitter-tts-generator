import os
# YTDL_PATH = "Path to yt-dlp executable"
YTDL_PATH = "C:\\...\\yt-dlp.exe"
# FFMPEG_PATH = "Path to ffmpeg executable"
FFMPEG_PATH = "C:\\...\\ffmpeg.exe"
# FFPROBE_PATH = "Path to ffprobe executable"
FFPROBE_PATH = "C:\\...\\ffprobe.exe"
# ATOMICPARSLEY_PATH = "Path to AtomicParsley executable - Useful for attaching artwork to audio files"
ATOMICPARSLEY_PATH = "C:\\...\\AtomicParsley.exe"
# TORTOISETTS_PATH = "Path to tortoise-tts do_tts.py script"
TORTOISETTS_PATH = "C:\\...\\Tortoise TTS\\tortoise\\do_tts.py"

#### OPTIONS - TURN OFF CERTAIN FUNCTIONALITY ####
FETCH_NEW_TWEETS = True
FETCH_MISSING_PARENT_TWEETS = True
# Fetch new tweets from a range of dates [y,m,d,Y,M,D] or False to fetch from last fetch
# TODO Not working
CUSTOM_FETCH_RANGE = False
CUSTOM_FETCH_PARAMS = [2019,2,22,2019,3,14]
# Get tweets to process from a list of json filenames (These should all be from the MAIN_ACCOUNT)
CUSTOM_TWEET_LIST = True
# Skip all tweets that are not responding to someone else
REPLIES_ONLY = False
# Write commands to a file instead of running them now
WRITE_COMMANDS = True
# Add tweets to an archive file after generating and check archive before generating
USE_ARCHIVE = True
USE_LOGS = True
# Delete asset JSON files, images, and videos after all tweets are processed
DELETE_ASSETS = True
# After generating the file, move it to PODCAST_DIR
MOVE_TO_DESTINATION = True
# Use AtomicParsley to attach images to audio. Seems to produce better results, but ffmpeg also works
USE_ATOMICPARSLEY = True

# turtle-tts voice names
VOICE_NORMAL = "voice for normal child tweets"
VOICE_MAD = "voice for ALL CAPS child tweets"
VOICE_GENERIC = "train_mouse"

# length to split tweet into multiple TTSs
MAX_TWEET_LENGTH = 350

# twitter account names
MAIN_ACCOUNT = "Main"
USER_DICT = {
  "twitter handle": "voice name",
}

# conda commands
# %windir%\System32\cmd.exe "/K" C:\Users\USER\miniconda3\Scripts\activate.bat tortoise
ACTIVATE_CONDA = 'C:\\WINDOWS\\System32\\cmd.exe "/K" C:\\Users\\USER\\miniconda3\\Scripts\\activate.bat tortoise'

###
## probably don't touch stuff below this point
###

# important directory names
PATH = os.path.dirname(os.path.realpath(__file__))
TTS_DIR = os.path.join(PATH, "AudioTTS")
TWEETS_DIR = os.path.join(PATH, "tweets")
JUSTCAST_DIR = "C:\\Dropbox\\Apps\\justcast"
PODCAST_DIR = os.path.join(JUSTCAST_DIR, "Feed FolderName")

ERRORLOG_FILEPATH = os.path.join(PATH, "logs.txt")
GENLOG_FILEPATH = os.path.join(PATH, "last-run-logs.txt")
ARCHIVE_FILEPATH = os.path.join(PATH, "archive.txt")
COMMANDS_FILEPATH = os.path.join(PATH, "commands.bat")
LAST_RUN_FILEPATH = os.path.join(PATH, "last-run.txt")
CUSTOM_TWEET_LIST_FILEPATH = os.path.join(PATH, "custom-tweet-list.txt")

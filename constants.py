import os
# DEST_DIR = "Path to \\Dropbox\\Apps\\justcast"
DEST_DIR = "C:\\Dropbox\\Apps\\justcast"
# YTDL_PATH = "Path to yt-dlp executable"

#### OPTIONS - TURN OFF CERTAIN FUNCTIONALITY ####
FETCH_NEW_TWEETS = True
# Write commands to a file instead of running them now
WRITE_COMMANDS = True
# Add tweets to an archive file after generating and check archive before generating
USE_ARCHIVE = True
USE_LOGS = True

# turtle-tts voice names
VOICE_NORMAL = "voice for normal child tweets"
VOICE_MAD = "voice for ALL CAPS child tweets"
VOICE_GENERIC = "train_mouse"

# twitter account names
MAIN_ACCOUNT = "Main"
USER_DICT = {
  "twitter handle": "voice name",
}

# important directory names
PATH = os.path.dirname(os.path.realpath(__file__))
TTS_DIR = os.path.join(PATH, "AudioTTS")
TWEETS_DIR = os.path.join(PATH, "tweets")

LOG_FILEPATH = os.path.join(PATH, "logs.txt")
ARCHIVE_FILEPATH = os.path.join(PATH, "archive.txt")
COMMANDS_FILEPATH = os.path.join(PATH, "commands.bat")
LAST_RUN_FILEPATH = os.path.join(PATH, "last-run.txt")

import os
# DEST_DIR = "Path to \\Dropbox\\Apps\\justcast"
DEST_DIR = "C:\\Dropbox\\Apps\\justcast"
# YTDL_PATH = "Path to yt-dlp executable"
YTDL_PATH = "C:\\yt-dlp.exe"

# turtle-tts voice names
VOICE_NORMAL = "voice for normal child tweets"
VOICE_MAD = "voice for ALL CAPS child tweets"
VOICE_GENERIC = "train_mouse"

# twitter account names
MAIN_ACCOUNT = "account name to fetch"
USER_DICT = {
  "twitter handle": "voice name",
}

# important directory names
PATH = os.path.dirname(os.path.realpath(__file__))
TTS_DIR = os.path.join(PATH, "AudioTTS")
TWEETS_DIR = os.path.join(PATH, "tweets")

LOG_FILEPATH = os.path.join(PATH, "logs.txt")
LAST_RUN_FILEPATH = os.path.join(PATH, "last-run.txt")

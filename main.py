import os
import re
import constants as c
import new_tweets as newtweets
import funcs as funcs

def main():
        # Get all new tweets 
    # newtweets.get()
        # Pick out tweets
    tweetsToProcess = funcs.pickTweetsByUser(c.MAIN_ACCOUNT, True)
        # For each
    for tweet in tweetsToProcess:
        child_media = None # (path to image or Null)
        parent_media = None # (path to image or Null)
        child_voice = "" # (normal or mad)
        child = "" # (path to audio)
        parent = "" # (path to audio)
            # get the content for the tweet
            # Sanitize the text or skip if blank
        child = funcs.tweetFileToAudioPath(c.TWEETS_DIR, tweet)
            # Generate a wav, normal or MAD, save the {choice}
            # If reply_id > 0:
                # save the name of the parent
                # get the content for the tweet
                # Sanitize the text or skip if blank
                # Generate a generic wav
            # If {choice}.wav && generic.wav:
                # Merge two wavs to m4a, save name
                # Check for child picture OR parent picture. Save name
            # If {choice}.wav &! generic.wav:
                # Convert to m4a, save name
                # Check for picture, save name
            # If child OR parent picture:
                # Add picture to m4a
            # Delete {choice}.wav
            # Delete generic.wav
            # Delete merged.wav
            # Delete parent.png
            # Delete child.png

if __name__ == "__main__":
    main()

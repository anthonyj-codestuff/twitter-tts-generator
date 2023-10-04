import os
import re
import constants as c
import new_tweets as newtweets
import funcs as funcs
import file_handlers as fileUtils
import audio

def main():
        # Get all new tweets 
    newtweets.get()
        # Pick out relevant child tweets
    tweetsToProcess = funcs.pickTweetsByUser(c.MAIN_ACCOUNT, False)

    for tweet in tweetsToProcess:
        # global values determine the structure of the final audio
        childTweet = os.path.join(c.TWEETS_DIR, tweet)
        parentTweet = None # ()
        childImage = None # (path to image or None)
        parentImage = None # (path to image or None)
        childVoice = None # (normal or mad)
        parentVoice = None # (defined in constants)
        child = None # (path to audio)
        parent = None # (path to audio)

        # Generate a child wav, it will return normal or mad, save the filepath and voice for later
        vars = funcs.tweetFileToAudioPath(c.TWEETS_DIR, tweet, True)
        if vars:
            child = vars[0]
            childVoice = vars[1]
            # check for Image
            childImage = fileUtils.findImageFile(c.TWEETS_DIR, os.path.splitext(tweet)[0])
        # Check for a parent tweet. If it exists, generate a new file
        parentId = funcs.checkTweetForParent(tweet)
        if parentId and child:
            parentFilename = fileUtils.findParentTweetById(parentId)
            if parentFilename:
                parentTweet = os.path.join(c.TWEETS_DIR, parentFilename)
                # save the name of the parent
                # get the content for the tweet
                parentVars = funcs.tweetFileToAudioPath(c.TWEETS_DIR, parentFilename, False)
                if parentVars:
                    parent = parentVars[0]
                    parentVoice = parentVars[1]
                    # While we're here, check for Image
                    parentImageVars = fileUtils.findImageFile(c.TWEETS_DIR, os.path.splitext(parentFilename)[0])
                    if parentImageVars:
                        parentImage = os.path.join(c.TWEETS_DIR, parentImageVars[0])
                        parentImageExt = parentImageVars[1]
        # at this point, everything has been collected and generated
        if child and not parent:
            # convert child audio to aac and attach image(?)
            convertedChild = audio.convertAudioFile(child, os.path.splitext(tweet)[0])
            # there might still be a parent image even if there is no parent audio
            eligibleImage = childImage if childImage else parentImage
            if eligibleImage:
                audio.addImageToFile(convertedChild, eligibleImage)
        elif child and parent:
            # merge child audio to parent, convert to aac, and attach image(?)
            # prefer the child image
            mergedWav = audio.mergeAudioFilesToWav(parent, child, os.path.splitext(tweet)[0])
            convertedChild = audio.convertAudioFile(mergedWav, os.path.splitext(tweet)[0])
            eligibleImage = childImage if childImage else parentImage
            if eligibleImage:
                audio.addImageToFile(convertedChild, eligibleImage)
        
        # if child and childVoice:
        #     fileUtils.deleteFile(os.path.join(c.TTS_DIR, f"{childVoice}_0.wav"))
        # if parent and parentVoice:
        #     fileUtils.deleteFile(os.path.join(c.TTS_DIR, f"{parentVoice}_0.wav"))
        # Delete {voice}.wav
        # Delete generic.wav
        # Delete merged.wav
        # Delete parent.png
        # Delete child.png
        print(f"final state for tweet: {tweet}")
        print(f"childTweet: {childTweet}")
        print(f"parentTweet: {parentTweet}")
        print(f"childImage: {childImage}")
        print(f"parentImage: {parentImage}")
        print(f"childVoice: {childVoice}")
        print(f"parentVoice: {parentVoice}")
        print(f"child: {child}")
        print(f"parent: {parent}")

if __name__ == "__main__":
    main()

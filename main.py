import os
import re
import constants as c
import new_tweets as newtweets
import funcs as funcs
import file_handlers as fileUtils
import audio

def main():
    fileUtils.addLogToFile(f" === === === NEW RUN === === ===")
    fileUtils.deleteFile(c.GENLOG_FILEPATH, True)
        # Get all new tweets 
    newtweets.get()
        # Pick out relevant child tweets
    tweetsToProcess = []
    filesToDelete = []
    if c.CUSTOM_TWEET_LIST:
        tweetsToProcess = funcs.loadCustomTweetList()
    else:
        tweetsToProcess = funcs.pickTweetsByUser(c.MAIN_ACCOUNT)

    for tweet in tweetsToProcess:
        tweetname = os.path.splitext(tweet)[0]
        fileUtils.echo(f"=== START {tweetname} ===")
        if fileUtils.existsInArchive(tweetname):
            fileUtils.addLogToFile(f"Skipping {tweetname}. Already in archive")
            continue

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
            childImageVars = fileUtils.findImageFile(c.TWEETS_DIR, tweetname)
            if childImageVars:
                childImage = childImageVars[0]
                childImageExt = childImageVars[1]

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
                    parentImage = parentImageVars[0]
                    parentImageExt = parentImageVars[1]

        # If there are missing images, check for a video and extract a frame
        if not childImage:
            videoFileVars = fileUtils.findVideoFile(c.TWEETS_DIR, tweetname)
            if videoFileVars:
                extractedImagePath = fileUtils.extractVideoFrameToAssets(videoFileVars[0])
                childImage = extractedImagePath
                filesToDelete.append(extractedImagePath)
        if parentTweet and not parentImage:
            file = os.path.basename(parentTweet)
            filename = os.path.splitext(file)[0]
            videoFileVars = fileUtils.findVideoFile(c.TWEETS_DIR, filename)
            if videoFileVars:
                extractedImagePath = fileUtils.extractVideoFrameToAssets(videoFileVars[0])
                parentImage = extractedImagePath
                filesToDelete.append(extractedImagePath)

        # at this point, everything has been collected and generated
        if child and not parent:
            # convert child audio to aac and attach image(?)
            convertedChild = audio.convertAudioFile(child, tweetname)
            # there might still be a parent image even if there is no parent audio
            eligibleImage = childImage if childImage else parentImage
            if eligibleImage:
                audio.addImageToFile(convertedChild, eligibleImage)
        elif child and parent:
            # merge child audio to parent, convert to aac, and attach image(?)
            # prefer the child image
            mergedWav = audio.mergeAudioFilesToWav(parent, child, tweetname)
            convertedChild = audio.convertAudioFile(mergedWav, tweetname)
            eligibleImage = childImage if childImage else parentImage
            if eligibleImage:
                audio.addImageToFile(convertedChild, eligibleImage)

        # Log current state for tweet and stage assets for deletion
        fileUtils.genlog(f"final state for tweet: {tweet}")
        if childTweet:
            fileUtils.genlog(f"childTweet: {childTweet}")
            filesToDelete.append(childTweet)
        if parentTweet:
            fileUtils.genlog(f"parentTweet: {parentTweet}")
            filesToDelete.append(parentTweet)
        if childImage:
            fileUtils.genlog(f"childImage: {childImage}")
            filesToDelete.append(childImage)
        if parentImage:
            fileUtils.genlog(f"parentImage: {parentImage}")
            filesToDelete.append(parentImage)
        if childVoice:
            fileUtils.genlog(f"childVoice: {childVoice}")
        if parentVoice:
            fileUtils.genlog(f"parentVoice: {parentVoice}")
        if child:
            fileUtils.genlog(f"child: {child}")
        if parent:
            fileUtils.genlog(f"parent: {parent}\n")
        fileUtils.addTweetToArchive(tweetname)

    if c.DELETE_ASSETS:
        fileUtils.deleteAssets(filesToDelete)
    print("done")

if __name__ == "__main__":
    main()

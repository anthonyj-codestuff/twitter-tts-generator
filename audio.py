import os
import subprocess
import constants as c
import file_handlers as fileUtils

generate_voice_template = (
    'python "' + c.TORTOISETTS_PATH + '" --text "{data}" --voice {voice} --preset fast --output_path "' + c.TTS_DIR + '" --candidates 1'
)

merge_wav_files_template = (
  c.FFMPEG_PATH + ' -i "{first_audio}" -i "{second_audio}" -filter_complex [0:a][1:a]concat=n=2:v=0:a=1 "{output_dir}\{output_name}.wav"'
)

convert_wav_file_template = (
  c.FFMPEG_PATH + ' -i "{input_audio}" -c:a aac -b:a 160k "{output_dir}\{output_name}.m4a"'
)

# This is a bit weird. Use ffprobe to check if the audio. If it exists, extract it. If it doesn't, generate a second of silence
extract_audio_template = (
  c.FFPROBE_PATH + ' -i "{input_video}" -show_entries stream=codec_type -loglevel error > "' + os.path.join(c.TWEETS_DIR, "temp.txt") + '"\n' +
  'findstr /c:"audio" "' + os.path.join(c.TWEETS_DIR, "temp.txt") + '" > nul\n' +
  'if %errorlevel% equ 0 (' + c.FFMPEG_PATH + ' -i {input_video} -vn -acodec pcm_s16le -ac 2 -y "{output_dir}\{output_name}.wav") else (' + c.FFMPEG_PATH + ' -f lavfi -t 1 -i anullsrc=r=44100:cl=stereo -acodec pcm_s16le -ac 2 -y "{output_dir}\{output_name}.wav")\n' +
  ':: gap command to stop delete from failing\n' +
  'IF EXIST "' + os.path.join(c.TWEETS_DIR, "temp.txt") + '" DEL "' + os.path.join(c.TWEETS_DIR, "temp.txt") + '"'
)

add_image_ffmpeg_template = (
  c.FFMPEG_PATH + ' -i "{input_audio}" -i "{input_image}" -map 0:a:0 -map 1:v:0 -filter:v "scale=w=500:h=500,format=yuvj420p" -c:a copy -c:v mjpeg -disposition:v:0 attached_pic -f ipod -movflags +faststart "{output_filepath}"'
)

add_image_atomicparsley_template = (
  c.ATOMICPARSLEY_PATH + ' "{input_audio}" --artwork "{input_image}" -W -o "{output_filepath}"'
)

rename_file_template = (
  'REN "{input_filepath}" "{output_file}"'
)

def getSubstringsByLength(input, maxLength=c.MAX_TWEET_LENGTH):
    words = input.split()
    result = []
    currentChunk = ""

    for word in words:
        if len(currentChunk) + len(word) + 1 <= maxLength:
            if currentChunk:
                currentChunk += " " + word
            else:
                currentChunk = word
        else:
            result.append(currentChunk)
            currentChunk = word

    if currentChunk:
        result.append(currentChunk)

    return result

def generateAudio(content, voice):
  if c.WRITE_COMMANDS:
    if len(content) > c.MAX_TWEET_LENGTH:
      # content needs to be split up into multiple files
      fileUtils.addLogToFile(f"WARNING: Contents are too long to be generated ({len(content)} characters)")
      substrings = getSubstringsByLength(content)
      # 1: Generate initial substring
      initialAudioGenCommand = generate_voice_template.format(data=substrings[0], voice=voice)
      fileUtils.addCommandToFile(initialAudioGenCommand)
      # 2: Rename generated file to allow concatenating new audio
      audioPath = os.path.join(c.TTS_DIR, f"{voice}_0.wav")
      renameCommand = rename_file_template.format(input_filepath=audioPath, output_file=f"{voice}_lump.wav")
      fileUtils.addCommandToFile(renameCommand)
      for string in substrings[1:]:
        # 3: generate next substring audio
        audioGenCommand = generate_voice_template.format(data=string, voice=voice)
        fileUtils.addCommandToFile(audioGenCommand)
        # 4: append new audio to lump file
        first = os.path.join(c.TTS_DIR, f"{voice}_lump.wav")
        second = os.path.join(c.TTS_DIR, f"{voice}_0.wav")
        mergeAudioFilesToWav(first, second, f"{voice}_new")
        # 5: rename new file to allow further concatenation
        new = os.path.join(c.TTS_DIR, f"{voice}_new.wav")
        renameCommand = rename_file_template.format(input_filepath=new, output_file=f"{voice}_lump.wav")
        fileUtils.addCommandToFile(renameCommand)
      # 6: Now that concatenation is done, rename the lump file to the finished filename
      lump = os.path.join(c.TTS_DIR, f"{voice}_lump.wav")
      renameCommand = rename_file_template.format(input_filepath=lump, output_file=f"{voice}_0.wav")
      fileUtils.addCommandToFile(renameCommand)
      # 7: return merged file
      return os.path.join(c.TTS_DIR, f"{voice}_0.wav")
    else:
      # proceed as normal
      audioCommand = generate_voice_template.format(data=content, voice=voice)
      fileUtils.addCommandToFile(audioCommand)
      return os.path.join(c.TTS_DIR, f"{voice}_0.wav")
  else:
    return
    audioCommand = generate_voice_template.format(data=content, voice=voice)
    ***REMOVED***
    ***REMOVED***
    try:
      ***REMOVED***
    except subprocess.CalledProcessError as a:
      print(a)
    ***REMOVED***
    ***REMOVED***
    ***REMOVED***

def convertAudioFile(input, output_filename):
  directory = os.path.dirname(input)
  convertCommand = convert_wav_file_template.format(input_audio=input, output_dir=directory, output_name=output_filename)
  if c.WRITE_COMMANDS:
    fileUtils.addCommandToFile(convertCommand)
    fileUtils.deleteFile(input)
    return os.path.join(directory, f"{output_filename}.m4a")
  else:
    # TODO: Run convert script immediately
    return
  
def extractAudioFromVideo(input): # extract audio into same directory as video
  directory = os.path.dirname(input)
  file = os.path.basename(input)
  fileUtils.addLogToFile(f"Extracting audio from {file}")
  extractCommand = extract_audio_template.format(input_video=input, output_dir=directory, output_name="video_audio")
  if c.WRITE_COMMANDS:
    fileUtils.addCommandToFile(extractCommand)
    # TODO: should I delete the video file?
    # fileUtils.deleteFile(input)
    return os.path.join(directory, f"video_audio.wav")
  else:
    # TODO: Run extract script immediately
    return


def mergeAudioFilesToWav(first, second, filename):
  mergeCommand = merge_wav_files_template.format(first_audio=first, second_audio=second, output_name=filename, output_dir=c.TTS_DIR)
  if c.WRITE_COMMANDS:
    fileUtils.addCommandToFile(mergeCommand)
    fileUtils.deleteFile(first)
    fileUtils.deleteFile(second)
    return os.path.join(c.TTS_DIR, f"{filename}.wav")
  else:
    # TODO: Run merge script immediately
    return
  
def addImageToFile(audioPath, imagePath):
  directory = os.path.dirname(audioPath)
  file = os.path.basename(audioPath)
  filename = os.path.splitext(file)[0]
  fileDotExt = os.path.splitext(file)[1]
  image_audio_filepath = os.path.join(directory, f"{filename}-image{fileDotExt}")
  imageCommand = ""

  if c.USE_ATOMICPARSLEY:
    imageCommand = add_image_atomicparsley_template.format(input_audio=audioPath, input_image=imagePath, output_filepath=image_audio_filepath)
  else:
    imageCommand = add_image_ffmpeg_template.format(input_audio=audioPath, input_image=imagePath, output_filepath=image_audio_filepath)
  renameCommand = rename_file_template.format(input_filepath=image_audio_filepath, output_file=file)
  if c.WRITE_COMMANDS:
    fileUtils.addCommandToFile(imageCommand)
    fileUtils.deleteFile(audioPath)
    fileUtils.addCommandToFile(renameCommand)
    return audioPath
  else:
    # TODO: Run metadata script immediately
    return
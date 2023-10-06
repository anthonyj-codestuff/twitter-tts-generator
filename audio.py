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

extract_audio_template = (
  c.FFMPEG_PATH + ' -i "{input_video}" -vn -acodec pcm_s16le -ac 2 "{output_dir}\{output_name}.wav"'
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

def generateAudio(content, voice):
  audioCommand = generate_voice_template.format(data=content, voice=voice)
  if c.WRITE_COMMANDS:
    fileUtils.addCommandToFile(audioCommand)
    return os.path.join(c.TTS_DIR, f"{voice}_0.wav")
  else:
    return
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
  
def extractAudioFromVideo(input):
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
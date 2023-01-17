import os.path
from vosk import Model
from vosk import KaldiRecognizer
import wave
import audioop
import json
import moviepy.editor as mp

if __name__ == '__main__':
    '''
    this script reads a mono wav file (inFileName) and writes out a json file (outfileResults) with the speech to text 
    conversion results.  It then writes out another json file (outfileText) that only has the "text" values.
    '''


    # set process variables
    # ########################################################################################################
    cwd = os.getcwd()
    pro_dir = os.path.join(cwd, 'processing')
    result_dir = os.path.join(cwd, 'Results')
    source_dir = os.path.join(cwd, 'Test Source')

    audio_in_file = os.path.join(pro_dir, 'audio.wav')
    audio_out_file = os.path.join(pro_dir, 'audioMono.wav')


    vosk_model = os.path.join(cwd, 'vosk-model')


    # inputs / get files
    # ########################################################################################################
    videoIn = os.path.join(source_dir, 'test_2.avi')
    out_json = os.path.join(result_dir, 'result.json')
    out_txt = os.path.join(result_dir, 'result_text.json')

    # Extract Audio from Video File
    # ########################################################################################################
    clip = mp.VideoFileClip(videoIn)
    clip.audio.write_audiofile(audio_in_file)  # generating the audio in file for next step


    # Convert to Mono channel
    # ########################################################################################################
    # read input file and write mono output file
    try:
        # open the input and output files
        inFile = wave.open(audio_in_file, 'rb')
        outFile = wave.open(audio_out_file, 'wb')
        # force mono
        outFile.setnchannels(1)
        # set output file like the input file
        outFile.setsampwidth(inFile.getsampwidth())
        outFile.setframerate(inFile.getframerate())
        # read
        soundBytes = inFile.readframes(inFile.getnframes())
        print("frames read: {} length: {}".format(inFile.getnframes(), len(soundBytes)))
        # convert to mono and write file
        monoSoundBytes = audioop.tomono(soundBytes, inFile.getsampwidth(), 1, 1)
        outFile.writeframes(monoSoundBytes)

    except Exception as e:
        print(e)

    # finally:
    #     inFile.close()
    #     outFile.close()


    # run VOSK Model
    # ########################################################################################################
    wf = wave.open(audio_out_file, "rb")

    # initialize a str to hold results
    results = ''
    textResults = []

    # build the model and recognizer objects.
    model = Model(vosk_model)
    recognizer = KaldiRecognizer(model, wf.getframerate())
    recognizer.SetWords(True)

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            recognizerResult = recognizer.Result()
            results = results + recognizerResult

            # convert the recognizerResult string into a dictionary
            resultDict = json.loads(recognizerResult)
            # save the 'text' value from the dictionary into a list
            textResults.append(resultDict.get('text', ''))
    # else:
    # print(recognizer.PartialResult())

    # process "final" result
    results = results + recognizer.FinalResult()
    resultDict = json.loads(recognizer.FinalResult())
    textResults.append(resultDict.get('text', ''))

    # write results to a file
    with open(out_json, 'w') as output:
        print(results, file=output)

    # write text portion of results to a file
    with open(out_txt, 'w') as output:
        print(json.dumps(textResults, indent=4), file=output)

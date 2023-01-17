import wave
import audioop

inFileName = r'C:\Users\Jody.Carter\Documents\GitHub\Video_Audio_Logger\converted_2.wav'
outFileName = r'C:\Users\Jody.Carter\Documents\GitHub\Video_Audio_Logger\convertedMono_2.wav'

# read input file and write mono output file
try:
    # open the input and output files
    inFile = wave.open(inFileName, 'rb')
    outFile = wave.open(outFileName, 'wb')
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

finally:
    inFile.close()
    outFile.close()

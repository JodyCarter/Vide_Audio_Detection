import speech_recognition as sr
import moviepy.editor as mp


if __name__ == '__main__':

    # clip = mp.VideoFileClip(r'C:\Users\Jody.Carter\Documents\GitHub\Video_Audio_Logger\test_2.avi')
    # clip.audio.write_audiofile(r'C:\Users\Jody.Carter\Documents\GitHub\Video_Audio_Logger\converted_2.wav')

    r = sr.Recognizer()
    audio = sr.AudioFile(r'C:\Users\Jody.Carter\Documents\GitHub\Video_Audio_Logger\convertedMono_2.wav')
    with audio as source:
        audio_file = r.record(source)
    result = r.recognize_google(audio_file, show_all=True, with_confidence=True)

    # exporting the result
    with open('recognized.txt', mode='w') as file:
        # file.write('Recognized Speech:')
        # file.write('\n')
        file.write(str(result))
        # print('ready!')

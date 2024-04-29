import speech_recognition as sr


audio_path = r"C:\Users\arsen\PycharmProjects\espanol\speech_api\voices\sample-9s.wav"
# result_path = audio_path.replace("mp3", "wav")
# sound = AudioSegment.from_mp3(audio_path)
# sound.export(result_path, format="wav")
r = sr.Recognizer()
harvard = sr.AudioFile(audio_path)
with harvard as source:
    audio = r.record(source)


if __name__ == "__main__":
    pass
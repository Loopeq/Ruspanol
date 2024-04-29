# import os
# from pathlib import Path
# from gtts import gTTS
#
# ROOT_PATH = Path("speech_api/voices")
#
# def get_voice(word: str, user_id: int):
#     word_name = Path(f"{user_id}.mp3")
#     apath = ROOT_PATH / word_name
#     language = 'es'
#     voice_obj = gTTS(text=word, tld="com", lang=language, slow=False)
#     voice_obj.save(str(apath))
#     return apath
#
# def remove_voice(apath: Path):
#     os.remove(apath)
#
# def main():
#     pass
#
# if __name__ == "__main__":
#     main()
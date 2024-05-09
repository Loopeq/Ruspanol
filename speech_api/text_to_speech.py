import asyncio
import json
import os
import random
import urllib.request as ur
import requests

from domain.settings import settings

URL = "http://api.voicerss.org/"


async def get_audio_rss(message: str, phrase_id: int) -> str:

    path = f"speech_api/voices/phrase_{phrase_id}.mp3"
    if os.path.isfile(path):
        return path

    params = {
        "key": settings.api_key,
        "src": message,
        "hl": "es-mx",
        "c": "MP3",
        "f": "44khz_16bit_stereo",
        "v": "Jose"
    }
    with requests.Session() as session:
        response = session.get(URL, params=params)
        with open(path, "wb") as f:
            f.write(response.content)
        return path


async def get_audio_eden(message: str, phrase_id: int):

    path = fr"speech_api/voices/phrase_{phrase_id}.mp3"
    if os.path.isfile(path):
        return path

    headers = {
        "Authorization": f"Bearer {settings.api_key_eden}"}

    url = "https://api.edenai.run/v2/audio/text_to_speech"

    payload = {
        "providers": "openai", "language": "es",
        "option": random.choice(["MALE", "FEMALE"]),
        "text": message,
        "fallback_providers": "google"
    }

    response = requests.post(url, json=payload, headers=headers)
    result = json.loads(response.text)
    result_url = result["openai"]["audio_resource_url"]


    ur.urlretrieve(result_url, path)
    return path

import asyncio
import json
import urllib.request as ur
import requests

from domain.settings import settings

URL = "http://api.voicerss.org/"


async def get_voice(user_id: int, message: str) -> str:
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
        path = f"speech_api/voices/{user_id}.mp3"
        with open(path, "wb") as f:
            f.write(response.content)
        return path


async def get_voice_eden(message: str, user_id: int):
    headers = {
        "Authorization": f"Bearer {settings.api_key_eden}"}

    url = "https://api.edenai.run/v2/audio/text_to_speech"
    payload = {
        "providers": "openai", "language": "es",
        "option": "MALE",
        "text": message,
        "fallback_providers": ""
    }

    response = requests.post(url, json=payload, headers=headers)
    result = json.loads(response.text)
    result_url = result["openai"]["audio_resource_url"]

    path = f"speech_api/voices/{user_id}.mp3"
    ur.urlretrieve(result_url, path)
    return path


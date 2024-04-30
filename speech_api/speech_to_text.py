import json
import requests
from aiogram.types import File

from domain.settings import settings


async def get_text_from_voice(voice_path: str):

    headers = {
        "Authorization": f"Bearer {settings.api_key_eden}"}
    url = "https://api.edenai.run/v2/audio/speech_to_text_async"
    data = {
        "providers": "openai",
        "language": "es-MX",
    }

    files = {'file': open(voice_path, 'rb')}

    response = requests.post(url, data=data, files=files, headers=headers)
    result = json.loads(response.text)
    return result["results"]["openai"]["text"]



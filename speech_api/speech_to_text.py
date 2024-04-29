import json
import requests

from domain.settings import settings


def get_text_from_voice():

    headers = {
        "Authorization": f"Bearer {settings.api_key_eden}"}
    url = "https://api.edenai.run/v2/audio/speech_to_text_async"
    data = {
        "providers": "openai",
        "language": "es-MX",
    }

    files = {'file': open("voices/952485476.mp3", 'rb')}

    response = requests.post(url, data=data, files=files, headers=headers)
    result = json.loads(response.text)
    print(result["results"]["openai"]["text"])



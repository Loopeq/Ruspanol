from g4f.client import Client

client = Client()

MESSAGES = [{"role": "system", "content": "Answer as my pen pal from Spain or Latin America."
                                          "Answer in Spanish. Don't pretend to be a bot and try to keep the conversation going."}]
def main(messages: list[dict]) -> None:

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=100,
    )
    print(response.choices[0].message.content)



if __name__ == "__main__":
    MESSAGES.append({"role": "user", "content": "Hola!. ¿Que tal? ¿De donde eres?"})
    main(MESSAGES)
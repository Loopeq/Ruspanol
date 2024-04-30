

class Strings:
    entry_info = "¡Hola! 👋 \nТебя приветствует бот для изучения испанского языка😊"
    start_conversation_info = "Начните разговор с вашим собеседником😊\n" \
                              "Вы можете использовать фразы ниже."
    wait_answer_info = "Ваш собеседник печатает.."

    cmd_dialogue_info = "Свободный разговор с ИИ💬"
    cmd_stt_info = "Переводите и проговоривайте основные фразы📖"


    @classmethod
    def message_length_info(cls, limit: int):
        return f"Кажется в вашем предложении больше {limit} слов =(. \nВаш собеседник не будет его читать."

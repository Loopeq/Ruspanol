

class Strings:
    entry_info = "¡Hola! 👋 Тебя приветствует бот для изучения испанского языка😊"
    wait_answer_info = "Ваш собеседник печатает.."

    @classmethod
    def message_length_info(cls, limit: int):
        return f"Кажется в вашем предложении больше {limit} слов =(. \nВаш собеседник не будет его читать."

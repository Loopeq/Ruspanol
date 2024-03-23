from aiogram.utils.markdown import text


class Strings:
    hello_words = "¡Hola! 👋 ¡Bienvenido al bot de español! 📚 Estoy aquí para ayudarte a explorar y enriquecer tu " \
                "vocabulario en español. 🇪🇸 ¡Vamos a aprender juntos! 😊\n/sections"
    available_sections = text(f"<b>Доступные разделы 📖</b>")

    oops_message = "Кажется тут пока ничего нет... 😿"
    back_button = "Назад ↩️"
    quit_button = "Завершить❌"

    delete_voice_button = "Удалить❌"
    voice_info = text("<b>\nНажмите на слово, чтобы послушать его🎤</b>")
    start_quiz = "Начать тест✅"
from aiogram.utils.markdown import text


class Strings:
    hello_words = "¡Hola! 👋 ¡Bienvenido al bot de español! 📚 Estoy aquí para ayudarte a explorar y enriquecer tu " \
                "vocabulario en español. 🇪🇸 ¡Vamos a aprender juntos! 😊\n/sections"
    available_sections = text(f"<b>Доступные разделы 📖</b>")

    oops_message = "Кажется тут пока ничего нет... 😿"
    back_button = "Назад ↩️"
    quit_button = "Завершить❌"
    cancel_button = "Отменить❌"
    quiz_info = "Переведите с русского на испанский - "
    delete_voice_button = "Удалить❌"
    voice_info = text("<b>\nНажмите на слово, чтобы послушать его🎤</b>")
    start_quiz = "Начать тест✅"
    yes_quiz = "✅"
    nope_quiz = "❌"
    total_quiz = "Всего:"
    quiz_final = "Тест завершен 😃"
    add_user_section = "Добавить раздел✏️"
    available_user_sections = text(f"<b>Ваши разделы 📖</b>")
    add_us_title = text(f"Введите название раздела: ")
    remove_section = "Удалить раздел🗑"

    @classmethod
    def add_us_word_info(cls, section_title):
        return f"Введите слова для раздела <b>{section_title}</b> " \
               f"в виде:\n<b>слово1 - перевод1; слово2 - перевод2</b>"

    @classmethod
    def add_us_final_info(cls, section_title):
        return f"Вы создали раздел {section_title}. Вы можете его редактировать.\n/my_sections"
from aiogram.utils.markdown import text


class Strings:
    entry_info = "¡Hola! 👋 Тебя приветствует бот для изучения испанской лексики.\n" \
                 "Ты можешь использовать мои разделы или создавать свои 😊\n/sections"
    sections_info = f"<b>Доступные разделы 📖</b>"

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
    us_start_practice = "Начать практику🧠"
    cancel_user_quiz = "Закончить практику❌"
    user_quiz_info = "⬇️Переведите с русского на испанский⬇️"
    add_word_to_us = "Добавить слова📌"
    cancel_edit = "Завершить❌"
    edit_us_info = "Редактировать раздел⚙️"
    delete_word_info = "Удалить слово↩️"

    @classmethod
    def section_title_info(cls, title, translate):
        return f"{title}\n{translate}"

    @classmethod
    def profile_data(cls, user_id: str):
        return f"{user_id}"

    @classmethod
    def add_us_word_info(cls, section_title):
        return f"Введите слова для раздела <b>{section_title}</b> " \
               f"в виде:\n<b>слово1 - перевод1; слово2 - перевод2<b>"

    @classmethod
    def add_us_final_info(cls, section_title):
        return f"Вы создали раздел {section_title}. Вы можете его редактировать.\n/my_sections"

    @classmethod
    def edit_user_section_info(cls, us_title):
        return f"⚙️Редактировать раздел: {us_title}"

    @classmethod
    def delete_word_us_info(cls, us_title):
        return f"<b>{us_title}</b>: Удаление слов\nНажмите на ❌ для удаления."
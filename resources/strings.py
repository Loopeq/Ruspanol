class Strings:
    welcome_cmd_start = "¡Hola! 👋 \nТебя приветствует бот для изучения испанского языка😊"
    welcome_cmd_phrases = "Добавляйте незнакомые и понравившиеся фразы в словарь.\n" \
                          "Все добавленные фразы и тест по ним можно найти в вашем словаре /vocab"
    welcome_cmd_test_filter = "Выберите формат тестирования из списка⬇️"
    phrase_error_message = "Кажется все доступные фразы закончились 🫡"
    dictionary_error_message = "В вашем словаре нет фраз🌵\n/phrases - для изучения фраз."

    cmd_phrases_info = "Изучайте и прослушивайте популярные испанский фразы📖"
    cmd_dictionary_info = "Все ваши фразы и тест по ним✏️"

    @classmethod
    def message_length_info(cls, limit: int):
        return f"Кажется в вашем предложении больше {limit} символов \nАссистент не справляется 😞"

    @classmethod
    def test_info(cls, current_task_phrase: str, user_phrase: str = None, correct_phrase: str = None,
                  prev_task_phrase: str = None, is_correct: bool = False):

        is_correct_message = "верный✅\n" if is_correct else "неверный❌\n"
        common_message = f"Ваш ответ {is_correct_message}" \
                         f"Фраза: {prev_task_phrase}\n" \
                         f"Ваш ответ: <b>{user_phrase}</b>\n" \
                         f"Правильный ответ: <b>{correct_phrase}</b>"

        if user_phrase is None:
            return f"Переводите фразы с русского на испанский.\n" \
                   f"(Перевод <b>НЕ</b> чувствителен к регистру, спец.символам и диакритечским знакам)\n\n" \
                   f"❗️Текущая фраза: <b>{current_task_phrase}</b>"

        if current_task_phrase is None:
            return common_message + "\n\nВы можете добавлять новые фразы для изучения /phrases"

        return common_message + f"\n\n" \
                                f"❗️Слeдующая фраза: <b>{current_task_phrase}</b>"

    @classmethod
    def welcome_dictionary_phrase(cls, count: int, percent: int):
        remains = count % 10
        match remains:
            case 1:
                phrase = "фраза"
            case 2 | 3 | 4:
                phrase = "фразы"
            case _:
                phrase = "фраз"

        return f"📗 В вашем словаре - <b>{count} {phrase}</b>\n" \
               f"🔄 Ваш текущий прогресс - <b>{percent}%</b>"





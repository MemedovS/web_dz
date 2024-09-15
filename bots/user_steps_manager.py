from aiogram.types import InlineKeyboardMarkup
# Функция для создания клавиатуры
def create_keyboard(buttons: list) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[button] for button in buttons]  # Каждая кнопка на отдельной строке
    )

# Словарь для хранения текущих и предыдущих шагов пользователей
user_steps = {}

# Функция для получения предыдущего шага
def get_previous_step(user_id):
    steps = user_steps.get(user_id, [])
    if len(steps) > 1:
        return steps[-2]  # Предыдущий шаг
    return None

# Функция для сохранения текущего шага
def save_step(user_id, step):
    if user_id not in user_steps:
        user_steps[user_id] = []
    user_steps[user_id].append(step)

    # Если больше 10 шагов, убираем старые шаги
    if len(user_steps[user_id]) > 10:
        user_steps[user_id].pop(0)

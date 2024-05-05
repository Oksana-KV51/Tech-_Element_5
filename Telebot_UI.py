# Импорт модуля pyTelegramBotAPI для создания телеграм-бота
# Импорт types для создания клавиатуры и кнопок в интерфейсе
import telebot
from telebot import types
# Следующая строка не нужна, так как предыдущая уже импортирует нужные классы объектов types
# ??? ЗАПРОС НА УДАЛЕНИЕ ???
# from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
# Импорт функций из файла Python Logic_Back_end.py
from Logic_Back_end import (add_or_get_user,
                            add_habit_to_user_list, get_user_habits, get_new_habits,
                            add_habit_to_user_list_directly, delete_habit_by_id, get_habit_info)  # get_all_habits

# Ввод токена основного телеграм-бота и инициализация программы:
# TOKEN = '6795112102:AAFBiEZg3Jgi2XxAoqsJvLzUGfSsmvNempo'
# bot = telebot.TeleBot(TOKEN)

# !!! ПЕРЕКЛЮЧИТЬ НА ОСНОВНОЙ ТЕЛЕГРАМ-БОТ В ФИНАЛЬНОЙ ВЕРСИИ ПРОГРАММЫ !!!

# Ввод токена тестового телеграм-бота и инициализация программы
TEST_TOKEN = '7121309234:AAFP6PfgdA1n9krO0OROiRI3EkdQSeYVETU'
bot = telebot.TeleBot(TEST_TOKEN)


# Функция вызова списка привычек из таблицы 'habits' в виде клавиатуры для выбора пользователя
def generate_markup(habits, page=0, list_type='habits'):
    markup = types.InlineKeyboardMarkup()
    start_index = page * 10
    end_index = min(start_index + 10, len(habits))
    for habit_id, habit_name in habits[start_index:end_index]:
        button = types.InlineKeyboardButton(habit_name, callback_data=f'add_{habit_id}')
        markup.add(button)

    if start_index > 0:
        markup.add(types.InlineKeyboardButton("⬅️ Назад", callback_data=f'page_{page - 1}_{list_type}'))
    if end_index < len(habits):
        markup.add(types.InlineKeyboardButton("Вперед ➡️", callback_data=f'page_{page + 1}_{list_type}'))

    return markup


# Функция - вывод id пользователя по его имени username
def get_user_id(user, reply_object):
    """ Получает user_id пользователя по его username. В случае отсутствия username отправляет уведомление.
    Args:
        user: объект пользователя (например, message.from_user или call.from_user)
        reply_object: объект для ответа (может быть message или call)
    Returns:
        user_id если username существует, иначе None
    """
    username = user.username
    if username is None:
        if isinstance(reply_object, telebot.types.Message):
            bot.reply_to(reply_object, "Ваш аккаунт Telegram не имеет username. Пожалуйста, установите его.")
        elif isinstance(reply_object, telebot.types.CallbackQuery):
            bot.answer_callback_query(reply_object.id, "У вашего профиля в Telegram нет username!")
        return None

    return add_or_get_user(username)


# Функция-приветствие нового пользователя
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = get_user_id(message.from_user, message)
    welcome_text = "Добро пожаловать! Вот основные команды, которые вы можете использовать в боте Привычек:"
    markup = types.InlineKeyboardMarkup(row_width=2)
    commands_buttons = [
        types.InlineKeyboardButton("Добавить свою П.", callback_data='add_new_habit'),
        types.InlineKeyboardButton("Настройка моих П.", callback_data='list_habits'),
        types.InlineKeyboardButton("База Привычек", callback_data='all_habits')
    ]
    markup.add(*commands_buttons)
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)


# Функция на команду menu - идентична функции на команду start выше
@bot.message_handler(commands=['menu'])
def send_welcome(message):
    user_id = get_user_id(message.from_user, message)
    welcome_text = "Добро пожаловать! Вот основные команды, которые вы можете использовать в боте Привычек:"
    markup = types.InlineKeyboardMarkup(row_width=1)
    commands_buttons = [
        types.InlineKeyboardButton("Добавить свою П.", callback_data='add_new_habit'),
        types.InlineKeyboardButton("Настройка моих П.", callback_data='list_habits'),
        types.InlineKeyboardButton("База Привычек", callback_data='all_habits')
    ]
    markup.add(*commands_buttons)
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)


# Функция добавления новой уникальной привычки пользователем
@bot.callback_query_handler(func=lambda call: call.data == 'add_new_habit')
def add_new_habit_button(call):
    # Начало диалога для добавления новой привычки
    msg = bot.send_message(call.message.chat.id, "Введите название новой привычки:")
    bot.register_next_step_handler(msg, process_habit_name_step, user_id=call.from_user.id)


# Функция - подгрузка имени новой привычки, переход к описанию привычки
def process_habit_name_step(message, user_id):
    habit_name = message.text
    msg = bot.send_message(message.chat.id, "Введите описание привычки:")
    bot.register_next_step_handler(msg, process_habit_description_step, user_id=user_id, habit_name=habit_name)


# Функция - подгрузка описания новой привычки, переход к цели привычки
def process_habit_description_step(message, user_id, habit_name):
    description = message.text
    msg = bot.send_message(message.chat.id, "Введите цель привычки:")
    bot.register_next_step_handler(msg, process_habit_goal_step, user_id=user_id, habit_name=habit_name,
                                   description=description)


# Функция - подгрузка цели новой привычки, переход к частоте напоминаний
def process_habit_goal_step(message, user_id, habit_name, description):
    goal = message.text
    msg = bot.send_message(message.chat.id, "Введите частоту напоминаний (например, 'ежедневно'):")
    bot.register_next_step_handler(msg, process_habit_frequency_step, user_id=user_id, habit_name=habit_name,
                                   description=description, goal=goal)


# Функция - подгрузка частоты напоминаний; вызов функции, которая добавит привычку в таблицы habits и user_habits
def process_habit_frequency_step(message, user_id, habit_name, description, goal):
    frequency = message.text
    username = message.from_user.username
    # Добавляем привычку в базу и связываем её с пользователем
    add_habit_to_user_list_directly(username, user_id, habit_name, description, goal, frequency)
    bot.send_message(message.chat.id, "Привычка успешно добавлена в ваш список.")


# Функция - обработка запроса на вызов функции show_all_habits()
@bot.callback_query_handler(func=lambda call: call.data == 'all_habits')
def show_all_habits(call):
    # Эта функция должна быть реализована для начала процесса добавления новой привычки
    # bot.send_message(call.message.chat.id, "Функция добавления новой привычки ещё не реализована.")
    username = call.from_user.username
    if username is None:
        bot.answer_callback_query(call.id, "У вашего профиля в Telegram нет username!")
        return

    user_id = add_or_get_user(username)
    new_habits = get_new_habits(user_id)
    if not new_habits:
        bot.send_message(call.message.chat.id, "Список привычек пуст.")
        return
    markup = generate_markup(new_habits, list_type='newhabits')
    bot.send_message(call.message.chat.id, "Выберите привычку для добавления:", reply_markup=markup)


# Функция - вывод всех привычек из таблицы 'habits' с возможностью выбора
# новой привычки для добавления в список привычек пользователя - СМ. СТРОКУ 61
# @bot.message_handler(commands=['allhabits'])
# def show_all_habits(message):
#     habits = get_all_habits()
#     if not habits:
#         bot.send_message(message.chat.id, "Список привычек пуст.")
#         return
#     markup = generate_markup(habits, list_type='habits')
#     bot.send_message(message.chat.id, "Выберите привычку для добавления:", reply_markup=markup)


# Функция - обработка запроса на добавление пользователю новой привычки из таблицы 'habits'
@bot.callback_query_handler(func=lambda call: call.data.startswith('add_'))
def handle_add_habit(call):
    habit_id = int(call.data.split('_')[1])
    user_id = add_or_get_user(call.from_user.username)
    result = add_habit_to_user_list(user_id, habit_id, "ежедневно")  # Пример частоты

    if result is None:
        # Обработка случая, когда достигнуто максимальное количество привычек
        bot.answer_callback_query(call.id, "Максимальное количество привычек достигнуто.")
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Максимальное количество привычек достигнуто!")
    else:
        # Обработка успешного добавления привычки
        bot.answer_callback_query(call.id, "Привычка добавлена в ваш список.")
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Привычка добавлена!")


# Функция - обработка запроса на перелистывание страниц списка привычек из 'habits'
@bot.callback_query_handler(func=lambda call: call.data.startswith('page_')) #листать список списка
def handle_pagination(call):
    _, page, list_type = call.data.split('_')
    page = int(page)
    user_id = get_user_id(call.from_user, call)
    habits = get_new_habits(user_id)
    markup = generate_markup(habits, page, list_type)
    bot.edit_message_text(
        chat_id=call.message.chat.id, message_id=call.message.message_id,
        text="Выберите привычку для добавления:", reply_markup=markup
    )


# Функция - обработка запроса на вывод списка привычек пользователя
@bot.callback_query_handler(func=lambda call: call.data == 'list_habits')
def list_user_habits(call):
    user_id = get_user_id(call.from_user, call)

    # Получение списка привычек пользователя
    habits = get_user_habits(user_id)
    print(habits)

    if not habits:
        bot.send_message(call.message.chat.id, "Ваш список привычек пуст.")
        return

    # Формирование текста сообщения со списком привычек в виде кнопок
    markup = types.InlineKeyboardMarkup()
    for user_id, habit_name, habit_id in habits:
        print(user_id, habit_name, habit_id)
        print(f'Callback Data: habit_{habit_id}_{habit_name}')
        print(f'Length: {len(f"habit_{habit_id}_{habit_name}".encode("utf-8"))} bytes')
        # habit_button = types.InlineKeyboardButton(habit_name, callback_data=f'habit_{habit_id}_{habit_name}')
        habit_button = types.InlineKeyboardButton(habit_name, callback_data=f'habit_{habit_id}')

        markup.add(habit_button)

    bot.send_message(call.message.chat.id, "Ваши привычки:\n", reply_markup=markup)


# Функция - вызов опций для работы с привычкой пользователя
@bot.callback_query_handler(func=lambda call: call.data.startswith('habit_'))
def habit_options(call):
    habit_id = call.data.split('_')[1]  # получаем ID привычки из данных callback
    # habit_name = call.data.split('_')[2] # получаем name привычки из данных callback

    markup = types.InlineKeyboardMarkup()

    # Создание кнопок для различных действий
    view_btn = types.InlineKeyboardButton("Просмотр", callback_data=f'view_{habit_id}')
    edit_btn = types.InlineKeyboardButton("Изменение", callback_data=f'edit_{habit_id}')
    delete_btn = types.InlineKeyboardButton("Удаление", callback_data=f'delete_{habit_id}')

    markup.add(view_btn, edit_btn, delete_btn)
    # bot.send_message(call.message.chat.id, f"Выберите действие для {habit_name}", reply_markup=markup)
    bot.send_message(call.message.chat.id, f"Выберите действие:", reply_markup=markup)


# Функция - вызов информации по привычке пользователя
@bot.callback_query_handler(func=lambda call: call.data.startswith('view_'))
def view_habit(call):
    habit_id = call.data.split('_')[1]
    habit_details = get_habit_info(habit_id)  # предполагается, что эта функция возвращает детали привычки
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, f'Название привычки: {habit_details[0][0]}\n'
                     f'Описание: {habit_details[0][1]}\n'
                     f'Цель: {habit_details[0][2]}')


# Функция - вызов редактирования привычки пользователя - ПОКА НЕ ОБРАБАТЫВАЕТ ДАННЫЕ
@bot.callback_query_handler(func=lambda call: call.data.startswith('edit_'))
def edit_habit(call):
    habit_id = call.data.split('_')[1]
    # Предполагаем, что функция редактирования возвращает успешный результат или сообщение об ошибке
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, "Введите новые данные для привычки. (Это место для диалога редактирования)")


# Функция - удаление привычки из списка привычек пользователя
@bot.callback_query_handler(func=lambda call: call.data.startswith('delete_'))
def delete_habit(call):
    user_id = get_user_id(call.from_user, call)
    habit_id = call.data.split('_')[1]  # Извлекаем ID привычки из данных callback
    result = delete_habit_by_id(habit_id, user_id)  # Пытаемся удалить привычку и получаем результат операции

    # Проверяем, было ли удаление успешным
    if result:
        bot.answer_callback_query(call.id, "Привычка успешно удалена.")
        bot.send_message(call.message.chat.id, "Привычка успешно удалена.")
    else:
        bot.answer_callback_query(call.id, "Не удалось удалить привычку. Пожалуйста, попробуйте позже.")
        bot.send_message(call.message.chat.id, "Не удалось удалить привычку. Пожалуйста, попробуйте позже.")


# Запуск работы телеграм-бота с пользователем
bot.polling()

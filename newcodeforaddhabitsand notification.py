# Импортируем модуль для работы с SQLite
import sqlite3


# Функция создания базы данных
def setup_database():
    conn = sqlite3.connect('habit_tracker01.db')
    cursor = conn.cursor()

    # Включение поддержки внешних ключей
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Создание таблицы пользователей
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        chat_id TEXT UNIQUE NOT NULL
    );
    ''')

    # Создание таблицы привычек
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS habits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        habit_name TEXT NOT NULL,
        habit_description TEXT,
        habit_goal TEXT,
        habit_frequency_per_week TEXT,
        habit_frequency_per_day TEXT,
        habit_succesfull INT DEFAULT 0,
        habit_failed INT DEFAULT 0,
        habit_start_date DATE,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    );
    ''')

    # Создание таблицы прогресса пользователей по привычкам
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_habits (
        user_id INTEGER,
        habit_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
        FOREIGN KEY (habit_id) REFERENCES habits (id) ON DELETE CASCADE
    );
    ''')

    conn.commit()
    conn.close()
    print("Database and tables created successfully.")


# Вызов функции создания базы данных при условии, что файл запущен как основная программа (не import)
if __name__ == "__main__":
    setup_database()
# Импортируем модуль для работы с SQLite
import sqlite3
from datetime import datetime, timedelta


# Подключаемся к базе данных 'habit_tracker1.db'
def connect_to_db():
    return sqlite3.connect('habit_tracker01.db')

# 📌--------------------------------------Creacted by sunTz1 -start-------------------------------------📌
# Adds new user to DB


def add_user(username, chat_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    print(f"DEBUG: Checking if user '{username}' exists in the database.")
    # Проверка, существует ли уже такой пользователь
    cursor.execute("SELECT id FROM users WHERE username = (?)", (username,))
    result = cursor.fetchone()
    if result:
        user_id = result[0]
        print(
            f"DEBUG: User '{username}' found with ID {user_id}. chat_id: {chat_id}")
    else:
        print(f"DEBUG: User '{username}' not found, adding to database.")
        cursor.execute(
            "INSERT INTO users (username, chat_id) VALUES (?,?)", (username, chat_id))
        conn.commit()
        user_id = cursor.lastrowid
        print(
            f"DEBUG: New user '{username}' added with ID {user_id}.chat_id: {chat_id}")
    conn.close()

# Get user id by username. Returned user's id


def get_user_id_by_username(username):
    conn = connect_to_db()
    cursor = conn.cursor()

    print(f"DEBUG: Checking if user '{username}' exists in the database.")

    cursor.execute("SELECT id FROM users WHERE username = (?)", (username,))
    result = cursor.fetchone()
    if result:
        user_id = result[0]
        return user_id
    conn.close()
    return 0

# Get user chat id by usersname. Usefull for sending notifications


def get_user_chat_id_by_username(username):
    conn = connect_to_db()
    cursor = conn.cursor()

    print(f"DEBUG: Checking if user '{username}' exists in the database.")

    cursor.execute(
        "SELECT chat_id FROM users WHERE username = (?)", (username,))
    result = cursor.fetchone()

    if result:
        user_id = result[0]
        return user_id
    conn.close()
    return 0


# Get all user habits id. Returns tuple with int


def get_all_user_habits_id(user_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_habits WHERE user_id= (?)", (user_id,))
    all_user_habits_id = cursor.fetchall()
    return all_user_habits_id

# Get habit by it's id. Returns tuple with habits information


def get_habit_by_id(habit_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM habits WHERE id= (?)", (habit_id,))
    habit = cursor.fetchone()
    return habit

# Set habit result (result: 1 - success, 0 - fail)


def set_habit_result(habit_id, result):
    conn = connect_to_db()
    cursor = conn.cursor()
    match result:
        case 1:
            cursor.execute(
                "SELECT habit_succesfull FROM habits WHERE id= (?)", (habit_id,))
            success_value = cursor.fetchone()
            success_value = success_value[0] + 1
            try:
                print(f"update value {success_value}")
                print(f"update id{habit_id}")

                cursor.execute(
                    "UPDATE habits SET habit_succesfull= ? WHERE id= ?", (success_value, habit_id))
                conn.commit()

            finally:
                conn.close()
        case 0:
            cursor.execute(
                "SELECT habit_succesfull FROM habits WHERE id= (?)", (habit_id,))
            failed_value = cursor.fetchone()
            failed_value = failed_value[0] + 1
            try:
                cursor.execute(
                    "UPDATE habits SET habit_failed= ? WHERE id= ?", (failed_value, habit_id))
                conn.commit()

            finally:
                conn.close()


# Get frequency per week (Returns tuple with strings: пн вт ср)
def habit_frequency_per_week(habit_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT habit_frequency_per_week FROM habits WHERE id= (?)", (habit_id,))
    return cursor.fetchone()

# Get frequency per day (Returns tuple with strings: 9:00 12:00 15:00)


def habit_frequency_per_day(habit_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT habit_frequency_per_day FROM habits WHERE id= (?)", (habit_id,))
    return cursor.fetchone()


# # def notification_time_cheсker(habits):
#     current_date = datetime.now()
#     day_of_week = current_date.weekday()
#     # Преобразование числового значения дня недели в текстовый формат
#     days_of_week = ["пн", "вт", "ср",
#                     "чт", "пт", "сб", "вс"]
#     today = days_of_week[day_of_week]
#     for habit in habits:
#         print(habit)
#         habit_days = habit[5].split()

#         for day in habit_days:
#             if (day == today):
#                 habit_times = habit[6].split()
#                 for time in habit_times:
#                     habit_time = datetime.strptime(time, "%H:%M").time()
#                     habit_time_limit = habit_time
#                     habit_time_limit += timedelta(minutes=1)
#                     current_time = datetime.now().time()
#                     print(f'TIME NOW: {current_time} CURRENT TIME: {time}')
#                     if (current_time >= habit_time & current_time <= habit_time_limit):
#                         return habit
#     return None


def notification_time_checker(habits):
    current_date = datetime.now()
    day_of_week = current_date.weekday()
    days_of_week = ["пн", "вт", "ср", "чт", "пт", "сб", "вс"]
    today = days_of_week[day_of_week]

    for habit in habits:
        habit_days = habit[5].split()
        if today in habit_days:
            habit_times = habit[6].split()
            for time in habit_times:
                habit_time = datetime.strptime(time, "%H:%M").time()
                current_time = datetime.now().time()
                # Create a one-minute interval starting at habit_time
                start_interval = habit_time
                end_interval = (datetime.combine(
                    datetime.today(), habit_time) + timedelta(minutes=1)).time()

                if start_interval <= current_time <= end_interval:
                    # Return the habit if the current time is within the one-minute interval
                    return habit

    return None

# 📌--------------------------------------Creacted by sunTz1 -end-------------------------------------📌


# Функция добавления новой привычки в базу данных - и в таблицу habits, и в таблицу user_habits


def add_habit_to_user_list_directly(username, user_id, habit_name, description, goal, frequency_per_week, frequency_per_day):
    conn = connect_to_db()
    cursor = conn.cursor()
    true_user_id = get_user_id_by_username(username)
    habit_start_date_and_time = datetime.today()
    print(f"USER_ID {true_user_id}")
    try:
        # Добавляем привычку в таблицу habits
        cursor.execute("INSERT INTO habits (user_id, habit_name, habit_description, habit_goal, habit_frequency_per_week, habit_frequency_per_day, habit_start_date)"
                       "VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (true_user_id, habit_name, description, goal, frequency_per_week, frequency_per_day, habit_start_date_and_time))
        habit_id = cursor.lastrowid  # Получаем ID новой привычки
        # Добавляем привычку в список привычек пользователя
        cursor.execute("INSERT INTO user_habits (user_id, habit_id) VALUES (?, ?)",
                       (true_user_id, habit_id))
        conn.commit()
    finally:
        conn.close()


# Функция вывода списка всех привычек из таблицы 'habits'
# def get_all_habits():
#     conn = connect_to_db()
#     cursor = conn.cursor()
#     cursor.execute("SELECT id, habit_name FROM habits")
#     habits = cursor.fetchall()
#     conn.close()
#     return habits

# def get_all_habits():
#     """
#     Получить список всех привычек, где user_id равен NULL.
#     Это могут быть общедоступные или стандартные привычки, доступные всем пользователям.
#     """
#     conn = connect_to_db()
#     cursor = conn.cursor()
#     # Изменение запроса для фильтрации привычек, где user_id равен NULL
#     cursor.execute("SELECT id, habit_name FROM habits WHERE user_id IS NULL")
#     habits = cursor.fetchall()
#     conn.close()
#     return habits


# Функция вывода списка всех привычек из таблицы 'habits', кроме тех,
# которые уже в списке пользователя
def get_new_habits(user_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT h.id, h.habit_name FROM habits h
    WHERE (h.user_id IS NULL) AND (h.id NOT IN (
        SELECT uh.habit_id FROM user_habits uh
        WHERE uh.user_id = ?))
    """, (user_id,)
    )

    new_habits = cursor.fetchall()
    conn.close()
    return new_habits


# Функция вывода списка всех привычек конкретного пользователя из таблицы 'user_habits'
def get_user_habits(user_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT uh.user_id, h.habit_name, h.id
        FROM habits h
        JOIN user_habits uh ON h.id = uh.habit_id
        WHERE uh.user_id = ?
    """, (user_id,))
    habits = cursor.fetchall()
    conn.close()
    return habits


# Функция вывода информации о привычке из таблицы 'habits'
def get_habit_info(habit_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT h.habit_name, h.habit_description, h.habit_goal, h.habit_frequency_per_week, habit_frequency_per_day, habit_succesfull, habit_failed, habit_start_date
        FROM habits h
        WHERE h.id = ?
    """, (habit_id,))
    habit_details = cursor.fetchall()
    conn.close()
    return habit_details


# Функция удаления привычки из таблицы 'user_habits'
def delete_habit_by_id(habit_id, user_id):
    try:
        with connect_to_db() as conn:
            cursor = conn.cursor()
            # Удаление привычки из таблицы user_habits
            cursor.execute("DELETE FROM user_habits WHERE (habit_id = ? AND user_id = ?)",
                           (habit_id, user_id, ))
            # Удаление привычки из таблицы habits - ЗАЧЕМ?
            # cursor.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
            conn.commit()
            print("Привычка успешно удалена.")
            return True
    except Exception as e:
        print(f"Ошибка при удалении привычки: {e}")
        return False
# Импорт модуля pyTelegramBotAPI для создания телеграм-бота
# Импорт types для создания клавиатуры и кнопок в интерфейсе
import telebot
import threading
import time
import datetime
from telebot import types
# Следующая строка не нужна, так как предыдущая уже импортирует нужные классы объектов types
# ??? ЗАПРОС НА УДАЛЕНИЕ ???
# from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
# Импорт функций из файла Python Logic_Back_end.py
from Logic_Back_end import (notification_time_checker, get_habit_by_id, get_all_user_habits_id, set_habit_result, add_user, get_user_id_by_username, get_user_chat_id_by_username,
                            get_user_habits, get_new_habits,
                            add_habit_to_user_list_directly, delete_habit_by_id, get_habit_info)  # get_all_habits

# Ввод токена основного телеграм-бота и инициализация программы:
# TOKEN = '6795112102:AAFBiEZg3Jgi2XxAoqsJvLzUGfSsmvNempo'
# bot = telebot.TeleBot(TOKEN)

# !!! ПЕРЕКЛЮЧИТЬ НА ОСНОВНОЙ ТЕЛЕГРАМ-БОТ В ФИНАЛЬНОЙ ВЕРСИИ ПРОГРАММЫ !!!

# Ввод токена тестового телеграм-бота и инициализация программы
# TEST_TOKEN = '7025920413:AAFdfbUqEeW5yH0A2-D3NEIjNwLTO6rBWkI'
# bot = telebot.TeleBot(TEST_TOKEN)


# Функция вызова списка привычек из таблицы 'habits' в виде клавиатуры для выбора пользователя
def generate_markup(habits, page=0, list_type='habits'):
    markup = types.InlineKeyboardMarkup()
    start_index = page * 10
    end_index = min(start_index + 10, len(habits))
    for habit_id, habit_name in habits[start_index:end_index]:
        button = types.InlineKeyboardButton(
            habit_name, callback_data=f'add_{habit_id}')
        markup.add(button)

    if start_index > 0:
        markup.add(types.InlineKeyboardButton(
            "⬅️ Назад", callback_data=f'page_{page - 1}_{list_type}'))
    if end_index < len(habits):
        markup.add(types.InlineKeyboardButton(
            "Вперед ➡️", callback_data=f'page_{page + 1}_{list_type}'))

    return markup


# # Функция - вывод id пользователя по его имени username
# def get_user_id(user, reply_object):
#     """ Получает user_id пользователя по его username. В случае отсутствия username отправляет уведомление.
#     Args:
#         user: объект пользователя (например, message.from_user или call.from_user)
#         reply_object: объект для ответа (может быть message или call)
#     Returns:
#         user_id если username существует, иначе None
#     """
#     username = user.username
#     if username is None:
#         if isinstance(reply_object, telebot.types.Message):
#             bot.reply_to(
#                 reply_object, "Ваш аккаунт Telegram не имеет username. Пожалуйста, установите его.")
#         elif isinstance(reply_object, telebot.types.CallbackQuery):
#             bot.answer_callback_query(
#                 reply_object.id, "У вашего профиля в Telegram нет username!")
#         return None

#     return add_or_get_user(username, reply_object.chat.id)


def create_new_user(user, reply_object):
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
            bot.reply_to(
                reply_object, "Ваш аккаунт Telegram не имеет username. Пожалуйста, установите его.")
        elif isinstance(reply_object, telebot.types.CallbackQuery):
            bot.answer_callback_query(
                reply_object.id, "У вашего профиля в Telegram нет username!")
        return False
    add_user(username, reply_object.chat.id)


# Функция-приветствие нового пользователя
@bot.message_handler(commands=['start'])
def send_welcome(message):
    create_new_user(message.from_user, message)
    welcome_text = "Добро пожаловать! Вот основные команды, которые вы можете использовать в боте Привычек:"
    markup = types.InlineKeyboardMarkup(row_width=2)
    commands_buttons = [
        types.InlineKeyboardButton(
            "Добавить свою П.", callback_data='add_new_habit'),
        types.InlineKeyboardButton(
            "Настройка моих П.", callback_data='list_habits'),
        types.InlineKeyboardButton("База Привычек", callback_data='all_habits')
    ]
    markup.add(*commands_buttons)
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)


# Функция на команду menu - идентична функции на команду start выше
@bot.message_handler(commands=['menu'])
def send_welcome(message):
    create_new_user(message.from_user, message)
    welcome_text = "Добро пожаловать! Вот основные команды, которые вы можете использовать в боте Привычек:"
    markup = types.InlineKeyboardMarkup(row_width=1)
    commands_buttons = [
        types.InlineKeyboardButton(
            "Добавить свою П.", callback_data='add_new_habit'),
        types.InlineKeyboardButton(
            "Настройка моих П.", callback_data='list_habits'),
        types.InlineKeyboardButton("База Привычек", callback_data='all_habits')
    ]
    markup.add(*commands_buttons)
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)


# Функция добавления новой уникальной привычки пользователем
@bot.callback_query_handler(func=lambda call: call.data == 'add_new_habit')
def add_new_habit_button(call):
    # Начало диалога для добавления новой привычки
    msg = bot.send_message(call.message.chat.id,
                           "Введите название новой привычки:")
    bot.register_next_step_handler(
        msg, process_habit_name_step, user_id=call.from_user.id)


# Функция - подгрузка имени новой привычки, переход к описанию привычки
def process_habit_name_step(message, user_id):
    habit_name = message.text
    msg = bot.send_message(message.chat.id, "Введите описание привычки:")
    bot.register_next_step_handler(
        msg, process_habit_description_step, user_id=user_id, habit_name=habit_name)


# Функция - подгрузка описания новой привычки, переход к цели привычки
def process_habit_description_step(message, user_id, habit_name):
    description = message.text
    msg = bot.send_message(message.chat.id, "Введите цель привычки:")
    bot.register_next_step_handler(msg, process_habit_goal_step, user_id=user_id, habit_name=habit_name,
                                   description=description)

# -------------------- UPDATED frequency logic (by sunTz1) -------------------------

# Функция - подгрузка цели новой привычки, переход к частоте напоминаний


def process_habit_goal_step(message, user_id, habit_name, description):
    goal = message.text
    msg = bot.send_message(
        message.chat.id, "Введите дни недели через пробел(Пример:пн вт ср чт пт сб вс):")
    bot.register_next_step_handler(msg, process_habit_frequency_step_1, user_id=user_id, habit_name=habit_name,
                                   description=description, goal=goal)

# ШАГ


def process_habit_frequency_step_1(message, user_id, habit_name, description, goal):
    frequency_per_week = message.text
    msg = bot.send_message(
        message.chat.id, "Введите время для напоминаний через пробел(Пример:8:00 15:00 17:00)")
    bot.register_next_step_handler(
        msg, process_habit_add, user_id=user_id, habit_name=habit_name, description=description, goal=goal, frequency_per_week=frequency_per_week)


# --ПОСЛЕДНЯЯ-- Функция - подгрузка частоты напоминаний; вызов функции, которая добавит привычку в таблицы habits и user_habits


def process_habit_add(message, user_id, habit_name, description, goal, frequency_per_week):
    frequency_per_day = message.text
    username = message.from_user.username
    # Добавляем привычку в базу и связываем её с пользователем
    add_habit_to_user_list_directly(
        username, user_id, habit_name, description, goal, frequency_per_week, frequency_per_day)
    start_habit_tracking = threading.Thread(
        target=start_tracking, args=(username,))
    start_habit_tracking.start()
    bot.send_message(
        message.chat.id, "Привычка успешно добавлена в ваш список.")

# -------------------- UPDATED frequency logic (by sunTz1) -------------------------


# Функция - обработка запроса на вызов функции show_all_habits()
@bot.callback_query_handler(func=lambda call: call.data == 'all_habits')
def show_all_habits(call):
    # Эта функция должна быть реализована для начала процесса добавления новой привычки
    # bot.send_message(call.message.chat.id, "Функция добавления новой привычки ещё не реализована.")
    username = call.from_user.username
    if username is None:
        bot.answer_callback_query(
            call.id, "У вашего профиля в Telegram нет username!")
        return

    user_id = get_user_id_by_username(username)
    new_habits = get_new_habits(user_id)
    if not new_habits:
        bot.send_message(call.message.chat.id, "Список привычек пуст.")
        return
    markup = generate_markup(new_habits, list_type='newhabits')
    bot.send_message(call.message.chat.id,
                     "Выберите привычку для добавления:", reply_markup=markup)


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
# @bot.callback_query_handler(func=lambda call: call.data.startswith('add_'))
# def handle_add_habit(call):
#     habit_id = int(call.data.split('_')[1])
#     user_id = add_or_get_user(call.from_user.username)
#     result = add_habit_to_user_list(
#         user_id, habit_id, "ежедневно")  # Пример частоты

#     if result is None:
#         # Обработка случая, когда достигнуто максимальное количество привычек
#         bot.answer_callback_query(
#             call.id, "Максимальное количество привычек достигнуто.")
#         bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                               text="Максимальное количество привычек достигнуто!")
#     else:
#         # Обработка успешного добавления привычки
#         bot.answer_callback_query(call.id, "Привычка добавлена в ваш список.")
#         bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                               text="Привычка добавлена!")


# Функция - обработка запроса на перелистывание страниц списка привычек из 'habits'
# листать список списка
@bot.callback_query_handler(func=lambda call: call.data.startswith('page_'))
def handle_pagination(call):
    _, page, list_type = call.data.split('_')
    page = int(page)
    username = call.from_user.username
    user_id = get_user_id_by_username(username)
    habits = get_new_habits(user_id)
    markup = generate_markup(habits, page, list_type)
    bot.edit_message_text(
        chat_id=call.message.chat.id, message_id=call.message.message_id,
        text="Выберите привычку для добавления:", reply_markup=markup
    )


# Функция - обработка запроса на вывод списка привычек пользователя
@bot.callback_query_handler(func=lambda call: call.data == 'list_habits')
def list_user_habits(call):
    username = call.from_user.username
    user_id = get_user_id_by_username(username)

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
        print(
            f'Length: {len(f"habit_{habit_id}_{habit_name}".encode("utf-8"))} bytes')
        # habit_button = types.InlineKeyboardButton(habit_name, callback_data=f'habit_{habit_id}_{habit_name}')
        habit_button = types.InlineKeyboardButton(
            habit_name, callback_data=f'habit_{habit_id}')

        markup.add(habit_button)

    bot.send_message(call.message.chat.id,
                     "Ваши привычки:\n", reply_markup=markup)


# Функция - вызов опций для работы с привычкой пользователя
@bot.callback_query_handler(func=lambda call: call.data.startswith('habit_'))
def habit_options(call):
    # получаем ID привычки из данных callback
    habit_id = call.data.split('_')[1]
    # habit_name = call.data.split('_')[2] # получаем name привычки из данных callback

    markup = types.InlineKeyboardMarkup()

    # Создание кнопок для различных действий
    view_btn = types.InlineKeyboardButton(
        "Просмотр", callback_data=f'view_{habit_id}')
    edit_btn = types.InlineKeyboardButton(
        "Изменение", callback_data=f'edit_{habit_id}')
    delete_btn = types.InlineKeyboardButton(
        "Удаление", callback_data=f'delete_{habit_id}')

    markup.add(view_btn, edit_btn, delete_btn)
    # bot.send_message(call.message.chat.id, f"Выберите действие для {habit_name}", reply_markup=markup)
    bot.send_message(call.message.chat.id,
                     f"Выберите действие:", reply_markup=markup)


# Функция - вызов информации по привычке пользователя
@bot.callback_query_handler(func=lambda call: call.data.startswith('view_'))
def view_habit(call):
    habit_id = call.data.split('_')[1]
    # предполагается, что эта функция возвращает детали привычки
    habit_details = get_habit_info(habit_id)
    foramtedDate = habit_details[0][7].split(' ', 1)[0]
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id,
                     f'------------------------------------\n'
                     f'📌 *Название привычки*: {habit_details[0][0]}\n'
                     f'------------------------------------\n'
                     f'🗓️ *Дата начала:* {foramtedDate}\n'
                     f'🗓️ *Ударный режим :* 0 дней подряд\n'
                     f'------------------------------------\n'
                     f'📝 *Описание*: {habit_details[0][1]}\n'
                     f'------------------------------------\n'
                     f'🔴 *Цель*: {habit_details[0][2]}\n\n'
                     f'-----------КОЛИЧЕСТВО-----------\n'
                     f'📣 *Кол-во повторов в неделю*: {habit_details[0][3]}\n'
                     f'📣 *Кол-во повторов в день*: {habit_details[0][4]}\n\n'
                     f'-----------РЕЗУЛЬТАТ-----------\n'
                     f'✅ *Успешно*: {habit_details[0][5]}\n'
                     f'❌ *Провалено*: {habit_details[0][6]}\n\n', parse_mode="Markdown")


# Функция - вызов редактирования привычки пользователя - ПОКА НЕ ОБРАБАТЫВАЕТ ДАННЫЕ


@bot.callback_query_handler(func=lambda call: call.data.startswith('edit_'))
def edit_habit(call):
    habit_id = call.data.split('_')[1]
    # Предполагаем, что функция редактирования возвращает успешный результат или сообщение об ошибке
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id,
                     "Введите новые данные для привычки. (Это место для диалога редактирования)")


# Функция - удаление привычки из списка привычек пользователя
@bot.callback_query_handler(func=lambda call: call.data.startswith('delete_'))
def delete_habit(call):
    username = call.from_user.username
    user_id = get_user_id_by_username(username)
    # Извлекаем ID привычки из данных callback
    habit_id = call.data.split('_')[1]
    # Пытаемся удалить привычку и получаем результат операции
    result = delete_habit_by_id(habit_id, user_id)

    # Проверяем, было ли удаление успешным
    if result:
        bot.answer_callback_query(call.id, "Привычка успешно удалена.")
        bot.send_message(call.message.chat.id, "Привычка успешно удалена.")
    else:
        bot.answer_callback_query(
            call.id, "Не удалось удалить привычку. Пожалуйста, попробуйте позже.")
        bot.send_message(
            call.message.chat.id, "Не удалось удалить привычку. Пожалуйста, попробуйте позже.")


# -----------NOTIFICATIONS BLOCK-------------
# Функция для отправки сообщения

def send_notifications(user_id, user_chat_id, notification_text, habit_id):
    markup = types.InlineKeyboardMarkup(row_width=2)
    commands_buttons = [
        types.InlineKeyboardButton(
            "ВЫПОЛНИЛ", callback_data=f"complete,{habit_id},{notification_text}"),
        types.InlineKeyboardButton(
            "ПРОПУСТИЛ", callback_data=f"failed,{habit_id},{notification_text}")
    ]
    markup.add(*commands_buttons)
    bot.send_message(user_chat_id, notification_text, reply_markup=markup)


@bot.callback_query_handler(func=lambda callback_query: callback_query.data.startswith('complete') or callback_query.data.startswith('failed'))
def notification_result_complete(callback_query):
    action, habit_id, notification_text = callback_query.data.split(',')

    if action == 'complete':
        set_habit_result(habit_id, 1)
        bot.send_message(callback_query.message.chat.id,
                         f"{notification_text} выполнена успешно 😎😁🤙")
        bot.delete_message(callback_query.message.chat.id,
                           callback_query.message.message_id)
    elif action == 'failed':
        set_habit_result(habit_id, 0)
        bot.send_message(callback_query.message.chat.id,
                         f"{notification_text} не выполнена 🤬😡😭")
        bot.delete_message(callback_query.message.chat.id,
                           callback_query.message.message_id)


def start_tracking(username):
    user_id = get_user_id_by_username(username)
    user_chat_id = get_user_chat_id_by_username(username)
    all_user_habits_id = get_all_user_habits_id(user_id)
    habits = []
    for id in all_user_habits_id:
        print(id)
        habits.append(get_habit_by_id(id[1]))

    while True:
        habit_to_notificate = notification_time_checker(habits)
        if habit_to_notificate:
            send_notifications(user_id, user_chat_id,
                               habit_to_notificate[2], habit_to_notificate[0])

        time.sleep(60)  # Проверка каждую минуту


# Запуск работы телеграм-бота с пользователем
# Главная функция
# Функция для выполнения проверки времени с периодичностью
if __name__ == "__main__":
    # Создание потока для выполнения проверки времени
    bot.polling(none_stop=True)

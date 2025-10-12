import telebot
import gspread
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import os
import json
from oauth2client.service_account import ServiceAccountCredentials
from telebot.types import ReplyKeyboardRemove
# Константы
SPREADSHEET_ID = '1aNzWinJl6ZJJ44vVPcmlGv7xA9MCx83AvuHhr_llayQ'
FOTO = r"Photo_2_vopr.png"
FOTO_KAZ = r"img_2.png"
PHOTO_RASP = r"PHOTO_RASP.png"

# Авторизация Google Sheets
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
key_json = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON')
if not TELEGRAM_TOKEN:
    raise ValueError("Переменная окружения TELEGRAM_TOKEN не установлена")
if not key_json:
    raise ValueError("Переменная окружения GOOGLE_APPLICATION_CREDENTIALS_JSON не установлена")

creds_dict = json.loads(key_json)

creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict)

client = gspread.authorize(creds)
sheet = client.open_by_key(SPREADSHEET_ID).sheet1

# Инициализация бота
bot = telebot.TeleBot(TELEGRAM_TOKEN)
user_states = {}
user_answers = {}
user_data = {}

QUESTIONS_BY_DAY = [
    ["Что такое хиральность?",
     "Перечислите теории динамического хаоса",
     "На основе чего реализуется автоматическое обнаружение и отслеживание структур сверхзвукового потока?",
     "В чём смысл параметра q в q-статфизике?",
     "Для чего студенты кафедры медицинской физики применяют суперкомпьютеры с массивно-параллельными вычислениями на базе графических процессоров?"],
    ["В чём основная сложность изучения рождения электрон-позитронных пар в сильном электрическом поле?",
     "При участии какой кафедры были открыты 102-105, 115, 117-118 элементы?",
     "Какие приборы используются при построении виртуальных моделей для «3D Цифрового пациента»?",
     "К какому классу относится солнечная вспышка, представленная на стенгазете кафедры физики космоса?",
     "Как называется каскад ускорителей, на котором исследуется короткодействующая корреляция при взаимодействии пучка с ядрами мишени?"],
    ["Совместно с каким университетом ведёт исследования кафедра физики полупроводников и криоэлектроники?",
     "Для чего модифицируются полимерные матрицы?",
     "Чьи работы послужили основой для создания теории электронной структуры и кинетических свойств неупорядоченных сплавов?",
     "На какой кафедре направлением исследований являются квантовые кооперативные явления в низкоразмерных системах?",
     "Характеристики каких лазеров изучает группа узкозонных полупроводников?"],
    ["При участии какой группы в 2016 году произошло открытие гравитационных волн?",
     "Какая научная группа обладает ускорителем атомарных и кластерных ионов и уникальным атомно-силовым микроскопом?",
     "Какое время жизни аналогов шаровых молний, воссозданных с помощью плазменных струй?",
     "Какая кафедра располагает уникальными сооружениями: звукомерной и реверберационной камерами?",
     "Функция распределения чего изображена на рисунке?"],
    ["Какие методы получили фундаментальные результаты по теории мер?",
     "Какая концепция существенно расширяет возможности экспериментальных исследований?",
     "Большое поле приложения современных методов решения некорректных задач даёт ...",
     "Какая галактика находится на картинке?", "В рамках какой научной группы организован семинар «Математического моделирования в прикладных задачах электродинамики»"],
    ["Какая проблема фундаментальной и прикладной сейсмологии является одной из центральных?",
     "Для чего необходимо изучать механизмы физических процессов, происходящих в залежах углеводородного сырья?",
     "Где можно познакомиться с процессами развития поверхностных и внутренних волн?",
     "Какая научная группа кафедры физики атмосферы исследует полярные льды Марса?",
     "В чём причина появления и эволюции волновых структур?"]
]

departments = [
        "Отделение экспериментальной и теоретической физики",
        "Отделение ядерной физики",
        "Отделение физики твердого тела",
        "Отделение радиофизики",
        "Отделение прикладной математики",
        "Отделение геофизики"
    ]

# Названия столбцов
HEADERS = ["ФИО", "Группа", "User ID"] + [f"{day} Вопрос {i + 1}" for day in
                                          ["эксп и теор", "ядро", "твёрдое тело", "радио", "мат", "геофиз"] for i in range(5)]
sheet.update([HEADERS])

######################################################################################################################
#bot.set_webhook(url="botkaz-production.up.railway.app")
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Введи своё ФИО:")
    user_states[message.chat.id] = "waiting_for_fio"


@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == "waiting_for_fio")
def process_fio(message):
    user_data[message.chat.id] = {"ФИО": message.text}
    bot.send_message(message.chat.id, "Теперь введи свою группу:")
    user_states[message.chat.id] = "waiting_for_group"


@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == "waiting_for_group")
def process_group(message):
    user_data[message.chat.id]["Группа"] = message.text
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Пройти квест"))
    markup.add(KeyboardButton("Узнать про КАЯ"))
    bot.send_message(message.chat.id, "Спасибо! Теперь нажмите Пройти квест, чтобы начать:", reply_markup=markup)
    user_states[message.chat.id] = "waiting_for_quest"

@bot.message_handler(func=lambda message: message.text == "Узнать про КАЯ")
def about_kaya(message):
    bot.send_photo(message.chat.id, open(FOTO_KAZ, 'rb'), "Проект «Кафедры от А до Я» традиционно проводит ежесеместровую выставку кафедр Физического факультета в холле ЦФА.Команда организаторов делает все возможное, чтобы у студентов 1-2 курсов была возможность встретиться с представителями всех кафедр в одной точке пространства и времени.Наши соцсети, где мы регулярно публикуем информацию о встречах с кафедрами: VK: vk.com/ffkayaTG: t.me/adoyakaf")

@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == "waiting_for_quest")
def select_department(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for department in departments:
        markup.add(KeyboardButton(department))
    bot.send_message(message.chat.id, "Выберите отделение:", reply_markup=markup)
    bot.register_next_step_handler(message, process_department_selection)

def process_department_selection(message):
    user_answers[message.chat.id] = [user_data[message.chat.id]["ФИО"], user_data[message.chat.id]["Группа"],str(message.chat.id)] + [""] * 30
    if message.text in departments:
        a = departments.index(message.text)
        ask_next_question(message.chat.id, a, 0)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, выберите одно из предложенных отделений.")
        select_department(message)

'''def start_quest(message):
    day = datetime.datetime.today().weekday()
    if day == 6:
        day = 3
    user_answers[message.chat.id] = [user_data[message.chat.id]["ФИО"], user_data[message.chat.id]["Группа"],
                                     str(message.chat.id)] + [""] * 30
    bot.send_message(message.chat.id,
                     f"Вы проходите квест за {['Понедельник', 'Вторник', 'Среду', 'Четверг', 'Пятницу', 'Субботу'][day]}.")
    ask_next_question(message.chat.id, day, 0)'''

def ask_next_question(chat_id, day, question_index):
    if question_index < len(QUESTIONS_BY_DAY[day]):
        user_states[chat_id] = f"answering_{day}_{question_index}"
        bot.send_message(chat_id, QUESTIONS_BY_DAY[day][question_index])
        question = QUESTIONS_BY_DAY[day][question_index]
        if question == "Функция распределения чего изображена на рисунке?":
            with open(PHOTO_RASP, 'rb') as img:
                bot.send_photo(chat_id, img)
        if question == "Какая галактика находится на картинке?":
            with open(FOTO, 'rb') as img:
                bot.send_photo(chat_id, img)
    else:
        save_answers(chat_id, day)


@bot.message_handler(func=lambda message: message.chat.id in user_states)
def process_answer(message):
    state = user_states.get(message.chat.id, "")
    parts = state.split("_")
    if len(parts) == 3 and parts[0] == "answering":
        day = int(parts[1])
        question_index = int(parts[2])
        user_answers[message.chat.id][3 + day * 5 + question_index] = message.text
        ask_next_question(message.chat.id, day, question_index + 1)


def save_answers(chat_id, day):
    records = sheet.get_all_records()
    user_id = str(chat_id)
    existing_row = None

    for i, row in enumerate(records, start=2):
        if str(row.get("User ID")) == user_id:
            existing_row = i
            break

    max_columns = len(HEADERS)
    row_data = user_answers[chat_id][:max_columns]

    if existing_row:
        current_data = sheet.row_values(existing_row)
        for j in range(len(current_data), max_columns):
            current_data.append("")
        for j in range(3, max_columns):
            if not row_data[j]:
                row_data[j] = current_data[j]
        sheet.update(range_name=f"A{existing_row}", values=[row_data])
    else:
        sheet.append_row(row_data)

    bot.send_message(chat_id, "Спасибо за участие! Ваши ответы сохранены.")


    # Если ещё есть отделения — снова предлагаем выбрать
    if "О" in str(departments):
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for department in departments:
            markup.add(KeyboardButton(department))
        bot.send_message(chat_id, "Выберите следующее отделение для прохождения квеста:", reply_markup=markup)
        bot.register_next_step_handler_by_chat_id(chat_id, process_department_selection)
    else:
        bot.send_message(chat_id, ".",reply_markup=ReplyKeyboardRemove())  # Отправляем "пустое" сообщение (невидимый символ)
        bot.send_message(chat_id, "Вы прошли все отделения! 🎉")

    # Удаляем состояние пользователя, чтобы начать заново
    del user_states[chat_id]
    del user_answers[chat_id]

bot.polling(none_stop=True)import telebot
import gspread
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import os
import json
from oauth2client.service_account import ServiceAccountCredentials
from telebot.types import ReplyKeyboardRemove
# Константы
TELEGRAM_TOKEN = '7918191420:AAGm1VUNmX3VY4He02wP7VxVN6aW-JwqvSI'
#7918191420:AAGm1VUNmX3VY4He02wP7VxVN6aW-JwqvSI
SPREADSHEET_ID = '1aNzWinJl6ZJJ44vVPcmlGv7xA9MCx83AvuHhr_llayQ'
FOTO = r"Photo_2_vopr.png"
FOTO_KAZ = r"img_2.png"
PHOTO_RASP = r"PHOTO_RASP.png"

# Авторизация Google Sheets
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]
"""key_json = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON')

if not key_json:
    raise ValueError("Переменная окружения GOOGLE_APPLICATION_CREDENTIALS_JSON не установлена")

creds_dict = json.loads(key_json)

creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict)"""
creds = ServiceAccountCredentials.from_json_keyfile_name(r'C:\Users\98519\PycharmProjects\PythonProject_bot\credentials.json', scope)
client = gspread.authorize(creds)
sheet = client.open_by_key(SPREADSHEET_ID).sheet1

'''key_json = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON')

if not key_json:
    raise ValueError("Переменная окружения GOOGLE_APPLICATION_CREDENTIALS_JSON не установлена")

creds_dict = json.loads(key_json)'''

client = gspread.authorize(creds)
sheet = client.open_by_key(SPREADSHEET_ID).sheet1

# Инициализация бота
bot = telebot.TeleBot(TELEGRAM_TOKEN)
user_states = {}
user_answers = {}
user_data = {}

QUESTIONS_BY_DAY = [
    ["Что такое хиральность🤔? Какое подтверждение получил расчёт хиральности рукава Ориона в галактике Млечный путь🌌? <i>(1/5)</i>",
     "Какая лаборатория <b>кафедры оптики, спектроскопии и физики наносистем</b> основана на использовании возобновляемых ресурсов♻️? <i>(2/5)</i>",
     "Какой из перечисленных курсов не читается📖 на <b>кафедре медицинской физики</b>? <i>(3/5)</i>",
     "Какие курсы преподает <b>кафедра общей физики</b> для студентов🙋🏻‍♂️ 1-2 курсов? <i>(4/5)</i>",
     "Какое ❗новое название получила <b>кафедра общей физики и молекулярной электроники?</b> <i>(5/5)</i>"],
    ["К какому классу относится солнечная вспышка ☀, представленная на стенгазете <b>кафедры физики космоса</b>☄? <i>(1/5)</i>",
     "При участии какой <b>кафедры</b> были открыты 102-105, 115, 117-118 элементы⚛️? <i>(2/5)</i>",
     "Какие приборы используются при построении виртуальных моделей для <b>«3D Цифрового пациента»</b>😷? <i>(3/5)</i>",
     "О каких астрофизических🔭 объектах может быть получена новая информация благодаря экспериментам на <b>NICA</b>? <i>(4/5)</i>",
     "В чём основная сложность изучения рождения🎂 электрон-позитронных пар в сильном электрическом поле, рассеяния света на свете🔦 и расщепления фотона γ? <i>(5/5)</i>"],
    ["Совместно с каким университетом ведёт исследования <b>кафедра физики полупроводников и криоэлектроники</b>? <i>(1/5)</i>",
     "Для чего <b>модифицируются полимерные матрицы</b>? <i>(2/5)</i>",
     "Чьи работы послужили основой для создания теории электронной структуры и кинетических свойств неупорядоченных сплавов? <i>(3/5)</i>",
     "На какой кафедре направлением исследований являются квантовые кооперативные явления в низкоразмерных системах? <i>(4/5)</i>",
     "Характеристики каких лазеров изучает группа узкозонных полупроводников? <i>(5/5)</i>"],
    ["При участии какой <b>группы</b> в 2016 году произошло открытие гравитационных волн🍎⬇️? <i>(1/5)</i>",
     "Какая <b>кафедра</b> располагает уникальными сооружениями: звукомерной🔊 и реверберационной〰️ камерами? <i>(2/5)</i>",
     "Что такое метод <b>двухфотонной лазерной литографии</b>🥽 и для чего он применяется? <i>(3/5)</i>",
     "Какие 2 🧪лаборатории🥼 включает <b>кафедра нанофотоники</b>? <i>(4/5)</i>",
     "Приведите пример не менее 2 экспериментальных групп <b>кафедры квантовой электроники</b>⚡. <i>(5/5)</i>"],
    ["Какая теория используется при <b>математическом моделировании</b> развития мегаполисов🏙️? <i>Дайте определение функций, которые применяются в рамках этой теории. (1/5)</i>",
     "На какой <b>кафедре</b> одним из научных направлений👨🏻‍🔬 является «Новые топологические и нейросетевые🤖 методы анализа материалов и данных»? <i>(2/5)</i>",
     "Какие основные физические процессы💡 и системы изучаются в рамках направления математического моделирования🧮 на <b>кафедре математики</b>?  <i>(3/5)</i>",
     "Какое <b>понятие</b>, основанное на доступной информации📋 об наблюдаемых величинах, противопоставляется задаче управления и представляет собой задачу определения текущего состояния системы🌐? <i>(4/5)</i>",
     "Какие <b>2</b>  из перечисленных направлений относятся к <b>кафедре физико-математических методов управления</b>👨🏻‍💼? <i>Укажите номера пунктов. Пример (1,3). (5/5)</i>"],
    ["Какая научная группа <b>кафедры физики атмосферы</b>🌦️ исследует полярные льды Марса? <i>(1/5)</i>",
     "Что такое Мониторинг высотного здания <b>МГУ</b>🏰? <i>(2/5)</i>",
     "Какой из перечисленных курсов не читается на <b>кафедре физики Земли</b>🌍? <i>(3/5)</i>",
     "Где обычно проходит летняя полевая практика студентов <b>кафедры физики моря🌊 и вод💧 суши🏜️</b>? <i>(4/5)</i>",
     "В чём причина появления и эволюции волновых структур🧬? <i>(5/5)</i>"]
]

departments = [
        "Отделение экспериментальной и теоретической физики",
        "Отделение ядерной физики",
        "Отделение физики твердого тела",
        "Отделение радиофизики",
        "Отделение прикладной математики",
        "Отделение геофизики"
    ]

# Названия столбцов
HEADERS = ["ФИО", "Группа", "User ID"] + [f"{day} Вопрос {i + 1}" for day in
                                          ["эксп и теор", "ядро", "твёрдое тело", "радио", "мат", "геофиз"] for i in range(5)]
sheet.update([HEADERS])

######################################################################################################################
#bot.set_webhook(url="botkaz-production.up.railway.app")
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Введи своё ФИО:")
    user_states[message.chat.id] = "waiting_for_fio"


@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == "waiting_for_fio")
def process_fio(message):
    user_data[message.chat.id] = {"ФИО": message.text}
    bot.send_message(message.chat.id, "Теперь введи свою группу:")
    user_states[message.chat.id] = "waiting_for_group"


@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == "waiting_for_group")
def process_group(message):
    user_data[message.chat.id]["Группа"] = message.text
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Узнать про КАЯ"))
    markup.add(KeyboardButton("Пройти квест"))
    bot.send_message(message.chat.id, "Спасибо! Теперь нажмите Пройти квест, чтобы начать:", reply_markup=markup)
    user_states[message.chat.id] = "waiting_for_quest"

@bot.message_handler(func=lambda message: message.text == "Узнать про КАЯ")
def about_kaya(message):
    bot.send_photo(message.chat.id, open(FOTO_KAZ, 'rb'), "Проект <b>«Кафедры от А до Я»</b> традиционно проводит ежесеместровую выставку кафедр Физического факультета в холле ЦФА. Команда организаторов делает все возможное, чтобы у студентов 1-2 курсов была возможность встретиться с представителями всех кафедр в одной точке <i>пространства и времени.</i> Наши соцсети, где мы регулярно публикуем информацию о встречах с кафедрами: <a href='vk.com/ffkaya'>vk</a> <a href='https://t.me/ff_kaya'>tg</a>", parse_mode="HTML")
    bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEPe6Zo3VmuQvMIrkqE1S_kI_XQbH1jrAAC-mIAAgSRoUiJ4qDOCcjHvzYE")

@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == "waiting_for_quest")
def select_department(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for department in departments:
        markup.add(KeyboardButton(department))
    bot.send_message(message.chat.id, "Выберите отделение:", reply_markup=markup)
    bot.register_next_step_handler(message, process_department_selection)
ind = 0
def process_department_selection(message):
    global ind
    user_answers[message.chat.id] = [user_data[message.chat.id]["ФИО"], user_data[message.chat.id]["Группа"],str(message.chat.id)] + [""] * 30
    if message.text in departments:
        ind = departments.index(message.text)
        ask_next_question(message.chat.id, ind, 0)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, выберите одно из предложенных отделений.")
        select_department(message)

'''def start_quest(message):
    day = datetime.datetime.today().weekday()
    if day == 6:
        day = 3
    user_answers[message.chat.id] = [user_data[message.chat.id]["ФИО"], user_data[message.chat.id]["Группа"],
                                     str(message.chat.id)] + [""] * 30
    bot.send_message(message.chat.id,
                     f"Вы проходите квест за {['Понедельник', 'Вторник', 'Среду', 'Четверг', 'Пятницу', 'Субботу'][day]}.")
    ask_next_question(message.chat.id, day, 0)'''

def ask_next_question(chat_id, day, question_index):
    if question_index < len(QUESTIONS_BY_DAY[day]):
        user_states[chat_id] = f"answering_{day}_{question_index}"
        bot.send_message(chat_id, QUESTIONS_BY_DAY[day][question_index],parse_mode="HTML", reply_markup= ReplyKeyboardRemove())
        question = QUESTIONS_BY_DAY[day][question_index]
        if question == QUESTIONS_BY_DAY[4][4]:
            bot.send_message(chat_id, "<b>1.</b> Методы и технологии искусственного интеллекта в автоматических и автоматизированных системах⚙️\n<b>2.</b> Информационные технологии морфологического анализа изображений🖼️ и сигналов📡\n<b>3.</b> Автоматизированное управление в больших системах🔥\n<b>4.</b> Квантовая информатика🐈", parse_mode="HTML")
        if question == QUESTIONS_BY_DAY[0][2]:
            bot.send_message(chat_id, "• <b>Биоинженерия</b>\n• <b>Современные клеточные технологии</b>\n• <b>Физические основы ядерной медицины</b>\n• <b>Основы нелинейной динамики</b>",parse_mode="HTML")
    else:
        save_answers(chat_id, day)


@bot.message_handler(func=lambda message: message.chat.id in user_states)
def process_answer(message):
    state = user_states.get(message.chat.id, "")
    parts = state.split("_")
    if len(parts) == 3 and parts[0] == "answering":
        day = int(parts[1])
        question_index = int(parts[2])
        user_answers[message.chat.id][3 + day * 5 + question_index] = message.text
        ask_next_question(message.chat.id, day, question_index + 1)


def save_answers(chat_id, day):
    if departments[ind][-1] != "✅":
        departments[ind] = departments[ind] + " ✅"
    records = sheet.get_all_records()
    user_id = str(chat_id)
    existing_row = None

    for i, row in enumerate(records, start=2):
        if str(row.get("User ID")) == user_id:
            existing_row = i
            break

    max_columns = len(HEADERS)
    row_data = user_answers[chat_id][:max_columns]

    if existing_row:
        current_data = sheet.row_values(existing_row)
        for j in range(len(current_data), max_columns):
            current_data.append("")
        for j in range(3, max_columns):
            if not row_data[j]:
                row_data[j] = current_data[j]
        sheet.update(range_name=f"A{existing_row}", values=[row_data])
    else:
        sheet.append_row(row_data)

    bot.send_message(chat_id, "Спасибо за участие! Ваши ответы сохранены.")


    # Если ещё есть отделения — снова предлагаем выбрать

    if [dep[-1] for dep in departments] != ["✅","✅","✅","✅","✅","✅"]:
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for department in departments:
            markup.add(KeyboardButton(department))
        bot.send_message(chat_id, "Выберите следующее отделение для прохождения квеста:", reply_markup=markup)
        bot.register_next_step_handler_by_chat_id(chat_id, process_department_selection)
    else:
        bot.send_message(chat_id, "Вы прошли все отделения! 🎉",reply_markup=ReplyKeyboardRemove())  # Отправляем "пустое" сообщение (невидимый символ)
        bot.send_photo(chat_id, open(FOTO_KAZ, 'rb'),
                       "Проект <b>«Кафедры от А до Я»</b> традиционно проводит ежесеместровую выставку кафедр Физического факультета в холле ЦФА. Команда организаторов делает все возможное, чтобы у студентов 1-2 курсов была возможность встретиться с представителями всех кафедр в одной точке <i>пространства и времени.</i> Наши соцсети, где мы регулярно публикуем информацию о встречах с кафедрами: <a href='vk.com/ffkaya'>vk</a> <a href='https://t.me/ff_kaya'>tg</a>",
                       parse_mode="HTML")
        bot.send_sticker(chat_id, "CAACAgIAAxkBAAEPe6Zo3VmuQvMIrkqE1S_kI_XQbH1jrAAC-mIAAgSRoUiJ4qDOCcjHvzYE")
    # Удаляем состояние пользователя, чтобы начать заново
    del user_states[chat_id]
    del user_answers[chat_id]


bot.polling(none_stop=True)
import telebot
import gspread
import datetime
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import os
import json
from oauth2client.service_account import ServiceAccountCredentials

import telebot
bot = telebot.TeleBot('7918191420:AAFC9r_p8zylOAr5U-jVQuOVwih-NIPg5_Y')
bot.get_updates(offset=-1)

# Константы
TELEGRAM_TOKEN = '7918191420:AAFC9r_p8zylOAr5U-jVQuOVwih-NIPg5_Y'
SPREADSHEET_ID = '1aNzWinJl6ZJJ44vVPcmlGv7xA9MCx83AvuHhr_llayQ'
FOTO = r"img.png"
FOTO_KAZ = r"photo_KAZ.jpg"

# Авторизация Google Sheets
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]


creds = ServiceAccountCredentials.from_json_keyfile_name(r'C:\Users\98519\PycharmProjects\PythonProject_bot\credentials.json', scope)

client = gspread.authorize(creds)
sheet = client.open_by_key(SPREADSHEET_ID).sheet1

# Инициализация бота
bot = telebot.TeleBot(TELEGRAM_TOKEN)
user_states = {}
user_answers = {}
user_data = {}

QUESTIONS_BY_DAY = [
    ["Какими методами описывается фронт пламени?",
     "Перечислите теории динамического хаоса",
     "На основе чего реализуется автоматическое обнаружение и отслеживание структур сверхзвукового потока?",
     "В чём смысл параметра q в q-статфизике?",
     "Где расположена экспериментальная база для исследования системы гемостаза?"],
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
    ["Какая проблема фундаментальной и прикладной сейсмологии является одной из центральных?",
     "Для чего необходимо изучать механизмы физических процессов, происходящих в залежах углеводородного сырья?",
     "Где можно познакомиться с процессами развития поверхностных и внутренних волн?",
     "Какая научная группа кафедры физики атмосферы исследует полярные льды Марса?",
     "В чём причина появления и эволюции волновых структур?"],
    ["Какие методы получили фундаментальные результаты по теории мер?",
     "Какая концепция существенно расширяет возможности экспериментальных исследований?",
     "Большое поле приложения современных методов решения некорректных задач даёт ...",
     " Какая галактика находится на картинке?", "В рамках какой научной группы организован семинар 'мат моделирования в прикладных задачах электродинамики'"],
    ["Какая проблема фундаментальной и прикладной сейсмологии является одной из центральных?",
     "Для чего необходимо изучать механизмы физических процессов, происходящих в залежах углеводородного сырья?",
     "Где можно познакомиться с процессами развития поверхностных и внутренних волн?",
     "Какая научная группа кафедры физики атмосферы исследует полярные льды Марса?",
     "В чём причина появления и эволюции волновых структур?"]
]

# Названия столбцов
HEADERS = ["ФИО", "Группа", "User ID"] + [f"{day} Вопрос {i + 1}" for day in
                                          ["эксп и теор", "ядро", "твёрдое тело", "радио", "мат", "геофиз"] for i in range(5)]
sheet.update([HEADERS])

######################################################################################################################


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
    bot.send_message(message.chat.id, "Спасибо! Теперь нажмите 'Пройти квест', чтобы начать:", reply_markup=markup)
    user_states[message.chat.id] = "waiting_for_quest"

@bot.message_handler(func=lambda message: message.text == "Узнать про КАЯ")
def about_kaya(message):
    bot.send_photo(message.chat.id, open(FOTO_KAZ, 'rb'), "КАЯ — это комиссия профкома, которая занимается помощью первокурсникам в нахождении своего места во вселенной")






@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == "waiting_for_quest")
def select_department(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    departments = [
        "Отделение экспериментальной и теоретической физики",
        "Отделение ядерной физики",
        "Отделение физики твердого тела",
        "Отделение радиофизики",
        "Отделение прикладной математики",
        "Отделение геофизики"
    ]
    for department in departments:
        markup.add(KeyboardButton(department))
    bot.send_message(message.chat.id, "Выберите отделение:", reply_markup=markup)
    bot.register_next_step_handler(message, process_department_selection)

def process_department_selection(message):
    departments = [
        "Отделение экспериментальной и теоретической физики",
        "Отделение ядерной физики",
        "Отделение физики твердого тела",
        "Отделение радиофизики",
        "Отделение прикладной математики",
        "Отделение геофизики"
    ]
    if message.text in departments:
        user_data[message.chat.id] = departments.index(message.text)
        ask_next_question(message.chat.id, departments.index(message.text), 0)
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
            with open(FOTO, 'rb') as img:
                bot.send_photo(chat_id, img)
        if question == "В рамках какой научной группы организован семинар 'мат моделирования в прикладных задачах электродинамики'":
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
    del user_states[chat_id]
    del user_answers[chat_id]
    del user_data[chat_id]



bot.polling(none_stop=True)

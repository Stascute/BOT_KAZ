import telebot
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
creds = ServiceAccountCredentials.from_json_keyfile_name(r'credentials.json', scope)
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
    ["<i>️✍️👩️‍🔬Вопрос 1 из 5</i>\n\nЧто такое хиральность🤔? Какое подтверждение получил расчёт хиральности рукава Ориона в галактике Млечный путь🌌?\n\n<i><pre>Ответ на стенгазете кафедры биофизики</pre></i>",
     "<i>️✍️👩️‍🔬Вопрос 2 из 5</i>\n\nКакая лаборатория <b>кафедры оптики, спектроскопии и физики наносистем</b> основана на использовании возобновляемых ресурсов♻️?",
     "<i>️✍️👩️‍🔬Вопрос 3 из 5</i>\n\nКакой из перечисленных курсов не читается📖 на <b>кафедре медицинской физики</b>?",
     "<i>️✍️👩️‍🔬Вопрос 4 из 5</i>\n\nКакие курсы преподает <b>кафедра общей физики</b> для студентов🙋🏻‍♂️ 1-2 курсов?",
     "<i>️✍️👩️‍🔬Вопрос 5 из 5</i>\n\nКакое ❗новое название получила <b>кафедра общей физики и молекулярной электроники?</b>\n\n<pre><i>Подсказка: первая часть названия сохранилась, ответ можно найти в стенгазете кафедры</i></pre>"],
    ["<i>️⚛️Вопрос 1 из 5</i>\n\nК какому классу относится солнечная вспышка ☀, представленная на стенгазете <b>кафедры физики космоса</b>☄?",
     "<i>️⚛️Вопрос 2 из 5</i>\n\nПри участии какой <b>кафедры</b> были открыты 102-105, 115, 117-118 элементы⚛️?",
     "<i>️⚛️Вопрос 3 из 5</i>\n\nКакие приборы используются при построении виртуальных моделей для <b>«3D Цифрового пациента»</b>😷?\n\n<pre><i>Ответ на стенгазете кафедры атомной физики, физики плазмы и микроэлектроники</i></pre>",
     "<i>️⚛️Вопрос 4 из 5</i>\n\nО каких астрофизических🔭 объектах может быть получена новая информация благодаря экспериментам на <b>NICA</b>?\n\n<pre><i>Ответ на стенгазете кафедры фундаментальных ядерных взаимодействий</i></pre>",
     "<i>️⚛️Вопрос 5 из 5</i>\n\nВ чём основная сложность изучения рождения🎂 электрон-позитронных пар в сильном электрическом поле, рассеяния света на свете🔦 и расщепления фотона γ?\n\n<pre><i>Ответ на стенгазете кафедра квантовой теории и физики высоких энергий</i></pre>"],
    ["<i>️💎Вопрос 1 из 5</i>\n\nСовместно с каким университетом ведёт исследования <b>кафедра физики полупроводников и 🧊криоэлектроники</b>?",
     "<i>️💎Вопрос 2 из 5</i>\n\nДля чего <b>модифицируются полимерные матрицы🔢</b>?\n\n<pre><i>Ответ на стенгазете кафедры физики полимеров и кристаллов</i></pre>",
     "<i>️💎Вопрос 3 из 5</i>\n\nКакие из перечисленных направлений относятся к <b>кафедре 🧲магнетизма</b>, а какие — к <b>кафедре физики 🪨твердого тела</b>?\n\n<pre><i>Укажите соответствующие номера направлений для каждой кафедры</i></pre>",
     "<i>️💎Вопрос 4 из 5</i>\n\nНа какой <b>кафедре</b> направлением исследований🔬 являются квантовые кооперативные явления в низкоразмерных📏 системах?\n\n<pre><i> Ответ на стенгазете кафедры общей физики и физики конденсированного состояния</i></pre>",
     "<i>️💎Вопрос 5 из 5</i>\n\nХарактеристики📝 каких лазеров изучает группа узкозонных полупроводников?"],
    ["<i>️📡Вопрос 1 из 5</i>\n\nПри участии какой <b>группы</b> в 2016 году произошло открытие гравитационных волн🍎⬇️?",
     "<i>️📡Вопрос 2 из 5</i>\n\nКакая <b>кафедра</b> располагает уникальными сооружениями: звукомерной🔊 и реверберационной〰️ камерами?",
     "<i>️📡Вопрос 3 из 5</i>\n\nЧто такое метод <b>двухфотонной лазерной литографии</b>🥽 и для чего он применяется?\n\n<pre><i>Ответ на стенгазете кафедры нанофотоники</i></pre>",
     "<i>️📡Вопрос 4 из 5</i>\n\nКакие 2 🧪лаборатории🥼 включает <b>кафедра нанофотоники</b>?",
     "<i>️📡Вопрос 5 из 5</i>\n\nПриведите пример не менее 2 экспериментальных групп <b>кафедры квантовой электроники</b>⚡."],
    ["<i>🧮Вопрос 1 из 5</i>\n\nКакая теория используется при <b>математическом моделировании</b> развития мегаполисов🏙️?\n<i>Дайте определение функций, которые применяются в рамках этой теории.</i>\n\n<pre><i>Ответ на стенгазете кафедры математики</i></pre>",
     "<i>🧮Вопрос 2 из 5</i>\n\nНа какой <b>кафедре</b> одним из научных направлений👨🏻‍🔬 является «Новые топологические и нейросетевые🤖 методы анализа материалов и данных»?",
     "<i>🧮Вопрос 3 из 5</i>\n\nКакие основные физические процессы💡 и системы изучаются в рамках направления математического моделирования🧮 на <b>кафедре математики</b>?\n<i>Приведите пример</i>",
     "<i>🧮Вопрос 4 из 5</i>\n\nКакое <b>понятие</b>, основанное на доступной информации📋 об наблюдаемых величинах, противопоставляется задаче управления и представляет собой задачу определения текущего состояния системы🌐?\n\n<pre><i>Ответ на стенгазете кафедры физико-математических методов управления</i></pre>",
     "<i>🧮Вопрос 5 из 5</i>\n\nКакие <b>2</b>  из перечисленных направлений относятся к <b>кафедре физико-математических методов управления</b>👨🏻‍💼?\n\n<pre><i>Укажите номера пунктов</i></pre>"],
    ["<i>️🌏Вопрос 1 из 5</i>\n\nКакая научная группа <b>кафедры физики атмосферы</b>🌦️ исследует полярные льды Марса?",
     "<i>️🌏Вопрос 2 из 5</i>\n\nЧто такое Мониторинг высотного здания <b>МГУ</b>🏰?\n\n<pre><i>Ответ на стенгазете кафедры физики Земли</i></pre>",
     "<i>️🌏Вопрос 3 из 5</i>\n\nКакой из перечисленных курсов не читается на <b>кафедре физики Земли</b>🌍?",
     "<i>️🌏Вопрос 4 из 5</i>\n\nГде обычно проходит летняя полевая практика студентов <b>кафедры физики моря🌊 и вод💧 суши🏜️</b>?",
     "<i>️🌏Вопрос 5 из 5</i>\n\nВ чём причина появления и эволюции волновых структур🧬?\n\n<pre><i>Ответ на стенгазете кафедры физики атмосферы</i></pre>"]
]

departments = [
        "✍️👩️‍🔬Отделение экспериментальной и теоретической физики",
        "⚛️Отделение ядерной физики",
        "💎Отделение физики твердого тела",
        "📡Отделение радиофизики",
        "🧮Отделение прикладной математики",
        "🌏Отделение геофизики"
    ]

# Названия столбцов
HEADERS = ["ФИО", "Группа", "User ID"] + [f"{day} Вопрос {i + 1}" for day in
                                          ["эксп и теор", "ядро", "твёрдое тело", "радио", "мат", "геофиз"] for i in range(5)]
sheet.update([HEADERS])

######################################################################################################################
#bot.set_webhook(url="botkaz-production.up.railway.app")
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! 👋 Это бот для прохождения квеста по стенгазетам выставки «Кафедр от А до Я».\n\n<b>Всё просто:</b>\n1. Выбери отделение.\n2. Найди ответы на вопросы на стендах кафедр, относящихся к этому отделению.\n3. Пройди все 6 отделений — и получи призы!", parse_mode="HTML")
    bot.send_message(message.chat.id, "Введи своё ФИО:")
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
    bot.send_photo(message.chat.id, open(FOTO_KAZ, 'rb'), "<b>Проект «Кафедры от А до Я», или «КАЯ»</b> — это\n\n— Выставка кафедр с представителями каждый семестр;\n\n— Информирование о встречах с кафедрами в группе ВКонтакте и телеграмм-канале;\n\n— Онлайн освещение деятельности кафедр в <b>медиа-ресурсах</b> проекта.\n\n💜 Знакомьтесь со всем спектром кафедр физфака МГУ вместе с нами: <a href='http://vk.com/ffkaya'>ВК</a> | <a href='https://t.me/ff_kaya'>ТГ</a>", parse_mode="HTML")

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
        elif question == QUESTIONS_BY_DAY[0][2]:
            bot.send_message(chat_id, "• <b>Биоинженерия</b>\n• <b>Современные клеточные технологии</b>\n• <b>Физические основы ядерной медицины</b>\n• <b>Основы нелинейной динамики</b>",parse_mode="HTML")
        elif question == QUESTIONS_BY_DAY[2][2]:
            bot.send_message(chat_id,"<b>1.Исследования динамики 🧲магнитных процессов\n2.✏️Дизайн материалов\n3.🧠Умные материалы для энергетики и космоса\n4.Прикладной магнетизм и 🔄спинтроника</b>",parse_mode="HTML")
        elif question == QUESTIONS_BY_DAY[5][2]:
            bot.send_message(chat_id,"<b>•Экстремальные явления в геофизике\n•Земной магнетизм\n•Спутниковые методы в геофизике\n•Основы петрофизики</b>",parse_mode="HTML")

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


    # Если ещё есть отделения — снова предлагаем выбрать

    if [dep[-1] for dep in departments] != ["✅","✅","✅","✅","✅","✅"]:
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for department in departments:
            markup.add(KeyboardButton(department))
        bot.send_message(chat_id, "Выберите следующее отделение для прохождения квеста:", reply_markup=markup)
        bot.register_next_step_handler_by_chat_id(chat_id, process_department_selection)
    else:
        bot.send_message(chat_id, "<b>Поздравляем!</b> 🎉\n\nТы прошёл квест по всем отделениям выставки <b>«Кафедры от А до Я».</b>\n\nРезультаты будут опубликованы после окончания выставки в <a href='https://t.me/ff_kaya'>телеграм-канале</a> проекта.\n\nНадеемся, что на нашей выставке ты найдёшь свой научный путь!",reply_markup=ReplyKeyboardRemove(), parse_mode="HTML")
        bot.send_photo(chat_id, open(FOTO_KAZ, 'rb'),"<b>Проект «Кафедры от А до Я», или «КАЯ»</b> — это\n\n— Выставка кафедр с представителями каждый семестр;\n\n— Информирование о встречах с кафедрами в группе ВКонтакте и телеграмм-канале;\n\n— Онлайн освещение деятельности кафедр в <b>медиа-ресурсах</b> проекта.\n\n💜 Знакомьтесь со всем спектром кафедр физфака МГУ вместе с нами: <a href='http://vk.com/ffkaya'>ВК</a> | <a href='https://t.me/ff_kaya'>ТГ</a>",parse_mode="HTML")
    # Удаляем состояние пользователя, чтобы начать заново
    del user_states[chat_id]
    del user_answers[chat_id]


bot.polling(none_stop=True)

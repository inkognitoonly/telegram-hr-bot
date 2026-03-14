import telebot

TOKEN = "7505831892:AAEXunB46sqfDxkas6G1ratUdvuEd6pn-88"
ADMIN_CHAT_ID = 6249456543

bot = telebot.TeleBot(TOKEN)

user_data = {}


@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    user_data[chat_id] = {}

    bot.send_message(
        chat_id,
        "Здравствуйте!\n\n"
        "Для быстрого отклика заполните короткую анкету.\n"
        "Это займет всего пару минут.\n\n"
        "1/6 — Как вас зовут?"
    )

    bot.register_next_step_handler(message, get_name)


def get_name(message):
    chat_id = message.chat.id
    user_data[chat_id]["name"] = message.text.strip()

    bot.send_message(chat_id, "2/6 — Сколько вам лет?")
    bot.register_next_step_handler(message, get_age)


def get_age(message):
    chat_id = message.chat.id
    age = message.text.strip()

    if not age.isdigit():
        bot.send_message(chat_id, "Пожалуйста, напишите возраст цифрами.")
        bot.register_next_step_handler(message, get_age)
        return

    user_data[chat_id]["age"] = age

    bot.send_message(chat_id, "3/6 — Из какого вы города?")
    bot.register_next_step_handler(message, get_city)


def get_city(message):
    chat_id = message.chat.id
    user_data[chat_id]["city"] = message.text.strip()

    bot.send_message(chat_id, "4/6 — Какие иностранные языки вы знаете?")
    bot.register_next_step_handler(message, get_languages)


def get_languages(message):
    chat_id = message.chat.id
    user_data[chat_id]["languages"] = message.text.strip()

    bot.send_message(chat_id, "5/6 — Есть ли у вас опыт работы? Если да, кратко опишите.")
    bot.register_next_step_handler(message, get_experience)


def get_experience(message):
    chat_id = message.chat.id
    user_data[chat_id]["experience"] = message.text.strip()

    bot.send_message(chat_id, "6/6 — Готовы ли вы к переезду в Киев?")
    bot.register_next_step_handler(message, get_relocation)


def get_relocation(message):
    chat_id = message.chat.id
    user_data[chat_id]["relocation"] = message.text.strip()

    data = user_data[chat_id]

    username = message.from_user.username
    if username:
        username_text = f"@{username}"
    else:
        username_text = "не указан"

    full_name = message.from_user.full_name
    user_id = message.from_user.id

    admin_text = (
        "📩 Новая анкета кандидата\n\n"
        f"👤 Имя: {data['name']}\n"
        f"🎂 Возраст: {data['age']}\n"
        f"🏙 Город: {data['city']}\n"
        f"🌍 Языки: {data['languages']}\n"
        f"💼 Опыт работы: {data['experience']}\n"
        f"🚚 Переезд: {data['relocation']}\n\n"
        f"🙍 Имя в Telegram: {full_name}\n"
        f"🔹 Username: {username_text}\n"
        f"🆔 Telegram ID: {user_id}"
    )

    bot.send_message(
        chat_id,
        "Спасибо! Ваша анкета принята ✅\n\n"
        "Мы рассмотрим анкету и свяжемся с вами в Telegram."
    )

    bot.send_message(ADMIN_CHAT_ID, admin_text)

    user_data.pop(chat_id, None)


bot.polling(none_stop=True)
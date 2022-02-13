import const
import telebot
import os

bot = telebot.TeleBot(const.token)

upd = bot.get_updates()
last_upd = upd[-1]
mfu = last_upd.message  # message from user

print(bot.get_me())  # logging


def log(mes, ans):
    print(" ---------")
    from datetime import datetime
    print(datetime.now())
    print("Message from {0} {1}. (id = {2}) \n Text - {3}".format(mes.from_user.first_name,
                                                                  mes.from_user.last_name,
                                                                  str(mes.from_user.id),
                                                                  str(mes.text)))
    print("Answer: ", ans)
    print(" ---------")

    file = open(const.dirLOG, "a")
    file.write("{0}\nMessage from {1} {2}. (id = {3}) \nText - {4}\nAnswer: {5}\n---------\n\n".format(
        str(datetime.now()),
        str(mes.from_user.first_name),
        str(mes.from_user.last_name),
        str(mes.from_user.id),
        str(mes.text),
        str(ans)
    ))


# ----------------------------------------------------------------------------------------------------------------
# bot commands


@bot.message_handler(commands=['start'])
def handle_start(mes):  # show keyboard by command "/start"
    file = open(const.dirActive, "r")
    for line in file:
        if line == "True":
            user_markup = telebot.types.ReplyKeyboardMarkup(True)
            user_markup.row("Найближчі події")
            user_markup.row("Театральний клас")
            user_markup.row("Замовити квитки")
            user_markup.row("\u274c")
            bot.send_message(mes.from_user.id, "Ласкаво просимо до головного меню.", reply_markup=user_markup)
            log(mes, "Chat started")
        elif line == "False":
            user_markup = telebot.types.ReplyKeyboardMarkup(True)
            user_markup.row("Найближчі події")
            user_markup.row("Театральний клас")
            user_markup.row("\u274c")
            bot.send_message(mes.from_user.id, "Ласкаво просимо до головного меню.", reply_markup=user_markup)
            log(mes, "Chat started")


@bot.message_handler(commands=['keyboard'])
def show_kb(mes):
    file = open(const.dirActive, "r")
    for line in file:
        if line == "True":
            user_markup = telebot.types.ReplyKeyboardMarkup(True)
            user_markup.row("Найближчі події")
            user_markup.row("Театральний клас")
            user_markup.row("Замовити квитки")
            user_markup.row("\u274c")
            bot.send_message(mes.from_user.id, "Клавіатура до ваших послуг.", reply_markup=user_markup)
        elif line == "False":
            user_markup = telebot.types.ReplyKeyboardMarkup(True)
            user_markup.row("Найближчі події")
            user_markup.row("Театральний клас")
            user_markup.row("\u274c")
            bot.send_message(mes.from_user.id, "Клавіатура до ваших послуг.", reply_markup=user_markup)


@bot.message_handler(commands=['tickets'])
def start_handler(mes):
    file = open(const.dirActive, "r")
    for line in file:
        if line == "True":
            msg = bot.send_message(mes.chat.id, "Відправте анкету у наступному вигляді:"
                                                "\n<Ім'я на кого бронюються квитки>"
                                                "\n<Номер телефону>"
                                                "\n<Дорослий/дитячий(до 16 років) квиток>"
                                                "\n<Кількість квитків>")
            bot.register_next_step_handler(msg, ask_form)
        elif line == "False":
            bot.send_message(mes.from_user.id, "На даний момент ця функція не є активною")


def ask_form(mes):
    text = mes.text
    if not text.isdigit() and not text.isalpha() and len(text) > 5:
        bot.send_message(mes.from_user.id, "Надіслано на опрацювання. Дякуємо за відвідування наших вистав")
        file = open(const.dirTick, "a")
        file.write("----------------------\nMessage from {0} {1}. \n{2} (id: {3}) \n Text: \n{4}"
                   " \n ----------------------".format(mes.from_user.first_name,
                                                       mes.from_user.last_name,
                                                       mes.from_user.username,
                                                       str(mes.from_user.id),
                                                       mes.text))
        file.close()
        file_2 = open(const.dirID, "a")
        file_2.write("{0}-".format(mes.from_user.id))
        file_2.close()
        log(mes, "message saved")
    else:
        bot.send_message(mes.from_user.id, "Анкету заповнено неправильно")


@bot.message_handler(commands=['help'])
def com_list(mes):
    if mes.from_user.id == const.mainId:
        bot.send_message(mes.from_user.id, const.com_list)
        bot.register_next_step_handler(mes, do_command)
    else:
        bot.send_message(mes.from_user.id, "enter password:")
        bot.register_next_step_handler(mes, ask_pass)


def ask_pass(mes):
    if mes.text == const.code:
        bot.send_message(mes.from_user.id, const.com_list)
        bot.register_next_step_handler(mes, do_command)
    else:
        bot.send_message(mes.from_user.id, "wrong password")


def do_command(mes):
    if mes.text == "Clear_Log":
        d_file = open(const.dirLOG, "w")
        from datetime import datetime
        d_file.write(str(datetime.now()))
        d_file.write("\n-----------------------------------------------------\n")
        d_file.close()
        bot.send_message(mes.from_user.id, "Log restarted")

    elif mes.text == "Clear_Files":
        d_file = open(const.dirID, "w")
        d_file.close()
        d_file = open(const.dirTick, "w")
        d_file.close()
        bot.send_message(mes.from_user.id, "Files cleared")
        log(mes, "FILES SUCCESSFULLY DELETED!!!")

    elif mes.text == "Clear_ActPhotos":
        to_remove = os.listdir(const.dirP)
        for file in to_remove:
            os.remove(const.dirP + "/" + file)
        bot.send_message(mes.from_user.id, "Photos deleted")
        log(mes, "delete photos")

    elif mes.text == "Change_ActDescrip":
        bot.send_message(mes.from_user.id, "Спочатку відправте новий опис(не менше 20 символів)")
        bot.register_next_step_handler(mes, change_a)

    elif mes.text == "Start_Notification":
        n_file = open(const.dirID, "r")  # notification file
        n_id = []

        for line in n_file:  # writhing to iterable(list)
            n_id.append(line)

        for el in n_id:  # formatting list
            n_id = el.split("-")

        for el in n_id:  # last step to creating list of id's
            if len(el) < 1:
                n_id.remove(el)

        log(mes, "Notification started")

        for us_id in n_id:  # sending notification to user with "us_id" id
            bot.send_message(us_id, const.notification)

    elif mes.text == "Change_TheatreClass":
        bot.send_message(mes.from_user.id, "Введіть нову інформацію про театральний клас(або 'відмінити'):")
        bot.register_next_step_handler(mes, change_t)

    elif mes.text == "Load_ActPhotos":
        bot.send_message(mes.from_user.id, "Відправте фото")
        bot.register_next_step_handler(mes, load_p)

    elif mes.text == "Change_NotificationText":
        bot.send_message(mes.from_user.id, "Відправте новий текст для нагадування")
        bot.register_next_step_handler(mes, n_notif)

    elif mes.text == "Change_Password":
        bot.send_message(mes.from_user.id, "Введіть новий пароль")
        bot.register_next_step_handler(mes, change_pass)

    elif mes.text == "Change_Tickets":
        bot.send_message(mes.from_user.id, "Tickets (OFF/ON)")
        bot.register_next_step_handler(mes, change_tickets)


def change_tickets(mes):
    if mes.text == "ON":
        file = open(const.dirActive, "w")
        file.write("True")
        bot.send_message(mes.from_user.id, "Клавіатуру оновлено, напишіть /start")
    elif mes.text == "OFF":
        file = open(const.dirActive, "w")
        file.write("False")
        bot.send_message(mes.from_user.id, "Клавіатуру оновлено, напишіть /start")
    else:
        bot.send_message(mes.from_user.id, "ON - ввімкнути кнопку\nOFF - вимкнути\nНапишіть один із варіантів")
        bot.register_next_step_handler(mes, change_tickets)


def change_t(mes):
    if mes.text == "відмінити":
        bot.send_message(mes.from_user.id, "Відмінено")
    else:
        file = open(const.dirInfo, "w")
        file.write(mes.text)
        file.close()
        bot.send_message(mes.from_user.id, "Інформацію оновлено")
        log(mes, "theatre info changed")


def change_a(mes):
    if len(mes.text) > 20:
        all_files = os.listdir(const.dirP)
        for file in all_files:
            if ".txt" in file:
                new_disc = open(const.dirP + "/" + file, "w")
                new_disc.write(mes.text)
                new_disc.close()
        log(mes, "actions description changed")
    else:
        bot.send_message(mes.from_user.id, "Опис містить менше 20 символів")


def load_p(mes):
    try:
        file_info = bot.get_file(mes.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        src = const.dirP + "/" + mes.document.file_name

        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

        bot.reply_to(mes, "Фотографію збережено")
        log(mes, "actions photo loaded")

    except Exception as e:
        bot.reply_to(mes, e)
        bot.send_message(mes.from_user.id, "Загрузіть фото як файл, а не зображення")


def n_notif(mes):
    const.notification = mes.text
    bot.send_message(mes.from_user.id, "Текст нагадування змінено")
    log(mes, "notification changed")


def change_pass(mes):
    if mes.from_user.id == const.mainId:
        const.code = mes.text
        bot.send_message(mes.from_user.id, "Пароль змінено")
        log(mes, "PASSWORD CHANGED!!!")
    else:
        bot.send_message(mes.from_user.id, "Пароль може змінювати лише головний користувач."
                                           "Якщо у нього немає можливости, то для його зміни"
                                           "зверніться до інструкції")


# ----------------------------------------------------------------------------------------------------------------
# bot functions


@bot.message_handler(content_types=['text'])
def handle_text(mes):

    if mes.text == "\u274c":  # hide keyboard
        hide_markup = telebot.types.ReplyKeyboardRemove()
        bot.send_message(mes.from_user.id, 'Щоб знову показати клавіатуру напишіть: /keyboard',
                         reply_markup=hide_markup)

    elif mes.text == "Найближчі події":  # upcoming events
        all_f_in_d = os.listdir(const.dirP)
        if len(all_f_in_d) > 0:  # if directory with photos has any files
            for file in all_f_in_d:

                if ".jpg" in file or ".png" in file or ".jpeg" in file or ".gif" in file:  # send photo files
                    img = open(const.dirP + "/" + file, "rb")
                    bot.send_chat_action(mes.from_user.id, "upload_photo")
                    bot.send_photo(mes.from_user.id, img)
                    img.close()

                elif ".txt" in file:  # send description to photo from .txt file
                    descrip = open(const.dirP + "/" + file)
                    bot.send_message(mes.from_user.id, descrip.read())
                    descrip.close()

                else:  # no actions
                    bot.send_message(mes.from_user.id, "На найближчий час подій не планується")
                    log(mes, "На найближчий час подій не планується")

                log(mes, ["Analysing and sending actions info from: ", all_f_in_d])

        else:  # no actions
            bot.send_message(mes.from_user.id, "На найближчий час подій не планується")
            log(mes, "На найближчий час подій не планується")

    elif mes.text == "Театральний клас":
        info = open(const.dirInfo, "r")
        info = str(info.read())

        bot.send_message(mes.from_user.id, info)
        bot.send_location(mes.from_user.id, const.lat, const.long)
        log(mes, "send location")

    elif mes.text == "Замовити квитки":  # buy tickets
        bot.send_message(mes.from_user.id, 'Щоб замовити квитки напішіть або натисніть: /tickets')
        log(mes, "tickets buy")

# ----------------------------------------------------------------------------------------------------------------


bot.polling(none_stop=True, interval=0)

input()

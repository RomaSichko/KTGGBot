# -*- coding: utf-8 -*-

from threading import Timer
from time import sleep, time
# from typing_extensions import runtime
import telebot
import changePass
import os
import codecs
from datetime import datetime
from telebot import types
import json


bot = telebot.TeleBot("")

global img_id
img_id = 0

global user_base_reset
user_base_reset = {}

global teacher_base_reset
teacher_base_reset = {}

global base_message
base_message = {}

global teacher_message
teacher_message = {}

global teacher_call
teacher_call = {}

admin_base = {}


def delete_contact(msg):
    bot.delete_message(msg.chat.id, msg.id)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    log = codecs.open("log.txt", "a", 'utf-8')
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton('Правила', callback_data='rules'),
        telebot.types.InlineKeyboardButton('FAQ', callback_data='but-faq')
    )
    keyboard.row(
        telebot.types.InlineKeyboardButton('Скинути пароль', callback_data='reset-pass'),
        telebot.types.InlineKeyboardButton('Для викладачів', callback_data='teacher')
    )
    keyboard.row(
        telebot.types.InlineKeyboardButton('Написати адміністратору', callback_data='message-admin')
    )
    keyboard.row(
        telebot.types.InlineKeyboardButton('Адміністратори онлайн', callback_data='admin-online')
     )
    bot.send_message(message.chat.id, "Привіт, я КТГГ-бот, допоможу Вам в роботі з MS Teams." + '\n' + "Оберіть потрібний пункт меню для продовження роботи",reply_markup = keyboard)
    log.write('[' + str(datetime.now()) + ']' + " ID: " + str(message.chat.id) + ' action:' + message.text + ' \n')
    log.close()

@bot.message_handler(commands=['menu'])
def main_menu(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton('Правила', callback_data='rules'),
        telebot.types.InlineKeyboardButton('FAQ', callback_data='but-faq')
    )
    keyboard.row(
        telebot.types.InlineKeyboardButton('Скинути пароль', callback_data='reset-pass'),
        telebot.types.InlineKeyboardButton('Для викладачів', callback_data='teacher')
    )
    keyboard.row(
        telebot.types.InlineKeyboardButton('Написати адміністратору', callback_data='message-admin')
    )
    keyboard.row(
        telebot.types.InlineKeyboardButton('Адміністратори онлайн', callback_data='admin-online')
     )

    bot.send_message(message.chat.id, "Оберіть подальшу дію", reply_markup=keyboard)

    log = codecs.open("log.txt", "a", 'utf-8')
    log.write('[' + str(datetime.now()) + ']' + " ID: " + str(message.chat.id) + ' action:' + message.text + ' \n')
    log.close()

# @bot.message_handler(commands=['help'])
# def help_command(message):
#     keyboard = telebot.types.InlineKeyboardMarkup()
#     keyboard.row(
#         telebot.types.InlineKeyboardButton('Повернутися до меню', callback_data='but-menu')
#     )
#     bot.send_message(message.chat.id, "Щоб змінити пароль відправ фото дійсного студентського квитка")
#     bot.send_message(message.chat.id, "Якщо у вас виникли проблеми зі зміною пароля, введіть команду '/admin' та напишіть звернення до адміністратора. Ваш запит відразу буде надіслано адміністратору")
#     bot.send_message(message.chat.id, "Правильне використання команди '/admin [твоє повідомлення]', не використовуйте команду '/admin' без повідомлення")
#     bot.send_message(message.chat.id, "Основні правила користуваня: " + "\n" +  "1. Не спамити боту, у випадку спаму ваш акаунт буде заблокований." + "\n" + "2. Всі дані (особовий id, час відправлення та запит) зберігаються в базі, тому не рекомендовано використовувати нецензурну лексику та тому подібні речі." +  "\n" + "3. У випадку зміни не свого пароля (не стосується людей, у яких однакові ім'я та прізвище), ваш запит буде відправлено куратору з переліком даних запиту", reply_markup=keyboard)

# @bot.message_handler(commands=['admin'])
# def admin_send(message):
#     file = codecs.open("messages.txt", "a", 'utf-8')
#     a = str(message.text).split()
#     if len(a) != 1:
#         bot.send_message(message.chat.id, "Ваше повідомлення надіслане адміністратору, будь ласка, зачекайте на відповідь")
#         bot.send_message(684828985, " ".join(message.text.split()[1:]) + "\n" + "id:" + str(message.chat.id))
#         file.write(str(datetime.now()) + "\n" + "id: " + str(message.chat.id) + "\n" + "username: " + str(message.chat.username) + "\n" + message.text + "\n" + "==========================" + "\n")
#     else:
#         bot.send_message(message.chat.id, "Неправильне використання команди")
#     file.close()

@bot.message_handler(content_types=['photo'])
def photo(message):
    global user_base_reset
    if message.chat.id in user_base_reset and user_base_reset[message.chat.id] and user_base_reset[message.chat.id]["stud"]:
        markup = types.ReplyKeyboardRemove(selective=False)

        file = codecs.open("pass.txt", "a", 'utf-8')

        bot.send_message(message.chat.id, "Зачекайте деякий час. Перевіряю ваші дані", reply_markup=markup)
        global img_id

        fileID = message.photo[-1].file_id
        file_info = bot.get_file(fileID)
        downloaded_file = bot.download_file(file_info.file_path)

        uphoto = "image" + str(message.chat.id) + ".jpg"

        with open(uphoto, 'wb') as new_file:
            new_file.write(downloaded_file)
        check_true = changePass.resetPass("image" + str(message.chat.id) + ".jpg")

        if check_true[0] == True:
            bot.send_message(message.chat.id, "Дані знайдено. Генерую тимчасовий пароль")
            msg = bot.send_message(message.chat.id,"Ваш логін: " + check_true[2] + "\n" + "Ваш тимчасовий пароль: " + check_true[1] + "\n" + "При вході змінюєте пароль на свій, який в подальшому буде використовуватися для входу")

            main_menu(msg)

            file.write(str(datetime.now()) + "\n" + "id: " + str(message.chat.id) + "\n" + "username: " + str(message.chat.username) + "\n" + "Ваш логін: " + check_true[2] + "\n" + "При вході змінюєте пароль на свій, який в подальшому буде використовуватися для входу" + "\n" + "==========================" + "\n")
        
        else:
            keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1, resize_keyboard=1)
            item = types.KeyboardButton("Відмінити")
            keyboard.row(item)

            bot.send_message(message.chat.id,"Вибачте, ваші дані в базі не знайдено, спробуйте відправити інше фото", reply_markup=keyboard)

            file.write(str(datetime.now()) + "\n" + "id: " + str(message.chat.id) + "\n" + "username: " + str(message.chat.username) + "\n" + "Вибачте, ваші дані в базі не знайдено, спробуйте відправити інше фото" + "\n" + "==========================" + "\n")
        
        file.close()
        try:
            os.remove(uphoto)
        except FileNotFoundError:
            pass
        img_id += 1

        log = codecs.open("log.txt", "a", 'utf-8')
        log.write('[' + str(datetime.now()) + ']' + " ID: " + str(message.chat.id) + ' action: photo' + ' \n')
        log.close()
    else:
        bot.send_message(message.chat.id, "Невідома дія")
    
# @bot.message_handler(commands=['resend_admin'])
# def resend_message(message):
#     m = message.text.split()
#     bot.send_message(int(m[1]), " ".join(m[2:]))

# @bot.message_handler(commands=['reset_admin'])
# def resend_message(message):
#     m = message.text.split()
#     if len(m) == 5:
#         if m[1] == "72847@a72847":
#             newpass = changePass.resetPass_bot(m[2], m[3], m[4])
#             bot.send_message(message.chat.id,"Логін: " + newpass[2] + "\n" + "Тимчасовий пароль: " + newpass[1] + "\n" + "При вході змінюєте пароль на свій, який в подальшому буде використовуватися для входу")
#         else:
#             bot.send_message(message.chat.id,"Невірні дані")
#     else:
#         bot.send_message(message.chat.id,"Невірні дані")

# @bot.message_handler(commands=['faq'])
# def resend_message(message):
#     keyboard = telebot.types.InlineKeyboardMarkup()
#     keyboard.row(
#         telebot.types.InlineKeyboardButton('Повернутися до меню', callback_data='but-menu')
#     )
#     bot.send_message(message.chat.id, "1. Я не можу зайти, моя пошта ...@gmail.com (ukr.net,...)" + "\n" + "Відповідь: кожному студенту створено обліковий запис типу ...@kdktgg.onmicrosoft.com або ...@ktgg.kiev.ua, тільки під цим записом ви можете користуватися MS Teams")
#     bot.send_message(message.chat.id, "2. Пароль невірний, я ввожу той що мені дав куратор" + "\n" + "Відповідь: при першому вході в свій акаунт ВСІ змінюють пароль на будь-який свій, тому при подальшому вході потрібно використовувати саме його")
#     bot.send_message(message.chat.id, "3. Я не бачу груп у себе" + "\n" + "Відповідь: уважно перевірте чи зайши ви під акаунтом, що вам надали, якщо ні, то перезайдіть, так - зверніться до адміністратора (/admin [повідомлення])")
#     bot.send_message(message.chat.id, "4. Я не бачу занять у календарі" + "\n" + "Відповідь: уважно перевірте чи зайши ви під акаунтом, що вам надали, якщо ні, то перезайдіть, якщо вас додали пізніше, то заняття створені раніше в календарі не відображаються, підключатися до них можна через 'Команди'")
#     bot.send_message(message.chat.id, "5. При вході просить ввести код" + "\n" + "Відповідь: перевірте правильність введення логіну", reply_markup=keyboard)


@bot.message_handler(commands=['admin_panel'])
def admin_panel(message):
    global admin_base

    if message.chat.id not in admin_base:
    
        bot.send_message(message.chat.id, "Введіть пароль")

        
        admin_base.update({message.chat.id:{}})
        admin_base[message.chat.id].update({"user":message.chat.id, "verify": False})

        print(admin_base)


    elif admin_base[message.chat.id]["verify"]:

        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton('Скинути пароль по id', callback_data='admin-id'),
            telebot.types.InlineKeyboardButton('Скинути пароль ПІБ', callback_data='admin-pib')
        )
        keyboard.row(
            telebot.types.InlineKeyboardButton('Відправити повідомлення', callback_data='admin-send'),
            telebot.types.InlineKeyboardButton('Видалити користувача', callback_data='admin-delete')
        )
        # keyboard.row(
        #     telebot.types.InlineKeyboardButton('Картриджі', callback_data='admin-cart')
        # )
        keyboard.row(
            telebot.types.InlineKeyboardButton('Вийти', callback_data='admin-quit')
        )

        bot.send_message(message.chat.id, "Оберіть дію", reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "Введіть пароль")

    log = codecs.open("log.txt", "a", 'utf-8')
    log.write('[' + str(datetime.now()) + ']' + " ID: " + str(message.chat.id) + ' action:' + message.text + ' \n')
    log.close()
    
@bot.message_handler(commands=['setstatus'])
def status(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1, resize_keyboard=1)
    keyboard.row(
        types.KeyboardButton("🔴"),
        types.KeyboardButton('🟠'),
        types.KeyboardButton("🟡"),
        types.KeyboardButton("🟢")
    )

    base = json.load(codecs.open("admin.json", 'r', 'utf-8-sig'))

    for i in base:
        if i['id'] == message.chat.id:
            bot.send_message(message.chat.id, "Оберіть один із статусів" + '\n' + '🔴 - зайнятий' + '\n' + '🟠 - не активний' + '\n' + '🟡 - на парі' + '\n' + '🟢 - вільний', reply_markup=keyboard)
            i['islog'] = True

    with open('admin.json', 'w') as file:
        json.dump(base, file)

    log = codecs.open("log.txt", "a", 'utf-8')
    log.write('[' + str(datetime.now()) + ']' + " ID: " + str(message.chat.id) + ' action:' + message.text + ' \n')
    log.close()

# @bot.message_handler(commands=['reset'])
# def exchange_command(message):
#     keyboard = telebot.types.InlineKeyboardMarkup()
#     keyboard.row(
#         telebot.types.InlineKeyboardButton('Студентський квиток', callback_data='get-stud'),
#         telebot.types.InlineKeyboardButton('ID карта', callback_data='get-idcard')
#     )

#     bot.send_message(message.chat.id, 'Оберіть тип верифікації: ', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True) 
def callback_worker(call):
    global user_base_reset
    global base_message
    global teacher_message
    global teacher_call

    if call.data == "get-stud":
        keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1, resize_keyboard=1)
        item = types.KeyboardButton("Відмінити")
        keyboard.row(item)
        bot.send_message(call.message.chat.id, "Відправте фото ДІЙСНОГО студентського квитка для отримання тимчасового пароля", reply_markup=keyboard)
        bot.delete_message(call.message.chat.id, call.message.id)
        # bot.edit_message_text("Відправте фото ДІЙСНОГО студентського квитка для отмимання тимчасового пароля", call.message.chat.id, call.message.id, reply_markup=keyboard)
        user_base_reset.update({call.message.chat.id:{}})
        user_base_reset[call.message.chat.id].update({"stud":1})

    elif call.data == "get-idcard":
        keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1, resize_keyboard=1)
        item = types.KeyboardButton("Відмінити")
        keyboard.row(item)
        user_base_reset.update({call.message.chat.id:{}})
        user_base_reset[call.message.chat.id].update({"idcard":1})

        bot.send_message(call.message.chat.id, "Для верифікації через ID картку, відправте ПІБ та останні чотири цифри номера паспорта" + '\n' + "Повідомлення повинно бути типу: Шевченко Тарас Григорович 0000. На всі інші типи повідомлень бот реагувати не буде", reply_markup=keyboard)
        bot.delete_message(call.message.chat.id, call.message.id)

    elif call.data == "rules":
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton('Повернутися до меню', callback_data='but-menu')
        )
        text = 'Основні правила користуваня:' + '\n' + "1. Не спамити боту, у випадку спаму ваш акаунт буде заблокований." + '\n' + '2. Надсилати лише фото студентського квитка. Надсилати фото можна з будь якого ракурсу, головне, щоб фото мало достатнє освітлення' + '\n' + '3. Фото студентського квитка з додатку Дія не приймаються, бот буде видавати помилку' + '\n' + "4. Обов'язковою умовою скидання пароля є ідентичність ПІБ в документі та MS Teams, у випадку, якщо ПІБ не співпадає, зверніться до адміністратора для зміни ПІБ" + '\n' + '\n' + 'Конфіденційність наданої інформації:' + '\n' + '1. Надсилаючи дані боту, ви надаєте згоду на обробку персональних даних.' + '\n' + '1.1. До персональних даних належать: ПІБ, Telegram User ID, Telegram Username, дані студентського квитка, дані документів (номер та серія).' + '\n' + '2. Зберігання та використання даних:' + '\n' + '2.1. Дані зберігаються на внутрішньому сервері з закритим доступом лише для адміністраторів. Фото студентського квитка зберігаються на час обробки інформації, після обробки даних фото видаляється.' + '\n' + '2.2. Дані зміненого пароля зберігаються в базі з метою контролю роботи бота та не зберігають конфіденційної інформації (пароля). Зберігаються час скидання пароля, Telegram User ID, Telegram Username, логін для MS Teams та повідомлення про успіх/помилку скидання пароля.' + '\n' + "2.3. Дані надісланого повідомлення до адміністратора зберігаються з метою зворотнього звязку з користувачем, до даних, що зберігаються належать: час надсилання повідомлення, Telegram User ID, Telegram Username та текст повідомлення." + '\n' + '2.4. Право на використання збережених даних мають лише адміністратори MS Teams КТГГ та адміністратори Telegram бота.' + '\n' + '3. Доступ до даних можуть отримати посторонні особи лише при визначених обставинах: скарги на користувача (зміна пароля іншого користувача, образа адміністраторів та користувачів Telegram бота), дії, які блокують роботу бота.' + '\n' + '4. Логування запитів.' + '\n' + '4.1. Логування даних проводиться з метою контролю роботи бота та виявлення помилок роботи.' + '\n' + '4.2. До даних, які зберігаються належать: дії, які виконуть користувачі, час дії, Telegram User ID'
        
        bot.edit_message_text(text, call.message.chat.id, call.message.id, reply_markup=keyboard)
        
    elif call.data == "but-faq":
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton('Повернутися до меню', callback_data='but-menu')
        )

        text = "1. Я не можу зайти, моя пошта ...@gmail.com (ukr.net,...)" + "\n" + "Відповідь: кожному студенту створено обліковий запис типу ...@kdktgg.onmicrosoft.com або ...@ktgg.kiev.ua, тільки під цим записом ви можете користуватися MS Teams" + '\n' + "2. Пароль невірний, я ввожу той що мені дав куратор" + "\n" + "Відповідь: при першому вході в свій акаунт ВСІ змінюють пароль на будь-який свій, тому при подальшому вході потрібно використовувати саме його" + '\n' + "3. Я не бачу груп у себе" + "\n" + "Відповідь: уважно перевірте чи зайши ви під акаунтом, що вам надали, якщо ні, то перезайдіть, так - зверніться до адміністратора" + '\n' + "4. Я не бачу занять у календарі" + "\n" + "Відповідь: уважно перевірте чи зайши ви під акаунтом, що вам надали, якщо ні, то перезайдіть, якщо вас додали пізніше, то заняття створені раніше в календарі не відображаються, підключатися до них можна через 'Команди'" + '\n' + '5. У мене залишився розклад минулого року' + '\n' + 'Відповідь: ви можете його видалити через \'Календар\''

        bot.edit_message_text(text, call.message.chat.id, call.message.id, reply_markup=keyboard)
    elif call.data == "reset-pass":
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton('Студентський квиток', callback_data='get-stud'),
            telebot.types.InlineKeyboardButton('ID карта', callback_data='get-idcard')
        )
        keyboard.row(
            telebot.types.InlineKeyboardButton('Повернутися до меню', callback_data='but-menu')
        )
        text = "Оберіть тип верифікації:"

        bot.edit_message_text(text, call.message.chat.id, call.message.id, reply_markup=keyboard)
    elif call.data == "but-menu":
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton('Правила', callback_data='rules'),
            telebot.types.InlineKeyboardButton('FAQ', callback_data='but-faq')
        )
        keyboard.row(
            telebot.types.InlineKeyboardButton('Скинути пароль', callback_data='reset-pass'),
            telebot.types.InlineKeyboardButton('Для викладачів', callback_data='teacher')
        )
        keyboard.row(
            telebot.types.InlineKeyboardButton('Написати адміністратору', callback_data='message-admin')
        )
        keyboard.row(
            telebot.types.InlineKeyboardButton('Адміністратори онлайн', callback_data='admin-online')
        )
        text = "Оберіть потрібну дію:"

        bot.edit_message_text(text, call.message.chat.id, call.message.id, reply_markup=keyboard)
        try:
            del(user_base_reset[call.message.chat.id])
        except KeyError:
            pass

    elif call.data == "message-admin":
        
        keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1, resize_keyboard=1)
        item = types.KeyboardButton("Відмінити")
        keyboard.row(item)
        bot.send_message(call.message.chat.id, "Відправте повідомлення або відмініть дію", reply_markup=keyboard)
        bot.delete_message(call.message.chat.id, call.message.id)
        # bot.edit_message_text("Відправте фото ДІЙСНОГО студентського квитка для отмимання тимчасового пароля", call.message.chat.id, call.message.id, reply_markup=keyboard)
        base_message.update({call.message.chat.id:{}})
        base_message[call.message.chat.id].update({"message":True})

    elif call.data == 'admin-online':
        base = json.load(codecs.open("admin.json", 'r', 'utf-8-sig'))
        baseStatus = {'🔴':'зайнятий', '🟠': 'не активний', '🟡': 'на парі', '🟢': 'вільний'}
        messageText = ''
        for i in base:
            if i['id'] == 684828985:
                messageText += 'Рома Січко: ' + i['status'] + ' - ' + baseStatus[i['status']] + '\n'
            if i['id'] == 461655305:
                messageText += 'Богдана Сергієнко: ' + i['status'] + ' - ' + baseStatus[i['status']] + '\n'
            if i['id'] == 365794368:
                messageText += 'Нікіта Папірний: ' + i['status'] + ' - ' + baseStatus[i['status']] + '\n'

        bot.delete_message(call.message.chat.id, call.message.id)
        msg = bot.send_message(call.message.chat.id, messageText)


        main_menu(msg)


    elif call.data == 'teacher':
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton('Скинути пароль', callback_data='teacher-reset')
        )
        keyboard.row(
            telebot.types.InlineKeyboardButton('Дзвінок адміністратору', callback_data='teacher-call'),
            telebot.types.InlineKeyboardButton('Повідомлення адміністратору', callback_data='teacher-message')
        )
        keyboard.row(
            telebot.types.InlineKeyboardButton('Повернутися до меню', callback_data='but-menu')
        )

        text = "Оберіть потрібну дію:"

        bot.edit_message_text(text, call.message.chat.id, call.message.id, reply_markup=keyboard)

    elif call.data == "teacher-reset":
        keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1, resize_keyboard=1)
        item = types.KeyboardButton("Відмінити")
        keyboard.row(item)
        teacher_base_reset.update({call.message.chat.id:{}})
        teacher_base_reset[call.message.chat.id].update({"id":1})

        bot.send_message(call.message.chat.id, "Для верифікації відправте прізвище, ім\'я, по батькові та особовий ID. Наприклад: Антонов Антон Антонович 123456", reply_markup=keyboard)

    elif call.data == 'teacher-message':
        keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1, resize_keyboard=1)
        item = types.KeyboardButton("Відмінити")
        keyboard.row(item)

        bot.send_message(call.message.chat.id, "Введіть особовий ID та ПІБ", reply_markup=keyboard)
        bot.delete_message(call.message.chat.id, call.message.id)

        teacher_message.update({call.message.chat.id: {}})
        teacher_message[call.message.chat.id].update({"isLog": False})

    elif call.data == 'teacher-call':
        keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1, resize_keyboard=1)
        item = types.KeyboardButton("Відмінити")
        keyboard.row(item)

        bot.send_message(call.message.chat.id, "Введіть особовий ID та ПІБ", reply_markup=keyboard)
        bot.delete_message(call.message.chat.id, call.message.id)

        teacher_call.update({call.message.chat.id: {}})
        teacher_call[call.message.chat.id].update({"isLog": False})



    elif call.data == "admin-quit":
        if call.message.chat.id in admin_base:
            bot.send_message(call.message.chat.id, "Ви покинули адмін панель. Щоб знову зайти напишіть команду")
            del(admin_base[call.message.chat.id])
        else:
            bot.send_message(call.message.chat.id, "Ви не були в адмін панелі")

    
    elif call.data == "admin-id":
        if call.message.chat.id in admin_base:
            bot.send_message(call.message.chat.id, "ID")
            admin_base[call.message.chat.id]["id"] = True
            admin_base[call.message.chat.id]["pib"] = False
            admin_base[call.message.chat.id]["id-message"] = False
            admin_base[call.message.chat.id]["delete"] = False
        else:
            bot.send_message(call.message.chat.id, "Не верифіковано")

    elif call.data == "admin-pib":
        if call.message.chat.id in admin_base:
            bot.send_message(call.message.chat.id, "Ім'я, прізвище")
            admin_base[call.message.chat.id]["pib"] = True
            admin_base[call.message.chat.id]["id"] = False
            admin_base[call.message.chat.id]["id-message"] = False
            admin_base[call.message.chat.id]["delete"] = False
        else:
            bot.send_message(call.message.chat.id, "Не верифіковано")

    elif call.data == "admin-send":
        if call.message.chat.id in admin_base:
            bot.send_message(call.message.chat.id, "ID user / message")
            admin_base[call.message.chat.id]["id-message"] = True
            admin_base[call.message.chat.id]["pib"] = False
            admin_base[call.message.chat.id]["id"] = False
            admin_base[call.message.chat.id]["delete"] = False
        else:
            bot.send_message(call.message.chat.id, "Не верифіковано")

    elif call.data == "admin-delete":
        if call.message.chat.id in admin_base:
            keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1, resize_keyboard=1)
            item = types.KeyboardButton("Завершити")
            keyboard.row(item)
            bot.send_message(call.message.chat.id, "Ім\'я, прізвище", reply_markup=keyboard)

            admin_base[call.message.chat.id]["id-message"] = False
            admin_base[call.message.chat.id]["pib"] = False
            admin_base[call.message.chat.id]["id"] = False
            admin_base[call.message.chat.id]["delete"] = True
        else:
            bot.send_message(call.message.chat.id, "Не верифіковано")
    # else: 
    #     bot.send_message(call.message.chat.id, "Не верифіковано")
    log = codecs.open("log.txt", "a", 'utf-8')
    log.write('[' + str(datetime.now()) + ']' + " ID: " + str(call.message.chat.id) + ' calldata: ' + call.data + ' \n')
    log.close()

@bot.message_handler(content_types=['text'])
def reset_idcard(message):
    global user_base_reset
    global admin_base
    global base_message
    global teacher_message

    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton('Повернутися до меню', callback_data='but-menu')
    )

    # if user_base_reset == {}:
    #     bot.send_message(message.chat.id,"Невідома команда")
    if message.text == "Відмінити":
        if message.chat.id in user_base_reset or message.chat.id in base_message or message.chat.id in teacher_message or message.chat.id in teacher_call:
            markup = types.ReplyKeyboardRemove(selective=False)
            msg = bot.send_message(message.chat.id, 'Ви повернулись до меню', reply_markup=markup)

            # bot.register_next_step_handler(msg, main_menu)

            main_menu(msg)

            if message.chat.id in user_base_reset:
                try:
                    del(user_base_reset[message.chat.id])
                except KeyError:
                    pass
            elif message.chat.id in base_message:
                try:
                    del(base_message[message.chat.id])
                except KeyError:
                    pass
            elif message.chat.id in teacher_message:
                try:
                    del(teacher_message[message.chat.id])
                except KeyError:
                    pass
            elif message.chat.id in teacher_call:
                try:
                    del(teacher_call[message.chat.id])
                except KeyError:
                    pass
        return

    elif message.text == "Завершити":
        if message.chat.id in admin_base:
            markup = types.ReplyKeyboardRemove(selective=False)
            msg = bot.send_message(message.chat.id, 'Оберіть дію', reply_markup=markup)

            admin_panel(msg)

            if "delete" in admin_base[message.chat.id] and admin_base[message.chat.id]["delete"]:
                admin_base[message.chat.id]["delete"] = False

    elif message.text == 'Завершити розмову':
        if message.chat.id in teacher_call:
            markup = types.ReplyKeyboardRemove(selective=False)
            
            if message.chat.id in teacher_call and 'msg' in teacher_call[message.chat.id]:
                for i in teacher_call[message.chat.id]['msg']:
                    bot.delete_message(message.chat.id, i)

            msg = bot.send_message(message.chat.id, 'Можете продовжити роботу', reply_markup=markup)

            # bot.register_next_step_handler(msg, main_menu)

            main_menu(msg)

            try:
                del(teacher_call[message.chat.id])

            except KeyError:
                pass

    elif message.text in '🔴🟠🟡🟢':

        markup = types.ReplyKeyboardRemove(selective=False)
        base = json.load(codecs.open("admin.json", 'r', 'utf-8-sig'))

        for i in base:
            if i['id'] == message.chat.id and i['islog'] == True:
                if message.text == '🔴':
                    i['status'] = '🔴'


                elif message.text == '🟠':
                    i['status'] = '🟠'

                elif message.text == '🟡':
                    i['status'] = '🟡'

                elif message.text == '🟢':
                    i['status'] = '🟢'

                with open('admin.json', 'w') as file:
                    json.dump(base, file)

                msg = bot.send_message(message.chat.id, 'Ваш статус змінено', reply_markup=markup)

                main_menu(msg)


    
    if message.chat.id in user_base_reset and user_base_reset[message.chat.id]:
        text = message.text.split()
        if len(text) == 4:
            check = changePass.resetPass_idcard(text[0], text[1], text[2], text[3])
            file = codecs.open("pass.txt", "a", 'utf-8')

            if check[0]:
                markup = types.ReplyKeyboardRemove(selective=False)
                bot.send_message(message.chat.id,"Дані знайдено." + '\n' + "Ваш логін: " + check[2] + "\n" + "Ваш тимчасовий пароль: " + check[1] + "\n" + "При вході змінюєте пароль на свій, який в подальшому буде використовуватися для входу", reply_markup=markup)
                bot.send_message(message.chat.id, "Продовжити роботу", reply_markup=keyboard)
                

                file.write(str(datetime.now()) + "\n" + "id: " + str(message.chat.id) + "\n" + "username: " + str(message.chat.username) + "\n" + "Ваш логін: " + check[2] + "\n" + "При вході змінюєте пароль на свій, який в подальшому буде використовуватися для входу" + "\n" + "==========================" + "\n")

                try:
                    del(user_base_reset[message.chat.id])
                except KeyError:
                    pass
            elif check[0] == False and check[1] != "":

                bot.send_message(message.chat.id, check[1])

                # try:
                #     del(user_base_reset[message.chat.id])
                # except KeyError:
                #     pass
                file.write(str(datetime.now()) + "\n" + "id: " + str(message.chat.id) + "\n" + "username: " + str(message.chat.username) + "\n" + "Вибачте, ваші дані в базі не знайдено" + "\n" + "==========================" + "\n")
    
        
            else:
                markup = types.ReplyKeyboardRemove(selective=False)

                bot.send_message(message.chat.id,"Вибачте, ваші дані в базі не знайдено, впевніться, що ви маєте акаунт в MS Teams або зверніться до адміністратора", reply_markup=markup)
                bot.send_message(message.chat.id, "Натисніть, щоб повернутися до меню", reply_markup=keyboard)
                
                try:
                    del(user_base_reset[message.chat.id])
                except KeyError:
                    pass

            file.close()
        
        else:
            bot.send_message(message.chat.id,"Невірно введені дані, спробуйте ще раз")

    elif message.chat.id in teacher_base_reset and teacher_base_reset[message.chat.id]:
        if teacher_base_reset[message.chat.id]["id"]:
            text = message.text.split()
            if len(text) == 4:
                check = changePass.resetPass_teacher(text[0], text[1], text[2], text[3])
                file = codecs.open("pass.txt", "a", 'utf-8')

                if check[0]:
                    markup = types.ReplyKeyboardRemove(selective=False)
                    bot.send_message(message.chat.id,"Дані знайдено." + '\n' + "Ваш логін: " + check[2] + "\n" + "Ваш тимчасовий пароль: " + check[1] + "\n" + "При вході змінюєте пароль на свій, який в подальшому буде використовуватися для входу", reply_markup=markup)
                    bot.send_message(message.chat.id, "Продовжити роботу", reply_markup=keyboard)
                    try:
                        del(teacher_base_reset[message.chat.id])
                    except KeyError:
                        pass

                    file.write(str(datetime.now()) + "\n" + "id: " + str(message.chat.id) + "\n" + "username: " + str(message.chat.username) + "\n" + "Ваш логін: " + check[2] + "\n" + "При вході змінюєте пароль на свій, який в подальшому буде використовуватися для входу" + "\n" + "==========================" + "\n")


                elif check[0] == False and check[1] != "":

                    bot.send_message(message.chat.id, check[1])
                    file.write(str(datetime.now()) + "\n" + "id: " + str(message.chat.id) + "\n" + "username: " + str(message.chat.username) + "\n" + "Вибачте, ваші дані в базі не знайдено" + "\n" + "==========================" + "\n")


                else:
                    markup = types.ReplyKeyboardRemove(selective=False)

                    bot.send_message(message.chat.id,"Вибачте, ваші дані в базі не знайдено, впевніться, що ви маєте акаунт в MS Teams або зверніться до адміністратора", reply_markup=markup)
                    bot.send_message(message.chat.id, "Натисніть, щоб повернутися до меню", reply_markup=keyboard)
                    try:
                        del(teacher_base_reset[message.chat.id])
                    except KeyError:
                        pass
                file.close()
            else:
                bot.send_message(message.chat.id,"Невірно введені дані, спробуйте ще раз")

    elif message.chat.id in base_message:
        if base_message[message.chat.id]["message"]:
            markup = types.ReplyKeyboardRemove(selective=False)
            bot.send_message(message.chat.id,"Повідомлення надіслано адміністратору", reply_markup=markup)
            bot.send_message(684828985,"id: " + str(message.chat.id) + '\n' + message.text)

            bot.send_message(message.chat.id, "Продовжити роботу", reply_markup=keyboard)
            try:
                del(base_message[message.chat.id])
            except KeyError:
                pass

    elif message.chat.id in admin_base:
            if admin_base[message.chat.id]["verify"] == False:
                if message.text == "13367008@id":
                    admin_base[message.chat.id]["verify"] = True
                    bot.send_message(message.chat.id,"Верифікація успішна")
                    admin_panel(message)
                else:
                    bot.send_message(message.chat.id,"Невірний пароль, верифікацію відмінено")   
            else:
                if "id" in admin_base[message.chat.id] and admin_base[message.chat.id]["id"]:
                    if '@ktgg.kiev.ua' in message.text or '@kdktgg.onmicrosoft.com' in message.text:
                        newpass = changePass.resetPass_bot(message.text)

                        bot.send_message(message.chat.id,"Логін: " + newpass[2] + "\n" + "Тимчасовий пароль: " + newpass[1] + "\n" + "При вході змінюєте пароль на свій, який в подальшому буде використовуватися для входу")

                    else:
                        bot.send_message(message.chat.id, "Невірно введені дані")

                    del(admin_base[message.chat.id]["id"])

                elif "pib" in admin_base[message.chat.id] and admin_base[message.chat.id]["pib"]:
                    text = message.text.split()
                    if len(text) == 2:
                        newpass = changePass.resetPass_bot("0", message.text.split()[0],message.text.split()[1])
                        
                        bot.send_message(message.chat.id,"Логін: " + newpass[2] + "\n" + "Тимчасовий пароль: " + newpass[1] + "\n" + "При вході змінюєте пароль на свій, який в подальшому буде використовуватися для входу")
                    else:
                        bot.send_message(message.chat.id, "Помилка введення")
                    

                    del(admin_base[message.chat.id]["pib"])
                
                elif "id-message" in admin_base[message.chat.id] and admin_base[message.chat.id]["id-message"]:
                    m = message.text.split()

                    if len(m) >= 2:

                        if m[0].isdigit():
                            bot.send_message(int(m[0]),m[1:])
                            

                        else:
                            bot.send_message(message.chat.id, "Невірно введені дані")
                    else:
                        bot.send_message(message.chat.id, "Невірно введені дані")

                    del(admin_base[message.chat.id]["id-message"])
                

                elif "delete" in admin_base[message.chat.id] and admin_base[message.chat.id]["delete"]:
                    m = message.text.split()

                    result = changePass.detete_user(m[0], m[1])

                    if result[0]:
                        bot.send_message(message.chat.id, "Користувач: " + result[2] + '\n' + "id: " + result[1] + '\n' + 'Успішно видалений')

                    else:
                        bot.send_message(message.chat.id, 'Помилка видалення: ' + m[0] + ' ' + m[1])

    elif message.chat.id in teacher_message:
        if teacher_message[message.chat.id]["isLog"] != True:
            messageText = message.text.split()
            teacherId = messageText[0]
            teacherName = ' '.join(messageText[1:])

            keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1, resize_keyboard=1)
            item = types.KeyboardButton("Відмінити")
            keyboard.row(item)

            if teacherId.isdigit() and teacherName:
                teachers = json.load(codecs.open("teacher.json", 'r', 'utf-8-sig'))

                for i in teachers:
                    # print(i)
                    if i['ID працівника'] == teacherId and i['ПІБ'] == teacherName:

                        teacher_message[message.chat.id]["isLog"] = True

                        bot.send_message(message.chat.id, "Верифікація успішна. Відправте повідомлення або відмініть дію", reply_markup=keyboard)
                        
                if teacher_message[message.chat.id]["isLog"] == False:
                    bot.send_message(message.chat.id, "Дані в базі не знайдено, повторіть введення або відмініть дію", reply_markup=keyboard)

            else:
                bot.send_message(message.chat.id, "Невірно введені дані, перевірте коректність введення", reply_markup=keyboard)

        elif teacher_message[message.chat.id]["isLog"]:
            markup = types.ReplyKeyboardRemove(selective=False)
            bot.send_message(message.chat.id, "Ваше повідомлення надіслано адміністратору, чекайте на відповідь", reply_markup=markup)

            bot.send_message(684828985,"id: " + str(message.chat.id) + '\n' + message.text)

            bot.send_message(message.chat.id, "Продовжити роботу", reply_markup=keyboard)

            try:
                del(teacher_message[message.chat.id])

            except KeyError:
                pass


    elif message.chat.id in teacher_call:
        if teacher_call[message.chat.id]["isLog"] != True:
            messageText = message.text.split()
            teacherId = messageText[0]
            teacherName = ' '.join(messageText[1:])

            keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1, resize_keyboard=1)
            item = types.KeyboardButton("Відмінити")
            keyboard.row(item)

            if teacherId.isdigit() and teacherName:
                teachers = json.load(codecs.open("teacher.json", 'r', 'utf-8-sig'))
                

                for i in teachers:
                    # print(i)
                    if i['ID працівника'] == teacherId and i['ПІБ'] == teacherName:

                        teacher_call[message.chat.id]["isLog"] = True


                        # bot.send_message(message.chat.id, "Верифікація успішна. Відправте повідомлення або відмініть дію", reply_markup=keyboard)
                        markup = types.ReplyKeyboardRemove(selective=False)
                        undocall = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1, resize_keyboard=1)
                        undocall.row(
                            types.KeyboardButton('Завершити розмову')
                        )
            
                        base = json.load(codecs.open("admin.json", 'r', 'utf-8-sig'))

                        msgIdList = []

                        for i in base:
                            if i['status'] == '🟢' and i['id'] == 684828985:
                                msg = bot.send_contact(message.chat.id, "+380990995728", 'Рома', 'Січко', timeout=5, reply_markup=markup)
                                msgIdList.append(msg.id)
                                
                            elif i['status'] == '🟢' and i['id'] == 461655305:
                                msg = bot.send_contact(message.chat.id, "+380674050260", 'Богдана', 'Сергієнко', timeout=5, reply_markup=markup)
                                msgIdList.append(msg.id)

                            elif i['status'] == '🟢' and i['id'] == 365794368:
                                msg = bot.send_contact(message.chat.id, "+380983106160", 'Нікіта', 'Папірний', timeout=5, reply_markup=markup)
                                msgIdList.append(msg.id)
                        
                        bot.send_message(message.chat.id, 'Оберіть адміністратора та зателефонуйте йому в Telegram. Після завершення натисніть "Завершити розмову" в боті', reply_markup=undocall)
                                
                        teacher_call[message.chat.id].update({'msg': msgIdList})
                        # teacher_call[message.chat.id].update({'time': datetime.now()})

                        # bot.send_message(message.chat.id, "Ваше повідомлення надіслано адміністратору, чекайте на відповідь", reply_markup=markup)

                        # bot.send_message(684828985,"id: " + str(message.chat.id) + '\n' + message.text)

                        # bot.send_message(message.chat.id, "Продовжити роботу", reply_markup=keyboard)



                        # try:
                        #     del(teacher_call[message.chat.id])

                        # except KeyError:
                        #     pass
                        
                if teacher_call[message.chat.id]["isLog"] == False:
                    bot.send_message(message.chat.id, "Дані в базі не знайдено, повторіть введення або відмініть дію", reply_markup=keyboard)

            else:
                bot.send_message(message.chat.id, "Невірно введені дані, перевірте коректність введення", reply_markup=keyboard)

        elif teacher_call[message.chat.id]["isLog"]:
            pass


    else:
        if message.chat.id == 684828985 or message.chat.id == 461655305 or message.chat.id == 365794368:
            pass
        else:
            bot.send_message(message.chat.id,"Невідома дія")
        

    log = codecs.open("log.txt", "a", 'utf-8')
    log.write('[' + str(datetime.now()) + ']' + " ID: " + str(message.chat.id) + ' action:' + message.text + ' \n')
    log.close()
    



while True:
    try:
        bot.polling(none_stop=True, interval=0)
            
    except ConnectionResetError:
        print("No conection")
        sleep(5)
    # print(1)
    


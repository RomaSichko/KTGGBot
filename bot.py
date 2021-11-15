from time import sleep
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

admin_base = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton('Правила', callback_data='rules'),
        telebot.types.InlineKeyboardButton('FAQ', callback_data='but-faq')
    )
    keyboard.row(
        telebot.types.InlineKeyboardButton('Скинути пароль', callback_data='reset-pass')
    )
    bot.send_message(message.chat.id, "Привіт, я КТГГ-бот, допоможу тобі змінити пароль від MS Teams." + '\n' + "Щоб змінити пароль відправ фото дійсного студентського квитка." + "\n" + "Правила і допомога: /help." + "\n" + "Найбільш поширені питання: /faq",reply_markup = keyboard)

@bot.message_handler(commands=['menu'])
def main_menu(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton('Правила', callback_data='rules'),
        telebot.types.InlineKeyboardButton('FAQ', callback_data='but-faq')
    )
    keyboard.row(
        telebot.types.InlineKeyboardButton('Скинути пароль', callback_data='reset-pass')
    )

    bot.send_message(message.chat.id, "Оберіть потрібну дію: ", reply_markup=keyboard)

@bot.message_handler(commands=['help'])
def help_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton('Повернутися до меню', callback_data='but-menu')
    )
    bot.send_message(message.chat.id, "Щоб змінити пароль відправ фото дійсного студентського квитка")
    bot.send_message(message.chat.id, "Якщо у вас виникли проблеми зі зміною пароля, введіть команду '/admin' та напишіть звернення до адміністратора. Ваш запит відразу буде надіслано адміністратору")
    bot.send_message(message.chat.id, "Правильне використання команди '/admin [твоє повідомлення]', не використовуйте команду '/admin' без повідомлення")
    bot.send_message(message.chat.id, "Основні правила користуваня: " + "\n" +  "1. Не спамити боту, у випадку спаму ваш акаунт буде заблокований." + "\n" + "2. Всі дані (особовий id, час відправлення та запит) зберігаються в базі, тому не рекомендовано використовувати нецензурну лексику та тому подібні речі." +  "\n" + "3. У випадку зміни не свого пароля (не стосується людей, у яких однакові ім'я та прізвище), ваш запит буде відправлено куратору з переліком даних запиту", reply_markup=keyboard)

@bot.message_handler(commands=['admin'])
def admin_send(message):
    file = codecs.open("messages.txt", "a", 'utf-8')
    a = str(message.text).split()
    if len(a) != 1:
        bot.send_message(message.chat.id, "Ваше повідомлення надіслане адміністратору, будь ласка, зачекайте на відповідь")
        bot.send_message(684828985, " ".join(message.text.split()[1:]) + "\n" + "id:" + str(message.chat.id))
        file.write(str(datetime.now()) + "\n" + "id: " + str(message.chat.id) + "\n" + "username: " + str(message.chat.username) + "\n" + message.text + "\n" + "==========================" + "\n")
    else:
        bot.send_message(message.chat.id, "Неправильне використання команди")
    file.close()

@bot.message_handler(content_types=['photo'])
def photo(message):
    file = codecs.open("pass.txt", "a", 'utf-8')

    bot.send_message(message.chat.id, "Зачекайте деякий час. Перевіряю ваші дані")
    global img_id

    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)

    uphoto = "image" + str(img_id) + ".jpg"

    with open(uphoto, 'wb') as new_file:
        new_file.write(downloaded_file)
    check_true = changePass.resetPass("image" + str(img_id) + ".jpg")

    if check_true[0] == True:
        bot.send_message(message.chat.id, "Дані знайдено. Генерую тимчасовий пароль")
        bot.send_message(message.chat.id,"Ваш логін: " + check_true[2] + "\n" + "Ваш тимчасовий пароль: " + check_true[1] + "\n" + "При вході змінюєте пароль на свій, який в подальшому буде використовуватися для входу")

        file.write(str(datetime.now()) + "\n" + "id: " + str(message.chat.id) + "\n" + "username: " + str(message.chat.username) + "\n" + "Ваш логін: " + check_true[2] + "\n" + "Ваш тимчасовий пароль: " + check_true[1] + "\n" + "При вході змінюєте пароль на свій, який в подальшому буде використовуватися для входу" + "\n" + "==========================" + "\n")
    else:
        bot.send_message(message.chat.id,"Вибачте, ваші дані в базі не знайдено, спробуйте відправити інше фото")

        file.write(str(datetime.now()) + "\n" + "id: " + str(message.chat.id) + "\n" + "username: " + str(message.chat.username) + "\n" + "Вибачте, ваші дані в базі не знайдено, спробуйте відправити інше фото" + "\n" + "==========================" + "\n")
    
    file.close()
    try:
        os.remove(uphoto)
    except FileNotFoundError:
        pass
    img_id += 1
    
@bot.message_handler(commands=['resend_admin'])
def resend_message(message):
    m = message.text.split()
    bot.send_message(int(m[1]), " ".join(m[2:]))

@bot.message_handler(commands=['reset_admin'])
def resend_message(message):
    m = message.text.split()
    if len(m) == 5:
        if m[1] == "72847@a72847":
            newpass = changePass.resetPass_bot(m[2], m[3], m[4])
            bot.send_message(message.chat.id,"Логін: " + newpass[2] + "\n" + "Тимчасовий пароль: " + newpass[1] + "\n" + "При вході змінюєте пароль на свій, який в подальшому буде використовуватися для входу")
        else:
            bot.send_message(message.chat.id,"Невірні дані")
    else:
        bot.send_message(message.chat.id,"Невірні дані")

@bot.message_handler(commands=['faq'])
def resend_message(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton('Повернутися до меню', callback_data='but-menu')
    )
    bot.send_message(message.chat.id, "1. Я не можу зайти, моя пошта ...@gmail.com (ukr.net,...)" + "\n" + "Відповідь: кожному студенту створено обліковий запис типу ...@kdktgg.onmicrosoft.com або ...@ktgg.kiev.ua, тільки під цим записом ви можете користуватися MS Teams")
    bot.send_message(message.chat.id, "2. Пароль невірний, я ввожу той що мені дав куратор" + "\n" + "Відповідь: при першому вході в свій акаунт ВСІ змінюють пароль на будь-який свій, тому при подальшому вході потрібно використовувати саме його")
    bot.send_message(message.chat.id, "3. Я не бачу груп у себе" + "\n" + "Відповідь: уважно перевірте чи зайши ви під акаунтом, що вам надали, якщо ні, то перезайдіть, так - зверніться до адміністратора (/admin [повідомлення])")
    bot.send_message(message.chat.id, "4. Я не бачу занять у календарі" + "\n" + "Відповідь: уважно перевірте чи зайши ви під акаунтом, що вам надали, якщо ні, то перезайдіть, якщо вас додали пізніше, то заняття створені раніше в календарі не відображаються, підключатися до них можна через 'Команди'")
    bot.send_message(message.chat.id, "5. При вході просить ввести код" + "\n" + "Відповідь: перевірте правильність введення логіну", reply_markup=keyboard)


@bot.message_handler(commands=['admin_panel'])
def admin_panel(message):
    global admin_base

    if message.chat.id not in admin_base:
    
        bot.send_message(message.chat.id, "Введіть пароль")

        admin_base[message.chat.id] = {"user":message.chat.id, "command":"panel", "verify":False, "cartridge":{"all":False, "refilled":False, "unfilled":False, "refueled":False}}

        print(admin_base)


    elif admin_base[message.chat.id]["verify"]:

        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton('Скинути пароль по id', callback_data='admin-id'),
            telebot.types.InlineKeyboardButton('Скинути пароль ПІБ', callback_data='admin-pib')
        )
        keyboard.row(
            telebot.types.InlineKeyboardButton('Відправити повідомлення', callback_data='admin-send'),
            telebot.types.InlineKeyboardButton('Вийти', callback_data='admin-quit')
        )
        # keyboard.row(
        #     telebot.types.InlineKeyboardButton('Картриджі', callback_data='admin-cart')
        # )

        bot.send_message(message.chat.id, "Оберіть дію", reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "Введіть пароль")
    


@bot.message_handler(commands=['reset'])
def exchange_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton('Студентський квиток', callback_data='get-stud'),
        telebot.types.InlineKeyboardButton('ID карта', callback_data='get-idcard')
    )

    bot.send_message(message.chat.id, 'Оберіть тип верифікації: ', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True) 
def callback_worker(call):
    global user_base_reset

    if call.data == "get-stud":
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton('Повернутися до меню', callback_data='but-menu')
        )
        bot.send_message(call.message.chat.id, "Відправте фото ДІЙСНОГО студентського квитка для отмимання тимчасового пароля", reply_markup=keyboard)
    elif call.data == "get-idcard":
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton('Повернутися до меню', callback_data='but-menu')
        )
        bot.send_message(call.message.chat.id, "Для верифікації через ID картку, відправте ПІБ та останні чотира цифри номера паспорта")
        bot.send_message(call.message.chat.id, "Повідомлення повинно бути типу: Шевченко Тарас Григорович 0000. На всі інші типи повідомлень бот реагувати не буде", reply_markup=keyboard)
        user_base_reset[call.message.chat.id] = {"idcard":1}
    elif call.data == "rules":
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton('Повернутися до меню', callback_data='but-menu')
        )
        bot.send_message(call.message.chat.id, "Щоб змінити пароль відправ фото дійсного студентського квитка")
        bot.send_message(call.message.chat.id, "Якщо у вас виникли проблеми зі зміною пароля, введіть команду '/admin' та напишіть звернення до адміністратора. Ваш запит відразу буде надіслано адміністратору")
        bot.send_message(call.message.chat.id, "Правильне використання команди '/admin [твоє повідомлення]', не використовуйте команду '/admin' без повідомлення")
        bot.send_message(call.message.chat.id, "Основні правила користуваня: " + "\n" +  "1. Не спамити боту, у випадку спаму ваш акаунт буде заблокований." + "\n" + "2. Всі дані (особовий id, час відправлення та запит) зберігаються в базі, тому не рекомендовано використовувати нецензурну лексику та тому подібні речі." +  "\n" + "3. У випадку зміни не свого пароля (не стосується людей, у яких однакові ім'я та прізвище), ваш запит буде відправлено куратору з переліком даних запиту", reply_markup=keyboard)
    elif call.data == "but-faq":
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton('Повернутися до меню', callback_data='but-menu')
        )
        bot.send_message(call.message.chat.id, "1. Я не можу зайти, моя пошта ...@gmail.com (ukr.net,...)" + "\n" + "Відповідь: кожному студенту створено обліковий запис типу ...@kdktgg.onmicrosoft.com або ...@ktgg.kiev.ua, тільки під цим записом ви можете користуватися MS Teams")
        bot.send_message(call.message.chat.id, "2. Пароль невірний, я ввожу той що мені дав куратор" + "\n" + "Відповідь: при першому вході в свій акаунт ВСІ змінюють пароль на будь-який свій, тому при подальшому вході потрібно використовувати саме його")
        bot.send_message(call.message.chat.id, "3. Я не бачу груп у себе" + "\n" + "Відповідь: уважно перевірте чи зайши ви під акаунтом, що вам надали, якщо ні, то перезайдіть, так - зверніться до адміністратора (/admin [повідомлення])")
        bot.send_message(call.message.chat.id, "4. Я не бачу занять у календарі" + "\n" + "Відповідь: уважно перевірте чи зайши ви під акаунтом, що вам надали, якщо ні, то перезайдіть, якщо вас додали пізніше, то заняття створені раніше в календарі не відображаються, підключатися до них можна через 'Команди'")
        bot.send_message(call.message.chat.id, "5. При вході просить ввести код" + "\n" + "Відповідь: перевірте правильність введення логіну", reply_markup=keyboard)
    elif call.data == "reset-pass":
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton('Студентський квиток', callback_data='get-stud'),
            telebot.types.InlineKeyboardButton('ID карта', callback_data='get-idcard')
        )
        keyboard.row(
            telebot.types.InlineKeyboardButton('Повернутися до меню', callback_data='but-menu')
        )

        bot.send_message(call.message.chat.id, 'Оберіть тип верифікації: ', reply_markup=keyboard)
    elif call.data == "but-menu":
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton('Правила', callback_data='rules'),
            telebot.types.InlineKeyboardButton('FAQ', callback_data='but-faq')
        )
        keyboard.row(
            telebot.types.InlineKeyboardButton('Скинути пароль', callback_data='reset-pass')
        )

        bot.send_message(call.message.chat.id, "Оберіть потрібну дію: ", reply_markup=keyboard)
        try:
            del(user_base_reset[call.message.chat.id])
        except KeyError:
            pass

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
        else:
            bot.send_message(call.message.chat.id, "Не верифіковано")

    elif call.data == "admin-pib":
        if call.message.chat.id in admin_base:
            bot.send_message(call.message.chat.id, "Ім'я, прізвище")
            admin_base[call.message.chat.id]["pib"] = True
            admin_base[call.message.chat.id]["id"] = False
            admin_base[call.message.chat.id]["id-message"] = False
        else:
            bot.send_message(call.message.chat.id, "Не верифіковано")

    elif call.data == "admin-send":
        if call.message.chat.id in admin_base:
            bot.send_message(call.message.chat.id, "ID user / message")
            admin_base[call.message.chat.id]["id-message"] = True
            admin_base[call.message.chat.id]["pib"] = False
            admin_base[call.message.chat.id]["id"] = False
        else:
            bot.send_message(call.message.chat.id, "Не верифіковано")

    elif call.data == "admin-cart":
        if call.message.chat.id in admin_base:
            keyboard = telebot.types.InlineKeyboardMarkup()
            keyboard.row(
                telebot.types.InlineKeyboardButton('Загальний список картриджів', callback_data='cart-all'),
                telebot.types.InlineKeyboardButton('Незаправлені', callback_data='cart-unfilled')
            )
            keyboard.row(
                telebot.types.InlineKeyboardButton('Заправлені', callback_data='cart-refilled'),
                telebot.types.InlineKeyboardButton('Віддали на заправку', callback_data='cart-refueled')
            )
            keyboard.row(
                telebot.types.InlineKeyboardButton('Скоригувати дані', callback_data='cart-reload')
            )
            bot.send_message(call.message.chat.id, "Оберіть потрібну дію:", reply_markup=keyboard)
        else:
            bot.send_message(call.message.chat.id, "Не верифіковано")

    elif call.data == "cart-all":
        if call.message.chat.id in admin_base:
            base_json = json.load(codecs.open("cartridge.json", 'r', 'utf-8-sig'))
            cart_list = []
            cart_str = ""

            keyboard = telebot.types.InlineKeyboardMarkup()
            keyboard.row(
                telebot.types.InlineKeyboardButton('Загальний список картриджів', callback_data='cart-all'),
                telebot.types.InlineKeyboardButton('Незаправлені', callback_data='cart-unfilled')
            )
            keyboard.row(
                telebot.types.InlineKeyboardButton('Заправлені', callback_data='cart-refilled'),
                telebot.types.InlineKeyboardButton('Віддали на заправку', callback_data='cart-refueled')
            )
            keyboard.row(
                telebot.types.InlineKeyboardButton('Скоригувати дані', callback_data='cart-reload')
            )

            for i in base_json:
                cart_str += "Картридж: " + i["cartridge"] + "\n" + "Всі: " + str(i["all"]) + "\n" + "Заправлені:" + str(i["refilled"]) + "\n" + "Незаправлені: " + str(i["unfilled"]) + "\n" + "Віддали на заправку: " + str(i["refueled"]) + "\n" + "=========" + "\n"
            
            bot.send_message(call.message.chat.id, cart_str, reply_markup=keyboard)

        else:
            bot.send_message(call.message.chat.id, "Не верифіковано")

    elif call.data == "cart-unfilled":
        if call.message.chat.id in admin_base:
            base_json = json.load(codecs.open("cartridge.json", 'r', 'utf-8-sig'))
            cart_list = []
            cart_str = ""

            keyboard = telebot.types.InlineKeyboardMarkup()
            keyboard.row(
                telebot.types.InlineKeyboardButton('Загальний список картриджів', callback_data='cart-all'),
                telebot.types.InlineKeyboardButton('Незаправлені', callback_data='cart-unfilled')
            )
            keyboard.row(
                telebot.types.InlineKeyboardButton('Заправлені', callback_data='cart-refilled'),
                telebot.types.InlineKeyboardButton('Віддали на заправку', callback_data='cart-refueled')
            )
            keyboard.row(
                telebot.types.InlineKeyboardButton('Скоригувати дані', callback_data='cart-reload')
            )

            for i in base_json:
                if i["unfilled"] != 0:
                    cart_str += "Картридж: " + i["cartridge"] + "\n" + "Всі: " + str(i["all"]) + "\n" + "Незаправлені: " + str(i["unfilled"]) + "\n" + "=========" + "\n"
            
            bot.send_message(call.message.chat.id, cart_str, reply_markup=keyboard)

        else:
            bot.send_message(call.message.chat.id, "Не верифіковано")

    elif call.data == "cart-refilled":
        if call.message.chat.id in admin_base:
            base_json = json.load(codecs.open("cartridge.json", 'r', 'utf-8-sig'))
            cart_list = []
            cart_str = ""

            keyboard = telebot.types.InlineKeyboardMarkup()
            keyboard.row(
                telebot.types.InlineKeyboardButton('Загальний список картриджів', callback_data='cart-all'),
                telebot.types.InlineKeyboardButton('Незаправлені', callback_data='cart-unfilled')
            )
            keyboard.row(
                telebot.types.InlineKeyboardButton('Заправлені', callback_data='cart-refilled'),
                telebot.types.InlineKeyboardButton('Віддали на заправку', callback_data='cart-refueled')
            )
            keyboard.row(
                telebot.types.InlineKeyboardButton('Скоригувати дані', callback_data='cart-reload')
            )

            for i in base_json:
                if i["refilled"] != 0:
                    cart_str += "Картридж: " + i["cartridge"] + "\n" + "Всі: " + str(i["all"]) + "\n" + "Заправлені: " + str(i["refilled"]) + "\n" + "=========" + "\n"
            
            bot.send_message(call.message.chat.id, cart_str, reply_markup=keyboard)

        else:
            bot.send_message(call.message.chat.id, "Не верифіковано")

    elif call.data == "cart-refueled":
        if call.message.chat.id in admin_base:
            base_json = json.load(codecs.open("cartridge.json", 'r', 'utf-8-sig'))
            cart_list = []
            cart_str = ""

            keyboard = telebot.types.InlineKeyboardMarkup()
            keyboard.row(
                telebot.types.InlineKeyboardButton('Загальний список картриджів', callback_data='cart-all'),
                telebot.types.InlineKeyboardButton('Незаправлені', callback_data='cart-unfilled')
            )
            keyboard.row(
                telebot.types.InlineKeyboardButton('Заправлені', callback_data='cart-refilled'),
                telebot.types.InlineKeyboardButton('Віддали на заправку', callback_data='cart-refueled')
            )
            keyboard.row(
                telebot.types.InlineKeyboardButton('Скоригувати дані', callback_data='cart-reload')
            )

            for i in base_json:
                if i["refueled"] != 0:
                    cart_str += "Картридж: " + i["cartridge"] + "\n" + "Всі: " + str(i["all"]) + "\n" + "Віддали на заправку: " + str(i["refueled"]) + "\n" + "=========" + "\n"
            
            bot.send_message(call.message.chat.id, cart_str, reply_markup=keyboard)

        else:
            bot.send_message(call.message.chat.id, "Не верифіковано")
    
    elif call.data == "cart-reload":
        if call.message.chat.id in admin_base:
            base_json = json.load(codecs.open("cartridge.json", 'r', 'utf-8-sig'))
            cart_list = []
            cart_str = ""

            keyboard = telebot.types.InlineKeyboardMarkup()
            keyboard.row(
                telebot.types.InlineKeyboardButton('Змінити загальну кількість', callback_data='cart-edit-all'),
                telebot.types.InlineKeyboardButton('Змінити незаправлені', callback_data='cart-edit-unfilled')
            )
            keyboard.row(
                telebot.types.InlineKeyboardButton('Змінити заправлені', callback_data='cart-edit-refilled'),
                telebot.types.InlineKeyboardButton('Змінити віддані', callback_data='cart-edit-refueled')
            )
            keyboard.row(
                telebot.types.InlineKeyboardButton('Перевірити дані', callback_data='cart-all')
            )

            bot.send_message(call.message.chat.id, "Оберіть дію", reply_markup=keyboard)

        else:
            bot.send_message(call.message.chat.id, "Не верифіковано")
    
    elif call.data == "cart-edit-all":
        if call.message.chat.id in admin_base:
            admin_base[call.message.chat.id]["cartridge"]["all"] = True
            admin_base[call.message.chat.id]["cartridge"]["unfilled"] = False
            admin_base[call.message.chat.id]["cartridge"]["refilled"] = False
            admin_base[call.message.chat.id]["cartridge"]["refueled"] = False

            bot.send_message(call.message.chat.id, "Введіть картридж та змінену кількіть: 728 8")

        else:
            bot.send_message(call.message.chat.id, "Не верифіковано")

    elif call.data == "cart-edit-unfilled":
        if call.message.chat.id in admin_base:
            admin_base[call.message.chat.id]["cartridge"]["all"] = False
            admin_base[call.message.chat.id]["cartridge"]["unfilled"] = True
            admin_base[call.message.chat.id]["cartridge"]["refilled"] = False
            admin_base[call.message.chat.id]["cartridge"]["refueled"] = False

            bot.send_message(call.message.chat.id, "Введіть картридж та змінену кількіть: 728 8")

        else:
            bot.send_message(call.message.chat.id, "Не верифіковано")

    elif call.data == "cart-edit-refilled":
        if call.message.chat.id in admin_base:
            admin_base[call.message.chat.id]["cartridge"]["all"] = False
            admin_base[call.message.chat.id]["cartridge"]["unfilled"] = False
            admin_base[call.message.chat.id]["cartridge"]["refilled"] = True
            admin_base[call.message.chat.id]["cartridge"]["refueled"] = False

            bot.send_message(call.message.chat.id, "Введіть картридж та змінену кількіть: 728 8")

        else:
            bot.send_message(call.message.chat.id, "Не верифіковано")

    elif call.data == "cart-edit-refueled":
        if call.message.chat.id in admin_base:
            admin_base[call.message.chat.id]["cartridge"]["all"] = False
            admin_base[call.message.chat.id]["cartridge"]["unfilled"] = False
            admin_base[call.message.chat.id]["cartridge"]["refilled"] = False
            admin_base[call.message.chat.id]["cartridge"]["refueled"] = True

            bot.send_message(call.message.chat.id, "Введіть картридж та змінену кількіть: 728 8")

        else:
            bot.send_message(call.message.chat.id, "Не верифіковано")

    # else: 
    #     bot.send_message(call.message.chat.id, "Не верифіковано")

@bot.message_handler(content_types=['text'])
def reset_idcard(message):
    global user_base_reset
    global admin_base

    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton('Повернутися до меню', callback_data='but-menu')
    )

    # if user_base_reset == {}:
    #     bot.send_message(message.chat.id,"Невідома команда")
    if message.chat.id in user_base_reset and user_base_reset[message.chat.id]:
        text = message.text.split()
        if len(text) == 4:
            check = changePass.resetPass_idcard(text[0], text[1], text[2], text[3])

            if check[0]:
                bot.send_message(message.chat.id, "Дані знайдено. Генерую тимчасовий пароль")
                bot.send_message(message.chat.id,"Ваш логін: " + check[2] + "\n" + "Ваш тимчасовий пароль: " + check[1] + "\n" + "При вході змінюєте пароль на свій, який в подальшому буде використовуватися для входу", reply_markup=keyboard)
                try:
                    del(user_base_reset[message.chat.id])
                except KeyError:
                    pass
            elif check[0] == False and check[1] != "":
                bot.send_message(message.chat.id, check[1])
                try:
                    del(user_base_reset[message.chat.id])
                except KeyError:
                    pass
            else:
                bot.send_message(message.chat.id,"Вибачте, ваші дані в базі не знайдено, впевніться, що ви маєте акаунт в MS Teams, за допомогою зверніться до адміністратора '/admin [повідомлення]'", reply_markup=keyboard)
                try:
                    del(user_base_reset[message.chat.id])
                except KeyError:
                    pass
        
        else:
            bot.send_message(message.chat.id,"Невірно введені дані, спробуйте ще раз", reply_markup=keyboard)

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
                    newpass = changePass.resetPass_bot(message.text)

                    bot.send_message(message.chat.id,"Логін: " + newpass[2] + "\n" + "Тимчасовий пароль: " + newpass[1] + "\n" + "При вході змінюєте пароль на свій, який в подальшому буде використовуватися для входу")

                    
                    del(admin_base[message.chat.id]["id"])

                elif "pib" in admin_base[message.chat.id] and admin_base[message.chat.id]["pib"]:
                    newpass = changePass.resetPass_bot("0", message.text.split()[0],message.text.split()[1])
                    
                    bot.send_message(message.chat.id,"Логін: " + newpass[2] + "\n" + "Тимчасовий пароль: " + newpass[1] + "\n" + "При вході змінюєте пароль на свій, який в подальшому буде використовуватися для входу")


                    del(admin_base[message.chat.id]["pib"])
                
                elif "id-message" in admin_base[message.chat.id] and admin_base[message.chat.id]["id-message"]:
                    m = message.text.split()

                    bot.send_message(int(m[0]),m[1:])
                    del(admin_base[message.chat.id]["id-message"])

                elif "cartridge" in admin_base[message.chat.id] and admin_base[message.chat.id]["cartridge"]["all"]:
                    m = message.text.split()
                    base_json = json.load(codecs.open("cartridge.json", 'r', 'utf-8-sig'))


                    keyboard = telebot.types.InlineKeyboardMarkup()
                    keyboard.row(
                        telebot.types.InlineKeyboardButton('Перевірити дані', callback_data='cart-all')
                    )

                    try:
                        for i in base_json:
                            if i["cartridge"] == m[0]:
                                i["all"] = int(m[1])
                    except ValueError:
                        pass
                    
                    with open("cartridge.json", 'w') as file:
                        json.dump(base_json, file)

                    bot.send_message(message.chat.id,"Дані успішно змінені", reply_markup=keyboard)

                    admin_base[message.chat.id]["cartridge"]["all"] = False
                
                elif "cartridge" in admin_base[message.chat.id] and admin_base[message.chat.id]["cartridge"]["refilled"]:
                    m = message.text.split()
                    base_json = json.load(codecs.open("cartridge.json", 'r', 'utf-8-sig'))


                    keyboard = telebot.types.InlineKeyboardMarkup()
                    keyboard.row(
                        telebot.types.InlineKeyboardButton('Перевірити дані', callback_data='cart-all')
                    )

                    try:
                        for i in base_json:
                            if i["cartridge"] == m[0]:
                                i["refilled"] = int(m[1])
                    except ValueError:
                        pass
                    
                    with open("cartridge.json", 'w') as file:
                        json.dump(base_json, file)

                    bot.send_message(message.chat.id,"Дані успішно змінені", reply_markup=keyboard)

                    admin_base[message.chat.id]["cartridge"]["refilled"] = False
                
                elif "cartridge" in admin_base[message.chat.id] and admin_base[message.chat.id]["cartridge"]["unfilled"]:
                    m = message.text.split()
                    base_json = json.load(codecs.open("cartridge.json", 'r', 'utf-8-sig'))


                    keyboard = telebot.types.InlineKeyboardMarkup()
                    keyboard.row(
                        telebot.types.InlineKeyboardButton('Перевірити дані', callback_data='cart-all')
                    )

                    try:
                        for i in base_json:
                            if i["cartridge"] == m[0]:
                                i["unfilled"] = int(m[1])
                    except ValueError:
                        pass
                    
                    with open("cartridge.json", 'w') as file:
                        json.dump(base_json, file)

                    bot.send_message(message.chat.id,"Дані успішно змінені", reply_markup=keyboard)

                    admin_base[message.chat.id]["cartridge"]["unfilled"] = False
                
                elif "cartridge" in admin_base[message.chat.id] and admin_base[message.chat.id]["cartridge"]["refueled"]:
                    m = message.text.split()
                    base_json = json.load(codecs.open("cartridge.json", 'r', 'utf-8-sig'))


                    keyboard = telebot.types.InlineKeyboardMarkup()
                    keyboard.row(
                        telebot.types.InlineKeyboardButton('Перевірити дані', callback_data='cart-all')
                    )

                    try:
                        for i in base_json:
                            if i["cartridge"] == m[0]:
                                i["refueled"] = int(m[1])
                    except ValueError:
                        pass
                    
                    with open("cartridge.json", 'w') as file:
                        json.dump(base_json, file)

                    bot.send_message(message.chat.id,"Дані успішно змінені", reply_markup=keyboard)

                    admin_base[message.chat.id]["cartridge"]["refueled"] = False
    
    
    else:
        bot.send_message(message.chat.id,"Невідома команда", reply_markup=keyboard)



try:
    bot.polling(none_stop=True, interval=0)

except ConnectionResetError:
    print("No conection")
    sleep(5)




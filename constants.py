from telebot import types


class ConstantMessages:
    START_MESSAGE = ("Привіт, я КТГГ-бот, допоможу Вам в роботі з MS Teams.\n"
                     "Оберіть потрібний пункт меню для продовження роботи")

    NEXT_ACTION = "Оберіть подальшу дію"

    ACCOUNT_DATA_TO_DB = "Ваші дані занесено до бази, перегляньте та допоповніть їх"

    WAIT_DATA_CHECK = "Зачекайте деякий час. Перевіряю ваші дані"

    DATA_FOUND = "Дані знайдено. Генерую тимчасовий пароль"

    NEW_PASSWORD = ("Ваш логін: {login}\nВаш тимчасовий пароль: {password}\n"
                    "При вході змінюєте пароль на свій, який в подальшому буде використовуватися для входу")

    PHOTO_DATA_NOT_FOUND = "Вибачте, ваші дані в базі не знайдено, спробуйте відправити інше фото"

    UNKWOWN_ACTION = "Невідома дія"

    ENTER_PASSWORD = "Введіть пароль"

    ACTION = "Оберіть дію"

    ADMIN_STATUSES = "Оберіть один із статусів\n🔴 - зайнятий\n🟠 - не активний\n🟡 - на парі\n🟢 - вільний"

    TICKET_PHOTO = "Відправте фото ДІЙСНОГО студентського квитка для отримання тимчасового пароля"

    CARD_DATA = ("Для верифікації через ID картку, відправте ПІБ та останні чотири цифри номера паспорта \n "
                 "Повідомлення повинно бути типу: Шевченко Тарас Григорович 0000.")

    RULES = ("Основні правила користуваня:\n1. Не спамити боту, у випадку спаму ваш акаунт буде заблокований.\n"
             "2. Надсилати лише фото студентського квитка. Надсилати фото можна з будь якого ракурсу, головне,"
             "щоб фото мало достатнє освітлення \n 3. Фото студентського квитка з додатку Дія не приймаються, "
             "бот буде видавати помилку \n 4. Обовязковою умовою скидання пароля є ідентичність ПІБ в документі та "
             "MS Teams, у випадку, якщо ПІБ не співпадає, зверніться до адміністратора для зміни ПІБ")

    FAQ = ("1. Я не можу зайти, моя пошта ...@gmail.com (ukr.net,...)\n"
           "Відповідь: кожному студенту створено обліковий запис типу ...@kdktgg.onmicrosoft.com або ...@ktgg.kiev.ua, "
           "тільки під цим записом ви можете користуватися MS Teams\n2. Пароль невірний, я ввожу той, що мені "
           "дав куратор\nВідповідь: при першому вході в свій акаунт ВСІ змінюють пароль на будь-який свій, тому при "
           "подальшому вході потрібно використовувати саме його\n3. Я не бачу груп у себе\nВідповідь: уважно перевірте "
           "чи зайши ви під акаунтом, що вам надали, якщо ні, то перезайдіть, так - зверніться до адміністратора\n"
           "4. Я не бачу занять у календарі\nВідповідь: уважно перевірте чи зайши ви під акаунтом, що вам надали, "
           "якщо ні, то перезайдіть, якщо вас додали пізніше, то заняття створені раніше в календарі не "
           "відображаються, підключатися до них можна через \'Команди\'\n5. У мене залишився розклад минулого року\n"
           "Відповідь: ви можете його видалити через \'Календар\'\n6. У мене немає логіна\nВідповідь: зверніться до "
           "куратора за логіном, у випадку відсутності у куратора зверніться до адміністратора\n7. Я втратив логін та "
           "пароль\nВідповідь: можете скинути пароль і отримати логін, у випадку відсутності документів, "
           "зверніться до адміністраторів")

    VERIFICATION_TYPE = "Оберіть тип верифікації:"

    SEND_MESSAGE_CANCEL = "Відправте повідомлення або відмініть дію"

    SEND_EMAIL_CANCEL = "Відправте адресу Вашої електронної пошти або відмініть дію"

    SEND_EMAIL_TEAMS_CANCEL = "Відправте логін (...@ktgg.kiev.ua або ...@kdktgg.onmicrosoft.com) або відмініть дію"

    SEND_LASTNAME_CANCEL = "Відправте Ваше прізвище"

    SEND_NAME_CANCEL = "Відправте Ваше ім\'я"

    TEACHER_ID = ("Для верифікації відправте особовий ID та прізвище, ім\'я, по батькові. "
                  "Наприклад: 123456 Антонов Антон Антонович")

    ADMIN_QUIT = "Ви покинули адмін панель. Щоб знову зайти напишіть команду"

    NO_IN_ADMIN = "Ви не були в адмін панелі"

    NO_VERIFY = "Не верифіковано"

    CANCEL = "Відмінити"

    FINISH = "Завершити"

    FINISH_CALL = "Завершити розмову"

    STATUS_CHANGE = "Ваш статус змінено"

    CARD_DATA_NOT_FOUND = ("Вибачте, ваші дані в базі не знайдено, "
                           "перевірте правильність введення даних та відправте ще раз")

    NOT_FOUND_WITHOUT_ACC = ("Вибачте, ваші дані в базі не знайдено, впевніться, "
                             "що ви маєте акаунт в MS Teams або зверніться до адміністратора")

    INVALID_DATA = "Невірно введені дані"

    MESSAGE_SENT_ADMIN = "Повідомлення надіслано адміністратору"

    SUCCESS_VERIFY = "Верифікація успішна"

    BAD_VERIFY = "Невірний пароль, верифікацію відмінено"

    MESSAGE_MARK = "Повідомлення відмічено"

    MESSAGE_FROM_ADMIN = "Відповідь адміністратора: \n{answer}"

    MESSAGE_SENT = "Повідомлення надіслано"

    ALREADY_ANSWERED = "На повідомлення уже відповіли"

    SUCCESS_DELETE = "Користувач: {user}\nid: {id}\nУспішно видалений"

    FAIL_DELETE = "Помилка видалення: {lastname} {name}"

    CALL_ADMIN = "Оберіть адміністратора та зателефонуйте йому в Telegram"

    MAIL_CONFIRM_CODE = ("На Вашу електронну пошту надісланий код підтвердження (можливо воно потрапило в спам), "
                         "надішліть його боту")

    INVALID_MAIL = "Ви ввели неіснуючу електронну пошту, надішліть правильну адресу або відмініть дію"

    MAIL_CONFIRMED = "Вашу електронну пошту підтвердженно, перегляньте Ваш акаунт"

    INVALID_CONFIRM_CODE = "Введений код невірний, спробуйте ще раз або відмініть дію"

    TEAMS_CONFIRM_CODE = ("Перейдіть за посиланням https://outlook.office.com/mail/inbox (якщо Вас просить увійти, "
                          "вводьте дані від MS Teams), у листі від no-reply@ktgg.kiev.ua вказаний код, відправте "
                          "його боту\nЯкщо виникли проблеми, можете звернутися до адміністратора @Roma_Sichko")

    INVALID_TEAMS = ("Не вдалося знайти ваш обліковий запис, перевірте правильність введення даних і "
                     "відправте ще раз або відмініть дію")

    UNREAL_MAIL = "Ви ввели неіснуючу електронну пошту, надішліть правильну адресу або відмініть дію"

    CONFIRMED_ACCOUNT = "Ваш обліковий запіс підтверджено, Вам доступні нові дії в акаунті"

    CHANGE_ACCOUNT_DATA = "Ваші дані змінено, перегляньте свій акаунт"




class Keypads:
    MAIN_MENU = types.InlineKeyboardMarkup([
        [
            types.InlineKeyboardButton('Правила', callback_data='rules'),
            types.InlineKeyboardButton('FAQ', callback_data='but-faq')],
        [
            types.InlineKeyboardButton('Скинути пароль', callback_data='reset-pass'),
            types.InlineKeyboardButton('Для працівників', callback_data='teacher')
        ],
        [
            types.InlineKeyboardButton('Написати адміністратору', callback_data='message-admin')
        ],
        [
            types.InlineKeyboardButton('Адміністратори', callback_data='admin-online')
        ]
    ])

    ACCOUNT_MENU = types.InlineKeyboardMarkup([
        [types.InlineKeyboardButton('Змінити ел. пошту', callback_data='acc-mail'),
         types.InlineKeyboardButton('Змінити MS Teams', callback_data='acc-teams')]
    ])

    CANCEL = types.ReplyKeyboardMarkup(
        one_time_keyboard=True,
        row_width=1,
        resize_keyboard=True
    ).row(types.KeyboardButton("Відмінити"))

    ADMIN_MENU = types.InlineKeyboardMarkup([[
        types.InlineKeyboardButton('Скинути пароль по id', callback_data='admin-id'),
        types.InlineKeyboardButton('Скинути пароль ПІБ', callback_data='admin-pib')
    ],
        [
            types.InlineKeyboardButton("Відправити повідомлення", callback_data='admin-send'),
            types.InlineKeyboardButton('Видалити користувача', callback_data='admin-delete')
        ],
        [
            types.InlineKeyboardButton('Add to BL', callback_data='admin-kill'),
            types.InlineKeyboardButton('Remove from BL', callback_data='admin-renewal'),
            types.InlineKeyboardButton('Вийти', callback_data='admin-quit')
        ]
    ])

    REMOVE = types.ReplyKeyboardRemove(selective=False)

    ADMIN_STATUS = types.ReplyKeyboardMarkup(
        one_time_keyboard=True,
        row_width=1,
        resize_keyboard=1
    ).row(
        types.KeyboardButton("🔴"),
        types.KeyboardButton('🟠'),
        types.KeyboardButton("🟡"),
        types.KeyboardButton("🟢")
    )

    BACK_TO_MAIN_MENU = types.InlineKeyboardMarkup(
        types.InlineKeyboardButton('Повернутися до меню', callback_data='but-menu'),
    )

    TYPE_OF_RESET = types.InlineKeyboardMarkup(
        row_width=2,
    ).add(
        types.InlineKeyboardButton('Студентський квиток', callback_data='get-stud'),
        types.InlineKeyboardButton('ID карта', callback_data='get-idcard'),
        types.InlineKeyboardButton('Повернутися до меню', callback_data='but-menu'),
    )

    TEACHER_MENU = types.InlineKeyboardMarkup(
        ([
             types.InlineKeyboardButton('Скинути пароль', callback_data='teacher-reset'),
         ],
         [
             types.InlineKeyboardButton('Дзвінок адміністратору', callback_data='teacher-call'),
             types.InlineKeyboardButton('Повідомлення адміністратору', callback_data='teacher-message'),
         ],
         [
             types.InlineKeyboardButton('Повернутися до меню', callback_data='but-menu'),
         ])
    )

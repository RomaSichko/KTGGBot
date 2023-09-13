class MessagesText:
    WELCOME = ("Привіт, я КТГГ-бот. Прочитай правила користування ботом. "
               "Попереджую, у разі порушення правил є можливість автоматичного додання до чорного списку. "
               "Обери дію, щоб продовжити роботу")

    MENU_MESSAGES = "Обери потрібну дію, не забувай, що неправильне використання може тебе заблокувати"

    ADDED_ACCOUNT_IN_DB = "Твої дані занесено до бази даних"

    MAIN_RULES = (
        "Основні правила користувача: \n"
        "1. Спам\n"
        "    1.1. Спамом вважається надсилання більше 2 повідомлень адміністратору однакового змісту.\n"
        "    1.2. За спам користувач додається до чорного списку.\n"
        "    1.3. Також спамом вважається часте натискання пунктів меню (частіше ніж раз в 1 секунду)\n"
        "2. Скидання пароля через фото студентського квитка\n"
        "    2.1. Надсилати фото студентського квитка зі сторони, де розташоване фото\n"
        "    2.2. Не надсилати інших фото\n"
        "    2.3. Скріни з додатку \'Дія\' не приймаються\n"
        "    2.4. Бот не зберігає фото довше, ніж на час обробки запиту\n"
        "3. Ідентичність даних користувача\n"
        "    3.1. Дані на платформі MS Teams повинні бути ідентичними до даних в документах\n"
        "4. Чорний список\n"
        "    4.1. Більшу частину модерації виконує бот, тому можливо, що користувач потрапить в чорний список випадково\n"
        "    4.2. У випадку потрапляння в чорний список, зверніться до адміністратора, для з\'ясування обставин\n"
        "5. Список правил може змінюватися після кожного оновлення бота"
    )

    MAIN_FAQ = (
        "1. Teams\n"
        "    1.1. Я на можу зайти в Teams, моя пошта ...@gmail.com (ukr.net,...)\n"
        "         Кожному створено обліковий запис типу ...@kdktgg.onmicrosoft.com або ...@ktgg.kiev.ua, "
        "тільки під цим записом можна користуватися MS Teams\n"
        "    1.2. Пароль невірний, я ввожу той, що мені дав куратор\n"
        "         При першому вході (або після зміни пароля) в свій акаунт ВСІ змінюють пароль на будь-який свій, "
        "тому при подальшому вході потрібно використовувати саме його\n"
        "    1.3. Я не бачу груп у себе\n"
        "         Уважно перевірте чи зайши ви під акаунтом, що вам надали, якщо ні, то перезайдіть, "
        "так - зверніться до адміністратора\n"
        "    1.4. Я не бачу занять у календарі\n"
        "         Уважно перевірте чи зайши ви під акаунтом, що вам надали, якщо ні, то перезайдіть, "
        "якщо вас додали пізніше, то заняття створені раніше в календарі не відображаються, підключатися до них можна "
        "через \'Команди\'\n"
        "    1.5. У мене залишився розклад минулого року\n"
        "         Ви можете його видалити через \'Календар\'\n"
        "    1.6. У мене немає логіна\n"
        "         Зверніться до куратора за логіном, у випадку відсутності у куратора зверніться до адміністратора\n"
        "    1.7. Я втратив логін та пароль\n"
        "         Можете скинути пароль і отримати логін, у випадку відсутності документів, зверніться до адміністраторів\n"
        "2. Bot Tasks\n"
        # TODO: Write
        "3. Oftop"
        # TODO: Write links
    )

    RESET_PASSWORD_WITHOUT_ACC_CHOICE_VERIFY_TYPE = (
        "Для зміни пароля, потрібно дізнатися твої дані будь ласка, обери тип верифікації")

    MESSAGE_TO_ADMIN = (
        "Напиши своє повідомлення та надішли його, бот постарається якнайшвидше передати його "
        "адміністраторам. Зауваж, що використовувати нецензурну лексику в повідомленні заборонено, "
        "в такому випадку акаунт може бути доданий до чорного списку. "
        "Якщо випадково перейшов(ла) сюди, відміни дію.\n*На деяку частину повідомлень може відповідати "
        "бот, але повідомлення в будь-якому разі отримають адміністратори")

    MESSAGE_TO_ADMIN_NO_TEAMS = (
        "Напиши своє повідомлення ОБОВ'ЯЗКОВО вказавши своє ПІБ та групу та надішли його, бот постарається якнайшвидше передати його "
        "адміністраторам. Зауваж, що використовувати нецензурну лексику в повідомленні заборонено, "
        "в такому випадку акаунт може бути доданий до чорного списку. "
        "Повідомлення цього типу відсилаються з більшою пріоритетністю."
        "Якщо випадково перейшов(ла) сюди, відміни дію.\n*На деяку частину повідомлень може відповідати "
        "бот, але повідомлення в будь-якому разі отримають адміністратори")

    MESSAGE_STUDENT_TICKET_RESET_TYPE = (
        "Ти обрав(ла) тип верифікації за допомогою студентького квитка. "
        "Надішли фото студентського квитка зі сторони, де знаходиться фото та штрихкод. "
        "Зауваж, що скріни з додатку \'Дія\' не є типом верифікації, бот в такому випадку буде видавати помилку"
    )

    MESSAGE_ID_CARD_RESET_TYPE = (
        "Ти обрав(ла) тип верифікації за допомогою id-картки. Надішли, будь ласка, свої дані в такому форматі:\n"
        "<Прізвище> <Ім\'я> <По батькові> <останні 4 цифри номера id-картки>\n"
        "Наприклад: Січко Роман Вікторович 0000. Зверни увагу на те, що такий спосіб верифікації можливий, "
        "якщо в тебе паспорт у формі картки"
    )

    MESSAGE_EDIT_EMAIL_ACCOUNT = (
        "Хочеш змінити свою електронну пошту? Без проблем, напиши, будь ласка, нову та відправ повідомлення, "
        "через деякий час твоя пошта зміниться. Не забувай, що потрібно підтвердити цю дію кодом з листа\n"
        "P.S. Якщо що, то там є кнопочка Відмінити"
    )

    MESSAGE_EDIT_TEAMS_ACCOUNT = (
        "Хочеш змінити акаунт MS Teams? Напиши, будь ласка, новий та відправ повідомлення, "
        "через деякий час твій MS Teams зміниться. Не забувай, що потрібно підтвердити цю дію кодом з листа\n"
        "P.S. Якщо що, то там є кнопочка Відмінити"
    )

    MESSAGE_ADD_EMAIL_ACCOUNT = (
        "Хочеш додати свою електронну пошту? Напиши, будь ласка, нову та відправ повідомлення, "
        "через деякий час твоя пошта зміниться. Не забувай, що потрібно підтвердити цю дію кодом з листа\n"
        "P.S. Якщо що, то там є кнопочка Відмінити"
    )

    MESSAGE_ADD_TEAMS_ACCOUNT = (
        "Хочеш додати акаунт MS Teams? Напиши, будь ласка, новий та відправ повідомлення, "
        "через деякий час твій MS Teams зміниться. Не забувай, що потрібно підтвердити цю дію кодом з листа\n"
        "P.S. Якщо що, то там є кнопочка Відмінити"
    )

    MESSAGE_RESET_PASSWORD_ACCOUNT = (
        "Твій пароль буде змінено найближчим часом і надішлеться в наступному повідомленні. Відмінити цю дію неможливо."
        "Пс... У нас тут є пасхалка, можна мемчики ввімкнути, а як, то вже секрет, але спробуй щось <memeees>"
    )

    MESSAGE_EDIT_DATA_ACCOUNT = (
        "Хочеш змінити свої дані? Без проблем, напиши, будь ласка, нові дані та відправ повідомлення, "
        "через деякий час вони зміниться.\nP.S.Якщо що, то там є кнопочка Відмінити"
    )

    MESSAGE_WAIT_ACTION = "Зачекай деякий час, я здійснюю перевірку даних"

    STUDENT_TICKET_NOT_FOUND = (
        "Дивно, але я не зміг найти твої дані, спробуй ще раз відправити більш якісне фото, "
        "або зміни тип верифікації"
    )

    NOT_CONFIRMED_ACTION = "Оу, ти не можеш виконати зараз цю дію, спробуй іншу"

    ADMIN_PANEL = (
        "Оооо, дааа... Хіба це не рай? Роби все що хочеш. Хоча ні, було б дуже просто... Тепер твої"
        " права визначаю я 😈. Можеш тицяти на кнопки, але якщо немає прав, то така твоя доля")

    ADMIN_PANEL_DANGER = (
        "Такс, тут небезпечно, натискай кнопки, якщо знаєш, що вони роблять, "
        "на деякі кнопки я встановив захист"
    )

    ADMIN_PANEL_DENIED = (
        "Ні ні ні... Так справа не піде, не твоя територія, не твої правила. "
        "Хоча, якщо ти все ж таки адмін, то додай собі права, це ти можеш."
    )

    ADMIN_PANEL_WITHOUT_RIGHTS = (
        "Хммм, хтось забув тобі дати права сюди, можеш піти попихати їх, "
        "або сам додай його"
    )

    ADMIN_PANEL_RESET_PASSWORD_BY_ID = (
        "Ну і хто той нещасний, пиши його айдішку (...@ktgg.kiev.ua, ...@kdktgg.onmicrosoft.com)"
    )

    ADMIN_PANEL_RESET_PASSWORD_BY_PIB = (
        "Ну і хто той нещасний, пиши його ім'я та прізвище (спочатку ім'я)"
    )

    MESSAGE_TO_ADMIN_SENDED = "✅Повідомлення надіслано адміністратору✅ \n⌛️Чекай на відповідь⌛️\n🆔 {id}"

    RESETED_PASSWORD = ("Твої облікові дані \nЛогін: {login}\nПароль: {password}\n"
                        "Нікому не передавай їх, бо це є прямим доступом до акаунту")

    FAIL_TO_RESET_PASSWORD = ("Дивно, я не зміг знайти твоїх облікових даних, "
                              "перевір правильність введення та спробуй ще раз, або відміни дію")

    ADMIN_RESET_BY_ID_WRONG_MAIL = "Якась крива пошта, спробуй ще раз"

    ADMIN_MESSAGE_SENT = "✅Повідомлення надіслано✅\n🆔 {id}"

    ADMIN_MESSAGE_ANSWER = "❗️Вам відповіли❗️\n🆔 {id}\nВідповідь адміністратора:\n{answer}"

    ADMIN_MESSAGE_ANSWERED = "На це повідомлення вже хтось відповів"

    ADMIN_MESSAGE_WRONG_MESSAGE_ID = (
        "Цього повідомлення немає в базі, впевнись, що вніс правильний номер")

    USER_ACCOUNT_MAIN = (
        "Вітаю, ти в своєму акаунті, тут можеш робити все, що захочеш. Але тільки є декілька умов. "
        "При відправці повідомлень, адміністратор буде бачити твої дані, трошки не конфіденційно, "
        "але тобі не доведеться це писати кожного разу, доречі твої дані: "
        "\nEmail: {email} \nІм\'я та прізвище: {name} \nTeams email: {teams}")

    USER_ACCOUNT_CONFIRM_CODE = (
        "На пошту {email} відправлено повідомлення з кодом, "
        "надішли цей код боту і дані будуть підтверджені. "
        "Якщо це підтвердження акаунту MS Teams, то перейди за посиланням: "
        "https://outlook.office.com/mail/inbox/ "
        "ввійди в свій акаунт MS Teams та відпав код з повідомлення"
    )

    USER_ACCOUNT_WRONG_MAIL = "Дивно, ти надіслав невірну пошту, спробуй ще раз або відміни дію"

    USER_ACCOUNT_WRONG_CONFIRM_CODE = (
        "Ти ввів невірний код, спробуй ще раз, якщо ти випадково зайшов сюди - відміни дію"
    )

    USER_ACCOUNT_EMAIL_CONFIRM = (
        "Дані підтверджено, вони будуть використовуватись за потреби в якості зв'язку"
    )

    USER_ACCOUNT_WRONG_TEAMS = "Ти надіслав невірний логін, надішли ще раз або відміни дію"

    USER_ACCOUNT_WORK = (
        "Вітаю, ти в своєму робочому акаунті, тут можеш робити все, що захочеш. Але тільки є декілька умов. "
        "При відправці повідомлень, адміністратор буде бачити твої дані, трошки не конфіденційно, "
        "але тобі не доведеться це писати кожного разу.Також рекомендую писати повідомлення "
        "відповідно до тем, адміністраторам простіше буде розподілити роботу. "
        "Також можеш створити задачу і слідкуватти за її статусом, доречі твої дані: "
        "\nEmail: {email} \nІм\'я та прізвище: {name} \nTeams email: {teams}")

    USER_ACCOUNT_WORK_NEW = (
        "Привіт, заблудша душа, що ти тут шукаєш... Окей, пропустимо цю церемонію, дивно, "
        "але ти тут вперше, мені потрібно підтвердити твою особистість. Пам'ятаєш, колись тобі "
        "давали 5-6 значний код, так ось. Тобі треба надіслати той код та ПІБ. Наприклад: "
        "1234567890 ТестПрізвище ТестІм'я ТестПоБатькові. Зауваж, порядок тут важливий. "
        "Цю процедуру потрібно зробити лише раз, думаю, це не складно"
    )

    USER_ACCOUNT_WORK_CONFIRM = (
        "Твої дані підтверджено, дані заношу до бази даних, після занесення "
        "тобі відкриється твоя панель з даними. Приємного користування"
    )

    USER_ACCOUNT_WORK_WRONG = (
        "Хммм, дивно, я тебе не бачу в своїй базі, спробуй ще раз, може десь допустив(ла) помилку. "
        "Якщо твої дані не знайшли, то попроси адміністраторів допомогти"
    )

    UNKNOWN_ACTION = "Невідома дія"

    ADMIN_DELETE_ACCOUNTS = (
        "Ти зайшов(ла) в небезпечну зону - видалення користувачів. У мене є 2 правила:\n"
        "1. Видаляти користувача можна за його поштою\n"
        "2. Видаляти користувача можна за його ім'ям та прізвищем.\n"
        "Для видалення просто пиши один із цих даних, далі бот тобі буде відповідати на "
        "повідомлення статус видалення.\n"
        "Приклади: \n"
        "\tr.sichko@kdktgg.onmicrosoft.com\n"
        "\tРоман Січко\n")

    WRONG_USER_DATA = "Якісь неправильні в тебе дані, спробуй ще раз написати"

    SUCCESS_DELETE_USER = "Користувача {name} успішно видалено"

    FAILED_DELETE_USER = "Помилка видалення користувача {name}"

    WRONG_ADMIN_MESSAGE_REPLY = (
        "Йой, я ж змінив тип відповіді на повідомлення, тепер потрібно тегати повідомлення")

    WRONG_ADMIN_STICKER = "Йой, це не відповідь на стікер"

    WRONG_MESSAGE_CHOICE = (
        "Нє, блін, ти вибрав якусь фігню, а не повідомлення, написано ж "
        "ТІЛЬКИ НА ПОВІДОМЛЕННЯ КОРИСТУВАЧІВ, бо я не буду ніфіга робити, чудо ти в лаптях")

    ADMIN_SEND_MESSAGE = (
        "Обираєш повідомлення, і відповідаєш на нього, без айді і без всякого такого. "
        "Understood? Надіюсь, що так")

    ADMIN_CALL_DELETE_GROUPS = (
        "Зараз є два вибори: видалити всі не ігноровані групи, чи відмінити дію, для "
        "підтвердження переходу відправ такий же стікер у відповідь до цього "
        "(маркни тільки, по іншому не спрацює)")

    ADMIN_STICKER_VERIFIED = ("Перевірка стікером пройдена, далі вкажи групи, які "
                              "потрібно залишити, або напиши \'all\', щоб видалити всі")

    ADMIN_STICKER_FAILED = "Та не той стікер, спробуй щей раз"

    ADMIN_DELETE_GROUPS_ERRORS = "При видаленні сталася помилка, не зміг вадилити ці групи {groups}"

    ADMIN_DELETE_GROUPS_SUCCESS = "Всі групи видалені успішно"

    ADMIN_BLACK_LIST = (
        "А тут найцікавіша частина, я б його назвав 'Місце катувань', тут всі наші грішники, "
        "та їхні грішки, видаляти грішників можна додавати по айді чи нікнейму, додавати так само, "
        "але бажано двічі не додавати, а то потім людина просто буде ігноруватися 2 рази")

    ADMIN_ADD_TO_BLACK_LIST = (
        "Напиши айді цієї людини чи нікнейм та причину додання, у тебе повинно буди повідомлення "
        "типу:\n1234567890 Спамив інтимними фото\n@RomaSichko Адмін офігів кікати мене")

    ADMIN_DELETE_FROM_BLACK_LIST = (
        "Напиши айді цієї людини чи нікнейм, у тебе повинно буди повідомлення "
        "типу, але зауваж, що він має бути в чорному списку:\n1234567890\n@RomaSichko"
    )

    ADMIN_WRONG_BLACK_LIST = "Невалідні дані, введи ще раз"

    ADMIN_ADDED_BLACK_LIST = "Користувач успішно доданий до чорного списку"

    ADMIN_DELETED_BLACK_LIST = "Користувач успішно видалений чорного списку"

    USER_IN_BLACK_LIST = (
        "Йой, схоже ти в чорному списку, і що тепер робити... "
        "Єдиний спосіб це звенутися до куратора по допомогу зі вказанням причини додавання, "
        "думаю ти її знаєш. А допоки будеш отримувати таке повідомлення")

    USER_WRONG_TEXT = "Невірно введені дані, спробуй ще раз"

    IN_PROGRESS = "Зачекай, опрацьовую дані"

    LAST_FILE_UPDATE = (
        "Останнє оновлення файлу {file} було {date}\n"
        "Якщо бажаєш оновити, то скинь файл з такою ж назвою і я заміню його в себе")

    UNKNOWN_ERROR = (
        "Сталась невідома помилка, перешли це повідомлення @Roma_Sichko\n"
        "Exception: {exc}"
    )

    UNKNOWN_FILE = (
        "Ти намагаєшся додати невідомий для мене файл"
    )

    FILE_UPDATED = "Файл успішно оновлено"

    VIDEO_LINKS = "Нижче наведені інструкції з користування MS Teams та даним ботом:\n\n"

    VIDEO_LINKS_BASE = "Назва інструкції: {name}\nПосилання: {link}\n-=====-\n"

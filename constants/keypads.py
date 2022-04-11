from telebot import types


class Keypads:
    # Main menu
    MAIN_MENU = types.InlineKeyboardMarkup([
        [
            types.InlineKeyboardButton("Правила користування", callback_data="main-rules"),
            types.InlineKeyboardButton("FAQ", callback_data="main-faq")],
        [
            types.InlineKeyboardButton("Скинути пароль (Студенти)", callback_data="reset-password-without-account"),
            types.InlineKeyboardButton("Адміністратори онлайн", callback_data="show-admin-online")
        ],
        [
            types.InlineKeyboardButton("Написати адміністратору", callback_data="message-to-admin")
        ],
    ])

    BACK_TO_MAIN_MENU = types.InlineKeyboardMarkup(
        [[types.InlineKeyboardButton("Повернутися до меню", callback_data="back-main-menu")]],
    )

    TYPE_OF_RESET = types.InlineKeyboardMarkup([
        [
            types.InlineKeyboardButton("Студентський квиток", callback_data="verify-student-ticket"),
            types.InlineKeyboardButton("ID карта", callback_data="verify-id-card")
        ],
        [
            types.InlineKeyboardButton('Повернутися до меню', callback_data="back-main-menu")
        ],
    ])

    # Account menu
    ACCOUNT_MENU_FULL = types.InlineKeyboardMarkup([
        [
            types.InlineKeyboardButton("Змінити ел. пошту", callback_data="edit-email-account"),
            types.InlineKeyboardButton("Змінити MS Teams", callback_data="edit-teams-account")
        ],
        [
            types.InlineKeyboardButton("Скинути пароль", callback_data="reset-password-account"),
            types.InlineKeyboardButton("Написати адміністратору", callback_data="message-to-admin-account")
        ],
    ])

    ACCOUNT_MENU_NEW_ACCOUNT = types.InlineKeyboardMarkup([
        [
            types.InlineKeyboardButton("Додати ел. пошту", callback_data="add-email-account"),
            types.InlineKeyboardButton("Додати MS Teams", callback_data="add-teams-account")
        ],
    ])

    ACCOUNT_MENU_WITH_MAIL = types.InlineKeyboardMarkup([
        [
            types.InlineKeyboardButton("Змінити ел. пошту", callback_data="add-email-account"),
            types.InlineKeyboardButton("Додати MS Teams", callback_data="add-teams-account")
        ],
    ])

    ACCOUNT_MENU_WITH_TEAMS = types.InlineKeyboardMarkup([
        [
            types.InlineKeyboardButton("Додати ел. пошту", callback_data="edit-email-account"),
            types.InlineKeyboardButton("Змінити MS Teams", callback_data="edit-teams-account")
        ],
        [
            types.InlineKeyboardButton("Скинути пароль", callback_data="reset-password-account"),
            types.InlineKeyboardButton("Написати адміністратору", callback_data="message-to-admin-account")
        ],
    ])

    # Work account menu
    WORK_ACCOUNT_MENU_FULL = types.InlineKeyboardMarkup([
        [
            types.InlineKeyboardButton("Змінити ел. пошту", callback_data="edit-email-account-work"),
            types.InlineKeyboardButton("Змінити MS Teams", callback_data="edit-teams-account-work")
        ],
        [
            types.InlineKeyboardButton("Скинути пароль", callback_data="reset-password-account"),
            types.InlineKeyboardButton("Змінити власні дані", callback_data="edit-data-account-work"),
        ],
        [
            types.InlineKeyboardButton("Повідомлення адміністратору (Teams)",
                                       callback_data="message-teams-to-admin-work"),
            types.InlineKeyboardButton("Повідомлення адміністратору (інше)",
                                       callback_data="message-other-to-admin-work"),
        ],
    ])

    WORK_ACCOUNT_MENU_NEW = types.InlineKeyboardMarkup([
        [
            types.InlineKeyboardButton("Додати ел. пошту", callback_data="add-email-account-work"),
            types.InlineKeyboardButton("Додати MS Teams", callback_data="add-teams-account-work"),
        ],
        [
            types.InlineKeyboardButton("Змінити власні дані", callback_data="edit-data-account-work"),
        ],
    ])

    WORK_ACCOUNT_MENU_WITH_MAIL = types.InlineKeyboardMarkup([
        [
            types.InlineKeyboardButton("Змінити ел. пошту", callback_data="edit-email-account-work"),
            types.InlineKeyboardButton("Додати MS Teams", callback_data="add-teams-account-work")
        ],
        [
            types.InlineKeyboardButton("Повідомлення адміністратору (Teams)",
                                       callback_data="message-teams-to-admin-work"),
            types.InlineKeyboardButton("Змінити власні дані", callback_data="edit-data-account-work"),
        ],
        [
            types.InlineKeyboardButton("Повідомлення адміністратору (інше)",
                                       callback_data="message-other-to-admin-work"),
        ],
    ])

    WORK_ACCOUNT_MENU_WITH_TEAMS = types.InlineKeyboardMarkup([
        [
            types.InlineKeyboardButton("Додати ел. пошту", callback_data="add-email-account-work"),
            types.InlineKeyboardButton("Змінити MS Teams", callback_data="edit-teams-account-work")
        ],
        [
            types.InlineKeyboardButton("Скинути пароль", callback_data="reset-password-account-work"),
            types.InlineKeyboardButton("Змінити власні дані", callback_data="edit-data-account-work"),
        ],
        [
            types.InlineKeyboardButton("Повідомлення адміністратору (Teams)",
                                       callback_data="message-teams-to-admin-work"),
            types.InlineKeyboardButton("Повідомлення адміністратору (інше)",
                                       callback_data="message-other-to-admin-work"),
        ],
    ])

    # Admin menu
    ADMIN_MAIN_MENU = types.InlineKeyboardMarkup([
        [
            types.InlineKeyboardButton("Скинути пароль id", callback_data="admin-reset-pass-id"),
            types.InlineKeyboardButton("Скинути пароль ПІБ", callback_data="admin-reset-pass-pib")
        ],
        [
            types.InlineKeyboardButton("Відправити повідомлення", callback_data="admin-send-message"),
            types.InlineKeyboardButton("Змінити статус", callback_data="admin-change-status")
        ],
        [
            types.InlineKeyboardButton("Чорний список", callback_data="admin-black-list"),
            types.InlineKeyboardButton("Покинути панель", callback_data="admin-logout")
        ]
    ])

    ADMIN_TASKS_MENU = types.InlineKeyboardMarkup([
        [
            types.InlineKeyboardButton("Список задач", callback_data="admin-tasks-list"),
            types.InlineKeyboardButton("Керування статусами", callback_data="admin-tasks-status")
        ],
        [
            types.InlineKeyboardButton("Керування виконавцями", callback_data="admin-worker-edit"),
            types.InlineKeyboardButton("Питання стосовно задачі", callback_data="admin-tasks-questions")
        ],
        [
            types.InlineKeyboardButton("Покинути панель", callback_data="admin-logout")
        ]
    ])

    ADMIN_DANGER_MENU = types.InlineKeyboardMarkup([
        [
            types.InlineKeyboardButton("Видалити користувача", callback_data="admin-delete-account"),
            types.InlineKeyboardButton("Реєстрація користувачів (.csv)", callback_data="admin-add-edbo-account"),
        ],
        [
            types.InlineKeyboardButton("Формування груп (.json)", callback_data="admin-new-groups"),
            types.InlineKeyboardButton("Новий навчальний рік", callback_data="admin-new-year"),
        ],
        [
            types.InlineKeyboardButton("Покинути панель", callback_data="admin-logout"),
        ]
    ])

    ADMIN_BLACK_LIST_MENU = types.InlineKeyboardMarkup([
        [
            types.InlineKeyboardButton("Додати користувача до ЧС", callback_data="admin-black-list-add"),
            types.InlineKeyboardButton("Видалити користувача з ЧС", callback_data="admin-black-list-remove")
        ],
        [
            types.InlineKeyboardButton("Повернутися назад", callback_data="admin-back-main-menu"),
        ]
    ])

    ADMIN_TASKS_STATUS = types.InlineKeyboardMarkup([
        [
            types.InlineKeyboardButton("Нова", callback_data="task-status-new"),
            types.InlineKeyboardButton("Стоп", callback_data="task-status-stoped"),
            types.InlineKeyboardButton("В роботі", callback_data="task-status-in-progress"),
            types.InlineKeyboardButton("Виконана", callback_data="task-status-done"),
        ],
    ])

    ADMIN_TASKS_EXECUTOR = types.InlineKeyboardMarkup([
        [
            types.InlineKeyboardButton("#1", callback_data="task-executor-1"),
            types.InlineKeyboardButton("#2", callback_data="task-executor-2"),
            types.InlineKeyboardButton("#3", callback_data="task-executor-3"),
            types.InlineKeyboardButton("#4", callback_data="task-executor-4"),
        ],
    ])

    # Oftop menu
    CANCEL = types.ReplyKeyboardMarkup(
        one_time_keyboard=True,
        row_width=1,
        resize_keyboard=True
    ).row(types.KeyboardButton("Відмінити"))

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

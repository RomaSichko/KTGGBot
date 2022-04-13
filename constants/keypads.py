from telebot import types

from KTGGBot.constants.user_actions import UserAction


class Keypads:
    # Main menu
    MAIN_MENU = types.InlineKeyboardMarkup([
        [
            types.InlineKeyboardButton("Правила користування", callback_data=UserAction.main_rules.value),
            types.InlineKeyboardButton("FAQ", callback_data=UserAction.main_faq.value)],
        [
            types.InlineKeyboardButton("Скинути пароль (Студенти)", callback_data=UserAction.reset_password_without_account.value),
            types.InlineKeyboardButton("Адміністратори онлайн", callback_data=UserAction.show_admin_online.value)
        ],
        [
            types.InlineKeyboardButton("Написати адміністратору", callback_data=UserAction.message_to_admin.value)
        ],
    ])

    BACK_TO_MAIN_MENU = types.InlineKeyboardMarkup(
        [[types.InlineKeyboardButton("Повернутися до меню", callback_data=UserAction.back_main_menu.value)]],
    )

    TYPE_OF_RESET = types.InlineKeyboardMarkup([
        [
            types.InlineKeyboardButton("Студентський квиток", callback_data=UserAction.verify_student_ticket.value),
            types.InlineKeyboardButton("ID карта", callback_data=UserAction.verify_id_card.value)
        ],
        [
            types.InlineKeyboardButton('Повернутися до меню', callback_data=UserAction.back_main_menu.value)
        ],
    ])

    # Account menu
    ACCOUNT_MENU_FULL = types.InlineKeyboardMarkup([
        [
            types.InlineKeyboardButton("Змінити ел. пошту", callback_data=UserAction.edit_email_account.value),
            types.InlineKeyboardButton("Змінити MS Teams", callback_data=UserAction.edit_teams_account.value)
        ],
        [
            types.InlineKeyboardButton("Скинути пароль", callback_data=UserAction.reset_password_account.value),
            types.InlineKeyboardButton("Написати адміністратору", callback_data=UserAction.message_to_admin_account.value)
        ],
    ])

    ACCOUNT_MENU_NEW_ACCOUNT = types.InlineKeyboardMarkup([
        [
            types.InlineKeyboardButton("Додати ел. пошту", callback_data=UserAction.add_email_account.value),
            types.InlineKeyboardButton("Додати MS Teams", callback_data=UserAction.add_teams_account.value)
        ],
    ])

    ACCOUNT_MENU_WITH_MAIL = types.InlineKeyboardMarkup([
        [
            types.InlineKeyboardButton("Змінити ел. пошту", callback_data=UserAction.edit_email_account.value),
            types.InlineKeyboardButton("Додати MS Teams", callback_data=UserAction.add_teams_account.value)
        ],
    ])

    ACCOUNT_MENU_WITH_TEAMS = types.InlineKeyboardMarkup([
        [
            types.InlineKeyboardButton("Додати ел. пошту", callback_data=UserAction.add_email_account.value),
            types.InlineKeyboardButton("Змінити MS Teams", callback_data=UserAction.edit_teams_account.value)
        ],
        [
            types.InlineKeyboardButton("Скинути пароль", callback_data=UserAction.reset_password_account.value),
            types.InlineKeyboardButton("Написати адміністратору", callback_data=UserAction.message_to_admin_account.value)
        ],
    ])

    # Work account menu
    WORK_ACCOUNT_MENU_FULL = types.InlineKeyboardMarkup([
        [
            types.InlineKeyboardButton("Змінити ел. пошту", callback_data=UserAction.edit_email_account_work.value),
            types.InlineKeyboardButton("Змінити MS Teams", callback_data=UserAction.edit_teams_account_work.value)
        ],
        [
            types.InlineKeyboardButton("Скинути пароль", callback_data=UserAction.reset_password_account.value),
            types.InlineKeyboardButton("Змінити власні дані", callback_data=UserAction.edit_data_account_work.value),
        ],
        [
            types.InlineKeyboardButton("Повідомлення адміністратору (Teams)",
                                       callback_data=UserAction.message_teams_to_admin_work.value),
            types.InlineKeyboardButton("Повідомлення адміністратору (інше)",
                                       callback_data=UserAction.message_other_to_admin_work.value),
        ],
    ])

    WORK_ACCOUNT_MENU_NEW = types.InlineKeyboardMarkup([
        [
            types.InlineKeyboardButton("Додати ел. пошту", callback_data=UserAction.add_email_account_work.value),
            types.InlineKeyboardButton("Додати MS Teams", callback_data=UserAction.add_teams_account_work.value),
        ],
        [
            types.InlineKeyboardButton("Змінити власні дані", callback_data=UserAction.edit_data_account_work.value),
        ],
    ])

    WORK_ACCOUNT_MENU_WITH_MAIL = types.InlineKeyboardMarkup([
        [
            types.InlineKeyboardButton("Змінити ел. пошту", callback_data=UserAction.edit_email_account_work.value),
            types.InlineKeyboardButton("Додати MS Teams", callback_data=UserAction.add_teams_account_work.value)
        ],
        [
            types.InlineKeyboardButton("Повідомлення адміністратору (Teams)",
                                       callback_data=UserAction.message_teams_to_admin_work.value),
            types.InlineKeyboardButton("Змінити власні дані",
                                       callback_data=UserAction.edit_data_account_work.value),
        ],
        [
            types.InlineKeyboardButton("Повідомлення адміністратору (інше)",
                                       callback_data=UserAction.message_other_to_admin_work.value),
        ],
    ])

    WORK_ACCOUNT_MENU_WITH_TEAMS = types.InlineKeyboardMarkup([
        [
            types.InlineKeyboardButton("Додати ел. пошту", callback_data=UserAction.add_email_account_work.value),
            types.InlineKeyboardButton("Змінити MS Teams", callback_data=UserAction.edit_teams_account_work.value)
        ],
        [
            types.InlineKeyboardButton("Скинути пароль", callback_data=UserAction.reset_password_account.value),
            types.InlineKeyboardButton("Змінити власні дані", callback_data=UserAction.edit_data_account_work.value),
        ],
        [
            types.InlineKeyboardButton("Повідомлення адміністратору (Teams)",
                                       callback_data=UserAction.message_teams_to_admin_work.value),
            types.InlineKeyboardButton("Повідомлення адміністратору (інше)",
                                       callback_data=UserAction.message_other_to_admin_work.value),
        ],
    ])

    # Admin menu
    ADMIN_MAIN_MENU = types.InlineKeyboardMarkup([
        [
            types.InlineKeyboardButton("Скинути пароль id", callback_data=UserAction.admin_reset_pass_id.value),
            types.InlineKeyboardButton("Скинути пароль ПІБ", callback_data=UserAction.admin_reset_pass_pib.value)
        ],
        [
            types.InlineKeyboardButton("Відправити повідомлення", callback_data=UserAction.admin_send_message.value),
            types.InlineKeyboardButton("Змінити статус", callback_data=UserAction.admin_change_status.value)
        ],
        [
            types.InlineKeyboardButton("Чорний список", callback_data=UserAction.admin_black_list.value),
            types.InlineKeyboardButton("Покинути панель", callback_data=UserAction.admin_logout.value)
        ]
    ])

    ADMIN_TASKS_MENU = types.InlineKeyboardMarkup([
        [
            types.InlineKeyboardButton("Список задач", callback_data=UserAction.admin_tasks_list.value),
            types.InlineKeyboardButton("Керування статусами", callback_data=UserAction.admin_tasks_status.value)
        ],
        [
            types.InlineKeyboardButton("Керування виконавцями", callback_data=UserAction.admin_worker_edit.value),
            types.InlineKeyboardButton("Питання стосовно задачі", callback_data=UserAction.admin_tasks_questions.value)
        ],
        [
            types.InlineKeyboardButton("Покинути панель", callback_data=UserAction.admin_logout.value)
        ]
    ])

    ADMIN_DANGER_MENU = types.InlineKeyboardMarkup([
        [
            types.InlineKeyboardButton("Видалити користувача", callback_data=UserAction.admin_delete_account.value),
            types.InlineKeyboardButton("Реєстрація користувачів (.csv)", callback_data=UserAction.admin_add_edbo_account.value),
        ],
        [
            types.InlineKeyboardButton("Формування груп (.json)", callback_data=UserAction.admin_new_groups.value),
            types.InlineKeyboardButton("Новий навчальний рік", callback_data=UserAction.admin_new_year.value),
        ],
        [
            types.InlineKeyboardButton("Покинути панель", callback_data=UserAction.admin_logout.value),
        ]
    ])

    ADMIN_BLACK_LIST_MENU = types.InlineKeyboardMarkup([
        [
            types.InlineKeyboardButton("Додати користувача до ЧС", callback_data=UserAction.admin_black_list_add.value),
            types.InlineKeyboardButton("Видалити користувача з ЧС", callback_data=UserAction.admin_black_list_remove.value)
        ],
        [
            types.InlineKeyboardButton("Повернутися назад", callback_data=UserAction.admin_back_main_menu.value),
        ]
    ])

    ADMIN_TASKS_STATUS = types.InlineKeyboardMarkup([
        [
            types.InlineKeyboardButton("Нова", callback_data=UserAction.task_status_new.value),
            types.InlineKeyboardButton("Стоп", callback_data=UserAction.task_status_stoped.value),
            types.InlineKeyboardButton("В роботі", callback_data=UserAction.task_status_in_progress.value),
            types.InlineKeyboardButton("Виконана", callback_data=UserAction.task_status_done.value),
        ],
    ])

    ADMIN_TASKS_EXECUTOR = types.InlineKeyboardMarkup([
        [
            types.InlineKeyboardButton("#1", callback_data=UserAction.task_executor_1.value),
            types.InlineKeyboardButton("#2", callback_data=UserAction.task_executor_2.value),
            types.InlineKeyboardButton("#3", callback_data=UserAction.task_executor_3.value),
            types.InlineKeyboardButton("#4", callback_data=UserAction.task_executor_4.value),
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
        types.KeyboardButton("🟠"),
        types.KeyboardButton("🟡"),
        types.KeyboardButton("🟢")
    )

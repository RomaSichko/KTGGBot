from telebot import types

from .user_actions import UserAction


class Keypads:
    # Main menu
    MAIN_MENU = types.InlineKeyboardMarkup([
        [
            types.InlineKeyboardButton("Правила користування", callback_data=UserAction.main_rules.name),
            types.InlineKeyboardButton("FAQ", callback_data=UserAction.main_faq.name)],
        [
            types.InlineKeyboardButton("Скинути пароль (Студенти)", callback_data=UserAction.reset_password_without_account.name),
            # TODO: add selection_committee
            # types.InlineKeyboardButton("Приймальна комісія", callback_data=UserAction.show_admin_online.name)
        ],
        [
            types.InlineKeyboardButton("Написати адміністратору", callback_data=UserAction.message_to_admin.name)
        ],
    ])

    BACK_TO_MAIN_MENU = types.InlineKeyboardMarkup(
        [[types.InlineKeyboardButton("Повернутися до меню", callback_data=UserAction.back_main_menu.name)]],
    )

    TYPE_OF_RESET = types.InlineKeyboardMarkup([
        [
            types.InlineKeyboardButton("Студентський квиток", callback_data=UserAction.verify_student_ticket.name),
            types.InlineKeyboardButton("ID карта", callback_data=UserAction.verify_id_card.name)
        ],
        [
            types.InlineKeyboardButton('Повернутися до меню', callback_data=UserAction.back_main_menu.name)
        ],
    ])

    # Account menu
    ACCOUNT_MENU_FULL = types.InlineKeyboardMarkup([
        [
            types.InlineKeyboardButton("Змінити ел. пошту", callback_data=UserAction.edit_email_account.name),
            types.InlineKeyboardButton("Змінити MS Teams", callback_data=UserAction.edit_teams_account.name)
        ],
        [
            types.InlineKeyboardButton("Скинути пароль", callback_data=UserAction.reset_password_account.name),
            types.InlineKeyboardButton("Написати адміністратору", callback_data=UserAction.message_to_admin_account.name)
        ],
    ])

    ACCOUNT_MENU_NEW_ACCOUNT = types.InlineKeyboardMarkup([
        [
            types.InlineKeyboardButton("Додати ел. пошту", callback_data=UserAction.add_email_account.name),
            types.InlineKeyboardButton("Додати MS Teams", callback_data=UserAction.add_teams_account.name)
        ],
        [
            types.InlineKeyboardButton("Написати адміністратору",
                                       callback_data=UserAction.message_to_admin_account.name)
        ],
    ])

    ACCOUNT_MENU_WITH_MAIL = types.InlineKeyboardMarkup([
        [
            types.InlineKeyboardButton("Змінити ел. пошту", callback_data=UserAction.edit_email_account.name),
            types.InlineKeyboardButton("Додати MS Teams", callback_data=UserAction.add_teams_account.name)
        ],
        [
            types.InlineKeyboardButton("Написати адміністратору",
                                       callback_data=UserAction.message_to_admin_account.name)
        ],
    ])

    ACCOUNT_MENU_WITH_TEAMS = types.InlineKeyboardMarkup([
        [
            types.InlineKeyboardButton("Додати ел. пошту", callback_data=UserAction.add_email_account.name),
            types.InlineKeyboardButton("Змінити MS Teams", callback_data=UserAction.edit_teams_account.name)
        ],
        [
            types.InlineKeyboardButton("Скинути пароль", callback_data=UserAction.reset_password_account.name),
            types.InlineKeyboardButton("Написати адміністратору", callback_data=UserAction.message_to_admin_account.name)
        ],
    ])

    # Work account menu
    WORK_ACCOUNT_MENU_FULL = types.InlineKeyboardMarkup([
        [
            types.InlineKeyboardButton("Змінити ел. пошту", callback_data=UserAction.edit_email_account_work.name),
            types.InlineKeyboardButton("Змінити MS Teams", callback_data=UserAction.edit_teams_account_work.name)
        ],
        [
            types.InlineKeyboardButton("Скинути пароль", callback_data=UserAction.reset_password_account_work.name),
            types.InlineKeyboardButton("Задачі", callback_data=UserAction.task_account_work.name),
        ],
        [
            types.InlineKeyboardButton("Повідомлення (Teams)",
                                       callback_data=UserAction.message_teams_to_admin_work.name),
            types.InlineKeyboardButton("Повідомлення (інше)",
                                       callback_data=UserAction.message_other_to_admin_work.name),
        ],
    ])

    WORK_ACCOUNT_MENU_NEW = types.InlineKeyboardMarkup([
        [
            types.InlineKeyboardButton("Додати ел. пошту", callback_data=UserAction.add_email_account_work.name),
            types.InlineKeyboardButton("Додати MS Teams", callback_data=UserAction.add_teams_account_work.name),
        ],
        [
            types.InlineKeyboardButton("Повідомлення (Teams)",
                                       callback_data=UserAction.message_teams_to_admin_work.name),
            types.InlineKeyboardButton("Задачі",
                                       callback_data=UserAction.task_account_work.name),
        ],
        [
            types.InlineKeyboardButton("Повідомлення (інше)",
                                       callback_data=UserAction.message_other_to_admin_work.name),
        ],
    ])

    WORK_ACCOUNT_MENU_WITH_MAIL = types.InlineKeyboardMarkup([
        [
            types.InlineKeyboardButton("Змінити ел. пошту", callback_data=UserAction.edit_email_account_work.name),
            types.InlineKeyboardButton("Додати MS Teams", callback_data=UserAction.add_teams_account_work.name)
        ],
        [
            types.InlineKeyboardButton("Повідомлення (Teams)",
                                       callback_data=UserAction.message_teams_to_admin_work.name),
            types.InlineKeyboardButton("Задачі",
                                       callback_data=UserAction.task_account_work.name),
        ],
        [
            types.InlineKeyboardButton("Повідомлення (інше)",
                                       callback_data=UserAction.message_other_to_admin_work.name),
        ],
    ])

    WORK_ACCOUNT_MENU_WITH_TEAMS = types.InlineKeyboardMarkup([
        [
            types.InlineKeyboardButton("Додати ел. пошту", callback_data=UserAction.add_email_account_work.name),
            types.InlineKeyboardButton("Змінити MS Teams", callback_data=UserAction.edit_teams_account_work.name)
        ],
        [
            types.InlineKeyboardButton("Скинути пароль", callback_data=UserAction.reset_password_account_work.name),
            types.InlineKeyboardButton("Задачі", callback_data=UserAction.task_account_work.name),
        ],
        [
            types.InlineKeyboardButton("Повідомлення (Teams)",
                                       callback_data=UserAction.message_teams_to_admin_work.name),
            types.InlineKeyboardButton("Повідомлення (інше)",
                                       callback_data=UserAction.message_other_to_admin_work.name),
        ],
    ])

    # Admin menu
    ADMIN_MAIN_MENU = types.InlineKeyboardMarkup([
        [
            types.InlineKeyboardButton("Скинути пароль id", callback_data=UserAction.admin_reset_pass_id.name),
            types.InlineKeyboardButton("Скинути пароль ПІБ", callback_data=UserAction.admin_reset_pass_pib.name)
        ],
        [
            types.InlineKeyboardButton("Відправити повідомлення", callback_data=UserAction.admin_send_message.name),
        ],
        [
            types.InlineKeyboardButton("Чорний список", callback_data=UserAction.admin_black_list.name),
            types.InlineKeyboardButton("Небезпечна зона", callback_data=UserAction.admin_danger_zone.name)
        ]
    ])

    ADMIN_TASKS_MENU = types.InlineKeyboardMarkup([
        [
            types.InlineKeyboardButton("Список задач", callback_data=UserAction.admin_tasks_list.name),
            types.InlineKeyboardButton("Керування статусами", callback_data=UserAction.admin_tasks_status.name)
        ],
        [
            types.InlineKeyboardButton("Керування виконавцями", callback_data=UserAction.admin_worker_edit.name),
            types.InlineKeyboardButton("Питання стосовно задачі", callback_data=UserAction.admin_tasks_questions.name)
        ],
        [
            types.InlineKeyboardButton("Покинути панель", callback_data=UserAction.admin_logout.name)
        ]
    ])

    ADMIN_DANGER_MENU = types.InlineKeyboardMarkup([
        [
            types.InlineKeyboardButton("Видалити користувача", callback_data=UserAction.admin_delete_account.name),
            types.InlineKeyboardButton("Видалити всі групи", callback_data=UserAction.admin_delete_groups.name),
        ],
        [
            types.InlineKeyboardButton("Видалити всі групи", callback_data=UserAction.admin_back_main_menu.name),
        ]
    ])

    ADMIN_BLACK_LIST_MENU = types.InlineKeyboardMarkup([
        [
            types.InlineKeyboardButton("Додати користувача до ЧС", callback_data=UserAction.admin_black_list_add.name),
            types.InlineKeyboardButton("Видалити користувача з ЧС", callback_data=UserAction.admin_black_list_remove.name)
        ],
        [
            types.InlineKeyboardButton("Повернутися назад", callback_data=UserAction.admin_back_main_menu.name),
        ]
    ])

    ADMIN_TASKS_STATUS = types.InlineKeyboardMarkup([
        [
            types.InlineKeyboardButton("Нова", callback_data=UserAction.task_status_new.name),
            types.InlineKeyboardButton("Стоп", callback_data=UserAction.task_status_stopped.name),
            types.InlineKeyboardButton("В роботі", callback_data=UserAction.task_status_in_progress.name),
            types.InlineKeyboardButton("Виконана", callback_data=UserAction.task_status_done.name),
        ],
    ])

    ADMIN_TASKS_EXECUTOR = types.InlineKeyboardMarkup([
        [
            types.InlineKeyboardButton("#1", callback_data=UserAction.task_executor_1.name),
            types.InlineKeyboardButton("#2", callback_data=UserAction.task_executor_2.name),
            types.InlineKeyboardButton("#3", callback_data=UserAction.task_executor_3.name),
            types.InlineKeyboardButton("#4", callback_data=UserAction.task_executor_4.name),
        ],
    ])

    # Oftop menu
    CANCEL = types.ReplyKeyboardMarkup(
        one_time_keyboard=True,
        row_width=1,
        resize_keyboard=True
    ).row(types.KeyboardButton("Відмінити"))

    REMOVE = types.ReplyKeyboardRemove(selective=False)

    MARK_ANSWERED = types.InlineKeyboardMarkup(
        [[types.InlineKeyboardButton("Приховати", callback_data=UserAction.mark_answered.name)]],
    )

    # TODO: download and upload files to server
    ADMIN_LOAD_MENU = types.InlineKeyboardMarkup(
        [
            []
        ]
    )

import enum


class UserAction(enum.Enum):
    main_rules = enum.auto()
    main_faq = enum.auto()
    reset_password_without_account = enum.auto()
    selection_committee = enum.auto()
    message_to_admin = enum.auto()
    back_main_menu = enum.auto()
    verify_student_ticket = enum.auto()
    verify_id_card = enum.auto()
    edit_email_account = enum.auto()
    edit_teams_account = enum.auto()
    reset_password_account = enum.auto()
    reset_password_account_work = enum.auto()
    message_to_admin_account = enum.auto()
    add_email_account = enum.auto()
    add_teams_account = enum.auto()
    edit_email_account_work = enum.auto()
    edit_teams_account_work = enum.auto()
    task_account_work = enum.auto()
    message_teams_to_admin_work = enum.auto()
    message_other_to_admin_work = enum.auto()
    add_email_account_work = enum.auto()
    add_teams_account_work = enum.auto()
    admin_reset_pass_id = enum.auto()
    admin_reset_pass_pib = enum.auto()
    admin_send_message = enum.auto()
    admin_black_list = enum.auto()
    admin_danger_zone = enum.auto()
    admin_logout = enum.auto()
    admin_tasks_list = enum.auto()
    admin_tasks_status = enum.auto()
    admin_worker_edit = enum.auto()
    admin_tasks_questions = enum.auto()
    admin_delete_account = enum.auto()
    admin_add_edbo_account = enum.auto()
    admin_new_groups = enum.auto()
    admin_delete_groups = enum.auto()
    admin_black_list_add = enum.auto()
    admin_black_list_remove = enum.auto()
    admin_back_main_menu = enum.auto()

    mark_answered = enum.auto()
    cancel = enum.auto()

    email_confirm_code = enum.auto()
    teams_confirm_code = enum.auto()
    email_confirm_code_work = enum.auto()
    teams_confirm_code_work = enum.auto()

    verify_work_account = enum.auto()
    verify_remove_groups = enum.auto()


class AdminRights(enum.Enum):
    switch = enum.auto()
    panel = enum.auto()
    add_admin = enum.auto()
    remove_admin = enum.auto()
    answer_message = enum.auto()
    reset_password = enum.auto()
    tasks = enum.auto()
    danger_zone = enum.auto()


class SentFrom(enum.Enum):
    main_menu = enum.auto()
    user_account = enum.auto()
    work_account = enum.auto()
    work_account_other = enum.auto()

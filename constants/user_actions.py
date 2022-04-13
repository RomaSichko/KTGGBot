import enum


class UserAction(enum.auto):
    main_rules = enum.auto()
    main_faq = enum.auto()
    reset_password_without_account = enum.auto()
    show_admin_online = enum.auto()
    message_to_admin = enum.auto()
    back_main_menu = enum.auto()
    verify_student_ticket = enum.auto()
    verify_id_card = enum.auto()
    edit_email_account = enum.auto()
    edit_teams_account = enum.auto()
    reset_password_account = enum.auto()
    message_to_admin_account = enum.auto()
    add_email_account = enum.auto()
    add_teams_account = enum.auto()
    edit_email_account_work = enum.auto()
    edit_teams_account_work = enum.auto()
    edit_data_account_work = enum.auto()
    message_teams_to_admin_work = enum.auto()
    message_other_to_admin_work = enum.auto()
    add_email_account_work = enum.auto()
    add_teams_account_work = enum.auto()
    admin_reset_pass_id = enum.auto()
    admin_reset_pass_pib = enum.auto()
    admin_send_message = enum.auto()
    admin_change_status = enum.auto()
    admin_black_list = enum.auto()
    admin_logout = enum.auto()
    admin_tasks_list = enum.auto()
    admin_tasks_status = enum.auto()
    admin_worker_edit = enum.auto()
    admin_tasks_questions = enum.auto()
    admin_delete_account = enum.auto()
    admin_add_edbo_account = enum.auto()
    admin_new_groups = enum.auto()
    admin_new_year = enum.auto()
    admin_black_list_add = enum.auto()
    admin_black_list_remove = enum.auto()
    admin_back_main_menu = enum.auto()
    task_status_new = enum.auto()
    task_status_stoped = enum.auto()
    task_status_in_progress = enum.auto()
    task_status_done = enum.auto()
    task_executor_1 = enum.auto()
    task_executor_2 = enum.auto()
    task_executor_3 = enum.auto()
    task_executor_4 = enum.auto()

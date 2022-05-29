import datetime
from random import randint, choice
from typing import Union, List

import telebot
from telebot.types import Message

import utils
import os
import codecs
import json
import base_commands
from constants.dbs import TestDbs, MainDbs
from constants.domains import Domains
from constants.keypads import Keypads
from constants.messages import MessagesText
from constants.user_actions import UserAction, AdminRights, SentFrom


class KTGGFunctions:

    def __init__(self, bot: telebot.TeleBot):
        self.bot = bot
        self.ms_teams = utils.MicrosoftTeamsFunctions()
        self.db_user = base_commands.DbExecutor()
        self.db_user.db_type = TestDbs if self.db_user.current_db() == "test" else MainDbs

        self.main_id_message = self.db_user.get_last_message_id() + 1

    def switch_db(self, message):
        db = message.text.split()[1]
        # TODO: get permissions from db
        if message.chat.id == 684828985:
            if db == "test":
                self.db_user.db_type = TestDbs
            elif db == "main":
                self.db_user.db_type = MainDbs
            self.db_user.switch_db(db)
        else:
            self.bot.send_message(message.chat.id, "Access denied")

    def welcome(self, message):
        self.delete_user_last_message(message=message)
        self.bot.send_message(
            chat_id=message.chat.id,
            text=MessagesText.WELCOME,
            reply_markup=Keypads.MAIN_MENU,
        )

    def main_menu(self, message):
        self.db_user.update_user_action(
            telegram_id=message.chat.id,
            action=UserAction.back_main_menu.name,
        )

        self.delete_user_last_message(message=message)
        self._remove_keyboard(message)

        self.bot.send_message(
            chat_id=message.chat.id,
            text=MessagesText.MENU_MESSAGES,
            reply_markup=Keypads.MAIN_MENU,
        )

    def my_account(self, message):
        self.delete_user_last_message(message=message)
        self._remove_keyboard(message)
        check = self.db_user.check_user_in_main_base(message.chat.id)

        if check:
            mail_exist = self.db_user.get_valid_mail_main_account(message.chat.id)
            teams_mail_exist = self.db_user.get_valid_teams_main_account(message.chat.id)

            if mail_exist and teams_mail_exist:
                keypad = Keypads.ACCOUNT_MENU_FULL
            elif teams_mail_exist:
                keypad = Keypads.ACCOUNT_MENU_WITH_TEAMS
            elif mail_exist:
                keypad = Keypads.ACCOUNT_MENU_WITH_MAIL
            else:
                keypad = Keypads.ACCOUNT_MENU_NEW_ACCOUNT

        else:
            keypad = Keypads.ACCOUNT_MENU_NEW_ACCOUNT
            self.db_user.add_data_main_account(
                telegram_id=message.chat.id,
                username=message.chat.username
            )
            self.bot.send_message(
                chat_id=message.chat.id,
                text=MessagesText.ADDED_ACCOUNT_IN_DB,
            )

        user_data_in_db = self.db_user.get_user_data_main_account(message.chat.id)
        self.bot.send_message(
            chat_id=message.chat.id,
            text=MessagesText.USER_ACCOUNT_MAIN.format(
                email=user_data_in_db["email"],
                name=user_data_in_db["userName"],
                teams=user_data_in_db["teamsEmail"],
            ),
            reply_markup=keypad,
        )

    def work_account(self, message):
        self.delete_user_last_message(message=message)
        self._remove_keyboard(message)
        check = self.db_user.check_user_in_work_base(message.chat.id)

        if check:
            mail_exist = self.db_user.get_valid_mail_work_account(message.chat.id)
            teams_mail_exist = self.db_user.get_valid_teams_work_account(message.chat.id)

            if mail_exist and teams_mail_exist:
                keypad = Keypads.WORK_ACCOUNT_MENU_FULL
            elif teams_mail_exist:
                keypad = Keypads.WORK_ACCOUNT_MENU_WITH_TEAMS
            elif mail_exist:
                keypad = Keypads.WORK_ACCOUNT_MENU_WITH_MAIL
            else:
                keypad = Keypads.WORK_ACCOUNT_MENU_NEW

            user_data_in_db = self.db_user.get_user_data_work_account(message.chat.id)
            self.bot.send_message(
                chat_id=message.chat.id,
                text=MessagesText.USER_ACCOUNT_WORK.format(
                    email=user_data_in_db["email"],
                    name=user_data_in_db["userName"],
                    teams=user_data_in_db["teamsEmail"],
                ),
                reply_markup=keypad,
            )
        else:
            self.bot.send_message(
                chat_id=message.chat.id,
                text=MessagesText.USER_ACCOUNT_WORK_NEW,
                reply_markup=Keypads.CANCEL,
            )

            self.db_user.update_user_action(
                telegram_id=message.chat.id,
                action=UserAction.verify_work_account.name,
            )

    def action_photo(self, message):
        if self.db_user.get_user_action(message.chat.id) == UserAction.verify_student_ticket.name:
            self.bot.send_message(
                chat_id=message.chat.id,
                text=MessagesText.MESSAGE_WAIT_ACTION,
                reply_markup=Keypads.REMOVE,
            )

            file_id = message.photo[-1].file_id
            file_info = self.bot.get_file(file_id)
            downloaded_file = self.bot.download_file(file_info.file_path)

            user_photo = f"image_{str(message.chat.id)}.jpg"

            with open(user_photo, 'wb') as new_file:
                new_file.write(downloaded_file)

            new_user_data = self.ms_teams.reset_password_by_student_ticket(user_photo)

            if new_user_data[0]:
                self.bot.send_message(
                    chat_id=message.chat.id,
                    text=MessagesText.RESETED_PASSWORD.format(
                        login=new_user_data[2],
                        password=new_user_data[1],
                    )
                )

                self.bot.send_message(
                    chat_id=message.chat.id,
                    text=MessagesText.MENU_MESSAGES,
                    reply_markup=Keypads.MAIN_MENU,
                )
                self.db_user.update_user_action(message.chat.id, UserAction.back_main_menu.name)

            else:
                self.bot.send_message(
                    chat_id=message.chat.id,
                    text=MessagesText.STUDENT_TICKET_NOT_FOUND,
                    reply_markup=Keypads.CANCEL,
                )

            try:
                os.remove(user_photo)
            except FileNotFoundError:
                pass

            self.delete_user_last_message(message)

        else:
            self.bot.send_message(
                chat_id=message.chat.id,
                text=MessagesText.NOT_CONFIRMED_ACTION,
            )

    def admin_panel(self, message):
        self.delete_user_last_message(message=message)
        self._remove_keyboard(message=message)

        if self._get_admin_right(message.chat.id):
            if self._get_admin_right(message.chat.id, AdminRights.panel):
                self.bot.send_message(
                        chat_id=message.chat.id,
                        text=MessagesText.ADMIN_PANEL,
                        reply_markup=Keypads.ADMIN_MAIN_MENU,
                    )
                self.db_user.update_user_action(message.chat.id,
                                                UserAction.admin_back_main_menu.name)
            else:
                self.bot.send_message(
                    chat_id=message.chat.id,
                    text=MessagesText.ADMIN_PANEL_WITHOUT_RIGHTS,
                )
        else:
            self.bot.send_message(
                chat_id=message.chat.id,
                text=MessagesText.ADMIN_PANEL_DENIED,
            )

    def callback_worker(self, call):
        new_calls = {
            UserAction.main_rules.name: self.call_main_rules_show,
            UserAction.main_faq.name: self.call_main_faq_show,
            UserAction.reset_password_without_account.name: self.call_reset_password_choice_verify_type,
            UserAction.message_to_admin.name: self.call_message_to_admin_call,
            UserAction.back_main_menu.name: self.call_back_to_main_menu,
            UserAction.verify_student_ticket.name: self.call_verify_type_student_ticket,
            UserAction.verify_id_card.name: self.call_verify_type_id_card,
            UserAction.edit_email_account.name: self.call_edit_email_personal_account,
            UserAction.edit_teams_account.name: self.call_edit_teams_personal_account,
            UserAction.reset_password_account.name: self.call_reset_password_account,
            UserAction.reset_password_account_work.name: self.call_reset_password_account_work,
            UserAction.message_to_admin_account.name: self.call_message_to_admin_account,
            UserAction.add_email_account.name: self.call_add_email_personal_account,
            UserAction.add_teams_account.name: self.call_add_teams_personal_account,
            UserAction.edit_email_account_work.name: self.call_edit_email_work_account,
            UserAction.edit_teams_account_work.name: self.call_edit_teams_work_account,
            UserAction.task_account_work.name: self.call_edit_data_work_account,
            UserAction.message_teams_to_admin_work.name: self.call_message_to_admin_work_account,
            UserAction.message_other_to_admin_work.name: self.call_message_other_to_admin_work_account,
            UserAction.add_email_account_work.name: self.call_add_email_work_account,
            UserAction.add_teams_account_work.name: self.call_add_teams_work_account,

            UserAction.admin_danger_zone.name: self.call_admin_danger_zone,
            UserAction.admin_reset_pass_id.name: self.call_admin_reset_password_by_id,
            UserAction.admin_reset_pass_pib.name: self.call_admin_reset_password_by_pib,
            UserAction.admin_send_message.name: self.call_admin_send_message,
            # UserAction.admin_black_list
            # UserAction.admin_logout
            # UserAction.admin_tasks_list
            # UserAction.admin_tasks_status
            # UserAction.admin_worker_edit
            # UserAction.admin_tasks_questions
            UserAction.admin_delete_account.name: self.call_admin_delete_account,
            # UserAction.admin_add_edbo_account
            # UserAction.admin_new_groups
            UserAction.admin_delete_groups.name: self.call_delete_groups,
            # UserAction.admin_black_list_add
            # UserAction.admin_black_list_remove
            # UserAction.admin_back_main_menu
            # UserAction.task_status_new
            # UserAction.task_status_stoped
            # UserAction.task_status_in_progress
            # UserAction.task_status_done
            # UserAction.task_executor_1
            # UserAction.task_executor_2
            # UserAction.task_executor_3
            # UserAction.task_executor_4
            UserAction.mark_answered.name: self.call_admin_mark_answered,
        }
        new_calls[call.data](call)

    def delete_user_last_message(self, message):
        self.bot.delete_message(
            chat_id=message.chat.id,
            message_id=message.id,
        )

    def call_main_rules_show(self, call):
        self._edit_message_call(
            text=MessagesText.MAIN_RULES,
            reply_markup=Keypads.BACK_TO_MAIN_MENU,
            call=call,
        )

    def call_main_faq_show(self, call):
        self._edit_message_call(
            text=MessagesText.MAIN_FAQ,
            reply_markup=Keypads.BACK_TO_MAIN_MENU,
            call=call
        )

    def call_reset_password_choice_verify_type(self, call):
        self._edit_message_call(
            text=MessagesText.RESET_PASSWORD_WITHOUT_ACC_CHOICE_VERIFY_TYPE,
            reply_markup=Keypads.TYPE_OF_RESET,
            call=call,
        )

    def call_message_to_admin_call(self, call):
        self._remove_old_message_send_message_call(
            text=MessagesText.MESSAGE_TO_ADMIN,
            reply_markup=Keypads.CANCEL,
            call=call,
        )

    def call_back_to_main_menu(self, call):
        self._edit_message_call(
            text=MessagesText.MENU_MESSAGES,
            reply_markup=Keypads.MAIN_MENU,
            call=call
        )

    def call_verify_type_student_ticket(self, call):
        self._remove_old_message_send_message_call(
            text=MessagesText.MESSAGE_STUDENT_TICKET_RESET_TYPE,
            reply_markup=Keypads.CANCEL,
            call=call,
        )

    def call_verify_type_id_card(self, call):
        self._remove_old_message_send_message_call(
            text=MessagesText.MESSAGE_ID_CARD_RESET_TYPE,
            reply_markup=Keypads.CANCEL,
            call=call,
        )

    def call_edit_email_personal_account(self, call):
        self.call_edit_email_account(call=call)

    def call_edit_teams_personal_account(self, call):
        self.call_edit_teams_account(call=call)

    def call_edit_email_work_account(self, call):
        self.call_edit_email_account(call=call)

    def call_edit_teams_work_account(self, call):
        self.call_edit_teams_account(call=call)

    def call_add_email_personal_account(self, call):
        self.call_add_email_account(call=call)

    def call_add_teams_personal_account(self, call):
        self.call_add_teams_account(call=call)

    def call_add_email_work_account(self, call):
        self.call_add_email_account(call=call)

    def call_add_teams_work_account(self, call):
        self.call_add_teams_account(call=call)

    def call_message_to_admin_account(self, call):
        self.call_message_to_admin_call(call=call)

    def call_message_to_admin_work_account(self, call):
        self.call_message_to_admin_call(call=call)

    def call_message_other_to_admin_work_account(self, call):
        self._remove_old_message_send_message_call(
            text=MessagesText.MESSAGE_TO_ADMIN_NO_TEAMS,
            reply_markup=Keypads.CANCEL,
            call=call,
        )

    def call_reset_password_account(self, call):
        self._remove_old_message_send_message_call(
            text=MessagesText.MESSAGE_RESET_PASSWORD_ACCOUNT,
            reply_markup=Keypads.REMOVE,
            call=call
        )
        checker, password, user_id = self.ms_teams.reset_password(
            user_id=self.db_user.get_teams_main_account(telegram_id=call.message.chat.id),
        )
        if checker:
            self.bot.send_message(
                chat_id=call.message.chat.id,
                text=MessagesText.RESETED_PASSWORD.format(
                    login=user_id,
                    password=password,
                ),
            )
            self.my_account(call.message)
        else:
            self.bot.send_message(
                chat_id=call.message.chat.id,
                text="Невідома помилка",
            )
            self.my_account(call.message)

    def call_reset_password_account_work(self, call):
        self._edit_message_call(
            text=MessagesText.MESSAGE_RESET_PASSWORD_ACCOUNT,
            reply_markup=Keypads.REMOVE,
            call=call
        )
        checker, password, user_id = self.ms_teams.reset_password(
            user_id=self.db_user.get_teams_work_account(telegram_id=call.message.chat.id),
        )
        if checker:
            self.bot.send_message(
                chat_id=call.message.chat.id,
                text=MessagesText.RESETED_PASSWORD.format(
                    login=user_id,
                    password=password,
                ),
            )
            self.work_account(call.message)
        else:
            self.bot.send_message(
                chat_id=call.message.chat.id,
                text="Невідома помилка",
            )
            self.work_account(call.message)

    def call_edit_data_work_account(self, call):
        self._remove_old_message_send_message_call(
            text="Дана дія поки що недоступна",
            reply_markup=Keypads.CANCEL,
            call=call,
        )
        self.work_account(call.message)

    def call_add_email_account(self, call):
        self._remove_old_message_send_message_call(
            text=MessagesText.MESSAGE_ADD_EMAIL_ACCOUNT,
            reply_markup=Keypads.CANCEL,
            call=call
        )

    def call_add_teams_account(self, call):
        self._remove_old_message_send_message_call(
            text=MessagesText.MESSAGE_ADD_TEAMS_ACCOUNT,
            reply_markup=Keypads.CANCEL,
            call=call,
        )

    def call_edit_email_account(self, call):
        self._remove_old_message_send_message_call(
            text=MessagesText.MESSAGE_EDIT_EMAIL_ACCOUNT,
            reply_markup=Keypads.CANCEL,
            call=call,
        )

    def call_edit_teams_account(self, call):
        self._remove_old_message_send_message_call(
            text=MessagesText.MESSAGE_EDIT_TEAMS_ACCOUNT,
            reply_markup=Keypads.CANCEL,
            call=call,
        )

    def _edit_message_call(self, text: str, reply_markup: telebot.REPLY_MARKUP_TYPES, call):
        self.bot.edit_message_text(
            message_id=call.message.id,
            chat_id=call.message.chat.id,
            text=text,
            reply_markup=reply_markup,
        )
        self.db_user.update_user_action(call.message.chat.id, call.data)

    def _remove_old_message_send_message_call(self, text: str, reply_markup: telebot.REPLY_MARKUP_TYPES, call):
        self.delete_user_last_message(message=call.message)
        self.bot.send_message(
            chat_id=call.message.chat.id,
            text=text,
            reply_markup=reply_markup,
        )
        self.db_user.update_user_action(call.message.chat.id, call.data)

    def _get_admin_right(self, user_id: int, right: AdminRights = None) -> bool:
        admin_in_db = self.db_user.get_admin(telegram_id=user_id)
        if admin_in_db:
            admin_in_db = admin_in_db[0]
            if right:
                return right.name in admin_in_db["rights"]
            return True
        return False

    def call_admin_reset_password_by_id(self, call):
        self._remove_old_message_send_message_call(
            text=MessagesText.ADMIN_PANEL_RESET_PASSWORD_BY_ID,
            reply_markup=Keypads.CANCEL,
            call=call
        )

    def call_admin_reset_password_by_pib(self, call):
        self._remove_old_message_send_message_call(
            text=MessagesText.ADMIN_PANEL_RESET_PASSWORD_BY_PIB,
            reply_markup=Keypads.CANCEL,
            call=call
        )

    def call_admin_send_message(self, call):
        # TODO: refactor message text
        if self._get_admin_right(call.message.chat.id, AdminRights.answer_message):
            messages = self.db_user.get_message_from_db()

            for message in messages:
                self.bot.send_message(
                    chat_id=call.message.chat.id,
                    text=(f"mainIdMessage: {message['mainIdMessage']} \n"
                          f"UserId: {message['userId']} \n"
                          f"username: {message['username']} \n"
                          f"Message: {message['message']} \n"
                          f"Topic: {message['topic']} \n"
                          f"SentFrom: {message['sentFrom']}\n"
                          f"Additional data: {message['additionalData']}\n"
                          f"Time: {message['time']} \n"),
                    reply_markup=Keypads.MARK_ANSWERED,
                )

            self.bot.send_message(
                chat_id=call.message.chat.id,
                text=MessagesText.ADMIN_SEND_MESSAGE,
                reply_markup=Keypads.CANCEL,
            )
            self.db_user.update_user_action(call.message.chat.id, call.data)
        else:
            self.bot.send_message(
                chat_id=call.message.chat.id,
                text=MessagesText.ADMIN_PANEL_WITHOUT_RIGHTS,
            )

    def call_admin_mark_answered(self, call):
        self.db_user.update_message(
            main_id_message=int(call.message.text.split()[1]),
        )

        self.delete_user_last_message(message=call.message)

    def call_admin_delete_account(self, call):
        self._remove_old_message_send_message_call(
            text=MessagesText.ADMIN_DELETE_ACCOUNTS,
            reply_markup=Keypads.CANCEL,
            call=call,
        )

    def call_admin_danger_zone(self, call):
        if self._get_admin_right(
            user_id=call.message.chat.id,
            right=AdminRights.danger_zone,
        ):
            self._remove_old_message_send_message_call(
                text=MessagesText.ADMIN_PANEL_DANGER,
                call=call,
                reply_markup=Keypads.ADMIN_DANGER_MENU,
            )
        else:
            self.bot.send_message(
                chat_id=call.message.chat.id,
                text=MessagesText.ADMIN_PANEL_DENIED,
            )

    def call_delete_groups(self, call):
        self._remove_old_message_send_message_call(
            call=call,
            text=MessagesText.ADMIN_CALL_DELETE_GROUPS,
            reply_markup=Keypads.CANCEL,
        )
        self.sticker_send_random_sticker(call.message)

    def sticker_send_random_sticker(self, message: Message):
        sticker_set = utils.get_random_sticker_set()
        sticker = choice(self.bot.get_sticker_set(name=sticker_set).stickers)
        self.bot.send_sticker(
            chat_id=message.chat.id,
            sticker=sticker.file_id,
        )

    def verify_sticker(self, message: Message):
        if (self.db_user.get_user_action(telegram_id=message.chat.id) ==
                UserAction.admin_delete_groups.name):
            if message.reply_to_message:
                if message.reply_to_message.sticker.file_unique_id == message.sticker.file_unique_id:
                    self.bot.send_message(
                        chat_id=message.chat.id,
                        text=MessagesText.ADMIN_STICKER_VERIFIED,
                    )
                    self.db_user.update_user_action(
                        telegram_id=message.chat.id,
                        action=UserAction.verify_remove_groups.name,
                    )
                else:
                    self.bot.send_message(
                        chat_id=message.chat.id,
                        text=MessagesText.ADMIN_STICKER_FAILED,
                    )
                    self.sticker_send_random_sticker(message=message)
            else:
                self.bot.send_message(
                    chat_id=message.chat.id,
                    text=MessagesText.WRONG_ADMIN_STICKER,
                )
        else:
            self.bot.send_message(
                chat_id=message.chat.id,
                text=MessagesText.NOT_CONFIRMED_ACTION,
            )

    def text_handler(self, message: Message):
        if message.text == "Відмінити":
            self.text_cancel_message(message)
            return

        message_handle = {
            UserAction.message_to_admin.name: self.test_message_to_admin_main_menu,
            UserAction.verify_id_card.name: self.text_verify_id_card,
            UserAction.edit_email_account.name: self.text_add_edit_email_account,
            UserAction.edit_teams_account.name: self.text_add_edit_teams_account,
            UserAction.message_to_admin_account.name: self.test_message_to_admin_account,
            UserAction.add_email_account.name: self.text_add_edit_email_account,
            UserAction.add_teams_account.name: self.text_add_edit_teams_account,
            UserAction.edit_email_account_work.name: self.text_add_edit_email_account_work,
            UserAction.edit_teams_account_work.name: self.text_add_edit_teams_account_work,
            UserAction.message_teams_to_admin_work.name: self.test_message_to_admin_work_account,
            UserAction.message_other_to_admin_work.name: self.test_message_to_admin_work_account_other,
            UserAction.verify_work_account.name: self.text_verify_work_account,
            UserAction.add_email_account_work.name: self.text_add_edit_email_account_work,
            UserAction.add_teams_account_work.name: self.text_add_edit_teams_account_work,
            UserAction.email_confirm_code.name: self.text_email_confirm_code,
            UserAction.teams_confirm_code.name: self.text_teams_confirm_code,
            UserAction.email_confirm_code_work.name: self.text_email_confirm_code_work,
            UserAction.teams_confirm_code_work.name: self.text_teams_confirm_code_work,

            UserAction.admin_reset_pass_id.name: self.text_admin_reset_pass_id,
            UserAction.admin_reset_pass_pib.name: self.text_admin_reset_pass_pib,
            UserAction.admin_send_message.name: self.text_admin_send_message,
            # UserAction.admin_change_status
            # UserAction.admin_black_list
            # UserAction.admin_worker_edit
            # UserAction.admin_tasks_questions
            UserAction.admin_delete_account.name: self.text_delete_user,
            # UserAction.admin_add_edbo_account
            UserAction.verify_remove_groups.name: self.text_admin_delete_groups,
            # UserAction.admin_new_year
            # UserAction.admin_black_list_add
            # UserAction.admin_black_list_remove
            # UserAction.task_executor_1
            # UserAction.task_executor_2
            # UserAction.task_executor_3
            # UserAction.task_executor_4
        }
        action = self.db_user.get_user_action(
            telegram_id=message.chat.id,
        )
        try:
            message_handle[action](message=message)
        except KeyError:
            self.bot.send_message(
                chat_id=message.chat.id,
                text=MessagesText.UNKNOWN_ACTION,
            )

    def text_common_message_to_admin(self, message: Message, sent_from: SentFrom):
        message_topics = {
            SentFrom.main_menu: None,
            SentFrom.user_account: "Проблема користувача",
            SentFrom.work_account: "Проблема працівника (Teams)",
            SentFrom.work_account_other: "Проблема працівника (Інше)"
        }

        self.db_user.add_message_to_db(
            telegram_id=message.chat.id,
            telegram_username=message.chat.username,
            main_id_message=self.main_id_message,
            message=message.text,
            topic=message_topics[sent_from],
            sent_from=sent_from.name,
            additional_data=self._generate_additional_data_message_to_admin(
                telegram_id=message.chat.id,
                sent_from=sent_from,
            ),
            time=datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S"),
        )

        self.bot.send_message(
            chat_id=message.chat.id,
            text=MessagesText.MESSAGE_TO_ADMIN_SENDED,
            reply_markup=Keypads.REMOVE,
        )

        self.main_id_message += 1
        self.main_menu(message)

    def test_message_to_admin_main_menu(self, message: Message):
        self.text_common_message_to_admin(
            message=message,
            sent_from=SentFrom.main_menu,
        )

    def test_message_to_admin_account(self, message: Message):
        self.text_common_message_to_admin(
            message=message,
            sent_from=SentFrom.user_account,
        )

    def test_message_to_admin_work_account(self, message: Message):
        self.text_common_message_to_admin(
            message=message,
            sent_from=SentFrom.work_account,
        )

    def test_message_to_admin_work_account_other(self, message: Message):
        self.text_common_message_to_admin(
            message=message,
            sent_from=SentFrom.work_account_other,
        )

    def text_verify_id_card(self, message: Message):
        lastname, name, thirdname, passport = message.text.split()
        response = self.ms_teams.reset_password_by_passport(
            user_lastname=lastname,
            user_name=name,
            user_thirdname=thirdname,
            user_card=passport,
        )

        if response:
            self.bot.send_message(
                chat_id=message.chat.id,
                text=MessagesText.RESETED_PASSWORD.format(
                    login=response[2],
                    password=response[1],
                ),
            )
            self.main_menu(message)
        else:
            self.bot.send_message(
                chat_id=message.chat.id,
                text=MessagesText.FAIL_TO_RESET_PASSWORD,
                reply_markup=Keypads.CANCEL
            )

    def text_admin_reset_pass_id(self, message: Message):
        # TODO: refactor
        user_id = message.text
        if utils.valid_mail(user_id):
            response = self.ms_teams.reset_password(user_id=user_id)
            if response:
                self.bot.send_message(
                    chat_id=message.chat.id,
                    text=MessagesText.RESETED_PASSWORD.format(
                        login=response[2],
                        password=response[1],
                    ),
                )
                self.main_menu(message)
        else:
            self.bot.send_message(
                chat_id=message.chat.id,
                text=MessagesText.ADMIN_RESET_BY_ID_WRONG_MAIL,
                reply_markup=Keypads.CANCEL,
            )

    def text_admin_reset_pass_pib(self, message: Message):
        # TODO: refactor
        name, lastname = message.text.split()
        response = self.ms_teams.reset_password_by_user_name(user_name=name,
                                                             user_lastname=lastname)

        if response:
            self.bot.send_message(
                chat_id=message.chat.id,
                text=MessagesText.RESETED_PASSWORD.format(
                    login=response[2],
                    password=response[1],
                ),
            )
            self.admin_panel(message)
        else:
            self.bot.send_message(
                chat_id=message.chat.id,
                text=MessagesText.FAIL_TO_RESET_PASSWORD,
                reply_markup=Keypads.CANCEL
            )

    def text_admin_send_message(self, message: Message):
        if message.reply_to_message:
            split_message = message.reply_to_message.text.split()
            if "mainIdMessage:" not in split_message:
                self.bot.send_message(
                    chat_id=message.chat.id,
                    text=MessagesText.WRONG_MESSAGE_CHOICE,
                )
                return
            message_id, chat_id = int(split_message[1]), split_message[3]

            admin_answer = message.text

            message_db = self.db_user.get_message_from_db(
                filters=f"mainIdMessage = {message_id}",
            )

            if message_db:
                if not message_db[0]["status"]:
                    self.bot.send_message(
                        chat_id=int(chat_id),
                        text=MessagesText.ADMIN_MESSAGE_ANSWER.format(
                            answer=admin_answer,
                        ))
                    self.bot.send_message(
                        chat_id=message.chat.id,
                        text=MessagesText.ADMIN_MESSAGE_SENT,
                    )
                    self.db_user.update_message(
                        main_id_message=message_id,
                        set_data=f"status = true, admin = {message.chat.id}, answer = \'{admin_answer}\'"
                    )
                else:
                    self.bot.send_message(
                        chat_id=message.chat.id,
                        text=MessagesText.ADMIN_MESSAGE_ANSWERED,
                    )
        else:
            self.bot.send_message(
                chat_id=message.chat.id,
                text=MessagesText.WRONG_ADMIN_MESSAGE_REPLY,
            )

    def text_delete_user(self, message: Message):
        message_text = message.text.split()

        if len(message_text) == 1:
            verify_action = self.ms_teams.delete_user(
                user_id=message.text,
            )
        elif len(message_text) == 2:
            verify_action = self.ms_teams.delete_user(
                user_name=message.text,
            )
        else:
            self.bot.reply_to(
                message=message,
                text=MessagesText.WRONG_USER_DATA,
            )
            return
        text = MessagesText.SUCCESS_DELETE_USER if (
            verify_action) else MessagesText.FAILED_DELETE_USER

        self.bot.reply_to(
            message=message,
            text=text.format(name=message.text)
        )

    def text_admin_delete_groups(self, message: Message):
        ignored_groups = []
        if message.text.lower() != "all":
            ignored_groups = message.text.split(", ")
        print(ignored_groups)
        result = self.ms_teams.delete_all_groups(ignored_groups=ignored_groups)
        if result:
            self.bot.send_message(
                chat_id=message.chat.id,
                text=MessagesText.ADMIN_DELETE_GROUPS_ERRORS.format(
                    groups=" ".join(result),
                ),
            )
        else:
            self.bot.send_message(
                chat_id=message.chat.id,
                text=MessagesText.ADMIN_DELETE_GROUPS_SUCCESS,
            )
        self.admin_panel(message=message)

    def text_common_add_edit_account(self,
                                     message: Message,
                                     code_type: str,
                                     user_action: UserAction):
        self.delete_user_last_message(message=message)
        email = message.text
        if utils.valid_mail(email):
            self.bot.send_message(
                chat_id=message.chat.id,
                text=MessagesText.USER_ACCOUNT_CONFIRM_CODE.format(email=email),
                reply_markup=Keypads.CANCEL
            )

            code = randint(10 ** 6, 10 ** 8)
            self.ms_teams.mail_send(to_user_email=email, code=code)
            self.db_user.add_user_email_code(
                telegram_id=message.chat.id,
                confirm_code=code,
                email=email,
                code_type=code_type,
            )

            self.db_user.update_user_action(
                telegram_id=message.chat.id,
                action=user_action.name,
            )
        else:
            self.bot.send_message(
                chat_id=message.chat.id,
                text=MessagesText.USER_ACCOUNT_WRONG_MAIL,
                reply_markup=Keypads.CANCEL
            )

    def text_add_edit_email_account(self, message: Message):
        self.text_common_add_edit_account(
            message=message,
            code_type="email",
            user_action=UserAction.email_confirm_code,
        )

    def text_add_edit_email_account_work(self, message: Message):
        self.text_common_add_edit_account(
            message=message,
            code_type="email",
            user_action=UserAction.email_confirm_code_work,
        )

    def text_add_edit_teams_account(self, message: Message):
        for domain in Domains:
            if domain.value in message.text:
                self.text_common_add_edit_account(
                    message=message,
                    code_type="teams",
                    user_action=UserAction.teams_confirm_code,
                )
                return
        self.bot.send_message(
            chat_id=message.chat.id,
            text=MessagesText.USER_ACCOUNT_WRONG_TEAMS,
        )

    def text_add_edit_teams_account_work(self, message: Message):
        for domain in Domains:
            if domain.value in message.text:
                self.text_common_add_edit_account(
                    message=message,
                    code_type="teams",
                    user_action=UserAction.teams_confirm_code_work,
                )
                return
        self.bot.send_message(
            chat_id=message.chat.id,
            text=MessagesText.USER_ACCOUNT_WRONG_TEAMS,
        )

    def text_common_confirm_code_account(self,
                                         message: Message,
                                         code_type: str,
                                         command):
        self.delete_user_last_message(message=message)
        confirm_code = message.text

        if int(confirm_code) == self.db_user.get_user_confirm_code(telegram_id=message.chat.id,
                                                                   code_type=code_type):
            email = self.db_user.get_user_email_confirm_codes(telegram_id=message.chat.id,
                                                              code_type=code_type)

            if code_type == "email":
                command(
                    telegram_id=message.chat.id,
                    mail=email,
                )
            else:
                user_name = self.ms_teams.get_user_data(user_mail=email)
                command(
                    telegram_id=message.chat.id,
                    user_name=user_name,
                    mail=email,
                )

            self.bot.send_message(
                chat_id=message.chat.id,
                text=MessagesText.USER_ACCOUNT_EMAIL_CONFIRM,
                reply_markup=Keypads.REMOVE,
            )

            self.db_user.delete_user_confirm_code(
                telegram_id=message.chat.id,
                code_type=code_type,
            )

            if command == self.db_user.update_user_email_main_account or command == self.db_user.update_user_teams_main_account:
                self.my_account(message)
            else:
                self.work_account(message)

        else:
            self.bot.send_message(
                chat_id=message.chat.id,
                text=MessagesText.USER_ACCOUNT_WRONG_CONFIRM_CODE,
                reply_markup=Keypads.CANCEL,
            )

    def text_email_confirm_code(self, message: Message):
        self.text_common_confirm_code_account(message=message,
                                              code_type="email",
                                              command=self.db_user.update_user_email_main_account)

    def text_teams_confirm_code(self, message: Message):
        self.text_common_confirm_code_account(message=message,
                                              code_type="teams",
                                              command=self.db_user.update_user_teams_main_account)

    def text_email_confirm_code_work(self, message: Message):
        self.text_common_confirm_code_account(message=message,
                                              code_type="email",
                                              command=self.db_user.update_user_email_work_account)

    def text_teams_confirm_code_work(self, message: Message):
        self.text_common_confirm_code_account(message=message,
                                              code_type="teams",
                                              command=self.db_user.update_user_teams_work_account)

    def text_verify_work_account(self, message: Message):
        code, user_name, user_lastname, user_thirdname = message.text.split()
        if utils.get_work_account_by_codes(
            code=code,
            user_name=user_name,
            user_lastname=user_lastname,
            user_thirdname=user_thirdname,
        ):
            self.bot.send_message(
                chat_id=message.chat.id,
                text=MessagesText.USER_ACCOUNT_WORK_CONFIRM,
            )
            self.db_user.add_data_work_account(
                telegram_id=message.chat.id,
                username=message.chat.username,
            )
            email = self.ms_teams.get_user_id_by_name(name=f"{user_name} {user_lastname}")

            self.db_user.update_user_teams_work_account(
                telegram_id=message.chat.id,
                user_name=f"{user_name} {user_lastname}",
                mail=email,
            )

            self._remove_keyboard(message)
            self.work_account(message)
        else:
            self.bot.send_message(
                chat_id=message.chat.id,
                text=MessagesText.USER_ACCOUNT_WORK_WRONG,
            )

    def text_cancel_message(self, message: Message):
        self.db_user.update_user_action(
            telegram_id=message.chat.id,
            action=UserAction.back_main_menu.name,
        )
        if self._get_admin_right(user_id=message.chat.id, right=AdminRights.panel):
            self.admin_panel(message=message)
        else:
            self.main_menu(message=message)

    def _remove_keyboard(self, message: Message):
        msg = self.bot.send_message(
            chat_id=message.chat.id,
            text="REMOVE_KEYBOARD",
            reply_markup=Keypads.REMOVE
        )
        self.bot.delete_message(
            chat_id=msg.chat.id,
            message_id=msg.id,
        )

    def _generate_additional_data_message_to_admin(self,
                                                   telegram_id: int,
                                                   sent_from: SentFrom) -> Union[str, None]:
        if sent_from == SentFrom.main_menu:
            return None
        elif sent_from == SentFrom.user_account:
            response = self.db_user.get_user_data_main_account(telegram_id=telegram_id)
        else:
            response = self.db_user.get_user_data_work_account(telegram_id=telegram_id)

        return f"email: {response['email']}, username: {response['userName']}, teams: {response['teamsEmail']}"
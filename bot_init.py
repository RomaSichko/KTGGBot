from random import randint

import telebot
import changePass
import os
import codecs
from telebot import types
import json
import base_commands
import key
from KTGGBot.constants.dbs import TestDbs, MainDbs
from KTGGBot.constants.keypads import Keypads
from KTGGBot.constants.messages import MessagesText
from KTGGBot.constants.user_actions import UserAction


class KTGGFunctions:

    def __init__(self, bot: telebot.TeleBot):
        self.bot = bot
        self.actions = {}
        self.db_user = base_commands.DbExecutor()
        self.db_user.db_type = TestDbs if self.db_user.current_db() == "test" else MainDbs

        self.mainIDMessage = json.load(codecs.open("message.json", 'r', 'utf-8-sig'))[-1]['mainIDMessage'] + 1

    def switch_db(self, message):
        db = message.text.split()[1]
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
        self.actions.update({message.chat.id: {"main_menu_action": None}})
        self.delete_user_last_message(message=message)
        self.bot.send_message(
            chat_id=message.chat.id,
            text=MessagesText.MENU_MESSAGES,
            reply_markup=Keypads.MAIN_MENU,
        )

    def my_account(self, message):
        self.delete_user_last_message(message=message)
        check = self.db_user.check_user_in_base(message.chat.id)

        if check:
            mail_exist = self.db_user.get_valid_mail(message.chat.id)
            teams_mail_exist = self.db_user.get_valid_teams(message.chat.id)

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
            self.db_user.add_data(
                telegram_id=message.chat.id,
                username=message.chat.username
            )
            self.bot.send_message(
                chat_id=message.chat.id,
                text=MessagesText.ADDED_ACCOUNT_IN_DB,
            )

        user_data_in_db = self.db_user.get_user_data(message.chat.id)
        self.bot.send_message(
            chat_id=message.chat.id,
            text=user_data_in_db,
            reply_markup=keypad,
        )

    def action_photo(self, message):
        if message.chat.id in self.user_base_reset and self.user_base_reset[message.chat.id] and \
                self.user_base_reset[message.chat.id]["stud"]:

            self.bot.send_message(
                chat_id=message.chat.id,
                text=ConstantMessages.WAIT_DATA_CHECK,
                reply_markup=Keypads.REMOVE,
            )

            file_id = message.photo[-1].file_id
            file_info = self.bot.get_file(file_id)
            downloaded_file = self.bot.download_file(file_info.file_path)

            uphoto = f"image_{str(message.chat.id)}.jpg"

            with open(uphoto, 'wb') as new_file:
                new_file.write(downloaded_file)

            new_user_data = changePass.reset_pass(uphoto)

            if new_user_data[0]:
                self.bot.send_message(
                    chat_id=message.chat.id,
                    text=ConstantMessages.DATA_FOUND,
                )
                self.bot.send_message(
                    chat_id=message.chat.id,
                    text=ConstantMessages.NEW_PASSWORD.format(
                        login=new_user_data[2],
                        password=new_user_data[1],
                    )
                )

                self.bot.send_message(
                    chat_id=message.chat.id,
                    text=ConstantMessages.NEXT_ACTION,
                    reply_markup=Keypads.MAIN_MENU,
                )

            else:
                self.bot.send_message(
                    chat_id=message.chat.id,
                    text=ConstantMessages.PHOTO_DATA_NOT_FOUND,
                    reply_markup=Keypads.CANCEL,
                )

            try:
                os.remove(uphoto)
            except FileNotFoundError:
                pass

        else:
            self.bot.send_message(
                chat_id=message.chat.id,
                text=ConstantMessages.UNKWOWN_ACTION,
            )

    def admin_panel(self, message):
        if message.chat.id not in self.admin_base:

            self.bot.send_message(
                chat_id=message.chat.id,
                text=ConstantMessages.ENTER_PASSWORD,
            )

            self.admin_base.update({message.chat.id: {}})
            self.admin_base[message.chat.id].update({"user": message.chat.id, "verify": False})

        elif self.admin_base[message.chat.id]["verify"]:

            self.bot.send_message(
                chat_id=message.chat.id,
                text=ConstantMessages.ACTION,
                reply_markup=Keypads.ADMIN_MAIN_MENU,
            )
        else:
            self.bot.send_message(
                chat_id=message.chat.id,
                text=ConstantMessages.ENTER_PASSWORD,
            )

    def status(self, message):
        base = json.load(codecs.open("admin.json", 'r', 'utf-8-sig'))

        for i in base:
            if i['id'] == message.chat.id:
                self.bot.send_message(
                    chat_id=message.chat.id,
                    text=ConstantMessages.ADMIN_STATUSES,
                    reply_markup=Keypads.ADMIN_STATUS,
                )
                i['islog'] = True

        with open('admin.json', 'w') as file:
            json.dump(base, file)

    def callback_worker(self, call):
        self.call = call
        print(self.actions)
        new_calls = {
            UserAction.main_rules: self.main_rules_show,
            UserAction.main_faq: self.main_faq_show,
            UserAction.reset_password_without_account: self.reset_password_choice_verify_type,
            UserAction.show_admin_online: self.admins_online_show,
            UserAction.message_to_admin: self.message_to_admin_call,
            UserAction.back_main_menu: self.back_to_main_menu,
            UserAction.verify_student_ticket: self.verify_type_student_ticket,
            UserAction.verify_id_card: self.verify_type_id_card,
            UserAction.edit_email_account: self.edit_email_personal_account,
            UserAction.edit_teams_account: self.edit_teams_personal_account,
            UserAction.reset_password_account: self.reset_password_account,
            UserAction.message_to_admin_account: self.message_to_admin_account,
            UserAction.add_email_account: self.add_email_personal_account,
            UserAction.add_teams_account: self.add_teams_personal_account,
            UserAction.edit_email_account_work: self.edit_email_work_account,
            UserAction.edit_teams_account_work: self.edit_teams_work_account,
            UserAction.edit_data_account_work: self.edit_data_work_account,
            UserAction.message_teams_to_admin_work: self.message_to_admin_work_account,
            UserAction.message_other_to_admin_work: self.message_other_to_admin_work_account,
            UserAction.add_email_account_work: self.add_email_work_account,
            UserAction.add_teams_account_work: self.add_teams_work_account,
            # UserAction.admin_reset_pass_id
            # UserAction.admin_reset_pass_pib
            # UserAction.admin_send_message
            # UserAction.admin_change_status
            # UserAction.admin_black_list
            # UserAction.admin_logout
            # UserAction.admin_tasks_list
            # UserAction.admin_tasks_status
            # UserAction.admin_worker_edit
            # UserAction.admin_tasks_questions
            # UserAction.admin_delete_account
            # UserAction.admin_add_edbo_account
            # UserAction.admin_new_groups
            # UserAction.admin_new_year
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
        }
        new_calls[call.data]()

    def text_handler(self, message):

        if message.text == ConstantMessages.CANCEL:
            self.remove_from_dict(message)
            return

        elif message.text == ConstantMessages.FINISH:
            if message.chat.id in self.admin_base:
                msg = self.bot.send_message(
                    chat_id=message.chat.id,
                    text=ConstantMessages.ACTION,
                    reply_markup=Keypads.REMOVE,
                )

                self.admin_panel(msg)

                if "delete" in self.admin_base[message.chat.id] and self.admin_base[message.chat.id]["delete"]:
                    self.admin_base[message.chat.id]["delete"] = False

        elif message.text == ConstantMessages.FINISH_CALL:
            if message.chat.id in self.teacher_call:

                if message.chat.id in self.teacher_call and 'msg' in self.teacher_call[message.chat.id]:
                    for i in self.teacher_call[message.chat.id]['msg']:
                        self.bot.delete_message(message.chat.id, i)

                msg = self.bot.send_message(
                    chat_id=message.chat.id,
                    text=ConstantMessages.ACTION,
                    reply_markup=Keypads.REMOVE,
                )

                self.main_menu(msg)

                self.remove_from_dict(message)

        elif message.text in '🔴🟠🟡🟢':

            markup = types.ReplyKeyboardRemove(selective=False)
            base = json.load(codecs.open("admin.json", 'r', 'utf-8-sig'))

            for i in base:
                if i['id'] == message.chat.id and i['islog']:
                    i['status'] = message.text

                    with open('admin.json', 'w') as file:
                        json.dump(base, file)

                    msg = self.bot.send_message(
                        chat_id=message.chat.id,
                        text=ConstantMessages.STATUS_CHANGE,
                        reply_markup=Keypads.REMOVE,
                    )

                    self.main_menu(msg)

        if message.chat.id in self.user_base_reset and self.user_base_reset[message.chat.id]:
            text = message.text.split()
            if len(text) == 4:
                self.bot.send_message(
                    chat_id=message.chat.id,
                    text=ConstantMessages.WAIT_DATA_CHECK,
                    reply_markup=Keypads.REMOVE,
                )

                new_data = changePass.reset_pass_idcard(text[0], text[1], text[2], text[3])
                file = codecs.open("pass.txt", "a", 'utf-8')

                if new_data[0]:
                    self.bot.send_message(
                        chat_id=message.chat.id,
                        text=ConstantMessages.NEW_PASSWORD.format(
                            login=new_data[2],
                            password=new_data[1],
                        ),
                        reply_markup=Keypads.REMOVE,
                    )
                    self.bot.send_message(
                        chat_id=message.chat.id,
                        text=ConstantMessages.NEXT_ACTION,
                        reply_markup=Keypads.MAIN_MENU,
                    )

                    self.remove_from_dict(message)

                elif not new_data[0] and new_data[1] != "":

                    self.bot.send_message(
                        chat_id=message.chat.id,
                        text=ConstantMessages.CARD_DATA_NOT_FOUND,
                    )

                else:
                    self.bot.send_message(
                        chat_id=message.chat.id,
                        text=ConstantMessages.NOT_FOUND_WITHOUT_ACC,
                        reply_markup=Keypads.REMOVE,
                    )

                    self.bot.send_message(
                        chat_id=message.chat.id,
                        text=ConstantMessages.NEXT_ACTION,
                        reply_markup=Keypads.MAIN_MENU,
                    )

                    self.remove_from_dict(message)

                file.close()

            else:
                self.bot.send_message(
                    chat_id=message.chat.id,
                    text=ConstantMessages.INVALID_DATA,
                )

        elif message.chat.id in self.teacher_base_reset and self.teacher_base_reset[message.chat.id]:
            if self.teacher_base_reset[message.chat.id]["id"]:
                text = message.text.split()
                if len(text) == 4:
                    new_data = changePass.reset_pass_teacher(text[0], text[1], text[2], text[3])
                    file = codecs.open("pass.txt", "a", 'utf-8')

                    if new_data[0]:
                        self.bot.send_message(
                            chat_id=message.chat.id,
                            text=ConstantMessages.NEW_PASSWORD.format(
                                login=new_data[2],
                                password=new_data[1],
                            ),
                            reply_markup=Keypads.REMOVE,
                        )
                        self.bot.send_message(
                            chat_id=message.chat.id,
                            text=ConstantMessages.NEXT_ACTION,
                            reply_markup=Keypads.MAIN_MENU,
                        )

                        self.remove_from_dict(message)

                    elif not new_data[0] and new_data[1] != "":

                        self.bot.send_message(
                            chat_id=message.chat.id,
                            text=ConstantMessages.CARD_DATA_NOT_FOUND,
                        )

                    else:
                        self.bot.send_message(
                            chat_id=message.chat.id,
                            text=ConstantMessages.NOT_FOUND_WITHOUT_ACC,
                            reply_markup=Keypads.REMOVE,
                        )

                        self.bot.send_message(
                            chat_id=message.chat.id,
                            text=ConstantMessages.NEXT_ACTION,
                            reply_markup=Keypads.MAIN_MENU,
                        )
                        self.remove_from_dict(message)
                    file.close()
                else:
                    self.bot.send_message(
                        chat_id=message.chat.id,
                        text=ConstantMessages.INVALID_DATA,
                    )

        elif message.chat.id in self.base_message:
            if self.base_message[message.chat.id]["message"]:
                base = json.load(codecs.open("message.json", 'r', 'utf-8-sig'))

                temp_base = {'mainIDMessage': self.mainIDMessage, "id": message.chat.id,
                            'username': message.chat.username,
                            "from": "Student", "status": False, "message": message.text}

                base.append(temp_base)

                with open("message.json", "w") as outfile:
                    json.dump(base, outfile)

                self.mainIDMessage += 1

                self.bot.send_message(
                    chat_id=message.chat.id,
                    text=ConstantMessages.MESSAGE_SENT_ADMIN,
                    reply_markup=Keypads.REMOVE,
                )

                self.bot.send_message(
                    chat_id=message.chat.id,
                    text=ConstantMessages.NEXT_ACTION,
                    reply_markup=Keypads.MAIN_MENU,
                )

                self.remove_from_dict(message)

        elif message.chat.id in self.admin_base:
            if not self.admin_base[message.chat.id]["verify"]:
                if message.text == key.get_admin_key():
                    self.admin_base[message.chat.id]["verify"] = True
                    self.bot.send_message(
                        chat_id=message.chat.id,
                        text=ConstantMessages.SUCCESS_VERIFY,
                    )
                    self.admin_panel(message)
                else:
                    self.bot.send_message(
                        chat_id=message.chat.id,
                        text=ConstantMessages.BAD_VERIFY,
                    )
            else:
                if "id" in self.admin_base[message.chat.id] and self.admin_base[message.chat.id]["id"]:
                    if '@ktgg.kiev.ua' in message.text or '@kdktgg.onmicrosoft.com' in message.text:
                        new_data = changePass.reset_pass_bot(message.text)

                        self.bot.send_message(
                            chat_id=message.chat.id,
                            text=ConstantMessages.NEW_PASSWORD.format(
                                login=new_data[2],
                                password=new_data[1],
                            ),
                            reply_markup=Keypads.REMOVE,
                        )

                    else:
                        self.bot.send_message(
                            chat_id=message.chat.id,
                            text=ConstantMessages.INVALID_DATA,
                        )

                    del (self.admin_base[message.chat.id]["id"])

                elif "pib" in self.admin_base[message.chat.id] and self.admin_base[message.chat.id]["pib"]:
                    text = message.text.split()
                    if len(text) == 2:
                        new_data = changePass.reset_pass_bot("0", message.text.split()[0], message.text.split()[1])

                        self.bot.send_message(
                            chat_id=message.chat.id,
                            text=ConstantMessages.NEW_PASSWORD.format(
                                login=new_data[2],
                                password=new_data[1],
                            ),
                            reply_markup=Keypads.REMOVE,
                        )

                    else:
                        self.bot.send_message(
                            chat_id=message.chat.id,
                            text=ConstantMessages.INVALID_DATA,
                        )

                    del (self.admin_base[message.chat.id]["pib"])

                elif "id-message" in self.admin_base[message.chat.id] and self.admin_base[message.chat.id][
                    "id-message"]:
                    m = message.text.split()

                    if len(m) >= 3:

                        if m[0].isdigit():
                            base = json.load(codecs.open("message.json", 'r', 'utf-8-sig'))

                            for i in base:
                                if i['mainIDMessage'] == int(m[0]) and i['id'] == int(m[1]):
                                    if not i['status']:

                                        if m[2].lower() == 'true':
                                            msg = self.bot.send_message(
                                                chat_id=message.chat.id,
                                                text=ConstantMessages.MESSAGE_MARK,
                                            )

                                        else:
                                            self.bot.send_message(
                                                chat_id=int(m[1]),
                                                text=ConstantMessages.MESSAGE_FROM_ADMIN.format(
                                                    answer=' '.join(m[2:]),
                                                ))
                                            msg = self.bot.send_message(
                                                chat_id=message.chat.id,
                                                text=ConstantMessages.MESSAGE_SENT,
                                            )
                                        self.admin_panel(msg)

                                        i['status'] = True
                                        i['answer'] = ' '.join(m[2:])
                                        i['admin'] = message.chat.id
                                    else:
                                        msg = self.bot.send_message(
                                            chat_id=message.chat.id,
                                            text=ConstantMessages.ALREADY_ANSWERED,
                                        )
                                        self.admin_panel(msg)

                            with open("message.json", "w") as outfile:
                                json.dump(base, outfile)

                        else:
                            self.bot.send_message(
                                chat_id=message.chat.id,
                                text=ConstantMessages.INVALID_DATA,
                            )
                    else:
                        self.bot.send_message(
                            chat_id=message.chat.id,
                            text=ConstantMessages.INVALID_DATA,
                        )

                    del (self.admin_base[message.chat.id]["id-message"])

                elif "delete" in self.admin_base[message.chat.id] and self.admin_base[message.chat.id]["delete"]:
                    m = message.text.split()

                    result = changePass.detete_user(m[0], m[1])

                    if result[0]:
                        self.bot.send_message(
                            chat_id=message.chat.id,
                            text=ConstantMessages.SUCCESS_DELETE.format(
                                user=result[2],
                                id=result[1],
                            )
                        )

                    else:
                        self.bot.send_message(
                            chat_id=message.chat.id,
                            text=ConstantMessages.FAIL_DELETE.format(
                                lastname=m[1],
                                name=m[0],
                            )
                        )

        elif message.chat.id in self.teacher_message:
            if not self.teacher_message[message.chat.id]["isLog"]:
                message_text = message.text.split()
                teacher_id = message_text[0]
                teacher_name = ' '.join(message_text[1:])

                if teacher_id.isdigit() and teacher_name:
                    teachers = json.load(codecs.open("teacher.json", 'r', 'utf-8-sig'))

                    for i in teachers:
                        # print(i)
                        if i['ID працівника'] == teacher_id and i['ПІБ'] == teacher_name:
                            self.teacher_message[message.chat.id]["isLog"] = True

                            self.bot.send_message(
                                chat_id=message.chat.id,
                                text=f"{ConstantMessages.SUCCESS_VERIFY}. {ConstantMessages.SEND_MESSAGE_CANCEL}",
                                reply_markup=Keypads.CANCEL,
                            )

                    if not self.teacher_message[message.chat.id]["isLog"]:
                        self.bot.send_message(
                            chat_id=message.chat.id,
                            text=ConstantMessages.CARD_DATA_NOT_FOUND,
                            reply_markup=Keypads.CANCEL,
                        )

                else:
                    self.bot.send_message(
                        chat_id=message.chat.id,
                        text=ConstantMessages.INVALID_DATA,
                        reply_markup=Keypads.CANCEL,
                    )

            elif self.teacher_message[message.chat.id]["isLog"]:
                base = json.load(codecs.open("message.json", 'r', 'utf-8-sig'))

                temp_base = {'mainIDMessage': self.mainIDMessage, "id": message.chat.id,
                            'username': message.chat.username,
                            "from": "Teacher", "status": False, "message": message.text}

                base.append(temp_base)

                # print(base)

                with open("message.json", "w") as outfile:
                    json.dump(base, outfile)

                self.mainIDMessage += 1
                self.bot.send_message(
                    chat_id=message.chat.id,
                    text=ConstantMessages.MESSAGE_SENT_ADMIN,
                    reply_markup=Keypads.REMOVE,
                )

                # bot.send_message(684828985,"id: " + str(message.chat.id) + '\n' + message.text)

                self.bot.send_message(
                    chat_id=message.chat.id,
                    text=ConstantMessages.NEXT_ACTION,
                    reply_markup=Keypads.BACK_TO_MAIN_MENU,
                )

                self.remove_from_dict(message)

        elif message.chat.id in self.teacher_call:
            if not self.teacher_call[message.chat.id]["isLog"]:
                message_text = message.text.split()
                teacher_id = message_text[0]
                teacher_name = ' '.join(message_text[1:])

                keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1, resize_keyboard=1)
                item = types.KeyboardButton("Відмінити")
                keyboard.row(item)

                if teacher_id.isdigit() and teacher_name:
                    teachers = json.load(codecs.open("teacher.json", 'r', 'utf-8-sig'))

                    for i in teachers:
                        # print(i)
                        if i['ID працівника'] == teacher_id and i['ПІБ'] == teacher_name:

                            self.teacher_call[message.chat.id]["isLog"] = True

                            base = json.load(codecs.open("admin.json", 'r', 'utf-8-sig'))

                            msg_id_list = []

                            for j in base:
                                if j['status'] == '🟢':
                                    msg = self.bot.send_contact(
                                        chat_id=message.chat.id,
                                        phone_number=j["phone"],
                                        first_name=j["name"],
                                        timeout=5,
                                        reply_markup=Keypads.REMOVE,
                                    )
                                    msg_id_list.append(msg.id)

                            self.bot.send_message(
                                chat_id=message.chat.id,
                                text=ConstantMessages.CALL_ADMIN,
                                reply_markup=Keypads.CANCEL,
                            )

                            self.teacher_call[message.chat.id].update({'msg': msg_id_list})

                    if not self.teacher_call[message.chat.id]["isLog"]:
                        self.bot.send_message(
                            chat_id=message.chat.id,
                            text=ConstantMessages.CARD_DATA_NOT_FOUND,
                            reply_markup=Keypads.CANCEL,
                        )

                else:
                    self.bot.send_message(
                        chat_id=message.chat.id,
                        text=ConstantMessages.INVALID_DATA,
                        reply_markup=Keypads.CANCEL,
                    )

            elif self.teacher_call[message.chat.id]["isLog"]:
                pass

        elif message.chat.id in self.mailAuth:
            if self.mailAuth[message.chat.id]["code"] is None:
                if changePass.valid_mail(message.text):
                    password = str(randint(100000, 999999))
                    self.mailAuth[message.chat.id]["code"] = password
                    self.mailAuth[message.chat.id]["mail"] = message.text
                    changePass.mail_send(message.text, password)
                    self.bot.send_message(
                        chat_id=message.chat.id,
                        text=ConstantMessages.MAIL_CONFIRM_CODE,
                    )
                else:
                    self.bot.send_message(
                        chat_id=message.chat.id,
                        text=ConstantMessages.INVALID_MAIL,
                        )
            elif self.mailAuth[message.chat.id]["code"]:
                if message.text == self.mailAuth[message.chat.id]["code"]:
                    markup = types.ReplyKeyboardRemove(selective=False)
                    base_commands.update_data_mail(message.chat.id, self.mailAuth[message.chat.id]["mail"])
                    msg = self.bot.send_message(
                        chat_id=message.chat.id,
                        text=ConstantMessages.MAIL_CONFIRMED,
                        reply_markup=Keypads.REMOVE,
                    )
                    self.remove_from_dict(message)
                    self.my_account(msg)
                else:
                    self.bot.send_message(
                        chat_id=message.chat.id,
                        text=ConstantMessages.INVALID_CONFIRM_CODE,
                    )

        elif message.chat.id in self.teamsAuth:
            if self.teamsAuth[message.chat.id]["code"] is None:
                if changePass.valid_mail(message.text):
                    if (message.text[message.text.find('@') + 1:] == "kdktgg.onmicrosoft.com"
                            or message.text[message.text.find('@') + 1:] == "ktgg.kiev.ua"):
                        if changePass.valid_teams(message.text):
                            password = str(randint(100000, 999999))
                            self.teamsAuth[message.chat.id]["code"] = password
                            self.teamsAuth[message.chat.id]["mail"] = message.text
                            changePass.mail_send(message.text, password)
                            self.bot.send_message(
                                chat_id=message.chat.id,
                                text=ConstantMessages.TEAMS_CONFIRM_CODE,
                                )
                        else:
                            self.bot.send_message(
                                chat_id=message.chat.id,
                                text=ConstantMessages.INVALID_TEAMS,
                                )
                    else:
                        self.bot.send_message(
                            chat_id=message.chat.id,
                            text=ConstantMessages.INVALID_TEAMS,
                        )
                else:
                    self.bot.send_message(
                        chat_id=message.chat.id,
                        text=ConstantMessages.UNREAL_MAIL,
                        )

            elif self.teamsAuth[message.chat.id]["code"]:
                if message.text == self.teamsAuth[message.chat.id]["code"]:
                    markup = types.ReplyKeyboardRemove(selective=False)
                    base_commands.update_data_teams(message.chat.id, self.teamsAuth[message.chat.id]["mail"])
                    msg = self.bot.send_message(
                        chat_id=message.chat.id,
                        text=ConstantMessages.CONFIRMED_ACCOUNT,
                        reply_markup=Keypads.REMOVE,
                    )
                    self.remove_from_dict(message)
                    self.my_account(msg)
                else:
                    self.bot.send_message(
                        chat_id=message.chat.id,
                        text=ConstantMessages.INVALID_CONFIRM_CODE,
                    )

        elif message.chat.id in self.lastnameNameAuth:
            if self.lastnameNameAuth[message.chat.id]['lastname']:
                base_commands.update_data_lastname(message.chat.id, message.text)
                msg = self.bot.send_message(
                    chat_id=message.chat.id,
                    text=ConstantMessages.CHANGE_ACCOUNT_DATA,
                    reply_markup=Keypads.REMOVE,
                )
                try:
                    del (self.lastnameNameAuth[message.chat.id])
                except KeyError:
                    pass
                self.my_account(msg)
            elif self.lastnameNameAuth[message.chat.id]['name']:
                base_commands.update_data_name(message.chat.id, message.text)
                msg = self.bot.send_message(
                    chat_id=message.chat.id,
                    text=ConstantMessages.CHANGE_ACCOUNT_DATA,
                    reply_markup=Keypads.REMOVE,
                )
                self.remove_from_dict(message)
                self.my_account(msg)

        else:
            if message.chat.id == 684828985 or message.chat.id == 461655305 or message.chat.id == 365794368:
                pass
            else:
                self.bot.send_message(
                    chat_id=message.chat.id,
                    text=ConstantMessages.UNKWOWN_ACTION,
                )

    def add_user_to_black_list_admin(self, message):
        pass

    @staticmethod
    def to_black_list(user_id, reason):
        black_list = json.load(codecs.open("black_list.json", 'r', 'utf-8-sig'))

        black_list.append({
            "id": user_id,
            "reason": reason,
        })

        with open("message.json", "w") as outfile:
            json.dump(black_list, outfile)

    def delete_user_last_message(self, message):
        self.bot.delete_message(
            chat_id=message.chat.id,
            message_id=message.id,
        )

    def main_rules_show(self):
        self._edit_message(
            text=MessagesText.MAIN_RULES,
            reply_markup=Keypads.BACK_TO_MAIN_MENU,
        )

    def main_faq_show(self):
        self._edit_message(
            text=MessagesText.MAIN_FAQ,
            reply_markup=Keypads.BACK_TO_MAIN_MENU,
        )

    def reset_password_choice_verify_type(self):
        self._edit_message(
            text=MessagesText.RESET_PASSWORD_WITHOUT_ACC_CHOICE_VERIFY_TYPE,
            reply_markup=Keypads.TYPE_OF_RESET,
        )

    def admins_online_show(self):
        admin_status_template = "\t{name} {status}\n"
        message_text = "Статуси:\n\t🔴 - зайнятий\n\t🟠 - не активний\n\t🟡 - на парі\n\t🟢 - вільний\nАдміни:\n"

        for admin in json.load(codecs.open("admin.json", 'r', 'utf-8-sig')):
            message_text += admin_status_template.format(
                name=admin["name"],
                status=admin["status"],
            )

        self._edit_message(
            text=message_text,
            reply_markup=Keypads.BACK_TO_MAIN_MENU,
        )

    def message_to_admin_call(self):
        self._remove_old_message_send_message(
            text=MessagesText.MESSAGE_TO_ADMIN,
            reply_markup=Keypads.CANCEL,
        )

    def back_to_main_menu(self):
        self._edit_message(
            text=MessagesText.MENU_MESSAGES,
            reply_markup=Keypads.MAIN_MENU,
        )

    def verify_type_student_ticket(self):
        self._remove_old_message_send_message(
            text=MessagesText.MESSAGE_STUDENT_TICKET_RESET_TYPE,
            reply_markup=Keypads.CANCEL,
        )

    def verify_type_id_card(self):
        self._remove_old_message_send_message(
            text=MessagesText.MESSAGE_ID_CARD_RESET_TYPE,
            reply_markup=Keypads.CANCEL,
        )

    def edit_email_personal_account(self):
        self.edit_email_account()

    def edit_teams_personal_account(self):
        self.edit_teams_account()

    def edit_email_work_account(self):
        self.edit_email_account()

    def edit_teams_work_account(self):
        self.edit_teams_account()

    def add_email_personal_account(self):
        self.add_email_account()

    def add_teams_personal_account(self):
        self.add_teams_account()

    def add_email_work_account(self):
        self.add_email_account()

    def add_teams_work_account(self):
        self.add_teams_account()

    def message_to_admin_account(self):
        self.message_to_admin_call()

    def message_to_admin_work_account(self):
        self.message_to_admin_call()

    def message_other_to_admin_work_account(self):
        self._remove_old_message_send_message(
            text=MessagesText.MESSAGE_TO_ADMIN_NO_TEAMS,
            reply_markup=Keypads.CANCEL,
        )

    def reset_password_account(self):
        self._edit_message(
            text=MessagesText.MESSAGE_RESET_PASSWORD_ACCOUNT,
            reply_markup=Keypads.REMOVE,
        )

    def edit_data_work_account(self):
        self._remove_old_message_send_message(
            text=MessagesText.MESSAGE_EDIT_DATA_ACCOUNT,
            reply_markup=Keypads.CANCEL,
        )

    def add_email_account(self):
        self._remove_old_message_send_message(
            text=MessagesText.MESSAGE_ADD_EMAIL_ACCOUNT,
            reply_markup=Keypads.CANCEL,
        )

    def add_teams_account(self):
        self._remove_old_message_send_message(
            text=MessagesText.MESSAGE_ADD_TEAMS_ACCOUNT,
            reply_markup=Keypads.CANCEL,
        )

    def edit_email_account(self):
        self._remove_old_message_send_message(
            text=MessagesText.MESSAGE_EDIT_EMAIL_ACCOUNT,
            reply_markup=Keypads.CANCEL,
        )

    def edit_teams_account(self):
        self._remove_old_message_send_message(
            text=MessagesText.MESSAGE_EDIT_TEAMS_ACCOUNT,
            reply_markup=Keypads.CANCEL,
        )

    def _edit_message(self, text: str, reply_markup: telebot.REPLY_MARKUP_TYPES):
        self.bot.edit_message_text(
            message_id=self.call.message.id,
            chat_id=self.call.message.chat.id,
            text=text,
            reply_markup=reply_markup,
        )
        self.db_user.update_user_action(self.call.message.chat.id, self.call.data)

    def _remove_old_message_send_message(self, text: str, reply_markup: telebot.REPLY_MARKUP_TYPES):
        self.delete_user_last_message(message=self.call.message)
        self.bot.send_message(
            chat_id=self.call.message.chat.id,
            text=text,
            reply_markup=reply_markup,
        )
        self.db_user.update_user_action(self.call.message.chat.id, self.call.data)




    def get_student_ticket(self):
        self.bot.send_message(
            chat_id=self.call.message.chat.id,
            text=ConstantMessages.TICKET_PHOTO,
            reply_markup=Keypads.CANCEL,
        )
        self.bot.delete_message(self.call.message.chat.id, self.call.message.id)

        self.user_base_reset.update({self.call.message.chat.id: {}})
        self.user_base_reset[self.call.message.chat.id].update({"stud": 1})

    def get_id_card(self):
        self.user_base_reset.update({self.call.message.chat.id: {}})
        self.user_base_reset[self.call.message.chat.id].update({"idcard": 1})

        self.bot.send_message(
            chat_id=self.call.message.chat.id,
            text=ConstantMessages.CARD_DATA,
            reply_markup=Keypads.CANCEL,
        )
        self.bot.delete_message(self.call.message.chat.id, self.call.message.id)

    def show_rules(self):
        msg = self.bot.edit_message_text(
            text=ConstantMessages.RULES,
            chat_id=self.call.message.chat.id,
            message_id=self.call.message.id,
            reply_markup=Keypads.BACK_TO_MAIN_MENU,
        )

        self.main_menu(msg)

    def show_faq(self):
        self.bot.edit_message_text(
            text=ConstantMessages.FAQ,
            chat_id=self.call.message.chat.id,
            message_id=self.call.message.id,
            reply_markup=Keypads.BACK_TO_MAIN_MENU)

    def choice_verify_type(self):
        self.bot.edit_message_text(
            text=ConstantMessages.VERIFICATION_TYPE,
            chat_id=self.call.message.chat.id,
            message_id=self.call.message.id,
            reply_markup=Keypads.TYPE_OF_RESET,
        )

    def show_menu(self):
        self.bot.edit_message_text(
            text=ConstantMessages.NEXT_ACTION,
            chat_id=self.call.message.chat.id,
            message_id=self.call.message.id,
            reply_markup=Keypads.MAIN_MENU,
        )

        try:
            del (self.user_base_reset[self.call.message.chat.id])
        except KeyError:
            pass

    def message_to_admin(self):
        self.bot.send_message(
            chat_id=self.call.message.chat.id,
            text=ConstantMessages.SEND_MESSAGE_CANCEL,
            reply_markup=Keypads.CANCEL,
        )
        self.bot.delete_message(
            chat_id=self.call.message.chat.id,
            message_id=self.call.message.id,
        )
        self.base_message.update({self.call.message.chat.id: {}})
        self.base_message[self.call.message.chat.id].update({"message": True})

    def get_email(self):
        self.bot.send_message(
            chat_id=self.call.message.chat.id,
            text=ConstantMessages.SEND_EMAIL_CANCEL,
            reply_markup=Keypads.CANCEL,
        )

        self.mailAuth.update({self.call.message.chat.id: {}})
        self.mailAuth[self.call.message.chat.id].update({"auth": False, "code": None, "mail": None})

    def get_teams_account(self):
        self.bot.send_message(
            chat_id=self.call.message.chat.id,
            text=ConstantMessages.SEND_EMAIL_TEAMS_CANCEL,
            reply_markup=Keypads.CANCEL,
        )

        self.teamsAuth.update({self.call.message.chat.id: {}})
        self.teamsAuth[self.call.message.chat.id].update({"auth": False, "code": None, "mail": None})

    def get_name(self):
        self.bot.send_message(
            chat_id=self.call.message.chat.id,
            text=ConstantMessages.SEND_LASTNAME_CANCEL,
            reply_markup=Keypads.CANCEL,
        )

        self.lastnameNameAuth.update({self.call.message.chat.id: {}})
        self.lastnameNameAuth[self.call.message.chat.id].update({"name": False, "lastname": True})

    def get_lastname(self):
        self.bot.send_message(
            chat_id=self.call.message.chat.id,
            text=ConstantMessages.SEND_NAME_CANCEL,
            reply_markup=Keypads.CANCEL,
        )

        self.lastnameNameAuth.update({self.call.message.chat.id: {}})
        self.lastnameNameAuth[self.call.message.chat.id].update({"name": True, "lastname": False})

    def change_password_account(self):
        self.bot.edit_message_text(
            text=ConstantMessages.WAIT_DATA_CHECK,
            chat_id=self.call.message.chat.id,
            message_id=self.call.message.id,
        )
        teams = base_commands.get_teams(self.call.message.chat.id)
        new_data = changePass.reset_pass_bot(teams)
        msg = self.bot.send_message(
            chat_id=self.call.message.chat.id,
            text=ConstantMessages.NEW_PASSWORD.format(
                login=new_data[2],
                password=new_data[1],
            )
        )
        self.my_account(msg)

    def show_admin_online(self):
        base = json.load(codecs.open("admin.json", 'r', 'utf-8-sig'))
        baseStatus = {'🔴': 'зайнятий', '🟠': 'не активний', '🟡': 'на парі', '🟢': 'вільний'}
        message_text = f''
        for i in base:
            message_text += f"{i['name']}: {i['status']} - {baseStatus[i['status']]} \n"

        self.bot.delete_message(self.call.message.chat.id, self.call.message.id)
        msg = self.bot.send_message(self.call.message.chat.id, message_text)

        self.main_menu(msg)

    def show_teacher_menu(self):
        self.bot.edit_message_text(
            text=ConstantMessages.NEXT_ACTION,
            chat_id=self.call.message.chat.id,
            message_id=self.call.message.id,
            reply_markup=Keypads.TEACHER_MENU,
        )

    def get_teacher_verify_reset(self):
        self.teacher_base_reset.update({self.call.message.chat.id: {}})
        self.teacher_base_reset[self.call.message.chat.id].update({"id": 1})

        self.bot.send_message(
            chat_id=self.call.message.chat.id,
            text=ConstantMessages.TEACHER_ID,
            reply_markup=Keypads.CANCEL,
        )

    def get_teacher_verify_message(self):
        self.bot.send_message(
            chat_id=self.call.message.chat.id,
            text=ConstantMessages.TEACHER_ID,
            reply_markup=Keypads.CANCEL,
        )
        self.bot.delete_message(self.call.message.chat.id, self.call.message.id)

        self.teacher_message.update({self.call.message.chat.id: {}})
        self.teacher_message[self.call.message.chat.id].update({"isLog": False})

    def get_teacher_verify_call(self):
        self.bot.send_message(
            chat_id=self.call.message.chat.id,
            text=ConstantMessages.TEACHER_ID,
            reply_markup=Keypads.CANCEL,
        )
        self.bot.delete_message(self.call.message.chat.id, self.call.message.id)

        self.teacher_call.update({self.call.message.chat.id: {}})
        self.teacher_call[self.call.message.chat.id].update({"isLog": False})

    def admin_quit(self):
        if self.call.message.chat.id in self.admin_base:
            self.bot.send_message(
                chat_id=self.call.message.chat.id,
                text=ConstantMessages.ADMIN_QUIT,
            )
            del (self.admin_base[self.call.message.chat.id])
        else:
            self.bot.send_message(
                chat_id=self.call.message.chat.id,
                text=ConstantMessages.NO_IN_ADMIN,
            )

    def admin_reset_id(self):
        if self.call.message.chat.id in self.admin_base:
            self.bot.send_message(self.call.message.chat.id, "ID")
            self.admin_base[self.call.message.chat.id]["id"] = True
            self.admin_base[self.call.message.chat.id]["pib"] = False
            self.admin_base[self.call.message.chat.id]["id-message"] = False
            self.admin_base[self.call.message.chat.id]["delete"] = False
        else:
            self.bot.send_message(
                chat_id=self.call.message.chat.id,
                text=ConstantMessages.NO_VERIFY,
            )

    def admin_reset_pib(self):
        if self.call.message.chat.id in self.admin_base:
            self.bot.send_message(self.call.message.chat.id, "Ім'я, прізвище")
            self.admin_base[self.call.message.chat.id]["pib"] = True
            self.admin_base[self.call.message.chat.id]["id"] = False
            self.admin_base[self.call.message.chat.id]["id-message"] = False
            self.admin_base[self.call.message.chat.id]["delete"] = False
        else:
            self.bot.send_message(
                chat_id=self.call.message.chat.id,
                text=ConstantMessages.NO_VERIFY,
            )

    def admin_send_message(self):
        if self.call.message.chat.id in self.admin_base:
            base = json.load(codecs.open("message.json", 'r', 'utf-8-sig'))
            # print(base)
            for i in base:
                if not i['status']:
                    self.bot.send_message(self.call.message.chat.id,
                                          'mainIDMessage: ' + str(i['mainIDMessage']) + '\n' + "id: " + str(
                                              i["id"]) + '\n' + 'username: ' + str(
                                              i['username']) + '\n' + 'From: ' + i[
                                              'from'] + '\n' + 'Message: ' + i['message'])

            self.bot.send_message(self.call.message.chat.id, "mainIDMessage / ID user / message")
            self.admin_base[self.call.message.chat.id]["id-message"] = True
            self.admin_base[self.call.message.chat.id]["pib"] = False
            self.admin_base[self.call.message.chat.id]["id"] = False
            self.admin_base[self.call.message.chat.id]["delete"] = False
        else:
            self.bot.send_message(
                chat_id=self.call.message.chat.id,
                text=ConstantMessages.NO_VERIFY,
            )

    def admin_delete_account(self):
        if self.call.message.chat.id in self.admin_base:
            self.bot.send_message(self.call.message.chat.id, "Ім\'я, прізвище", reply_markup=self.cancel_key)

            self.admin_base[self.call.message.chat.id]["id-message"] = False
            self.admin_base[self.call.message.chat.id]["pib"] = False
            self.admin_base[self.call.message.chat.id]["id"] = False
            self.admin_base[self.call.message.chat.id]["delete"] = True
        else:
            self.bot.send_message(
                chat_id=self.call.message.chat.id,
                text=ConstantMessages.NO_VERIFY,
            )

    def admin_black_list(self):
        if self.call.message.chat.id in self.admin_base:
            self.bot.send_message(
                chat_id=self.call.message.chat.id,
                text="ID / reason (айдішник юзера / причина його бану *для особливих)",
                reply_markup=Keypads.CANCEL,
            )

            self.admin_base[self.call.message.chat.id]["id-message"] = False
            self.admin_base[self.call.message.chat.id]["pib"] = False
            self.admin_base[self.call.message.chat.id]["id"] = False
            self.admin_base[self.call.message.chat.id]["delete"] = False
            self.admin_base[self.call.message.chat.id]["kill"] = True

        else:
            self.bot.send_message(
                chat_id=self.call.message.chat.id,
                text=ConstantMessages.NO_VERIFY,
            )

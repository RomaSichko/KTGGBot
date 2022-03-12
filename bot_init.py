from random import randint

import telebot
import changePass
import os
import codecs
from telebot import types
import json
import base_commands
import key
from constants import ConstantMessages, Keypads


class KTGGFunctions:

    def __init__(self, bot: telebot.TeleBot):
        self.bot = bot

        self.user_base_reset = {}
        self.teacher_base_reset = {}
        self.base_message = {}
        self.teacher_message = {}
        self.teacher_call = {}
        self.admin_base = {}
        self.mainIDMessage = json.load(codecs.open("message.json", 'r', 'utf-8-sig'))[-1]['mainIDMessage'] + 1
        self.mailAuth = {}
        self.teamsAuth = {}
        self.lastnameNameAuth = {}

    def welcome(self, message):
        self.bot.send_message(
            chat_id=message.chat.id,
            text=ConstantMessages.START_MESSAGE,
            reply_markup=Keypads.MAIN_MENU,
        )

    def main_menu(self, message):
        self.bot.send_message(
            chat_id=message.chat.id,
            text=ConstantMessages.NEXT_ACTION,
            reply_markup=Keypads.MAIN_MENU,
        )

    def my_account(self, message):
        check = base_commands.check_user_in_base(message.chat.id)

        temp_keypad = Keypads.ACCOUNT_MENU
        if check:
            if base_commands.get_valid_teams(message.chat.id):
                temp_keypad.row(
                    telebot.types.InlineKeyboardButton('Скинути пароль', callback_data='acc-password')
                )

        else:
            base_commands.add_data(message.chat.id, message.chat.username)
            self.bot.send_message(
                chat_id=message.chat.id,
                text=ConstantMessages.ACCOUNT_DATA_TO_DB,
            )

        user_data_in_db = base_commands.get_user_data(message.chat.id)
        self.bot.send_message(
            chat_id=message.chat.id,
            text=user_data_in_db,
            reply_markup=temp_keypad,
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

            uphoto = f"image {str(message.chat.id)}.jpg"

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
                reply_markup=Keypads.ADMIN_MENU,
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
        # Main menu
        calls = {
            "get-stud": CallHandler.get_student_ticket,
            "get-idcard": CallHandler.get_id_card,
            "rules": CallHandler.show_rules,
            "but-faq": CallHandler.show_faq,
            "reset-pass": CallHandler.choice_verify_type,
            "but-menu": CallHandler.show_menu,
            "message-admin": CallHandler.message_to_admin,
            "acc-mail": CallHandler.get_email,
            "acc-teams": CallHandler.get_teams_account,
            "acc-lastname": CallHandler.get_lastname,
            "acc-name": CallHandler.get_name,
            "acc-password": CallHandler.change_password_account,
            "admin-online": CallHandler.show_admin_online,
            "teacher": CallHandler.show_teacher_menu,
            "teacher-reset": CallHandler.get_teacher_verify_reset,
            "teacher-message": CallHandler.get_teacher_verify_message,
            "teacher-call": CallHandler.get_teacher_verify_call,
            "admin-quit": CallHandler.admin_quit,
            "admin-id": CallHandler.admin_reset_id,
            "admin-pib": CallHandler.admin_reset_pib,
            "admin-send": CallHandler.admin_send_message,
            "admin-delete": CallHandler.admin_delete_account,
            "admin-kill": CallHandler.admin_black_list,
        }

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

    def remove_from_dict(self, message):
        msg = self.bot.send_message(
            chat_id=message.chat.id,
            text=ConstantMessages.NEXT_ACTION,
            reply_markup=Keypads.REMOVE,
        )
        self.main_menu(msg)

        if message.chat.id in self.user_base_reset:
            try:
                del (self.user_base_reset[message.chat.id])
                del (self.base_message[message.chat.id])
                del (self.teacher_message[message.chat.id])
                del (self.teacher_call[message.chat.id])
                del (self.teacher_base_reset[message.chat.id])
                del (self.mailAuth[message.chat.id])
                del (self.lastnameNameAuth[message.chat.id])
                del (self.teamsAuth[message.chat.id])
            except KeyError:
                pass

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


class MessageHandler(KTGGFunctions):
    pass


class CallHandler(KTGGFunctions):

    def __init__(self, call, bot: telebot.TeleBot):
        super().__init__(bot)
        self.call = call

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

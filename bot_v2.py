# -*- coding: utf-8 -*-
import telebot

import key
from bot_init import KTGGFunctions

# test bot
bot = telebot.TeleBot(key.get_main_bot_api())

ktgg_bot = KTGGFunctions(bot)


@bot.message_handler(commands=["start"])
def send_welcome(message):
    """Trigger for command start"""
    ktgg_bot.welcome(message)


@bot.message_handler(commands=["menu"])
def main_menu(message):
    """Trigger for command menu"""
    ktgg_bot.main_menu(message)


@bot.message_handler(commands=["account"])
def my_account(message):
    """Trigger for command account"""
    ktgg_bot.my_account(message)


@bot.message_handler(commands=["account_work"])
def work_account(message):
    """Trigger for command account_work"""
    ktgg_bot.work_account(message)


@bot.message_handler(content_types=["photo"])
def photo(message):
    """Trigger for photo message"""
    ktgg_bot.action_photo(message)


@bot.message_handler(commands=["admin_panel"])
def admin_panel(message):
    """Trigger for command admin_panel"""
    ktgg_bot.admin_panel(message)


@bot.message_handler(commands=["switch"])
def switch_dbs(message):
    """Trigger for command admin_panel"""
    ktgg_bot.switch_db(message)


@bot.callback_query_handler(func=lambda call: True)
def callback_messages(call):
    """Trigger for calls"""
    ktgg_bot.callback_worker(call)


@bot.message_handler(content_types=["text"])
def text_messages(message):
    """Trigger for text messages"""
    ktgg_bot.text_handler(message)


@bot.message_handler(content_types=["document"])
def document_message(document):
    ktgg_bot.action_document(document)


@bot.message_handler(content_types=["sticker"])
def sticker_messages(sticker):
    """Trigger for stickers"""
    ktgg_bot.verify_sticker(sticker)


bot.infinity_polling()

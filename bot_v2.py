# -*- coding: utf-8 -*-

from random import randint
import telebot
import changePass
import os
import codecs
from datetime import datetime
from telebot import types
import json
import key
import picture_generator as pg
from bot_init import KTGGFunctions

# test bot
bot = telebot.TeleBot(key.get_test_bot_api())

KTGG_bot = KTGGFunctions(bot)


def delete_contact(msg):
    bot.delete_message(msg.chat.id, msg.id)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    KTGG_bot.welcome(message)


@bot.message_handler(commands=['menu'])
def main_menu(message):
    KTGG_bot.main_menu(message)


@bot.message_handler(commands=['account'])
def my_account(message):
    KTGG_bot.my_account(message)


@bot.message_handler(content_types=['photo'])
def photo(message):
    KTGG_bot.action_photo(message)


@bot.message_handler(commands=['admin_panel'])
def admin_panel(message):
    KTGG_bot.admin_panel(message)


@bot.message_handler(commands=['setstatus'])
def status(message):
    KTGG_bot.status(message)


@bot.message_handler(commands=['csc'])
def csc(message):
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton('Помітити, як виконане', callback_data='csc-finish')
    )
    bot.send_photo(message.chat.id, pg.generate(message), 'Твої завдання на сьогодні')
    bot.send_message(message.chat.id, 'Test')
    pass


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    KTGG_bot.callback_worker(call)


@bot.message_handler(content_types=['text'])
def reset_idcard(message):
    KTGG_bot.text_handler(message)


bot.infinity_polling()

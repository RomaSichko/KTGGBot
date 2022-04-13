# -*- coding: utf-8 -*-

import telebot
import key
from bot_init import KTGGFunctions

# test bot
bot = telebot.TeleBot(key.get_test_bot_api())

ktgg_bot = KTGGFunctions(bot)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    ktgg_bot.welcome(message)


@bot.message_handler(commands=['menu'])
def main_menu(message):
    ktgg_bot.main_menu(message)


@bot.message_handler(commands=['account'])
def my_account(message):
    ktgg_bot.my_account(message)


@bot.message_handler(commands=['account_work'])
def work_account(message):
    ktgg_bot.my_account(message)


@bot.message_handler(content_types=['photo'])
def photo(message):
    ktgg_bot.action_photo(message)


@bot.message_handler(commands=['admin_panel'])
def admin_panel(message):
    ktgg_bot.admin_panel(message)


@bot.message_handler(commands=['admin_panel_tasks'])
def admin_panel_tasks(message):
    ktgg_bot.admin_panel(message)


@bot.message_handler(commands=['admin_panel_danger'])
def admin_panel_danger(message):
    ktgg_bot.admin_panel(message)


@bot.message_handler(commands=['switch'])
def switch_dbs(message):
    ktgg_bot.switch_db(message)


@bot.callback_query_handler(func=lambda call: True)
def callback_messages(call):
    ktgg_bot.callback_worker(call)


@bot.message_handler(content_types=['text'])
def text_messages(message):
    ktgg_bot.text_handler(message)


bot.infinity_polling()

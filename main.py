# -*- coding: utf-8 -*-
"""
Created on 2020-04-09
@author: Bruno Arine
"""

from telegram.ext import Updater, CommandHandler
import pickle
import os
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def _read_user_data(chat_id):
    stocks_file = "userdata/{}.p".format(chat_id)
    try:
        user_data = pickle.load(open(stocks_file, "rb"))
    except IOError:
        user_data = {}
    return user_data


def _list_user_stocks(chat_id):
    user_data = _read_user_data(chat_id)
    stocks_list = ["{} {}".format(symbol, trigger) \
                   for (symbol, trigger) in user_data.items()]
    return "\n".join(stocks_list)

def _write_user_data(chat_id, dictionary):
    stocks_file = "userdata/{}.p".format(chat_id)
    pickle.dump(dictionary, open(stocks_file, "wb"))
    print("Writing to {}".format(stocks_file))

          
def start(update, context):
    print("Starting chat with {}".format(update.effective_chat.id))
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Eu sou um bot, pfv fale comigo!")

def hello(update, context):
    update.message.reply_text('Olá {}'.format(update.message.from_user.first_name))


def list(update, context):
    user_stocks = _list_user_stocks(update.effective_chat.id)
    update.message.reply_text(user_stocks)


def add(update, context):    
    user_data = _read_user_data(update.effective_chat.id)
    symbol = context.args[0]
    trigger = context.args[1]
    user_data[symbol] = trigger
    _write_user_data(update.effective_chat.id, dictionary=user_data)
    update.message.reply_text("Ação adicionada na lista de monitoramento.")

          
def remove(update, context):
    user_data = _read_user_data(update.effective_chat.id)
    symbol = context.args[0]
    try:
        del user_data[symbol]
        _write_user_data(update.effective_chat.id, dictionary=user_data)
        update.message.reply_text("Ativo removido com sucesso.")
    except KeyError:
        update.message.reply_text("Erro: esse ativo não está na sua lista.")


def reset(update, context):
    stocks_file = "userdata/{}.p".format(chat_id)
    if os.path.exists(stocks_file):
        os.remove(stocks_file)
        update.message.reply_text("Lista apagada com sucesso.")
    else:
        update.message.reply_text("Sua lista já está zerada.")
        


with open('../telegram_bot_token.txt') as f:
    bot_token = f.readline().strip()
    
updater = Updater(bot_token, use_context=True)

updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('list', list))
updater.dispatcher.add_handler(CommandHandler('add', add))
updater.dispatcher.add_handler(CommandHandler('remove', remove))
updater.dispatcher.add_handler(CommandHandler('reset', reset))


updater.start_polling()
updater.idle()

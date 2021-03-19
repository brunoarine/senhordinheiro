# -*- coding: utf-8 -*-
"""
Created on 2020-04-09
@author: Bruno Arine
"""

import requests
from pandas_datareader import data as pdr
from datetime import date
import pickle




with open('../telegram_bot_token.txt') as f:
    bot_token = f.readline().strip()


def telegram_bot_sendtext(bot_message, bot_token, bot_chatid):
    send_text = 'https://api.telegram.org/bot' + bot_token + \
        '/sendMessage?chat_id=' + bot_chatid + \
        '&parse_mode=Markdown&text=' + bot_message
    if bot_message != "":
        response = requests.get(send_text)
        return response.json()
    else:
        return


def check_stock_target(chatid):
    '''
    Extracts stocks data from Yahoo Finance according to a list of symbols and
    their respective triggers inside a custom user file.
    '''
    stocks_file = "userdata/{}.p".format(chatid)
    try:
        user_data = pickle.load(open(stocks_file, "rb"))
    except IOError:
        return

    # initial state: no target has been hit
    reached_target = False

    symbols = user_data.keys()
    operators = [x[0] for x in user_data.values()]
    targets = [float(x[1:]) for x in user_data.values()]
    web_data = pdr.get_data_yahoo(symbols,
                                  start=date.today(),
                                  end=date.today())
    prices = (web_data["Close"]).round(2)

    zipped_data = zip(symbols, prices[symbols].values[0], operators, targets)
    for symbol, price, operator, target in zipped_data:
        if (operator == ">") and (price > target):
            reached_target = True
        elif (operator == "<") and (price < target):
            reached_target = True
        if reached_target:
            message = "O preço atual de " + symbol + " é " \
                + str(price) + " (o gatilho era " \
                + operator + str(target) + ")"
            telegram_bot_sendtext(message)
    return message


bot_chatid = '464941059'

check_stock_target(bot_chatid)

import telebot
from telebot import types
import config
import requests
import json
import time

bot = telebot.TeleBot(config.TOKEN)

# словарь с аккаунтами, которые подключены к боту
# у каждого usera: coin_unit = '', menu_funk = '', level = '', language = ''
users = {}

#подключение кнопок к боту
# кнонки основного меню - level 1
markup_main = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
itembtn1_main = types.KeyboardButton('Binance')
itembtn2_main = types.KeyboardButton('Help')
itembtn3_main = types.KeyboardButton('CoinMarketCap')
#itembtn4_main = types.KeyboardButton('Ethplorer')
markup_main.add(itembtn1_main, itembtn2_main, itembtn3_main) #, itembtn4_main)

# кнопки после нажатия на Binance - level 2
markup_binance = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
itembtn1_binance = types.KeyboardButton('BTC')
itembtn2_binance = types.KeyboardButton('ETH')
itembtn3_binance = types.KeyboardButton('USDT')
itembtn4_binance = types.KeyboardButton('BNB')
itembtn5_binance = types.KeyboardButton('Назад')
markup_binance.add(itembtn1_binance, itembtn2_binance, itembtn3_binance, itembtn4_binance, itembtn5_binance)

markup_binance_us = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
itembtn1_binance = types.KeyboardButton('BTC')
itembtn2_binance = types.KeyboardButton('ETH')
itembtn3_binance = types.KeyboardButton('USDT')
itembtn4_binance = types.KeyboardButton('BNB')
itembtn5_binance = types.KeyboardButton('Назад')
markup_binance_us.add(itembtn1_binance, itembtn2_binance, itembtn3_binance, itembtn4_binance, itembtn5_binance)

# кнопка назад
markup_backward = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
itembtn_backward = types.KeyboardButton('Назад')
markup_backward.add(itembtn_backward)

markup_backward_us = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
itembtn_backward = types.KeyboardButton('Назад')
markup_backward_us.add(itembtn_backward)

# кнопки для С
# главное меню
markup_C = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
itembtn1_C = types.KeyboardButton('ТОП')
itembtn2_С = types.KeyboardButton('Назад')
markup_C.add(itembtn1_C, itembtn2_С)

markup_C_us = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
itembtn1_C = types.KeyboardButton('TOP')
itembtn2_С = types.KeyboardButton('Back')
markup_C_us.add(itembtn1_C, itembtn2_С)

# меню с ТОП
markup_C1_TOP = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
itembtn1_C1_TOP = types.KeyboardButton('ТОП-10')
itembtn2_C1_TOP = types.KeyboardButton('ТОП-50')
itembtn3_C1_TOP = types.KeyboardButton('ТОП-100')
itembtn4_С1_TOP = types.KeyboardButton('Назад')
markup_C1_TOP.add(itembtn1_C1_TOP, itembtn2_C1_TOP, itembtn3_C1_TOP, itembtn4_С1_TOP)

markup_C1_TOP_us = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
itembtn1_C1_TOP = types.KeyboardButton('TOP-10')
itembtn2_C1_TOP = types.KeyboardButton('TOP-50')
itembtn3_C1_TOP = types.KeyboardButton('TOP-100')
itembtn4_С1_TOP = types.KeyboardButton('Back')
markup_C1_TOP_us.add(itembtn1_C1_TOP, itembtn2_C1_TOP, itembtn3_C1_TOP, itembtn4_С1_TOP)

# кнопки с языком
markup_language = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
itembtn1_language = types.KeyboardButton('Eng')
itembtn2_language = types.KeyboardButton('Ru')
markup_language.add(itembtn1_language, itembtn2_language)


# оброботчик /start
@bot.message_handler(commands=['start'])
def handle_language(message):
    if not (message.chat.id == users):
        users[message.chat.id] = {'coin_unit':' ', 'menu_funk':' ', 'level':'', 'language':''}
    # изначальный уровень "" со стандартными настройками
    users[message.chat.id]['menu_funk'] = '1'
    users[message.chat.id]['level'] = '1'
    users[message.chat.id]['coin_unit'] = '1'
    users[message.chat.id]['language'] = '1'
    msg = bot.send_message(message.chat.id, 'Language',reply_markup=markup_language)
    bot.register_next_step_handler(msg, handler_start)

def handler_start(message):
    if message.text == 'Ru':
        users[message.chat.id]['language'] = 'Ru'
    else:
        users[message.chat.id]['language'] = 'Eng'

    text = ''
    if users[message.chat.id]['language'] == 'Ru':
        text = "Выбери интересующую функцию в меню \n"
    else:
        text = "Select the function of interest in the menu \n"

    msg = bot.send_message(message.chat.id, text, reply_markup=markup_main)
    bot.register_next_step_handler(msg, funk_handler_makup)



# оброботчик /help
# Забыл что я могу делать? Все очень просто. У меня есть есть две функции:
# 1. Binance - с помощью биржы Binance ты можешь узнать стоимость монеты относительно BTC/ETH/USTD/BNB. Для этого просто введи название монеты
# заглавными буквами (напр., EOS)
# 2. Coinmarketcap - тут ты можешь узнать ТОП монет

@bot.message_handler(commands=['help'])
def handler_help(message):

    text = ''
    if users[message.chat.id]['language'] == 'Ru':
        text = "Забыл что я могу делать? \n\nВсе очень просто. У меня  есть две функции: \n" \
               "1. Binance - с помощью биржи Binance ты можешь узнать стоимость монеты относительно BTC/ETH/USTD/BNB. \n" \
               "2. CoinMarketCap - с помощью данного сервиса ТОП монет по рыночной капитализации."
    else:
        text = "You forgot what I can do? \n\nEverything is very simple. I have two functions: \n" \
               "1. Binance - with the help of the Binance Exchange you can find out the cost of the coin relatively to BTC/ETH/USTD/BNB. \n" \
               "2. CoinMarketCap - with the help of this service TOP coins by market capitalization."

    bot.send_message(message.chat.id, text)
    time.sleep(3)
    handler_start(message)

# запись json ответа от telegram в файл
def write_json(data, filename='answer.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

#.....................................................................................................................
#
#                                                      ВЕТКА Binance
#
#.....................................................................................................................

# парсер монет с биржи Binance
def parse_price(binance):
    btc = float(binance[11]['lastPrice'])
    eth = float(binance[12]['lastPrice'])
    bnb = float(binance[98]['lastPrice'])
    price = {}
    len_end = 3
    for i in range(370):
        len_str = len(binance[i]['symbol'])
        symbol = binance[i]['symbol']

        if symbol[len_str - 3: len_str] == 'SDT':
            len_end = 4
        else:
            len_end = 3

        coin_unit = symbol[len_str - len_end: len_str]
        coin = symbol[0:len_str - len_end]

        cost = float("{0:.6f}".format(float(binance[i]["lastPrice"])))
        if not (coin in price):
            price[coin] = {'BTC': '', 'USDT': '', 'ETH': '', 'BNB': ''}

        if coin_unit == 'BTC' and not (coin == 'BTC'):
            coin_usdt = float("{0:.6f}".format(cost * btc))
            coin_eth = float("{0:.6f}".format(coin_usdt / eth))
            coin_bnb = float("{0:.6f}".format(coin_usdt / bnb))

            price[coin]['BTC'] = str(cost)
            price[coin]['USDT'] = str(coin_usdt)
            price[coin]['ETH'] = str(coin_eth)
            price[coin]['BNB'] = str(coin_bnb)

        price[coin][coin_unit] = str(cost)

    return price
    #print(price)

# функции оброботчики ответа Binance
# запись ответа на запрос (стоимость монеты с Binance)
def resp(req, price, message):
    res = 'Binance: \n'
    if users[message.chat.id]['coin_unit'] == 'BTC':
        res += price[req]['BTC'] + ' '+ req + '/BTC'
    elif users[message.chat.id]['coin_unit'] == 'ETH':
        res += price[req]['ETH'] + ' '+ req + '/ETH'
    elif users[message.chat.id]['coin_unit'] == 'BNB':
        res += price[req]['BNB'] + ' '+ req + '/BNB'
    elif users[message.chat.id]['coin_unit'] == 'USDT':
        res += price[req]['USDT'] + ' '+ req + '/USDT'
    return res

# функция оброботчик кнопки 'Назад' или 'ввода монеты' ответ с биржы Binance
def handler_binance(message):
    if  not (message.text == 'Назад'):
        req = str(message.text)
        if req.islower():

            text = ''
            if users[message.chat.id]['language'] == 'Ru':
                text = "В следующий раз введи название монеты в верхнем регистре.\nПодождите..."
            else:
                text = "Next, enter the name of the coin in uppercase.\nWait, please..."

            bot.send_message(message.chat.id, text)
            write_json(message.text)
            req = req.upper()

        if config.name.get(req) == None:

            text = ''
            if users[message.chat.id]['language'] == 'Ru':
                text = "Такой монеты нет. Сделай запрос заново."
            else:
                text = "There is no such coin. Make a request again."

            bot.send_message(message.chat.id, text)
            write_json(message.text)
        else:
            url = "https://api.binance.com/api/v1/ticker/24hr"
            r = requests.get(url).json()
            price = parse_price(r)
            res = resp(req, price, message)
            bot.send_message(message.chat.id, res)
            write_json(r)

            time.sleep(3)

            text = ''
            if users[message.chat.id]['language'] == 'Ru':
                text = "Введите монету..."
                msg = bot.send_message(message.chat.id, text, reply_markup=markup_backward)
                bot.register_next_step_handler(msg, handler_binance)
            else:
                text = "Enter a coin..."
                msg = bot.send_message(message.chat.id, text, reply_markup=markup_backward_us)
                bot.register_next_step_handler(msg, handler_binance)



    elif (message.text == 'Назад') or (message.text == 'Back'):
        users[message.chat.id]['coin_unit'] = '1'
        users[message.chat.id]['level'] = 'B'
        funk_handler_binance(message)
    else:
        text = ''
        if users[message.chat.id]['language'] == 'Ru':
            text = "Ввели не ту команду"
        else:
            text = "Enter the wrong team"

        bot.send_message(message.chat.id, text)

def funk_coin_unit(message):
    if message.text == 'Назад' or (message.text == 'Back'):
        users[message.chat.id]['menu_funk'] = '1'
        users[message.chat.id]['coin_unit'] = '1'
        users[message.chat.id]['level'] = '1'
        handler_start(message)
    else:
        users[message.chat.id]['level'] = 'B1'
        users[message.chat.id]['coin_unit'] = message.text

        text = ''
        if users[message.chat.id]['language'] == 'Ru':
            text = "Введите монету..."
            msg = bot.send_message(message.chat.id, text, reply_markup=markup_backward)
            bot.register_next_step_handler(msg, handler_binance)
        else:
            text = "Enter a coin..."
            msg = bot.send_message(message.chat.id, text, reply_markup=markup_backward_us)
            bot.register_next_step_handler(msg, handler_binance)

def funk_handler_binance(message):

    text = ''
    if users[message.chat.id]['language'] == 'Ru':
        text = 'В меню выберите относительно чего хотите выразить монету, либо вернитесь ' \
               'в главное меню с помощью кнопки \'Назад\''
        msg = bot.send_message(message.chat.id, text, reply_markup=markup_binance)
        bot.register_next_step_handler(msg, funk_coin_unit)
    else:
        text = 'In the menu, choose whether you want to express a coin or return ' \
               'to the main menu using the button \'Назад\''
        msg = bot.send_message(message.chat.id, text, reply_markup=markup_binance_us)
        bot.register_next_step_handler(msg, funk_coin_unit)



#.....................................................................................................................
#
#                                                      ВЕТКА CoinMarketCap
#
#.....................................................................................................................

# coindmarketcap_top: https://api.coinmarketcap.com/v2/ticker/?start=101&limit=10&sort=id&structure=array
# start - начиная с какого брать ТОП
# limit - сколько брать топ, начиная со start (если его не писать, то по умолчанию 0)
# structure - структура массив

url_coinmarket_top = 'https://api.coinmarketcap.com/v2/ticker/?limit=100&structure=array'

def funk_resp_top(message, num, r):
    string = ''
    r_data = r['data']
    for i in range(num):
        string += r_data[i]['symbol'] + ' : $' + str( r_data[i]["quotes"]["USD"]["market_cap"] ) + '\n'
    bot.send_message(message.chat.id, string)

    text = ''
    if users[message.chat.id]['language'] == 'Ru':
        text = 'Выберите количество ТОП первых монет'
        msg = bot.send_message(message.chat.id, text, reply_markup=markup_C1_TOP)
        bot.register_next_step_handler(msg, funk_hadler_top)
    else:
        text = 'Select the number of TOP first coins'
        msg = bot.send_message(message.chat.id, text, reply_markup=markup_C1_TOP_us)
        bot.register_next_step_handler(msg, funk_hadler_top)



def funk_hadler_top(message):
    if message.text == 'ТОП-10' or message.text == 'TOP-10':
        r = requests.get(url_coinmarket_top).json()
        funk_resp_top(message, 10, r)
    elif message.text == 'ТОП-50' or message.text == 'TOP-50':
        r = requests.get(url_coinmarket_top).json()
        funk_resp_top(message, 50, r)
    elif message.text == 'ТОП-100' or message.text == 'TOP-100':
        r = requests.get(url_coinmarket_top).json()
        funk_resp_top(message, 100, r)
    elif message.text == 'Назад' or message.text == 'Back':
        users[message.chat.id]['level'] = 'C'
        users[message.chat.id]['menu_funk'] = 'CoinMarketCap'
        users[message.chat.id]['coin_unit'] = '1'
        funk_handler_coinmarketcap(message)
    else:
        pass


def funk_coinmarketcap_menu(message):
    if message.text == 'Назад' or message.text == 'Back':
        users[message.chat.id]['level'] = '1'
        users[message.chat.id]['menu_funk'] = '1'
        users[message.chat.id]['coin_unit'] = '1'
        handler_start(message)
    elif message.text == 'ТОП' or message.text == 'TOP':
        users[message.chat.id]['level'] = 'C1_ТОП'
        users[message.chat.id]['menu_funk'] = 'CoinMarketCap'
        users[message.chat.id]['coin_unit'] = '1'

        text = ''
        if users[message.chat.id]['language'] == 'Ru':
            text = 'Выберите количество ТОП первых монет'
            msg = bot.send_message(message.chat.id, text, reply_markup=markup_C1_TOP)
            bot.register_next_step_handler(msg, funk_hadler_top)
        else:
            text = 'Select the number of TOP first coins'
            msg = bot.send_message(message.chat.id, text, reply_markup=markup_C1_TOP_us)
            bot.register_next_step_handler(msg, funk_hadler_top)
    else:
        text = ''
        if users[message.chat.id]['language'] == 'Ru':
            text = 'Вы ввели не правильную функцию! Выберите функцию или вернитесь назад'
            msg = bot.send_message(message.chat.id, text, reply_markup=markup_C)
            bot.register_next_step_handler(msg, funk_coinmarketcap_menu)
        else:
            text = 'You entered the wrong function! Select function or go back'
            msg = bot.send_message(message.chat.id, text, reply_markup=markup_C_us)
            bot.register_next_step_handler(msg, funk_coinmarketcap_menu)



def funk_handler_coinmarketcap(message):

    text = ''
    if users[message.chat.id]['language'] == 'Ru':
        text = 'В меню выберите функцию или вернитесь назад'
        msg = bot.send_message(message.chat.id, text, reply_markup=markup_C)
        bot.register_next_step_handler(msg, funk_coinmarketcap_menu)
    else:
        text = 'From the menu, select a function or go back'
        msg = bot.send_message(message.chat.id, text, reply_markup=markup_C_us)
        bot.register_next_step_handler(msg, funk_coinmarketcap_menu)


#.....................................................................................................................
#
#                                                      ВЕТКА Ethplorer
#
#.....................................................................................................................

# комер кошелька ethplorer: http://api.ethplorer.io/getAddressInfo/TOKEN?apiKey=freekey

url_ethplorer = 'http://api.ethplorer.io/getAddressInfo/'

def funk_ethplorer_menu(message):
    if message.text == 'Назад' or message.text == 'Back':
        handler_start(message)
    else:
        string = 'Token Balances: \n\n'
        url_ethplorer_coin = url_ethplorer + message.text + '?apiKey=freekey'
        r = requests.get(url_ethplorer_coin).json()
        #write_json(r)
        string += 'ETH: ' + str(r['ETH']['balance']) + '\n\n'
        print(len(r['tokens']))
        for i in range( len(r['tokens']) ):
            string += r['tokens'][i]['tokenInfo']['symbol'] + ' = '
            balance = r['tokens'][i]['balance']
            # string += '( ' + str(r['tokens'][i]['balance']) + ')'
            if balance >= 10**18:
                balance /= 10**18
            if balance > 10 ** 8:
                balance /= 10 * 8
            elif balance == 10 ** 8:
                balance /= 10 ** 4
            string += str( balance ) + '\n'

        #print(string)
        bot.send_message(message.chat.id, string)
        funk_handler_ethplorer(message)




def funk_handler_ethplorer(message):

    text = ''
    if users[message.chat.id]['language'] == 'Ru':
        text = 'Введите номер Вашего кошелька'
        msg = bot.send_message(message.chat.id, text, reply_markup=markup_backward)
        bot.register_next_step_handler(msg, funk_ethplorer_menu)
    else:
        text = 'Enter the number of your wallet'
        msg = bot.send_message(message.chat.id, text, reply_markup=markup_backward_us)
        bot.register_next_step_handler(msg, funk_ethplorer_menu)



#.....................................................................................................................
#
#                                                      ОСНОВНОЕ МЕНЮ
#
#.....................................................................................................................


# функция обробочик основного меню (Binance, CoinMarketCap и help)
def funk_handler_makup(message):
    if message.text == 'Binance':
        users[message.chat.id]['menu_funk'] = 'Binance'
        users[message.chat.id]['level'] = 'B'
        users[message.chat.id]['coin_unit'] = '1'
        types.ReplyKeyboardRemove(selective=False)
        funk_handler_binance(message)
    elif  message.text == 'CoinMarketCap':
        users[message.chat.id]['menu_funk'] = 'CoinMarketCap'
        users[message.chat.id]['menu_funk'] = 'C'
        users[message.chat.id]['coin_unit'] = '1'
        types.ReplyKeyboardRemove(selective=False)
        funk_handler_coinmarketcap(message)
    elif message.text == 'Ethplorer':
        users[message.chat.id]['menu_funk'] = 'Ethplorer'
        users[message.chat.id]['menu_funk'] = 'E'
        users[message.chat.id]['coin_unit'] = '1'
        types.ReplyKeyboardRemove(selective=False)
        funk_handler_ethplorer(message)
    elif message.text == 'Help':
        users[message.chat.id]['menu_funk'] = 'Help'
        users[message.chat.id]['menu_funk'] = 'H'
        users[message.chat.id]['coin_unit'] = '1'
        types.ReplyKeyboardRemove(selective=False)
        handler_help(message)
    else:

        text = ''
        if users[message.chat.id]['language'] == 'Ru':
            text = 'Вы ввели не правильную функцию! Выберите нужную функцию'
        else:
            text = 'You entered the wrong function! Select the desired function'

        msg = bot.send_message(message.chat.id, text, reply_markup=markup_main)
        bot.register_next_step_handler(msg, handler_start)


# оброботчик 'text'
@bot.message_handler(content_types=['text'])
def handler_text(message):
    if users[message.chat.id]['level'] == '1':
        handler_start(message)
    elif users[message.chat.id]['level'] == 'B':
        funk_handler_binance(message)
    elif users[message.chat.id]['level'] == 'B1':
        handler_binance(message)
    else:

        text = ''
        if users[message.chat.id]['language'] == 'Ru':
            text = 'Что-то пошло не так :('
        else:
            text = 'Something went wrong :('

        bot.send_message(message.chat.id, text)


while True:
    try:
        bot.polling()
    except Exception:
        time.sleep(15)

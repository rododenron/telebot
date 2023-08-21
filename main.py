import telebot
import configparser

from extensions import ConversionException, APILayerException, APILayer, Utils


config = configparser.ConfigParser()
config.read("config.ini")
token = config.get('secrets', 'token')
apikey = config.get('secrets', 'apikey')


bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = ('Чтобы начать работу введите команду в следующем формате: \n <имя валюты> <в какую валюту перевести>' \
            ' <количество переводимой валюты>')


    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    currencies = APILayer.get_values(apikey=apikey)
    currencies_list = telebot.util.split_string(str(currencies), 3000)
    for part in currencies_list:
        bot.reply_to(message, part)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    message_text = message.text
    try:
        Utils.check_input(message_text, APILayer.get_values(apikey=apikey))
        currency_from, currency_to, amount = message.text.split(' ')
        text = APILayer.get_price(currency_from, currency_to, amount, apikey)
        bot.reply_to(message, text)
    except ConversionException as e:
        bot.reply_to(message, e)
    except APILayerException as e:
        bot.reply_to(message, e)
    except Exception as e:
        bot.reply_to(message, e)


bot.polling()

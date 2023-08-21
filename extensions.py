import requests
import json


class ConversionException(BaseException):
    def __int__(self):
        pass


class APILayerException(BaseException):
    def __int__(self):
        pass


class APILayer:
    @staticmethod
    def get_price(currency_to: str, currency_from: str, amount: str, apikey: str):
        ans = requests.get(f"https://api.apilayer.com/exchangerates_data/convert?to={currency_to}&from={currency_from}&amount={amount}&apikey={apikey}")
        ans_json = json.loads(ans.content)
        if ans_json.get('success', False):
            text = f"Price {amount} {currency_from} in {currency_to} is {ans_json['result']}"
        else:
            raise APILayerException(f"{ans_json['message']}")
        return text

    @staticmethod
    def get_values(apikey: str):
        ans = requests.get(f"https://api.apilayer.com/exchangerates_data/symbols?apikey={apikey}")
        ans_json = json.loads(ans.content)
        if ans_json.get('success', False):
            text = "\n".join([f"{key}: {value}" for key, value in ans_json['symbols'].items()])
        else:
            raise APILayerException(f"{ans_json['message']}")
        return text


class Utils:
    @staticmethod
    def check_input(input_string: str, template):

        if len(input_string.split(' ')) != 3:
            raise ConversionException('Неверное количество входных данных')

        currency_from, currency_to, amount = input_string.split(' ')

        if currency_from == currency_to:
            raise ConversionException(f'Невозможно перевести одинаковые валюты {currency_to}')

        if not amount.isnumeric():
            raise ConversionException(f'Невозможно конвертировать величину {amount}')

        if not (currency_to in template):
            raise ConversionException(f'Валюта не найдена {currency_to}')

        if not (currency_from in template):
            raise ConversionException(f'Валюта не найдена {currency_from}')

        return currency_from, currency_to, amount

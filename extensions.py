import json
import requests
from config import keys


class ApiException(Exception):
    pass


class ValuesConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise ApiException(f'Невозможно перевести одинаковые валюты - {base}.')
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ApiException(f'Не удалось обработать валюту - {quote}')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise ApiException(f'Не удалось обработать валюту - {base}')
        try:
            amount = float(amount)
        except ValueError:
            raise ApiException(f'Не удалось обработать колличество - {amount}')

        r = requests.get(
            f"https://v6.exchangerate-api.com/v6/81842709da87ccfb2c12a20d/pair/{quote_ticker}/{base_ticker}/"
            f"{amount}")
        total_base = json.loads(r.content)['conversion_result']

        return total_base

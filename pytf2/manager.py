import requests
from pytf2 import currency


class Manager:
    def __init__(self, cache=True, bp_api_key='', bp_user_token=''):
        self.cache = cache
        self.bp_api_key = bp_api_key
        self.bp_user_token = bp_user_token
        self.mp_item_cache = {}
        self.bp_user_cache = {}

    def clear_mp_item_cache(self):
        self.mp_item_cache = {}

    def clear_bp_user_cache(self):
        self.bp_user_cache = {}

    def bp_get_prices(self, raw=0, since=None):
        # backpack.tf docs - https://backpack.tf/api/docs/IGetPrices

        if not self.bp_api_key:
            raise ValueError("bp_api_key not set")

        data = {"key": self.bp_api_key}
        if raw:
            data["raw"] = raw
        if since:
            data["since"] = since

        response = requests.get("https://backpack.tf/api/IGetPrices/v4", data=data).json()

        if not response["response"]["success"]:
            raise Exception(response["response"]["message"])

        return response

    def bp_get_currencies(self, raw=0, parse=True):
        # backpack.tf docs - https://backpack.tf/api/docs/IGetCurrencies

        if not self.bp_api_key:
            raise ValueError("bp_api_key not set")

        data = {"key": self.bp_api_key}
        if raw:
            data["raw"] = raw

        response = requests.get("https://backpack.tf/api/IGetCurrencies/v1", data=data).json()

        if not response["response"]["success"]:
            raise Exception(response["response"]["message"])

        if not parse:
            return response

        to_return = {}

        for item in response["response"]["currencies"]:
            to_return[item] = currency.Currency(response["response"]["currencies"]["item"])

        return to_return

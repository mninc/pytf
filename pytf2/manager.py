import requests


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
        # Uses the IGetPrices API
        # Returns the raw json (too complicated for parsing

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

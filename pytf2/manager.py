import requests
from pytf2 import currency, bp_user


class Manager:
    def __init__(self, cache: bool=True, bp_api_key: str='', bp_user_token: str=''):
        self.cache = cache
        self.bp_api_key = bp_api_key
        self.bp_user_token = bp_user_token
        self.mp_item_cache = {}
        self.bp_user_cache = {}

    def clear_mp_item_cache(self):
        self.mp_item_cache = {}

    def clear_bp_user_cache(self):
        self.bp_user_cache = {}

    def bp_get_prices(self, raw: bool=0, since: int=0):
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

    def bp_get_currencies(self, raw: int=0, parse: bool=True):
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
            to_return[item] = currency.Currency(response["response"]["currencies"][item])

        return to_return

    def bp_user_info(self, steamids: list, parse: bool=True):
        # backpack.tf docs - https://backpack.tf/api/docs/user_info

        to_return = {}

        if not self.bp_api_key:
            raise ValueError("bp_api_key not set")

        steamids_str = []
        for steamid in steamids:
            steamids_str.append(str(steamid))

        for steamid in steamids_str:
            if steamid in self.bp_user_cache and parse:
                steamids_str.remove(steamid)
                to_return[steamid] = self.bp_user_cache[steamid]

        if not steamids_str:
            return to_return

        data = {"key": self.bp_api_key,
                "steamids": ",".join(steamids_str)}

        response = requests.get("https://backpack.tf/api/users/info/v1", data=data).json()

        if "message" in response:
            raise Exception(response["message"])

        if not parse:
            return response

        for steamid, data in response["users"].items():
            to_return[steamid] = bp_user.BackpackUser(data)

        if self.cache:
            for steamid, info in to_return.items():
                self.bp_user_cache[steamid] = info

        return to_return

    def bp_user_name(self, steamid):
        steamid = str(steamid)
        return self.bp_user_info([steamid])[steamid].name

    def bp_avatar(self, steamid):
        steamid = str(steamid)
        return self.bp_user_info([steamid])[steamid].avatar

    def bp_last_online(self, steamid):
        steamid = str(steamid)
        return self.bp_user_info([steamid])[steamid].last_online

    def bp_admin(self, steamid):
        steamid = str(steamid)
        return self.bp_user_info([steamid])[steamid].admin

    def bp_donated(self, steamid):
        steamid = str(steamid)
        return self.bp_user_info([steamid])[steamid].donated

    def bp_premium(self, steamid):
        steamid = str(steamid)
        return self.bp_user_info([steamid])[steamid].premium

    def bp_premium_months_gifted(self, steamid):
        steamid = str(steamid)
        return self.bp_user_info([steamid])[steamid].premium_months_gifted

    def bp_can_trade(self, steamid):
        steamid = str(steamid)
        user = self.bp_user_info([steamid])[steamid]
        if not user.bans:
            return True
        if user.bans.steamrep_scammer or user.bans.bp_bans["all"]:
            return False
        return True


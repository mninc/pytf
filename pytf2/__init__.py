import requests
from pytf2 import bp_currency, bp_user, bp_price_history, bp_classified, item_data, mp_deal, mp_item, mp_sale, \
    sr_reputation
from time import time
from lxml import html
from pytrade import EconItem


class Manager:
    def __init__(self, cache: bool = True, bp_api_key: str = '', bp_user_token: str = '', mp_api_key: str = ''):
        self.cache = cache
        self.bp_api_key = bp_api_key
        if bp_user_token:
            self.bp_user_token = bp_user_token
        else:
            self.bp_user_token = self.bp_get_user_token()
        self.mp_api_key = mp_api_key
        self.mp_item_cache = {}
        self.bp_user_cache = {}

    def clear_mp_item_cache(self):
        self.mp_item_cache = {}

    def clear_bp_user_cache(self):
        self.bp_user_cache = {}

    @staticmethod
    def st_item_to_str(item):
        name = item.market_name
        # Assume it's craftable
        craftable = True
        # Assume it's not unusual with no effect
        effect = ""
        unusual = False
        if name.startswith("Unusual "):
            unusual = True
        if item.descriptions != list():
            for line in item.descriptions:
                if line["value"] == "( Not Usable in Crafting )":
                    craftable = False
                elif line["value"].startswith("★ Unusual Effect: ") and unusual:
                    name = name[8:]
                    effect = line["value"][18:]

        # Combine craftability and effect where applicable
        if not craftable and effect:
            name = "Non-Craftable " + effect + " " + name
        elif not craftable:
            name = "Non-Craftable " + name
        elif effect:
            name = effect + " " + name
        return name

    @staticmethod
    def s_get_inventory(user_id, game=440, parse: bool = True):
        url = "http://steamcommunity.com/inventory/" + str(user_id) + "/" + str(game) + "/2?l=english&count=5000"

        response = requests.get(url).json()

        if not parse:
            return response

        to_return = []
        classid_item = {}
        for item in response["descriptions"]:
            classid_item[item["classid"]] = item

        for item in response["assets"]:
            item.update(classid_item[item["classid"]])
            item = EconItem.Item(item)
            to_return.append(item)

        return to_return

    def bp_get_prices(self, raw: bool = 0, since: int = 0):
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

    def bp_get_currencies(self, raw: int = 0, parse: bool = True):
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
            to_return[item] = bp_currency.Currency(response["response"]["currencies"][item])

        return to_return

    def bp_user_info(self, steamids: list, parse: bool = True):
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

    def bp_voting_rep(self, steamid):
        steamid = str(steamid)
        user = self.bp_user_info([steamid])[steamid]
        if not user.voting:
            return
        return user.voting.reputation

    def bp_backpack_rank(self, steamid):
        steamid = str(steamid)
        user = self.bp_user_info([steamid])[steamid]
        if not user.inventory:
            return
        if "440" not in user.inventory.inventories:
            return
        return user.inventory.inventories["440"].ranking

    def bp_backpack_value(self, steamid):
        steamid = str(steamid)
        user = self.bp_user_info([steamid])[steamid]
        if not user.inventory:
            return
        if "440" not in user.inventory.inventories:
            return
        return user.inventory.inventories["440"].value

    def bp_backpack_metal(self, steamid):
        steamid = str(steamid)
        user = self.bp_user_info([steamid])[steamid]
        if not user.inventory:
            return
        if "440" not in user.inventory.inventories:
            return
        return user.inventory.inventories["440"].metal

    def bp_backpack_keys(self, steamid):
        steamid = str(steamid)
        user = self.bp_user_info([steamid])[steamid]
        if not user.inventory:
            return
        if "440" not in user.inventory.inventories:
            return
        return user.inventory.inventories["440"].keys

    def bp_backpack_slots_total(self, steamid):
        steamid = str(steamid)
        user = self.bp_user_info([steamid])[steamid]
        if not user.inventory:
            return
        if "440" not in user.inventory.inventories:
            return
        return user.inventory.inventories["440"].slots["total"]

    def bp_backpack_slots_used(self, steamid):
        steamid = str(steamid)
        user = self.bp_user_info([steamid])[steamid]
        if not user.inventory:
            return
        if "440" not in user.inventory.inventories:
            return
        return user.inventory.inventories["440"].slots["used"]

    def bp_positive_trust(self, steamid):
        steamid = str(steamid)
        user = self.bp_user_info([steamid])[steamid]
        if not user.trust:
            return
        return user.trust.positive

    def bp_negative_trust(self, steamid):
        steamid = str(steamid)
        user = self.bp_user_info([steamid])[steamid]
        if not user.trust:
            return
        return user.trust.negative

    def bp_get_price_history(self, item, quality=None, tradable=1, craftable=1, priceindex: int = 0, appid: int = 440,
                             parse: bool = True):
        # backpack.tf docs - https://backpack.tf/api/docs/IGetPriceHistory

        if not self.bp_api_key:
            raise ValueError("bp_api_key not set")

        data = {"key": self.bp_api_key,
                "item": item,
                "tradable": tradable,
                "craftable": craftable,
                "priceindex": priceindex,
                "appid": appid}

        if quality:
            data["quality"] = quality

        response = requests.get("https://backpack.tf/api/IGetPriceHistory/v1", data=data).json()

        if not response["response"]["success"]:
            raise Exception(response["response"]["message"])

        if not parse:
            return response

        to_return = []
        for history in response["response"]["history"]:
            to_return.append(bp_price_history.PriceHistory(history))

        return to_return

    def bp_classifieds_search(self, data: dict, parse: bool = True):
        # backpack.tf docs - https://backpack.tf/api/docs/classifieds_search

        if not self.bp_api_key:
            raise ValueError("bp_api_key not set")

        data["key"] = self.bp_api_key

        response = requests.get("https://backpack.tf/api/classifieds/search/v1", data=data).json()

        if "response" in response:
            raise Exception(response["response"])

        if not parse:
            return response

        to_return = {"sell": [],
                     "buy": [],
                     "total": response["total"]}

        if response["sell"]:
            to_return["sell_total"] = response["sell"]["total"]
            to_return["sell_fold"] = response["sell"]["fold"]
            for listing in response["sell"]["listings"]:
                to_return["sell"].append(bp_classified.Classified(listing, bool(data.get("item_names", False))))
        else:
            to_return["sell_total"] = 0
            to_return["sell_fold"] = False

        if response["buy"]:
            to_return["buy_total"] = response["buy"]["total"]
            to_return["buy_fold"] = response["buy"]["fold"]
            for listing in response["buy"]["listings"]:
                to_return["buy"].append(bp_classified.Classified(listing, bool(data.get("item_names", False))))
        else:
            to_return["buy_total"] = 0
            to_return["buy_fold"] = False

        return to_return

    @staticmethod
    def bp_classified_make_data(name, user=False, unusual: bool = False, set_elevated=False, page_size=10, fold=1):
        # Take off any unneccesary prefixes
        if name[:4] == "The ":
            name = name[4:]
        if name[:14] == "Non-Craftable ":
            name = name[14:]
            craftable = -1
        else:
            craftable = 1
        if name[:4] == "The ":
            name = name[4:]

        # Assume it's unique
        quality = 6
        elevated = False
        use_elevated = False
        for _quality in item_data.qualities:
            if name.startswith(_quality):
                quality = item_data.qualities[_quality]
                elevated = quality
                name = name[len(_quality) + 1:]

        # Assume it has no killstreak
        killstreak = 0
        for _killstreak in item_data.killstreaks:
            if name.startswith(_killstreak):
                killstreak = item_data.killstreaks[_killstreak]
                name = name[len(_killstreak) + 1:]

        # Assume it's not australium
        australium = -1
        if name.startswith("Australium"):
            australium = 1
            name = name[11:]
            quality = item_data.qualities["Strange"]

        # Assume it's not unusual
        effect = False
        for _effect in item_data.effects:
            if name.startswith(_effect):
                effect = item_data.effects[_effect]
                name = name[len(_effect) + 1:]
                quality = item_data.qualities["Unusual"]
                if elevated:  # Item already has quality (probably Strange Unusual)
                    use_elevated = True

        for wear in item_data.wear:
            if name.endswith("(" + wear + ")"):
                quality = item_data.qualities["Decorated Weapon"]

        data = {"item_names": True,
                "page_size": page_size,
                "killstreak_tier": str(killstreak),
                "australium": str(australium),
                "quality": str(quality),
                "craftable": str(craftable),
                "item": name,
                "fold": fold}

        if effect:
            data["particle"] = effect
        if use_elevated:
            data["elevated"] = elevated

        # Things we were told at the beginning
        if unusual:
            data["quality"] = item_data.qualities["Unusual"]
        if set_elevated:
            data["elevated"] = set_elevated
        if user:
            data["steamid"] = user

        return data

    def bp_get_special_items(self, appid: int = 440):
        if not self.bp_api_key:
            raise ValueError("bp_api_key not set")

        data = {"key": self.bp_api_key,
                "appid": appid}
        return requests.get("https://backpack.tf/api/IGetSpecialItems/v1", data=data).json()

    def bp_get_user_token(self):
        if not self.bp_api_key:
            raise ValueError("bp_api_key not set")

        data = {"key": self.bp_api_key}

        response = requests.get("https://backpack.tf/api/aux/token/v1", data=data).json()

        if "message" in response:
            raise Exception(response["message"])

        return response["token"]

    def bp_send_heartbeat(self, automatic: str = "all"):
        if not self.bp_user_token:
            raise ValueError("bp_user_token not set")

        data = {"token": self.bp_user_token,
                "automatic": automatic}

        response = requests.post("https://backpack.tf/api/aux/heartbeat/v1", data=data).json()

        if "message" in response:
            raise Exception(response["message"])

        return response["bumped"]

    def bp_my_listings(self, item_names: bool = False, intent=None, inactive: int = 1, parse: bool = True):
        if not self.bp_user_token:
            raise ValueError("bp_user_token not set")

        data = {"token": self.bp_user_token,
                "inactive": inactive}

        if item_names:
            data["item_names"] = True
        if type(intent) == int:
            data["intent"] = intent

        response = requests.get("https://backpack.tf/api/classifieds/listings/v1", data=data).json()

        if "message" in response:
            raise Exception(response["message"])

        if not parse:
            return response

        to_return = {"cap": response.get("cap", 0),
                     "promotes_remaining": response.get("promotes_remaining", 0),
                     "listings": []}

        for listing in response["listings"]:
            to_return["listings"].append(bp_classified.Classified(listing, item_names))

        return to_return

    def bp_create_listing(self, listings: list, parse: bool = True):
        if not self.bp_user_token:
            raise ValueError("bp_user_token not set")

        data = {"token": self.bp_user_token,
                "listings": listings}

        response = requests.post("https://backpack.tf/api/classifieds/list/v1", json=data).json()

        if "message" in response:
            raise Exception(response["message"])

        if not parse:
            return response

        to_return = {"successful": [],
                     "unsuccessful": {}}
        for item, success in response["listings"].items():
            if "created" in success:
                to_return["successful"].append(item)
            else:
                to_return["unsuccessful"][item] = success["error"]

        return to_return

    @staticmethod
    def bp_create_listing_create_data(intent: int, currencies: dict, item_or_id, offers: int = 1, buyout: int = 1,
                                      promoted: int = 0, details: str = ""):
        data = {"intent": intent,
                "currencies": currencies,
                "offers": offers,
                "buyout": buyout,
                "promoted": promoted,
                "details": details}

        if intent:
            data["id"] = item_or_id
        else:
            data["item"] = item_or_id

        return data

    def bp_delete_listings(self, listing_ids, parse: bool = True):
        if not self.bp_user_token:
            raise ValueError("bp_user_token not set")

        data = {"token": self.bp_user_token,
                "listing_ids": listing_ids}

        response = requests.delete("https://backpack.tf/api/classifieds/delete/v1", json=data).json()

        if "message" in response:
            raise Exception(response["message"])

        if not parse:
            return response

        return response["deleted"], response["errors"]

    def bp_delete_listing(self, listing_id, parse: bool = True):
        return self.bp_delete_listings([listing_id], parse)

    @staticmethod
    def bp_is_duped(itemid):
        tree = html.fromstring(requests.get("https://backpack.tf/item" + str(itemid)).content)
        return bool(tree.xpath("""//button[@id="dupe-modal-btn"]/text()"""))

    @staticmethod
    def bp_parse_inventory(user):
        requests.get("https://backpack.tf/profiles/" + str(user))

    def mp_user_is_banned(self, steamid):
        if not self.mp_api_key:
            raise ValueError("mp_api_key not set")

        steamid = str(steamid)

        data = {"key": self.mp_api_key,
                "steamid": steamid}

        response = requests.get("https://marketplace.tf/api/Bans/GetUserBan/v1", data=data).json()

        if not response["success"]:
            raise Exception(response)

        if not response["is_banned"]:
            return False, None

        return True, response["ban_type"]

    def mp_deals(self, num: int = 100, skip: int = 0, parse: bool = True):
        if not self.mp_api_key:
            raise ValueError("mp_api_key not set")

        data = {"key": self.mp_api_key,
                "num": num,
                "skip": skip}

        response = requests.post("https://marketplace.tf/api/Deals/GetDeals/v2", data=data).json()

        if not response["success"]:
            raise Exception(response)

        if not parse:
            return response

        to_return = {"num_items": response["num_items"],
                     "items": []}

        for item in response["items"]:
            to_return["items"].append(mp_deal.Deal(item))

        return to_return

    def mp_dashboard_items(self, parse: bool = True):
        if not self.mp_api_key:
            raise ValueError("mp_api_key not set")

        data = {"key": self.mp_api_key}

        response = requests.get("https://marketplace.tf/api/Seller/GetDashboardItems/v2", data=data).json()

        if not response["success"]:
            raise Exception(response)

        if not parse:
            return response

        to_return = {"num_item_groups": response["num_item_groups"],
                     "total_items": response["total_items"],
                     "items": []}

        for item in response["items"]:
            to_return["items"].append(mp_item.Item(item))

        return to_return

    def mp_sales(self, num: int = 100, start_before: int = time(), parse: bool = True):
        if not self.mp_api_key:
            raise ValueError("mp_api_key not set")

        data = {"key": self.mp_api_key,
                "num": num,
                "start_before": start_before}

        response = requests.get("https://marketplace.tf/api/Seller/GetSales/v2", data=data).json()

        if not response["success"]:
            raise Exception(response)

        if not parse:
            return response

        to_return = []
        for sale in response["sales"]:
            to_return.append(mp_sale.Sale(sale))

        return to_return

    def mp_item_info(self, sku):
        if sku in self.mp_item_cache:
            return self.mp_item_cache[sku]["price"], self.mp_item_cache[sku]["amount"]

        chars1 = "\nn$ each" + chr(92)
        chars2 = "\nn, Availbe" + chr(92)

        page = requests.get("https://marketplace.tf/items/" + sku + "/")
        tree = html.fromstring(page.content)
        price = tree.xpath("""//div[@class="current-bid-amount"]/text()""")
        amount = tree.xpath("""//div[@class="current-bids"]/text()""")
        price = ''.join(price)
        amount = ''.join(amount)
        price2 = []
        amount2 = []
        for char in price:
            if char in chars1:
                pass
            else:
                price2.append(char)
        price = ''.join(price2)
        for char in amount:
            if char in chars2:
                pass
            else:
                amount2.append(char)
        amount = ''.join(amount2)

        if self.cache:
            self.mp_item_cache[sku]["price"] = price
            self.mp_item_cache[sku]["amount"] = amount

        return price, amount

    def mp_item_price(self, sku):
        return self.mp_item_info(sku)[0]

    def mp_item_amount(self, sku):
        return self.mp_item_info(sku)[1]

    @staticmethod
    def sr_reputation(steamid, parse: bool = True):
        response = requests.get("http://steamrep.com/api/beta4/reputation/" + str(steamid), data={"json": 1,
                                                                                                  "tagdetails": 1,
                                                                                                  "extended": 1}).json()

        if not parse:
            return response

        else:
            return sr_reputation.Reputation(response["steamrep"])

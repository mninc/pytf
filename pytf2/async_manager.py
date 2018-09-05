import aiohttp
from pytf2 import bp_currency, bp_user, bp_price_history, bp_classified, item_data, mp_deal, mp_item, mp_sale, \
    sr_reputation, exceptions
from time import time
from lxml import html
import json


class Manager:
    @classmethod
    async def create(cls, cache: bool = True, bp_api_key: str = '', bp_user_token: str = '', mp_api_key: str = '',
                     no_rate_limits: bool=False, async_client: aiohttp.ClientSession = None):
        self = cls()

        self.no_rate_limits = no_rate_limits
        self._past_requests = []

        if async_client:
            self.async_client = async_client
        else:
            self.async_client = aiohttp.ClientSession()
        self.request = self.async_request

        self.cache = cache
        self.bp_api_key = bp_api_key
        if bp_user_token:
            self.bp_user_token = bp_user_token
        else:
            self.bp_user_token = await self.bp_get_user_token()
        self.mp_api_key = mp_api_key
        self.mp_item_cache = {}
        self.bp_user_cache = {}

        return self

    @staticmethod
    async def _response_ok(status_code, url, response):
        if status_code < 200 or status_code >= 300:
            raise exceptions.BadStatusError(url, status_code, response)

    async def _check_params(self, params):
        new_params = {}
        for key, value in params.items():
            if type(value) is dict:
                value = await self._check_params(value)
            elif type(value) is bool:
                value = int(value)
            new_params[key] = value

        return new_params

    async def async_request(self, method, url, params=None, to_json=True):
        while len(self._past_requests) and time() - self._past_requests[0] > 60:
            del self._past_requests[0]
        if not self.no_rate_limits and len(self._past_requests) >= 120:
            raise exceptions.RateLimited()
        self._past_requests.append(time())

        params = await self._check_params(params)  # aiohttp does not accept bools in parameters
        if params:
            async with self.async_client.request(method, url, json=params) as response:
                await self._response_ok(response.status, url, await response.text())
                response = await response.text()

                if to_json:
                    return json.loads(response)
                else:
                    return response
        else:
            async with self.async_client.request(method, url) as response:
                await self._response_ok(response.status, url)
                response = await response.text()

                if to_json:
                    return json.loads(response)
                else:
                    return response

    async def clear_mp_item_cache(self):
        self.mp_item_cache = {}

    async def clear_bp_user_cache(self):
        self.bp_user_cache = {}

    @staticmethod
    async def st_item_to_str(item):
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

    async def s_get_inventory(self, user_id, game=440, parse: bool = True):
        from pytrade import EconItem
        url = "http://steamcommunity.com/inventory/" + str(user_id) + "/" + str(game) + "/2?l=english&count=5000"

        response = await self.request("GET", url)

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

    async def bp_get_prices(self, raw: bool = 0, since: int = 0):
        # backpack.tf docs - https://backpack.tf/api/docs/IGetPrices

        if not self.bp_api_key:
            raise exceptions.KeyNotSetError("bp_api_key")

        data = {"key": self.bp_api_key}
        if raw:
            data["raw"] = raw
        if since:
            data["since"] = since

        response = await self.request("GET", "https://backpack.tf/api/IGetPrices/v4", params=data)

        if not response["response"]["success"]:
            raise exceptions.BadResponseError("https://backpack.tf/api/IGetPrices/v4", response["response"]["message"])

        return response

    async def bp_get_currencies(self, raw: int = 0, parse: bool = True):
        # backpack.tf docs - https://backpack.tf/api/docs/IGetCurrencies

        if not self.bp_api_key:
            raise exceptions.KeyNotSetError("bp_api_key")

        data = {"key": self.bp_api_key}
        if raw:
            data["raw"] = raw

        response = await self.request("GET", "https://backpack.tf/api/IGetCurrencies/v1", params=data)

        if not response["response"]["success"]:
            raise exceptions.BadResponseError("https://backpack.tf/api/IGetCurrencies/v1",
                                              response["response"]["message"])

        if not parse:
            return response

        to_return = {}

        for item in response["response"]["currencies"]:
            to_return[item] = bp_currency.Currency(response["response"]["currencies"][item])

        return to_return

    async def bp_user_info(self, steamids: list, parse: bool = True):
        # backpack.tf docs - https://backpack.tf/api/docs/user_info

        to_return = {}

        if not self.bp_api_key:
            raise exceptions.KeyNotSetError("bp_api_key")

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

        response = await self.request("GET", "https://backpack.tf/api/users/info/v1", params=data)

        if "message" in response:
            raise exceptions.BadResponseError("https://backpack.tf/api/users/info/v1", response["message"])

        if not parse:
            return response

        for steamid, data in response["users"].items():
            to_return[steamid] = bp_user.BackpackUser(data)

        if self.cache:
            for steamid, info in to_return.items():
                self.bp_user_cache[steamid] = info

        return to_return

    async def bp_user_name(self, steamid):
        steamid = str(steamid)
        return await self.bp_user_info([steamid])[steamid].name

    async def bp_avatar(self, steamid):
        steamid = str(steamid)
        return await self.bp_user_info([steamid])[steamid].avatar

    async def bp_last_online(self, steamid):
        steamid = str(steamid)
        return await self.bp_user_info([steamid])[steamid].last_online

    async def bp_admin(self, steamid):
        steamid = str(steamid)
        return await self.bp_user_info([steamid])[steamid].admin

    async def bp_donated(self, steamid):
        steamid = str(steamid)
        return await self.bp_user_info([steamid])[steamid].donated

    async def bp_premium(self, steamid):
        steamid = str(steamid)
        return await self.bp_user_info([steamid])[steamid].premium

    async def bp_premium_months_gifted(self, steamid):
        steamid = str(steamid)
        return await self.bp_user_info([steamid])[steamid].premium_months_gifted

    async def bp_can_trade(self, steamid):
        steamid = str(steamid)
        user = await self.bp_user_info([steamid])[steamid]
        if not user.bans:
            return True
        if user.bans.steamrep_scammer or user.bans.bp_bans["all"]:
            return False
        return True

    async def bp_voting_rep(self, steamid):
        steamid = str(steamid)
        user = await self.bp_user_info([steamid])[steamid]
        if not user.voting:
            return
        return user.voting.reputation

    async def bp_backpack_rank(self, steamid):
        steamid = str(steamid)
        user = await self.bp_user_info([steamid])[steamid]
        if not user.inventory:
            return
        if "440" not in user.inventory.inventories:
            return
        return user.inventory.inventories["440"].ranking

    async def bp_backpack_value(self, steamid):
        steamid = str(steamid)
        user = await self.bp_user_info([steamid])[steamid]
        if not user.inventory:
            return
        if "440" not in user.inventory.inventories:
            return
        return user.inventory.inventories["440"].value

    async def bp_backpack_metal(self, steamid):
        steamid = str(steamid)
        user = await self.bp_user_info([steamid])[steamid]
        if not user.inventory:
            return
        if "440" not in user.inventory.inventories:
            return
        return user.inventory.inventories["440"].metal

    async def bp_backpack_keys(self, steamid):
        steamid = str(steamid)
        user = await self.bp_user_info([steamid])[steamid]
        if not user.inventory:
            return
        if "440" not in user.inventory.inventories:
            return
        return user.inventory.inventories["440"].keys

    async def bp_backpack_slots_total(self, steamid):
        steamid = str(steamid)
        user = await self.bp_user_info([steamid])[steamid]
        if not user.inventory:
            return
        if "440" not in user.inventory.inventories:
            return
        return user.inventory.inventories["440"].slots["total"]

    async def bp_backpack_slots_used(self, steamid):
        steamid = str(steamid)
        user = await self.bp_user_info([steamid])[steamid]
        if not user.inventory:
            return
        if "440" not in user.inventory.inventories:
            return
        return user.inventory.inventories["440"].slots["used"]

    async def bp_positive_trust(self, steamid):
        steamid = str(steamid)
        user = await self.bp_user_info([steamid])[steamid]
        if not user.trust:
            return
        return user.trust.positive

    async def bp_negative_trust(self, steamid):
        steamid = str(steamid)
        user = await self.bp_user_info([steamid])[steamid]
        if not user.trust:
            return
        return user.trust.negative

    async def bp_get_price_history(self, item, quality=None, tradable=1, craftable=1, priceindex: int = 0, appid: int = 440,
                             parse: bool = True):
        # backpack.tf docs - https://backpack.tf/api/docs/IGetPriceHistory

        if not self.bp_api_key:
            raise exceptions.KeyNotSetError("bp_api_key")

        data = {"key": self.bp_api_key,
                "item": item,
                "tradable": tradable,
                "craftable": craftable,
                "priceindex": priceindex,
                "appid": appid}

        if quality:
            data["quality"] = quality

        response = await self.request("GET", "https://backpack.tf/api/IGetPriceHistory/v1", params=data)

        if not response["response"]["success"]:
            raise exceptions.BadResponseError("https://backpack.tf/api/IGetPriceHistory/v1",
                                              response["response"]["message"])

        if not parse:
            return response

        to_return = []
        for history in response["response"]["history"]:
            to_return.append(bp_price_history.PriceHistory(history))

        return to_return

    async def bp_classifieds_search(self, data: dict, parse: bool = True):
        # backpack.tf docs - https://backpack.tf/api/docs/classifieds_search

        if not self.bp_api_key:
            raise exceptions.KeyNotSetError("bp_api_key")

        data["key"] = self.bp_api_key

        response = await self.request("GET", "https://backpack.tf/api/classifieds/search/v1", params=data)

        if "response" in response:
            raise Exception(response["response"])

        if not parse:
            return response

        to_return = {"sell": [],
                     "buy": [],
                     "total": response["total"],
                     "skip": response["skip"]}

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
    async def bp_classified_make_data(name, user=False, unusual: bool = False, set_elevated=False, page_size=10, fold=1,
                                      page=1):
        # Take off any unneccesary prefixes
        if name[:14] == "Non-Craftable ":
            name = name[14:]
            craftable = -1
        else:
            craftable = 1

        # Assume it's unique
        quality = 6
        elevated = False
        use_elevated = False
        if not name.startswith("Haunted Phantasm") and name != "Strange Bacon Grease" and \
                not name.startswith("Strange Filter") and not name.startswith("Strange Count") and \
                not name.startswith("Strange Cosmetic") and name != "Vintage Tyrolean" and \
                name != "Vintage Merryweather" and name != "Haunted Hat" and name != "Haunted Metal Scrap" and \
                not name.startswith("Haunted Ghosts"):
            for _quality in item_data.qualities:
                if name.startswith(_quality + " "):
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
        if name.startswith("Australium") and name != "Australium Gold":
            australium = 1
            name = name[11:]
            quality = item_data.qualities["Strange"]

        # Assume it's not unusual
        effect = False
        if "Hot Heels" not in name:
            for _effect in item_data.effects:
                if name.startswith(_effect + " "):
                    effect = item_data.effects[_effect]
                    name = name[len(_effect) + 1:]
                    quality = item_data.qualities["Unusual"]
                    if elevated:  # Item already has quality (probably Strange Unusual)
                        use_elevated = True

        for wear in item_data.wear_brackets:
            if name.endswith(wear):
                quality = item_data.qualities["Decorated Weapon"]

        data = {"item_names": True,
                "page_size": page_size,
                "killstreak_tier": str(killstreak),
                "australium": str(australium),
                "quality": str(quality),
                "craftable": str(craftable),
                "item": name,
                "fold": fold,
                "page": page}

        if effect:
            data["particle"] = effect
        elif quality == "Unusual":
            data["particle"] = 0
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

    async def bp_get_special_items(self, appid: int = 440):
        if not self.bp_api_key:
            raise exceptions.KeyNotSetError("bp_api_key")

        data = {"key": self.bp_api_key,
                "appid": appid}
        return await self.request("GET", "https://backpack.tf/api/IGetSpecialItems/v1", params=data)

    async def bp_get_user_token(self):
        if not self.bp_api_key:
            raise exceptions.KeyNotSetError("bp_api_key")

        data = {"key": self.bp_api_key}

        response = await self.request("GET", "https://backpack.tf/api/aux/token/v1", params=data)

        if "message" in response:
            raise Exception(response["message"])

        return response["token"]

    async def bp_send_heartbeat(self, automatic: str = "all"):
        if not self.bp_user_token:
            raise exceptions.KeyNotSetError("bp_user_token")

        data = {"token": self.bp_user_token,
                "automatic": automatic}

        response = await self.request("POST", "https://backpack.tf/api/aux/heartbeat/v1", params=data)

        if "message" in response:
            raise Exception(response["message"])

        return response["bumped"]

    async def bp_my_listings(self, item_names: bool = False, intent=None, inactive: int = 1, parse: bool = True):
        if not self.bp_user_token:
            raise exceptions.KeyNotSetError("bp_user_token")

        data = {"token": self.bp_user_token,
                "inactive": inactive}

        if item_names:
            data["item_names"] = True
        if type(intent) == int:
            data["intent"] = intent

        response = await self.request("GET", "https://backpack.tf/api/classifieds/listings/v1", params=data)

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

    async def bp_create_listing(self, listings: list, parse: bool = True):
        if not self.bp_user_token:
            raise exceptions.KeyNotSetError("bp_user_token")

        data = {"token": self.bp_user_token,
                "listings": listings}

        response = await self.request("POST", "https://backpack.tf/api/classifieds/list/v1", params=data)

        if "message" in response:
            raise Exception(response["message"])

        if not parse:
            return response

        to_return = {"successful": [],
                     "unsuccessful": {}}
        if not response["listings"]:
            return to_return

        for item, success in response["listings"].items():
            if "created" in success:
                to_return["successful"].append(item)
            else:
                to_return["unsuccessful"][item] = success["error"]

        return to_return

    @staticmethod
    async def bp_create_listing_create_data(intent: int, currencies: dict, item_or_id, offers: int = 1, buyout: int = 1,
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

    async def bp_delete_listings(self, listing_ids, parse: bool = True):
        if not self.bp_user_token:
            raise exceptions.KeyNotSetError("bp_user_token")

        data = {"token": self.bp_user_token,
                "listing_ids": listing_ids}

        response = await self.request("DELETE", "https://backpack.tf/api/classifieds/delete/v1", params=data)

        if "message" in response:
            raise Exception(response["message"])

        if not parse:
            return response

        return response["deleted"], response["errors"]

    async def bp_delete_listing(self, listing_id, parse: bool = True):
        return await self.bp_delete_listings([listing_id], parse)

    async def bp_is_duped(self, itemid):
        response = await self.request("GET", "https://backpack.tf/item" + str(itemid), to_json=False).encode()
        tree = html.fromstring(response)
        return bool(tree.xpath("""//button[@id="dupe-modal-btn"]/text()"""))

    async def bp_parse_inventory(self, user):
        await self.request("GET", "https://backpack.tf/_inventory/" + str(user), to_json=False)

    async def bp_number_exist(self, quality: str, name: str, tradable: str = "Tradable", craftable: str = "Craftable",
                        priceindex: int = 0):

        response = await self.request("GET", "https://backpack.tf/stats/{}/{}/{}/{}/{}".format(quality, name, tradable,
                                                                                         craftable, priceindex),
                                to_json=False)

        if "Stats for this item are not available." in response:
            return 0
        try:
            first = "inventories, there are <strong>"
            last = "</strong> known instances of this item."
            start = response.index(first) + len(first)
            end = response.index(last, start)
            return int(response[start:end])
        except ValueError:
            first = "inventories, there is <strong>"
            last = "</strong> known instance of this item."
            start = response.index(first) + len(first)
            end = response.index(last, start)
            if response[start:end] == "only one":
                return 1

    async def mp_user_is_banned(self, steamid):
        if not self.mp_api_key:
            raise exceptions.KeyNotSetError("mp_api_key")

        steamid = str(steamid)

        data = {"key": self.mp_api_key,
                "steamid": steamid}

        response = await self.request("GET", "https://marketplace.tf/api/Bans/GetUserBan/v1", params=data)

        if not response["success"]:
            raise exceptions.BadResponseError("https://marketplace.tf/api/Bans/GetUserBan/v1", response)

        if not response["is_banned"]:
            return False, None

        return True, response["ban_type"]

    async def mp_deals(self, num: int = 100, skip: int = 0, parse: bool = True):
        if not self.mp_api_key:
            raise exceptions.KeyNotSetError("mp_api_key")

        data = {"key": self.mp_api_key,
                "num": num,
                "skip": skip}

        response = await self.request("POST", "https://marketplace.tf/api/Deals/GetDeals/v2", params=data)

        if not response["success"]:
            raise exceptions.BadResponseError("https://marketplace.tf/api/Deals/GetDeals/v2", response)

        if not parse:
            return response

        to_return = {"num_items": response["num_items"],
                     "items": []}

        for item in response["items"]:
            to_return["items"].append(mp_deal.Deal(item))

        return to_return

    async def mp_dashboard_items(self, parse: bool = True):
        if not self.mp_api_key:
            raise exceptions.KeyNotSetError("mp_api_key")

        data = {"key": self.mp_api_key}

        response = await self.request("GET", "https://marketplace.tf/api/Seller/GetDashboardItems/v2", params=data)

        if not response["success"]:
            raise exceptions.BadResponseError("https://marketplace.tf/api/Seller/GetDashboardItems/v2", response)

        if not parse:
            return response

        to_return = {"num_item_groups": response["num_item_groups"],
                     "total_items": response["total_items"],
                     "items": []}

        for item in response["items"]:
            to_return["items"].append(mp_item.Item(item))

        return to_return

    async def mp_sales(self, num: int = 100, start_before: int = time(), parse: bool = True):
        if not self.mp_api_key:
            raise exceptions.KeyNotSetError("mp_api_key")

        data = {"key": self.mp_api_key,
                "num": num,
                "start_before": start_before}

        response = await self.request("GET", "https://marketplace.tf/api/Seller/GetSales/v2", params=data)

        if not response["success"]:
            raise exceptions.BadResponseError("https://marketplace.tf/api/Seller/GetSales/v2", response)

        if not parse:
            return response

        to_return = []
        for sale in response["sales"]:
            to_return.append(mp_sale.Sale(sale))

        return to_return

    async def mp_item_info(self, sku):
        if sku in self.mp_item_cache:
            return self.mp_item_cache[sku]["price"], self.mp_item_cache[sku]["amount"]

        chars1 = "\nn$ each" + chr(92)
        chars2 = "\nn, Availbe" + chr(92)

        page = await self.request("GET", "https://marketplace.tf/items/" + sku + "/", to_json=False)
        tree = html.fromstring(page.encode())
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

    async def mp_item_price(self, sku):
        return await self.mp_item_info(sku)[0]

    async def mp_item_amount(self, sku):
        return await self.mp_item_info(sku)[1]

    async def sr_reputation(self, steamid, parse: bool = True):
        data = {"json": 1,
                "tagdetails": 1,
                "extended": 1}

        response = await self.request("GET", "http://steamrep.com/api/beta4/reputation/" + str(steamid), params=data)

        if not parse:
            return response
        else:
            return sr_reputation.Reputation(response["steamrep"])

from pytf2 import item_data
from time import time
from AdvancedHTMLParser import AdvancedHTMLParser


class Item:
    def __init__(self, data, name, quality, tradable, craftable, priceindex=None):
        if data["value"] is None:
            self.invalid = True
            return
        else:
            self.invalid = False
        self.base_name = name
        self.mean_value = (data["value"] + data.get("value_high", data["value"])) / 2
        self.value = data["value"]
        self.value_high = data.get("value_high")
        self.last_update = data["last_update"]
        self.difference = data["difference"]
        self.currency = data["currency"]
        self.tradable = True if tradable == "Tradable" else False
        self.craftable = True if craftable == "Craftable" else False

        self.quality = quality
        self.quality_name = None
        for quality_name, quality_key in item_data.qualities.items():
            if str(quality_key) == quality:
                self.quality_name = quality_name

        self.priceindex = priceindex
        self.effect_name = None
        if priceindex and (self.quality_name == "Unusual" or priceindex == "4"):  # community sparkle
            for effect_name, effect_key in item_data.effects.items():
                if str(effect_key) == priceindex:
                    self.effect_name = effect_name

        self.url = "https://backpack.tf/stats/{}/{}/{}/{}".format(self.quality_name, name, tradable, craftable)
        if priceindex:
            self.url += "/" + priceindex
        self.url = self.url.replace(" ", "%20")

        if self.effect_name:
            name = self.effect_name + " " + name
        if self.quality_name and self.quality_name != "Unique" and (self.quality_name != "Unusual" or (self.quality_name == "Unusual" and not priceindex)):
            name = self.quality_name + " " + name
        if not self.tradable:
            name = tradable + " " + name
        if not self.craftable:
            name = craftable + " " + name
        self.name = name

    def in_date(self, days: int):
        current_time = time()
        suggestion_time = self.last_update
        difference = current_time - suggestion_time
        difference /= 60  # to minutes
        difference /= 60  # to hours
        difference /= 24  # to days
        if difference > days:
            return False
        return True


class Prices:
    def __init__(self, prices):
        prices = prices["response"]["items"]
        self.items = {}
        for item in prices:
            name = item
            if "prices" in prices[item]:
                item = prices[item]["prices"]
                for quality in item:
                    for tradable in item[quality]:
                        for craftable in item[quality][tradable]:
                            arr = item[quality][tradable][craftable]
                            if type(arr) is list:
                                for price in arr:
                                    price = Item(price, name, quality, tradable, craftable)
                                    if price.invalid:
                                        continue
                                    self.items[price.name] = price
                            elif type(arr) is dict:
                                for effect, price in arr.items():
                                    price = Item(price, name, quality, tradable, craftable, priceindex=effect)
                                    if price.invalid:
                                        continue
                                    self.items[price.name] = price

    def get_item(self, name):
        if name in self.items:
            return self.items[name]
        for item in self.items:
            if name in item:
                return self.items[item]
        return


class OpenSuggestion:
    def __init__(self, name, currency, price, item):
        self.name = name
        self.currency = currency
        self.price = price
        self.quality = item["quality"]
        self.item_name = item["item_name"]
        self.craftable = item["craftable"]
        self.priceindex = item["priceindex"]
        
        self.url = "https://backpack.tf/stats/{}/{}/{}/{}/{}".format(
            self.quality, self.item_name, "Tradable", "Craftable" if self.craftable else "Non-Craftable",
            self.priceindex
        )


class OpenPrices:
    def __init__(self, name_to_item):
        self.name_to_item = name_to_item
        self.items = []
        
    def _add_items(self, data):
        parser = AdvancedHTMLParser()
        parser.parseStr(data)
        suggs = parser.getElementsByClassName("suggestion")
        end = len(suggs) != 10
        for sugg in suggs:
            name = sugg.getElementsByClassName("item-name")[0].innerText.strip()
            new_price = sugg.getElementsByClassName("price-new")
            if not len(new_price):
                new_price = sugg.getElementsByClassName("price-refresh")
            new_price = new_price[0].innerText.strip()
            if "key" in new_price:
                currency = "keys"
                multiple = "keys" in new_price
                i = len(new_price) - 4
                if multiple:
                    i -= 1
                
                new_price = new_price[:i]
                if "–" in new_price:  # bear in mind - not a normal dash
                    values = new_price.split("–")
                    price = (float(values[0]) + float(values[1])) / 2
                else:
                    price = float(new_price)
            else:
                currency = "ref"
                new_price = new_price[:len(new_price)-4]
                if "–" in new_price:
                    values = new_price.split("–")
                    price = (float(values[0]) + float(values[1])) / 2
                else:
                    price = float(new_price)
            self.items.append(OpenSuggestion(name, currency, price, self.name_to_item(name)))
        return end
    
    def get_item(self, name):
        for item in self.items:
            if item.name == name:
                return item
        for item in self.items:
            if name in item.name:
                return item

class ClassifiedValue:
    def __init__(self, data):
        self.metal = data.get("metal", 0)
        self.keys = data.get("keys", 0)


class ClassifiedItem:
    def __init__(self, intent, data, item_names):
        self.defindex = data.get("defindex")
        self.quality = data.get("quality")

        if item_names:
            self.name = data.get("name")

        if intent:
            self.id = data.get("id")
            self.original_id = data.get("original_id")
            self.level = data.get("level")
            self.inventory = data.get("inventory")
            self.quantity = data.get("quantity")
            self.origin = data.get("origin")
            self.style = data.get("style")
            self.attributes = data.get("attributes")


class Classified:
    def __init__(self, data, item_names):
        if data["intent"]:  # Sell
            self.intent = 1
            self.id = data.get("id")
            self.steamid = data.get("steamid")
            self.item = ClassifiedItem(1, data.get("item"), item_names)
            self.appid = data.get("appid")
            self.currencies = ClassifiedValue(data.get("currencies"))
            self.offers = bool(data.get("offers", 0))
            self.buyout = bool(data.get("buyout", 0))
            self.details = data.get("details", "")
            self.created = data.get("created")
            self.bump = data.get("bump")
            self.automatic = bool(data.get("automatic", 0))
        else:  # Buy
            self.intent = 0
            self.id = data.get("id")
            self.steamid = data.get("steamid")
            self.item = ClassifiedItem(0, data.get("item"), item_names)
            self.currencies = ClassifiedValue(data.get("currencies"))
            self.offers = bool(data.get("offers", 0))
            self.buyout = bool(data.get("buyout", 0))
            self.details = data.get("details", "")
            self.created = data.get("created")
            self.bump = data.get("bump")
            self.automatic = bool(data.get("automatic", 0))

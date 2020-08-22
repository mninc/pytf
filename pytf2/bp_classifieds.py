class ClassifiedValue:
    def __init__(self, data):
        self.metal = data.get("metal", 0)
        self.keys = data.get("keys", 0)
        self.usd = data.get("usd", 0)
    
    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    
    def pretty_print(self, key: str = "key", metal: str = "ref"):
        if not self.keys and not self.metal:
            return ""
        elif not self.keys:
            return "{} {}".format(self.metal, metal)
        elif self.keys == 1 and not self.metal:
            return "1 {}".format(key)
        elif self.keys == 1 and self.metal:
            return "1 {} {} {}".format(key, self.metal, metal)
        elif self.keys and not self.metal:
            return "{} {}s".format(self.keys, key)
        else:
            return "{} {}s {} {}".format(self.keys, key, self.metal, metal)


class ClassifiedItem:
    def __init__(self, intent, data):
        self.defindex = data.get("defindex")
        self.quality = data.get("quality")
        self.attributes = data.get("attributes")
        self.name = data.get("name")
        
        if intent:
            self.id = data.get("id")
            self.original_id = data.get("original_id")
            self.level = data.get("level")
            self.inventory = data.get("inventory")
            self.quantity = data.get("quantity")
            self.origin = data.get("origin")
            self.style = data.get("style")


class Classified:
    def __init__(self, data):
        if data["intent"]:  # sell
            self.intent = 1
            self.id = data.get("id")
            self.steamid = data.get("steamid")
            self.item = ClassifiedItem(1, data.get("item"))
            self.appid = data.get("appid")
            self.currencies = ClassifiedValue(data.get("currencies"))
            self.offers = bool(data.get("offers", 0))
            self.buyout = bool(data.get("buyout", 0))
            self.details = data.get("details", "")
            self.created = data.get("created")
            self.bump = data.get("bump")
            self.automatic = bool(data.get("automatic", 0))
        else:  # buy
            self.intent = 0
            self.id = data.get("id")
            self.steamid = data.get("steamid")
            self.item = ClassifiedItem(0, data.get("item"))
            self.currencies = ClassifiedValue(data.get("currencies"))
            self.offers = bool(data.get("offers", 0))
            self.buyout = bool(data.get("buyout", 0))
            self.details = data.get("details", "")
            self.created = data.get("created")
            self.bump = data.get("bump")
            self.automatic = bool(data.get("automatic", 0))
    
    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class Listings:
    def __init__(self, data):
        self.listings = [Classified(listing) for listing in data]
    
    def get_highest_buyer(self, exclude: list = "", automatic_only: bool = False):
        # highest ref and highest keys
        highest_k = 0
        highest_r = 0
        highest = None
        for listing in self.listings:
            if listing.steamid in exclude:
                continue
            if automatic_only:
                if not listing.automatic:
                    continue
            if listing.intent == 0:
                if listing.currencies.keys > highest_k:
                    highest_k = listing.currencies.keys
                    highest_r = listing.currencies.metal
                    highest = listing
                elif listing.currencies.keys == highest_k and listing.currencies.metal > highest_r:
                    highest_k = listing.currencies.keys
                    highest_r = listing.currencies.metal
                    highest = listing
        return highest
    
    def get_lowest_seller(self, exlude: list = "", automatic_only: bool = False, usd: bool = False):
        # lowest ref and lowest keys
        lowest_k = 5000
        lowest_r = 5000
        lowest_usd = 5000
        lowest = None
        for listing in self.listings:
            if listing.steamid in exlude:
                continue
            if automatic_only:
                if not listing.automatic:
                    continue
            if listing.intent == 1:
                if usd:
                    if listing.currencies.usd and listing.currencies.usd < lowest_usd:
                        lowest_usd = listing.currencies.usd
                        lowest = listing
                else:
                    if listing.currencies.keys < lowest_k:
                        lowest_k = listing.currencies.keys
                        lowest_r = listing.currencies.metal
                        lowest = listing
                    elif listing.currencies.keys == lowest_k and listing.currencies.metal < lowest_r:
                        lowest_k = listing.currencies.keys
                        lowest_r = listing.currencies.metal
                        lowest = listing
        return lowest
    
    def get_listings_by_steamid(self, steamid):
        steamid = str(steamid)
        to_return = []
        for listing in self.listings:
            if listing.steamid == steamid:
                to_return.append(listing)
        return to_return
    
    def get_listings_by_intent(self, intent: int):
        to_return = []
        for listing in self.listings:
            if listing.intent == intent:
                to_return.append(listing)
        return to_return
    
    def filter(self, filter_func):
        self.listings = list(filter(filter_func, self.listings))
    
    def __add__(self, other):
        if other == 0:
            return self
        elif type(self) is MyListings and type(other) is MyListings:
            self.listings += other.listings
            return self
        elif type(self) is Classifieds and type(other) is Classifieds:
            self.total += other.total
            self.skip = None
            self.page_size += other.page_size
            self.sell_total += other.sell_total
            self.buy_total += other.buy_total
            self.listings += other.listings
            return self
        else:
            raise TypeError("unsupported operand type(s) for +: '{}' and '{}'".format(self.__class__.__name__,
                                                                                      other.__class__.__name__))


class Classifieds(Listings):
    def __init__(self, data):
        self.total = data["total"]
        self.skip = data["skip"]
        self.page_size = data["page_size"]
        self.sell_total = data["sell"]["total"]
        self.buy_total = data["buy"]["total"]
        Listings.__init__(self, data["sell"]["listings"] + data["buy"]["listings"])


class MyListings(Listings):
    def __init__(self, data):
        self.cap = data["cap"]
        self.promotes_remaining = data["promotes_remaining"]
        Listings.__init__(self, data["listings"])

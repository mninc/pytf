class Item:
    def __init__(self, data):
        self.sku = data.get("sku")
        self.name = data.get("name")
        self.defindex = data.get("defindex")
        self.quality = data.get("quality")
        self.num_for_sale = data.get("num_for_sale")
        self.lowest_price = data.get("lowest_price")


class Deal:
    def __init__(self, data):
        self.item = Item(data["item"])
        self.deal_pct_off = data.get("deal_pct_off")
        self.deal_dollars_off = data.get("deal_dollars_off")

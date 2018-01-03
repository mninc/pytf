class Item:
    def __init__(self, data):
        self.sku = data.get("sku")
        self.full_sku = data.get("full_sku")
        self.name = data.get("name")
        self.defindex = data.get("defindex")
        self.quality = data.get("quality")
        self.num_for_sale = data.get("num_for_sale")
        self.price = data.get("price")

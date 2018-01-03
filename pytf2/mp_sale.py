class SaleItem:
    def __init__(self, data):
        self.id = data.get("id")
        self.original_id = data.get("original_id")
        self.name = data.get("name")
        self.price = data.get("price")
        self.sku = data.get("sku")


class Sale:
    def __init__(self, data):
        self.id = data.get("id")
        self.earned_credit = data.get("earned_credit")
        self.paid = data.get("paid")
        self.time = data.get("time")
        self.items = [SaleItem(item) for item in data["items"]]

class InventoryItem:
    def __init__(self, item, descriptions):
        self.item_data = item
        self.appid = item["appid"]
        self.contextid = item["contextid"]
        self.assetid = item["assetid"]
        self.classid = item["classid"]
        self.instanceid = item["instanceid"]
        self.amount = item["amount"]

        self.description_data = descriptions
        self.currency = descriptions["currency"]
        self.background_color = descriptions["background_color"]
        self.icon_url = "https://steamcommunity-a.akamaihd.net/economy/image/" + descriptions["icon_url"]
        self.icon_url_key = descriptions["icon_url"]
        self.icon_url_large = "https://steamcommunity-a.akamaihd.net/economy/image/" + descriptions["icon_url_large"]
        self.icon_url_large_key = descriptions["icon_url_large"]
        self.tradable = bool(descriptions["tradable"])
        self.actions = descriptions["actions"]
        self.name = descriptions["name"]
        self.name_color = descriptions["name_color"]
        self.type = descriptions["type"]
        self.market_name = descriptions["market_name"]
        self.market_hash_name = descriptions["market_hash_name"]
        self.commodity = descriptions["commodity"]
        self.market_tradable_restriction = descriptions["market_tradable_restriction"]
        self.market_marketable_restriction = descriptions["market_marketable_restriction"]
        self.marketable = bool(descriptions["marketable"])
        self.tags = descriptions["tags"]

        # Get backpack.tf name
        name = self.market_name
        # assumptions
        craftable = True
        effect = ""
        unusual = False
        if name.startswith("Unusual "):
            unusual = True
        if item.get("descriptions"):
            for line in item["descriptions"]:
                if line["value"] == "( Not Usable in Crafting )":
                    craftable = False
                elif line["value"].startswith("★ Unusual Effect: ") and unusual:
                    name = name[8:]
                    effect = line["value"][18:]

        if not craftable and effect:
            name = "Non-Craftable " + effect + " " + name
        elif not craftable:
            name = "Non-Craftable " + name
        elif effect:
            name = effect + " " + name

        if name.startswith("The "):
            name = name[4:]
        self.bp_name = name


class Inventory:
    def __init__(self, data):
        self.total_inventory_count = data["total_inventory_count"]
        self.success = data["success"]
        self.rwgrsn = data["rwgrsn"]
        self.data = data

        classid_item = {}
        for item in data["descriptions"]:
            classid_item[item["classid"]] = item

        self.items = []
        for item in data["assets"]:
            if item["classid"] in classid_item:
                self.items.append(InventoryItem(item, classid_item[item["classid"]]))

    def get_items(self, item_name):
        items = []
        for item in self.items:
            if item.bp_name == item_name:
                items.append(item)

        return items

    def get_stock(self, item_name):
        return len(self.get_items(item_name))

    def get_assets(self, item_name):
        return [item.assetid for item in self.get_items(item_name)]

## inventory.Inventory object

### Properties:

* items - an array of [inventory.InventoryItem](#inventoryinventoryitem-object) objects

### Methods:

#### `get_items(self, item_name)`

Get an array of items from `self.items` whose `bp_name` mathes `item_name`.

#### `get_stock(self, item_name)`

Gets the stock of the item `item_name`. Actually just returns the length of [`get_items(item_name)`](#get_itemsself-item_name).

#### `get_assets(self, item_name)`

Get an array of assetids for the item `item_name`. 

## inventory.InventoryItem object

### Properties:

* All the properties found in the [original dictionary from steam](https://media.discordapp.net/attachments/337943916613599234/499980505802997760/unknown.png)
* item_data - the original dictionary
* All the properties from the [descriptions dictionary from steam](https://cdn.discordapp.com/attachments/337943916613599234/499981248949780480/unknown.png) with the following changes:
    * icon_url and icon_url_large have the start of the url added (adding `https://steamcommunity-a.akamaihd.net/economy/image/`)
    * icon_url_key and icon_url_large_key have been added for the original value of icon_url and icon_url_large
    * tradable and marketable have been coverted to booleans
* description_data - the original dictionary
* bp_name - the name of the item as it probably appears on backpack.tf

### todo

* Add quality, effect properties etc
* Add methods (such as create_item_dict to make a dictionary that can be used to make a buy order on backpack.tf)

[s](#inventoryinventory-object)
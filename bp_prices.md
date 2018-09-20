## bp_prices.Prices object

### Properties:

* items - a dictionary with full item name keys and `bp_prices.Item` object values

### Methods

#### `get_item(self, name)`

Fetch a `bp_prices.Item` object from `self.items`. If the exact name is not found it will check to see if the input name is partially in one of the items in `self.items` and return that. If it still cannot find a match, returns nothing.

### todo

* Add more methods to this object (maybe get items with a certain quality, items with a certain effect etc)
## bp_prices.Item

### Properties:

All the properties that can be found in the value section of the prices are properties:
```json
{"value": 0.08,
 "currency": "usd",
 "difference": 0,
 "last_update": 1488385886,
 "value_high": 0.12
}
```

Additional properties:
* mean_value - the price of the item (average of value and value_high if there is a range, otherwise just value)
* tradable - bool
* craftable - bool
* quality - quality number as a string
* quality_name
* priceindex - priceindex if set, else None
* effect_name - effect name if the item has an unusual effect, else None
* name
* url - a backpack.tf stats url for the item
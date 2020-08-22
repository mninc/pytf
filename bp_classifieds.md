## bp_classifieds.Listings object

### `__init__(self, data)`
* **data** - an array of listings from the backpack.tf api

### Properties:

* **listings** - an array of [Classified](https://github.com/mninc/pytf/blob/master/bp_classifieds.md#bp_classifiedsclassified-object) objects

### Methods:

#### `get_highest_buyer(self, exclude: list="", automatic_only: bool=False)`

Returns the highest buy order, or `None` if there are none.

The exclude parameter should be an array of steamids to ignore (you probably want to exclude yourself when fetching the highest buyer)

The automatic_only should be set to true if you do not want non-automatic buyers.

#### `get_lowest_seller(self, exlude: list = "", automatic_only: bool = False, usd: bool = False)`

Returns the lowest sell order, or `None` if there are none.

The exclude parameter should be an array of steamids to ignore (you probably want to exclude yourself when fetching the lowest seller)

The automatic_only should be set to true if you do not want non-automatic sellers.

The usd parameter will set whether you want the lowest seller in keys/ref or in USD (because of marketplace.tf cross-listings). At the moment there is no support for getting both at the same time.

#### `get_listings_by_steamid(self, steamid)`

Returns an array of listings from the specified steamid64.

### `get_listings_by_intent(self, intent: int)`

Returns an array of listings with the specified intent (1: sell, 0: buy).

## bp_classifieds.Classifieds object

Inherits all properties and methods from a [Listings](https://github.com/mninc/pytf/blob/master/bp_classifieds.md#bp_classifiedslistings-object) object.

### `__init__(self, data)`
* **data** - a [classifieds search](https://backpack.tf/api/docs/classifieds_search) response.

## bp_classifieds.MyListings object

Inherits all properties and methods from a [Listings](https://github.com/mninc/pytf/blob/master/bp_classifieds.md#bp_classifiedslistings-object) object. Some of the methods may not make sense for this data, but should still work as expected.

### `__init__(self, data)`
* **data** - a [my listings](https://backpack.tf/api/docs/my_listings) response.

## bp_classifieds.Classified object

Contains all the properties of a listing from the backpack.tf api with the following changes:

* `offers`, `buyout` and `automatic` are converted to bools
* The `item` property is a [ClassifiedsItem](https://github.com/mninc/pytf/blob/master/bp_classifieds.md#bp_classifiedsclassifieditem-object) object
* The `currencies` property is a [ClassifiedsValue](https://github.com/mninc/pytf/blob/master/bp_classifieds.md#bp_classifiedsclassifiedvalue-object) object

### `__init__(self, data)`
* **data** - a listing from the backpack.tf api

## bp_classifieds.ClassifiedItem object

Contains all the properties of the dictionary passed to it

### `__init__(self, intent, data)`
* **intent** - 1 or 0
* **data** - the raw json

## bp_classifieds.ClassifiedValue object

### Properties

`metal` and `keys`

### Methods

#### `pretty_print(self, key: str="key", metal: str="ref")`

* **key** - what keys should be displayed as
* **metal** - what ref should be displayed as (eg '12 ref' or '12 metal')

Returns a string representation of the value (only including a value if it's over 0, pluralising keys etc)

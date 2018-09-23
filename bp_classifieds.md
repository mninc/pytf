## bp_classifieds.Listings object

### `__init__(self, data)`
* **data** - an array of listings from the backpack.tf api

### Properties:

* **listings** - an array of bp_classifieds.Classified objects

### Methods:

#### `get_highest_buyer(self)`

Returns the highest buy order, or `None` if there are none.

#### `get_lowest_seller(self)`

Returns the lowest sell order, or `None` if there are none.

#### `get_listings_by_steamid(self, steamid)`

Returns an array of listings from the specified steamid64.

## bp_classifieds.Classifieds object

Inherits all properties and methods from a Listings object.

### `__init__(self, data)`
* **data** - a [classifieds search](https://backpack.tf/api/docs/classifieds_search) response.

## bp_classifieds.MyListings object

Inherits all properties and methods from a Listings object. Some of the methods may not make sense for this data, but should still work as expected.

### `__init__(self, data)`
* **data** - a [my listings](https://backpack.tf/api/docs/my_listings) response.

## bp_classifieds.Classified object

Contains all the properties of a listing from the backpack.tf api with the following changes:

* `offers`, `buyout` and `automatic` are converted to bools
* The `item` property is a ClassifiedsItem object
* The `currencies` property is a ClassifiedsValue object

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

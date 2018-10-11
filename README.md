# pytf2
An API wrapper for some TF2-related sites. Created by [manic](http://manic.tf/).

These methods are designed so I can use this module rather than pasting functions into many blocks of code. It is not intended to be an API wrapper for every tf2 site. If you want to add some methods, feel free to make a pull request.

# Installation
Run `pip install pytf2`.

# Usage
```python
import pytf2
tf2_manager = pytf2.Manager(params)
```

`__init__(self, cache: bool=True, bp_api_key: str='', bp_user_token: str='', mp_api_key: str='', no_rate_limits: bool=False, bypass_cf: bool=False)`
* **cache** - Keep results of APIs etc for use later without calling the API again. Useful for getting multiple bits of info from the same endpoint without receiving a cooldown
* **bp_api_key** - [Your backpack.tf api key](https://backpack.tf/developer/apikey/view)
* **bp_user_token** - [Your backpack.tf user token](https://backpack.tf/connections) (click 'Show Token')
* **mp_api_key** - [Your marketplace.tf api key](https://marketplace.tf/apisettings)
* **no_rate_limits** - By default an error is raised if you try to make more than 120 requests per minute as this can cause your ip to be temporarily blocked by backpack.tf. If you want to disable this feature set this to True
* **bypass_cf** - Uses the [cfscrape](https://pypi.org/project/cfscrape/) for every request so requests will still work when a site is in under attack mode. This option is currently only available synchronously. You should read the docs for this module before enabling this option - it might not work out of the box and will need updating on occasion


## Asynchronous usage
To use the library asynchronously, you need to do this:
```python
tf2_manager = await pytf2.async_manager.Manager.create(params)
```
An additional parameter is available: 
* **async_client** - an aiohttp.ClientSession object (default: `None`)

Every method can now be used with `await`.

# Nicknames
Some site names are shortened to keep function names at a reasonable length
<table>
  <tr>
    <th>Shortened name</th>
    <th>Site</th>
  </tr>
  <tr>
    <td>bp</td>
    <td><a href='https://backpack.tf/' >backpack.tf</a></td>
  </tr>
  <tr>
    <td>mp</td>
    <td><a href='https://marketplace.tf/' >marketplace.tf</a></td>
  </tr>
  <tr>
    <td>sr</td>
    <td><a href='https://steamrep.com/' >steamrep</a></td>
  </tr>
  <tr>
    <td>st</td>
    <td><a href='https://github.com/Zwork101/steam-trade' >steam-trade</a></td>
  </tr>
  <tr>
    <td>s</td>
    <td><a href='http://store.steampowered.com' >steam</a></td>
  </tr>
</table>

# Methods

## `clear_mp_item_cache(self)`
Clears the marketplace.tf item cache

Takes no arguments

Returns nothing

## `clear_bp_user_cache(self)`
Clears the backpack.tf user cache

Takes no arguments

Returns nothing

## `st_item_to_str(item)`
Changes a steam-trade EconItem object to a string. Please note - this method may not work for all items. Use with care

* **item** - A steam-trade EconItem object

Returns the name of the item

##  `s_get_inventory(self, user_id, game=440, context=2, language="english", count=5000, start_assetid=None, parse: bool = True)`
Gets the inventory of a user

* **user_id** - the steamid64 of the user
* **game** - the id of the game to get inventory for (440 - TF2)
* **context** - the inventory context. For TF2 this is always 2. 
* **language** - the language to fetch the inventory in. If you choose something other than english parsing may break
* **count** - maximum number of items to fetch. Maximum 5000
* **start_assetid** - used for pagination. First item to fetch in the inventory. Currently unnecessary for TF2 as the maximum inventory size is less than 5000
* **parse** - if False, returns raw data from steam. If True, returns a [inventory.Inventory](https://github.com/mninc/pytf/blob/master/inventory.md#inventoryinventory-object) object.

## `bp_get_prices(self, raw: bool=0, since: int=0, parse: bool=True)`
[Gets the backpack.tf suggested price info](https://backpack.tf/api/docs/IGetPrices)

* **raw** - If set to 1, adds a value_raw to the priceindex objects which represents the value of the item in the lowest currency without rounding. If a high value is set, the raw value will be an average between the low and high value. Setting raw to 2 prevents this behaviour by adding a new field, value_high_raw.
* **since** - If set, only returns prices that have a last_update value greater than or equal to this UNIX time.
* **parse** - If False, returns a dict [like the one here](https://backpack.tf/api/docs/IGetPrices). If True, returns a [bp_prices.Prices](https://github.com/mninc/pytf/blob/master/bp_prices.md#bp_pricesprices-object) object

## `bp_get_currencies(self, raw: int=0, parse: bool=True)`
[Gets the backpack.tf currency info](https://backpack.tf/api/docs/IGetCurrencies)

* **raw** - If set to 1, adds a value_raw to the priceindex objects which represents the value of the item in the lowest currency without rounding. If a high value is set, the raw value will be an average between the low and high value. Setting raw to 2 prevents this behaviour by adding a new field, value_high_raw.
* **parse** - If false, will return the dict from backpack.tf. If true, parses each currency with `bp_currency.py` and returns a dict like this:
```
{"metal": <pytf2.bp_currency.Currency object>, "hat": <pytf2.bp_currency.Currency object>, "keys": <pytf2.bp_currency.Currency object>, "earbuds": <pytf2.bp_currency.Currency object>}
```

## `bp_user_info(self, steamids: list, parse: bool=True)`
[Gets user info from backpack.tf](https://backpack.tf/api/docs/user_info). Will use the cache where possible.

* **steamids** - list of steamid64s to check
* **parse** - if false, returns the dict from backpack.tf. If true, parses each user with `bp_user.py` and returns a dict of id to object

## Generic User Info functions
All of these functions operate the same way - they return a specific piece of info about a player. 
They all use the `bp_user_info` to get info and use the cache where possible.

All functions require the steamid64 of the player.
<table>
    <tr>
        <th>Function</th>
        <th>Returns</th>
    </tr>
    <tr>
        <td>bp_user_name(self, steamid)</td>
        <td>steam name of the user</td>
    </tr>
    <tr>
        <td>bp_avatar(self, steamid)</td>
        <td>URL of the user's profile picture</td>
    </tr>
    <tr>
        <td>bp_last_online(self, steamid)</td>
        <td>unix timestamp when the user last visited backpack.tf</td>
    </tr>
    <tr>
        <td>bp_admin(self, steamid)</td>
        <td>True if the user is a backpack.tf admin</td>
    </tr>
    <tr>
        <td>bp_donated(self, steamid)</td>
        <td>the amount the user has donated to backpack.tf</td>
    </tr>
    <tr>
        <td>bp_premium(self, steamid)</td>
        <td>True if the user has backpack.tf premium</td>
    </tr>
    <tr>
        <td>bp_premium_months_gifted(self, steamid)</td>
        <td>how many months of backpack.tf premium the user has gifted</td>
    </tr>
    <tr>
        <td>bp_can_trade(self, steamid)</td>
        <td>True if it is ok to trade with the user</td>
    </tr>
    <tr>
        <td>bp_voting_rep(self, steamid)</td>
        <td>the voting reputation of the user (None if no rep)</td>
    </tr>
    <tr>
        <td>bp_backpack_rank(self, steamid)</td>
        <td>the TF2 inventory rank of the user (None if inventory not parsed by backpack.tf, False if not ranked)</td>
    </tr>
    <tr>
        <td>bp_backpack_value(self, steamid)</td>
        <td>the value of the user's TF2 inventory (None if inventory not parsed)</td>
    </tr>
    <tr>
        <td>bp_backpack_metal(self, steamid)</td>
        <td>the raw metal (ref, rec, scrap) value of the user's inventory (None if not parsed)</td>
    </tr>
    <tr>
        <td>bp_backpack_keys(self, steamid)</td>
        <td>the amount of raw keys in the user's inventory (None if not parsed)</td>
    </tr>
    <tr>
        <td>bp_backpack_slots_total(self, steamid)</td>
        <td>the total amount of slots in the user's inventory (None if not parsed)</td>
    </tr>
    <tr>
        <td>bp_backpack_slots_used(self, steamid)</td>
        <td>the amount of slots used in the user's inventory (None if not parsed)</td>
    </tr>
    <tr>
        <td>bp_positive_trust(self, steamid)</td>
        <td>how many positive trusts the user has</td>
    </tr>
    <tr>
        <td>bp_negative_trust(self, steamid)</td>
        <td>how many negative trusts the user has</td>
    </tr>
</table>

## `bp_get_price_history(self, item, quality=None, tradable: int=1, craftable=1, priceindex: int=0, appid: int=440, parse: bool=True)`
[Gets the suggested price history from backpack.tf](https://backpack.tf/api/docs/IGetPriceHistory)

* **item** - The item - this can be a name or a definition index
* **quality** - The quality - this can be a name or a definition index
* **tradable** - The item's tradability. Use 'Tradable' or 1 to signify that the item should be tradable, or 'Non-Tradable' or 0 to signify that the item should not be tradable
* **craftable** - The item's craftability. Use 'Craftable' or 1 to signify that the item should be craftable, or 'Non-Craftable' or 0 to signify that the item should not be craftable
* **priceindex** - The item's priceindex. See [this](https://backpack.tf/api/docs/IGetPrices) page and scroll down to `Priceindex` for more info
* **appid** - Steam app to return data for. Default: 440 (Team Fortress 2). Valid options: 440, 570, 730
* **parse** - if false, returns the dict from backpack.tf. If true, returns an array of `bp_price_history.py` objects

## `bp_classifieds_search(self, data: dict, parse: bool=True)`
[Searches backpack.tf classifieds](https://backpack.tf/api/docs/classifieds_search)

* **data** - a dict of all the data to be sent to backpack.tf (as written [here](https://backpack.tf/api/docs/classifieds_search)). 'key' paramater is not required.
* **parse** - if false, returns the dict from backpack.tf. If true, returns a [bp_classifieds.Classifieds object](https://github.com/mninc/pytf/blob/master/bp_classifieds.md#bp_classifiedsclassifieds-object)

## `bp_classified_make_data(name, user=False, unusual: bool=False, set_elevated=False, page_size=10, fold=1)`
Creates data for use with the `bp_classifieds_search` method

* **name** - name of the item including qualities etc. Works well with the `st_item_to_str` method
* **user** - a specific user's steamid4 to get the listing from
* **unusual** - manual override to set the quality to unusual (for searching for generic unusuals)
* **set_elevated** - manually set the elevated quality of the item
* **page_size** - how many listings to load for sell and buy orders. Max 30
* **fold** - if 0, disables listing folding

Returns a dict. Normal usage:
```python
tf2_manager.bp_classifieds_search(tf2_manager.bp_classified_make_data("Item name"))
```

## `bp_get_special_items(self, appid=440)`
[Gets the internal backpack.tf item placeholders](https://backpack.tf/api/docs/IGetSpecialItems)

* **appid** - the appid of the game (note - anything other than 440 (TF2) will not work. I'm just leaving this in because the docs say you can use 570 and 730 as well)

Returns the response from backpack.tf

## `bp_get_user_token(self)`
Returns the backpack.tf user token. API key must be set

## `bp_send_heartbeat(self, automatic: str="all")`
Send a heartbeat to backpack.tf. Bumps listings where possible and gives you the lightning bolt on your listings

* **automatic** - which listings to set as automatic. 'all' makes all of them, 'sell' only makes sell orders auto

Returns how many listings were bumped

## `bp_my_listings(self, item_names: bool=False, intent=None, inactive: int=1, parse: bool=True)`
Returns your listings from backpack.tf

* **item_names** - if True, each listing item will have a 'name' property
* **intent** - set to 0 for only buy listings and 1 for only sell listings
* **inactive** - set to 0 to hide inactive listings
* **parse** - if False, returns the response from backpack.tf. If True, returns a [bp_classifieds.MyListings](https://github.com/mninc/pytf/blob/master/bp_classifieds.md#bp_classifiedsmylistings-object) object.

## `bp_create_listing(self, listings: list, parse: bool=True)`
Creates listings

* **listings** - an array of listings to create (like [this](https://backpack.tf/api/docs/create_listings))
* **parse** - if False, returns the response from backpack.tf. If True, returns:
```
{"successful": ["item name (buying) or id (selling)", ...], "unsuccessful": {"item": reason, ...}}
```

## `bp_create_listing_create_data(intent: int, currencies: dict, item_or_id, offers: int=1, buyout: int=1, promoted: int=0, details: str="")`
Creates a listing dict for use in the `bp_create_listing` method as part of a list.

* **intent** - 0 (Buy) or 1 (Sell)
* **currencies** - the price for the listing, eg:
```json
{"metal": 10, "keys": 11}
```
* **item_or_id** - if the intent is sell, this is the current id of the item. Can also be the id of an item in you marketplace.tf inventory if you have integration set up.
If the intent is to buy, this is a dict object:
```json
{"quality": "quality name or id. Supports elevated qualities, just use a space (eg 'Strange Unusual')", 
 "item_name": "name of the item or it's defindex. supports killstreaks and australium (prefix the name with it)",
 "craftable": "0 or 'Non-Craftable' if the item isn't craftable",
 "priceindex": "priceindex of the item (see https://backpack.tf/api/docs/IGetPrices and scroll down to 'priceindex'"}
 ```
 * **offers** - set to 0 to only accept steam friend requests
 * **buyout** - set to 0 to allow negotiation (blue trade icon)
 * **promoted** - set to 1 to promote the listing (sell orders only, must have a promote slot free)
 * **details** - the details for the listing
 
 Returns a dict for use in the `bp_create_listing` method.
 Example:
 ```python
tf2_manager.bp_create_listing([tf2_manager.bp_create_listing_data(1, {"metal": 1}, "6426729449", details="buy this item"),
                               tf2_manager.bp_create_listing_data(0, {"metal": 3, "keys": 2}, {"quality": "Unique",
                                                                                               "item_name": "B.M.O.C."},
                                                                  details="buying this")])
```

## `bp_delete_listings(self, listing_ids, parse: bool=True)`
Deletes the specified listings

* **listing_ids** - an array of listing ids to delete
* **parse** - if False, returns data from backpack.tf. If True, returns `{"deleted": number of listings deleted, "errors": [list of errors]}`

## `bp_delete_listing(self, listing_id, parse: bool=True)`
Deletes a single listing

* **listing_id** - listing id to delete
* **parse** - whether or not to parse the response

Returns the same as the `bp_delete_listings` method

## `bp_is_duped(itemid)`
Checks if the item is duped. This method does not require an API key. Due to the way it collects data this method may break in the future

* **itemid** - the id of the item. This can be any id that works when put into [this page](http://backpack.tf/item/id).

Returns True if the item is duped

## `bp_parse_inventory(user)`
Makes backpack.tf parse the inventory of the user (to enable you to list items that just came into your inventory
for example)

* **user** - the steamid64 of the user

Does not return anything

## `bp_number_exist(quality: str, name: str, tradable: str="Tradable", craftable: str="Craftable", priceindex: int=0`
Checks how many of that item exist

* **quality** - the quality of the item (string not number)
* **name** - the name of the item
* **tradable** - if the item is tradable
* **craftable** - if the item is craftable
* **priceindex** - priceindex of the item

Returns the number of items that exist, 0 if none.

## `mp_user_is_banned(self, steamid)`
Checks if the user is banned on marketplace.tf

* **steamid** - steamid64 of the user

Returns `False, None` if the user is not banned, `True, reason` if the user is banned

## `mp_deals(self, num: int=100, skip: int=0, parse: bool=True)`
Gets marketplace.tf deals. Sorted by $ deal value descending

* **num** - number of deals to fetch. Max 1000
* **skip** - skip first x deals. used to paginate
* **parse** - if False, returns the data from marketplace.tf. If True, returns:
```json
{"num_items": "how many deals found",
"items": ["mp_deal.py Deal object", ...]}
```

## `mp_dashboard_items(self, parse: bool=True)`
Gets all the items currently on your marketplace.tf dashboard and available for sale

* **parse** - If False, returns the response from marketplace.tf. If True, returns:
```json
{"num_item_groups": 0, "total_items": 1, "items": ["mp_item.py Item object"]}
```

## `mp_sales(self, num: int=100, start_before: int=time(), parse: bool=True)`
Gets your marketplace.tf sales, most recent first

* **num** - how many sales to fetch. max 500
* **start_before** - unix timestamp to fetch sales from before. used to paginate
* **parse** - if False, returns response from marketplace.tf. If True, returns 
```json
["mp_sale.py Sale object", ...]
```

## `mp_item_info(self, sku)`
Gets info on an item from marketplace.tf

* **sku** - the sku of the item

Returns the price of the item and the number available 

## `mp_item_price(self, sku)`
Gets info on the price of an item from marketplace.tf

* **sku** - the sku of the item

Returns the price

## `mp_item_amount(self, sku)`
Gets info on the amount of an item available from marketplace.tf

* **sku** - the sku of the item

Returns the amount

## `sr_reputation(steamid, parse: bool=True)`
Gets user info from steamrep

Note - it is recommended to use the `bp_user_info` method instead

* **steamid** - the user's steamid64
* **parse** - if False, will return the response from steamrep. If True, returns a `sr_reputation.py` Reputation object

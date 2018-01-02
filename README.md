# Installation
Run `pip install pytf2`.

# Usage
```python
from pytf2 import manager
tf2_manager = manager.Manager(cache=True, bp_api_key='', bp_user_token='')
```
* cache - Keep results of APIs etc for use later without calling the API again. Useful for getting multiple bits of info from the same endpoint without receiving a cooldown
* bp_api_key - [Your backpack.tf api key](https://backpack.tf/developer/apikey/view)
* bp_user_token - [Your backpack.tf user token](https://backpack.tf/connections) (click 'Show Token')

# Nicknames
Some site names are shortened to keep function names at a reasonable length
<table class="tg">
  <tr>
    <th class="tg-yw4l">Shortened name</th>
    <th class="tg-yw4l">Site</th>
  </tr>
  <tr>
    <td class="tg-yw4l">bp</td>
    <td class="tg-yw4l"><a href='https://backpack.tf/' >backpack.tf</a></td>
  </tr>
  <tr>
    <td class="tg-yw4l">mp</td>
    <td class="tg-yw4l"><a href='https://marketplace.tf/' >marketplace.tf</a></td>
  </tr>
  <tr>
    <td class="tg-yw4l">sr</td>
    <td class="tg-yw4l"><a href='https://steamrep.com/' >steamrep</a></td>
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

## `bp_get_prices(self, raw=0, since=None)`
[Gets the backpack.tf suggested price info](https://backpack.tf/api/docs/IGetPrices)

* **raw** - If set to 1, adds a value_raw to the priceindex objects which represents the value of the item in the lowest currency without rounding. If a high value is set, the raw value will be an average between the low and high value. Setting raw to 2 prevents this behaviour by adding a new field, value_high_raw.
* **since** - If set, only returns prices that have a last_update value greater than or equal to this UNIX time.

Returns a dict [like the one here](https://backpack.tf/api/docs/IGetPrices) if successful, otherwise raises and exception.

## `bp_get_currencies(self, raw=0, parse=True)`
[Gets the backpack.tf currency info](https://backpack.tf/api/docs/IGetCurrencies)

* **raw** - If set to 1, adds a value_raw to the priceindex objects which represents the value of the item in the lowest currency without rounding. If a high value is set, the raw value will be an average between the low and high value. Setting raw to 2 prevents this behaviour by adding a new field, value_high_raw.
* **parse** - If false, will return the dict from backpack.tf. If true, parses each currency with `currency.py` and returns a dict like this:




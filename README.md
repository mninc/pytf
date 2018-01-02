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
<style type="text/css">
.tg  {border-collapse:collapse;border-spacing:0;}
.tg td{font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;}
.tg th{font-family:Arial, sans-serif;font-size:14px;font-weight:normal;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;}
.tg .tg-yw4l{vertical-align:top}
</style>
<table class="tg">
  <tr>
    <th class="tg-yw4l">Shortened name</th>
    <th class="tg-yw4l">Site</th>
  </tr>
  <tr>
    <td class="tg-yw4l">bp</td>
    <td class="tg-yw4l">[backpack.tf](https://backpack.tf/)</td>
  </tr>
  <tr>
    <td class="tg-yw4l">mp</td>
    <td class="tg-yw4l">[marketplace.tf](https://marketplace.tf/)</td>
  </tr>
  <tr>
    <td class="tg-yw4l">sr</td>
    <td class="tg-yw4l">[steamrep](https://steamrep.com/)</td>
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



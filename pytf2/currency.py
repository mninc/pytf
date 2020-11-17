from functools import total_ordering


def keys_to_scrap(keyprice, keys, metal):
    return round(keys * round(keyprice * 9)) + round(metal * 9)


def scrap_to_keys(keyprice, scrap):
    keys = 0
    while scrap > round(keyprice * 9):
        keys += 1
        scrap -= round(keyprice * 9)
    ref = scrap / 9
    ref = fix_ref(ref)
    return keys, ref


def fix_ref(ref):
    ref = str(round(ref * 18) / 18)
    if "." in ref:
        bd, ad = ref.split(".")
        if ad == "0":
            ref = int(bd)
        else:
            ad = ad[:2]
            ref = float(bd + "." + ad)
    else:
        ref = int(ref)
    return ref


@total_ordering
class Currency:
    def __init__(self, keys=0, metal=0, scrap=0, keyprice=56.11):
        self.keyprice = keyprice
        if scrap:
            self.scrap = scrap
            self.raw_keys = 0
            self.raw_metal = 0
        else:
            self.scrap = self.keys_to_scrap(keys, metal)
            self.raw_keys = keys
            self.raw_metal = metal
    
    @property
    def keys(self):
        return self.scrap_to_keys(self.scrap)[0]
    
    @property
    def metal(self):
        return self.scrap_to_keys(self.scrap)[1]
    
    @property
    def ref(self):
        return self.scrap_to_keys(self.scrap)[1]
    
    def keys_to_scrap(self, keys, metal):
        return keys_to_scrap(self.keyprice, keys, metal)
    
    def scrap_to_keys(self, scrap):
        return scrap_to_keys(self.keyprice, scrap)
    
    def __eq__(self, other):
        return self.scrap == other.scrap
    
    def __gt__(self, other):
        return self.scrap > other.scrap

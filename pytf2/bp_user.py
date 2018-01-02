class BackpackTrust:
    def __init__(self, data):
        self.positive = data.get("positive", 0)
        self.negative = data.get("negative", 0)


class Inventory:
    def __init__(self, data):
        self.ranking = data.get("ranking", False)
        self.value = data.get("value", 0)
        self.updated = data.get("updated")
        self.metal = data.get("metal", 0)
        self.keys = data.get("keys", 0)
        self.slots = data.get("slots", {})


class Inventories:
    def __init__(self, data):
        self.inventories = {}
        for appid in data:
            self.inventories[appid] = Inventory(data[appid])


class BackpackVotingSuggestions:
    def __init__(self, data):
        self.created = data.get("created", 0)
        self.accepted = data.get("accepted", 0)
        self.accepted_unusual = data.get("accepted_unusual", 0)


class BackpackVotingVotes:
    def __init__(self, data):
        self.positive = data.get("positive", 0)
        self.negative = data.get("negative", 0)
        self.accepted = data.get("accepted", 0)


class BackpackVoting:
    def __init__(self, data):
        self.reputation = data.get("reputation", 0)
        self.votes = BackpackVotingVotes(data["votes"]) if "votes" in data else False
        self.suggestions = BackpackVotingSuggestions(data["suggestions"]) if "suggestions" in data else False


class BackpackBans:
    def __init__(self, data):
        self.end = data.get("end")
        self.reason = data.get("reason", "")


class ValveBans:
    def __init__(self, data):
        self.economy_ban = True if "economy" in data else False
        self.community_ban = True if "community" in data else False
        self.vac_ban = True if "vac" in data else False
        self.game_ban = True if "game" in data else False


class Bans:
    backpack_ban_types = ["all", "suggestions", "comments", "trust", "issues", "classifieds", "customizations",
                          "reports"]

    def __init__(self, data):
        self.steamrep_scammer = True if "steamrep_scammer" in data else False
        self.steamrep_caution = True if "steamrep_caution" in data else False
        self.valve = ValveBans(data.get("valve", {}))
        self.bp_bans = []
        for ban_type in Bans.backpack_ban_types:
            self.bp_bans[ban_type] = False if ban_type not in data else BackpackBans(data[ban_type])


class BackpackIntegrations:
    def __init__(self, data):
        self.group_member = True if "group_member" in data else False
        self.marketplace_seller = True if "marketplace_seller" in data else False
        self.automatic = True if "automatic" in data else False
        self.steamrep_admin = True if "steamrep_admin" in data else False


class BackpackUser:
    def __init__(self, data):
        self.name = data.get("name")
        self.avatar = data.get("avatar")
        self.last_online = data.get("last_online", 0)
        self.admin = True if "admin" in data else False
        self.donated = data.get("donated", 0)
        self.premium = True if "premium" in data else False
        self.premium_months_gifted = data.get("premium_months_gifted", 0)
        self.integrations = BackpackIntegrations(data.get("integrations", {}))
        self.bans = Bans(data["bans"]) if "bans" in data else False
        self.voting = BackpackVoting(data["voting"]) if "voting" in data else False
        self.inventory = Inventories(data["inventory"]) if "inventory" in data else False
        self.trust = BackpackTrust(data["trust"]) if "trust" in data else False

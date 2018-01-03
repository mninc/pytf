class Stats:
    def __init__(self, data):
        self.bannedfriends = data.get("bannedfriends")
        self.unconfirmedreports = data.get("unconfirmedreports")


class Rep:
    def __init__(self, data):
        self.full = data.get("full")
        self.summary = data.get("summary")
        self.tags = data.get("tags")


class Reputation:
    def __init__(self, data):
        self.flags = data.get("flags")
        self.steamid32 = data.get("steamID32")
        self.steamid64 = data.get("steamID64")
        self.steamrepurl = data.get("steamrepurl")
        self.displayname = data.get("displayname")
        self.rawdisplayname = data.get("rawdisplayname")
        self.avatar = data.get("avatar")
        self.membersince = data.get("membersince")
        self.customurl = data.get("customurl")
        self.tradeban = data.get("tradeban")
        self.vacban = data.get("vacban")
        self.lastsynctime = data.get("lastsynctime")
        self.reputation = Rep(data.get("reputation"))
        self.stats = Stats(data.get("stats"))

effects = {}

qualities = {"Normal": 0,
             "Genuine": 1,
             "Vintage": 3,
             "rarity3": 4,
             "Unusual": 5,
             "Unique": 6,
             "Community": 7,
             "Valve": 8,
             "Self-Made": 9,
             "Customized": 10,
             "Strange": 11,
             "Completed": 12,
             "Haunted": 13,
             "Collector's": 14,
             "Decorated Weapon": 15}

killstreaks = {"None": 0,
               "Killstreak": 1,
               "Specialized Killstreak": 2,
               "Professional Killstreak": 3}

wear = ["Factory New",
        "Minimal Wear",
        "Field-Tested",
        "Well-Worn",
        "Battle Scarred"]
wear_brackets = ["(Factory New)",
                 "(Minimal Wear)",
                 "(Field-Tested)",
                 "(Well-Worn)",
                 "(Battle Scarred)"]

paints = {
    "Indubitably Green": 7511618,
    "Zepheniah's Greed": 4345659,
    "Noble Hatter's Violet": 5322826,
    "Color No. 216-190-216": 14204632,
    "A Deep Commitment to Purple": 8208497,
    "Mann Co. Orange": 13595446,
    "Muskelmannbraun": 10843461,
    "Peculiarly Drab Tincture": 12955537,
    "Radigan Conagher Brown": 6901050,
    "Ye Olde Rustic Colour": 8154199,
    "Australium Gold": 15185211,
    "Aged Moustache Grey": 8289918,
    "An Extraordinary Abundance of Tinge": 15132390,
    "A Distinctive Lack of Hue": 1315860,
    "Team Spirit": 12073019,
    "Pink as Hell": 16738740,
    "A Color Similar to Slate": 3100495,
    "Drably Olive": 8421376,
    "The Bitter Taste of Defeat and Lime": 3329330,
    "The Color of a Gentlemann's Business Pants": 15787660,
    "Dark Salmon Injustice": 15308410,
    "Operator's Overalls": 4732984,
    "Waterlogged Lab Coat": 11049612,
    "Balaclavas Are Forever": 3874595,
    "An Air of Debonair": 6637376,
    "The Value of Teamwork": 8400928,
    "Cream Spirit": 12807213,
    "A Mann's Mint": 12377523,
    "After Eight": 2960676
}

parts = {0: "Kills", 1: "Ubers", 2: "Kill Assists", 3: "Sentry Kills", 4: "Sodden Victims",
         5: "Spies Shocked", 6: "Heads Taken", 7: "Humiliations", 8: "Gifts Given", 9: "Deaths Feigned",
         10: "Scouts Killed", 11: "Snipers Killed", 12: "Soldiers Killed", 13: "Demomen Killed",
         14: "Heavies Killed", 15: "Pyros Killed", 16: "Spies Killed", 17: "Engineers Killed",
         18: "Medics Killed", 19: "Buildings Destroyed", 20: "Projectiles Reflected", 21: "Headshot Kills",
         22: "Airborne Enemy Kills", 23: "Gib Kills", 24: "Buildings Sapped", 25: "Tickle Fights Won",
         26: "Opponents Flattened", 27: "Kills Under A Full Moon", 28: "Dominations", 30: "Revenges",
         31: "Posthumous Kills", 32: "Teammates Extinguished", 33: "Critical Kills",
         34: "Kills While Explosive-Jumping", 36: "Sappers Removed", 37: "Cloaked Spies Killed",
         38: "Medics Killed That Have Full ÜberCharge", 39: "Robots Destroyed", 40: "Giant Robots Destroyed",
         44: "Kills While Low Health", 45: "Kills During Halloween", 46: "Robots Killed During Halloween",
         47: "Defenders Killed", 48: "Submerged Enemy Kills", 49: "Kills While Invuln ÜberCharged",
         50: "Food Items Eaten", 51: "Banners Deployed", 58: "Seconds Cloaked",
         59: "Health Dispensed to Teammates", 60: "Teammates Teleported", 61: "Tanks Destroyed",
         62: "Long-Distance Kills", 63: "KillEaterEvent_UniquePlayerKills", 64: "Points Scored",
         65: "Double Donks", 66: "Teammates Whipped", 67: "Kills during Victory Time",
         68: "Robot Scouts Destroyed", 74: "Robot Spies Destroyed", 77: "Taunt Kills",
         78: "Unusual-Wearing Player Kills", 79: "Burning Player Kills", 80: "Killstreaks Ended",
         81: "Freezecam Taunt Appearances", 82: "Damage Dealt", 83: "Fires Survived", 84: "Allied Healing Done",
         85: "Point Blank Kills", 86: "Wrangled Sentry Kills", 87: "Kills", 88: "Full Health Kills",
         89: "Taunting Player Kills", 90: "Carnival Kills", 91: "Carnival Underworld Kills",
         92: "Carnival Games Won", 93: "Not Crit nor MiniCrit Kills", 94: "Players Hit", 95: "Assists",
         96: "Contracts Completed", 97: "Kills", 98: "Contract Points", 99: "Contract Bonus Points",
         100: "Times Performed", 101: "Kills and Assists during Invasion Event",
         102: "Kills and Assists on 2Fort Invasion", 103: "Kills and Assists on Probed",
         104: "Kills and Assists on Byre", 105: "Kills and Assists on Watergate", 106: "Souls Collected",
         107: "Merasmissions Completed", 108: "Halloween Transmutes Performed", 109: "Power Up Canteens Used",
         110: "Contract Points Earned", 111: "Contract Points Contributed To Friends"}


def swap(obj):
    obj.update({value: key for key, value in obj.items()})


swap(paints)

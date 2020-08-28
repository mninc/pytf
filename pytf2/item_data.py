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


def swap(obj):
    obj.update({value: key for key, value in obj.items()})


swap(paints)

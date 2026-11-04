"""Byte, drawn by hand, one pixel at a time. Grid is 26 wide."""
from pixel import mirror

# left half of the sitting cat, mirrored into a 26 px wide body
BODY = mirror([
    "..o..........",  # 0
    "..oo.........",  # 1
    "..opo........",  # 2
    "..oppo.......",  # 3
    "..opppo......",  # 4
    ".offppfoooooo",  # 5
    ".offffffffdfd",  # 6
    "offfffffffffd",  # 7
    "offffffffffff",  # 8
    "offffffffffff",  # 9
    "offffffffffff",  # 10
    "offkkffffflll",  # 11
    ".offfffffllll",  # 12
    "..oofffffllll",  # 13
    "...offfffffff",  # 14
    "...offfffflll",  # 15
    "..odfffllllll",  # 16
    "..odfflllllll",  # 17
    "..offflllllll",  # 18
    ".offfflllllll",  # 19
    ".offfffllllll",  # 20
    ".offffffollll",  # 21
    ".offffffollll",  # 22
    ".offffffololl",  # 23
    "..ooooooooooo",  # 24
])

# face layers, each one a list of (x, y, rows)
NOSE = [(12, 11, ["pp"]), (12, 12, ["ll"])]

EYES = {
    "open": [(5, 8, ["we", "ee", "ee"]), (19, 8, ["we", "ee", "ee"])],
    "big": [(4, 8, ["wwe", "wee", "eee"]), (19, 8, ["wwe", "wee", "eee"])],
    "shut": [(5, 10, ["oo"]), (19, 10, ["oo"])],
    "sleep": [(4, 9, ["o..o", ".oo."]), (18, 9, ["o..o", ".oo."])],
    "happy": [(4, 9, [".oo.", "o..o"]), (18, 9, [".oo.", "o..o"])],
    "meh": [(5, 9, ["oo", "ee"]), (19, 9, ["oo", "ee"])],
}

MOUTH = {
    "smile": [(11, 12, ["o..o"]), (12, 13, ["oo"])],
    "flat": [(11, 13, ["oooo"])],
    "open": [(11, 12, ["o..o"]), (12, 13, ["mm"]), (12, 14, ["mm"])],
}

# tail frames, drawn relative to the body's bottom right corner
TAIL = [
    [
        "...oo..",
        "..oddo.",
        "..offo.",
        "...offo",
        "...odfo",
        "...offo",
        "..offo.",
        ".offo..",
        "offo...",
        "ffo....",
    ],
    [
        "....oo.",
        "...oddo",
        "...offo",
        "...offo",
        "...odfo",
        "...offo",
        "..offo.",
        ".offo..",
        "offo...",
        "ffo....",
    ],
    [
        "..oo...",
        ".oddo..",
        ".offo..",
        "..offo.",
        "...odfo",
        "...offo",
        "..offo.",
        ".offo..",
        "offo...",
        "ffo....",
    ],
]

HEART = [".hh.hh.", "hhhhhhh", "hhhhhhh", ".hhhhh.", "..hhh..", "...h..."]
ZED = ["zzzz", "..z.", ".z..", "zzzz"]
ZED_S = ["zzz", ".z.", "zzz"]

YARN = [
    "..oooo..",
    ".oyyYyo.",
    "oyYyyyYo",
    "oyyYYyyo",
    "oYyyyYyo",
    "oyyYyyyo",
    ".oyyyYo.",
    "..oooo.y",
]

BOWL = [
    "oooooooooooo",
    "obbbbbbbbbbo",
    ".oBBBBBBBBo.",
    "..oooooooo..",
]

FISH = [
    "..oooo...o",
    ".occcco.oco",
    "ocwcccccco.",
    "occccccooco",
    ".oooooo..o",
]

RUG = [
    "....rrrrrrrrrrrrrrrrrrrrrrrrrr....",
    "..rrRrrRrrRrrRrrRrrRrrRrrRrrRrrr..",
    ".rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr.",
    "..rrRrrRrrRrrRrrRrrRrrRrrRrrRrrr..",
    "....rrrrrrrrrrrrrrrrrrrrrrrrrr....",
]

TEA = [
    "..oooooooooooo..",
    "..oggggggggggo..",
    "..ottttttttTto..",
    "...otttttttTo...",
    "....ottttTto....",
    ".....ottTto.....",
    ".....ottTto.....",
    "....otttttTo....",
    "....otttttTo....",
    "....oooooooo....",
    ".oooooooooooooo.",
    "..obbbbbbbbbbo..",
    "...oooooooooo...",
]

STEAM = [
    ["...s.", "..s..", "..s..", "...s.", "....s"],
    ["..s..", "...s.", "...s.", "..s..", ".s..."],
    [".s...", "..s..", "...s.", "...s.", "..s.."],
]

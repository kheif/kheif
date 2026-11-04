"""Tiny pixel art helpers: ASCII sprites in, crisp SVG rects out."""

PALETTE = {
    "o": "#2a2320",  # ink / outline
    "f": "#e8964a",  # fur
    "d": "#c4682e",  # fur stripes
    "l": "#fbe6c8",  # cream
    "p": "#e88a8a",  # pink
    "k": "#f2b49a",  # blush
    "e": "#2a2320",  # eye
    "w": "#ffffff",  # shine
    "m": "#8b3a3a",  # open mouth
    "h": "#e05a6b",  # heart
    "t": "#b5442f",  # tea
    "T": "#d4664a",  # tea highlight
    "g": "#d9e6ea",  # glass
    "s": "#b8b0a6",  # steam / soft grey
    "r": "#7c9a8e",  # rug
    "R": "#5f7d72",  # rug dark
    "y": "#6f8fd1",  # yarn
    "Y": "#4b6bb0",  # yarn dark
    "b": "#c9c2b8",  # bowl
    "B": "#a39b90",  # bowl dark
    "z": "#8a7f74",  # zzz
    "c": "#6ec6ff",  # fish
}


def mirror(rows):
    """Each row is the left half; the right half is its reflection."""
    return [r + r[::-1] for r in rows]


def sprite(rows, x=0, y=0, px=8, cls=None, palette=PALETTE):
    """Render rows of characters as rects. '.' and ' ' are transparent.

    Horizontal runs of the same colour are merged into one rect to keep
    the file small.
    """
    out = []
    for j, row in enumerate(rows):
        i = 0
        while i < len(row):
            ch = row[i]
            if ch in ". ":
                i += 1
                continue
            k = i
            while k < len(row) and row[k] == ch:
                k += 1
            out.append(
                f'<rect x="{x + i * px}" y="{y + j * px}" width="{(k - i) * px}" '
                f'height="{px}" fill="{palette[ch]}"/>'
            )
            i = k
    body = "".join(out)
    if cls:
        return f'<g class="{cls}">{body}</g>'
    return body


def text(rows, x, y, px, color):
    """Same as sprite() but every non-transparent cell gets one colour."""
    return sprite([r.replace("o", "X") for r in rows], x, y, px, palette={"X": color})


FONT = {
    "m": [".....", ".....", "oo.o.", "o.o.o", "o.o.o", "o.o.o", "o.o.o"],
    "e": [".....", ".....", ".ooo.", "o...o", "ooooo", "o....", ".ooo."],
    "h": ["o....", "o....", "oooo.", "o...o", "o...o", "o...o", "o...o"],
    "t": [".o...", ".o...", "oooo.", ".o...", ".o...", ".o..o", "..oo."],
    "b": ["o....", "o....", "oooo.", "o...o", "o...o", "o...o", "oooo."],
    "y": [".....", ".....", "o...o", "o...o", ".oooo", "....o", "oooo."],
}


def word(s, x, y, px, color, gap=1):
    out = []
    cx = x
    for ch in s:
        g = FONT[ch]
        out.append(text(g, cx, y, px, color))
        cx += (len(g[0]) + gap) * px
    return "".join(out), cx - gap * px

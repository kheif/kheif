#!/usr/bin/env python3
"""Draws the parts of the profile that never change: header and buttons."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cat as C  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")


def tea(x, y):
    """Ince belli tea glass on a saucer, origin at the bottom centre."""
    steam = "".join(
        f'<path class="steam" style="animation-delay:{d}s" d="M{dx} -78 q-7 -10 0 -20 q7 -10 0 -20" '
        f'stroke="#f1e3c8" stroke-width="3" fill="none" stroke-linecap="round" opacity=".6"/>'
        for dx, d in [(-8, 0), (2, 1.1), (12, 2.2)]
    )
    return f"""
  <g transform="translate({x} {y})">
    <ellipse cx="0" cy="2" rx="48" ry="8" fill="#000" opacity=".35"/>
    <ellipse class="ln" cx="0" cy="-6" rx="46" ry="10" fill="#b9b2a6" stroke-width="3"/>
    <ellipse cx="0" cy="-8" rx="34" ry="6" fill="#d9d3c8"/>
    {steam}
    <path d="M-26 -76 C-26 -58 -10 -54 -10 -40 C-10 -28 -22 -24 -20 -12 L20 -12 C22 -24 10 -28 10 -40 C10 -54 26 -58 26 -76z" fill="#a8301e"/>
    <path d="M-26 -80 C-26 -58 -10 -54 -10 -40 C-10 -28 -22 -24 -20 -12 L20 -12 C22 -24 10 -28 10 -40 C10 -54 26 -58 26 -80"
          fill="#e6eef0" fill-opacity=".18" stroke="#1c110b" stroke-width="3.5" stroke-linejoin="round"/>
    <path d="M-27 -80 H27" stroke="#1c110b" stroke-width="3.5" stroke-linecap="round"/>
    <path d="M-20 -72 C-20 -58 -6 -52 -6 -42" stroke="#fff" stroke-width="3" fill="none" opacity=".45" stroke-linecap="round"/>
    <path d="M-24 -76 Q0 -72 24 -76" stroke="#d65a3a" stroke-width="3" fill="none" opacity=".7"/>
  </g>"""


def header():
    W, H = 900, 250
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="hi, i'm mehmet">
  <defs>
    {C.defs()}
    <clipPath id="card"><rect width="{W}" height="{H}" rx="18"/></clipPath>
  </defs>
  <style>{C.CSS}</style>
  <g clip-path="url(#card)">
    {C.backdrop(W, H, table_y=212)}
    <g class="light"><circle cx="640" cy="150" r="230" fill="url(#candle)"/></g>
    {C.motes(18, W, H, seed=11)}

    <text x="56" y="70" font-family="{C.SERIF}" font-style="italic" font-size="20" fill="{C.MUTED}">hi, i'm</text>
    <text x="52" y="140" font-family="{C.SERIF}" font-size="76" fill="#ffb35c" opacity=".35" filter="url(#blur)">Mehmet</text>
    <text x="52" y="140" font-family="{C.SERIF}" font-size="76" fill="{C.TEXT}">Mehmet</text>
    <text x="56" y="178" font-family="{C.SERIF}" font-style="italic" font-size="18" fill="{C.TEXT}" opacity=".85">i write software. mostly on purpose.</text>
    <text x="56" y="202" font-family="{C.SERIF}" font-style="italic" font-size="18" fill="{C.MUTED}">powered by tea, supervised by a cat.</text>

    {tea(600, 222)}
    {C.cat("fine", x=780, y=H + 92, scale=0.82, tail=False)}
    {C.overlay(W, H)}
  </g>
  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="18" fill="none" stroke="#000" stroke-opacity=".5" stroke-width="2"/>
</svg>
"""


ICONS = {
    "feed": """<path class="ln" d="M-14 0 C-8 -9 6 -9 12 0 C6 9 -8 9 -14 0z M12 0 L20 -7 L20 7z" fill="#7fb0d6" stroke-width="2.6"/>
               <circle cx="-7" cy="-2" r="1.8" fill="#1c110b"/>""",
    "play": """<circle class="ln" r="11" fill="#5f7fb8" stroke-width="2.6"/>
               <path d="M-9 -5 Q0 3 9 -6 M-10 2 Q0 9 10 1 M-3 -10 Q5 0 3 10" stroke="#2f4a7a" stroke-width="1.6" fill="none"/>""",
    "pet": """<path class="ln" d="M0 -3 C-4 -11 -15 -8 -13 1 C-11 7 -3 10 0 15 C3 10 11 7 13 1 C15 -8 4 -11 0 -3z" fill="#d9606c" stroke-width="2.6" transform="translate(0 -3)"/>""",
}


def button(kind, label):
    W, H = 150, 48
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{label}">
  <defs>
    <linearGradient id="b" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#4a2c19"/><stop offset="1" stop-color="#2a180e"/>
    </linearGradient>
  </defs>
  <style>.ln {{ stroke: #1c110b; stroke-linejoin: round; }}</style>
  <rect x="1.5" y="1.5" width="{W - 3}" height="{H - 3}" rx="24" fill="url(#b)" stroke="#000" stroke-opacity=".6" stroke-width="2"/>
  <path d="M24 4 H{W - 24}" stroke="#ffcf8a" stroke-opacity=".25" stroke-width="2" stroke-linecap="round"/>
  <g transform="translate(30 {H / 2}) scale(.85)">{ICONS[kind]}</g>
  <text x="60" y="{H / 2 + 6}" font-family="{C.SERIF}" font-style="italic" font-size="18" fill="{C.TEXT}">{label}</text>
</svg>
"""


def main():
    with open(os.path.join(ASSETS, "header.svg"), "w") as f:
        f.write(header())
    for kind, label in [("feed", "feed"), ("play", "play"), ("pet", "pet")]:
        with open(os.path.join(ASSETS, f"btn-{kind}.svg"), "w") as f:
            f.write(button(kind, label))
    print("ok")


if __name__ == "__main__":
    main()

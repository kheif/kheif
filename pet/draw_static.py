#!/usr/bin/env python3
"""Draws the parts of the profile that never change: header and buttons.

Both panels show the same evening corner: a back wall, a side wall with
a window on the right, and a wooden sill that the tea and Byte sit on.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import art as A  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")


def svg(w, h, label, body):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{label}">
  <defs>
    {A.defs()}
    <clipPath id="card"><rect width="{w}" height="{h}" rx="16"/></clipPath>
  </defs>
  <style>{A.CSS}</style>
  <g clip-path="url(#card)"><rect width="{w}" height="{h}" fill="{A.WOOD_DARK}"/>{body}</g>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="16" fill="none" stroke="#1c100a" stroke-opacity=".6" stroke-width="2"/>
</svg>
"""


def intro(x, y, name_size, line_size, gap):
    return f"""
    <text x="{x + 4}" y="{y}" font-family="{A.SERIF}" font-style="italic" font-size="{line_size + 2}" fill="{A.TEXT_SOFT}">hi, i'm</text>
    <text x="{x}" y="{y + name_size * 0.95}" font-family="{A.SERIF}" font-size="{name_size}" fill="{A.TEXT}">Mehmet</text>
    <text x="{x + 4}" y="{y + name_size * 0.95 + gap}" font-family="{A.SERIF}" font-style="italic" font-size="{line_size}" fill="{A.TEXT}" opacity=".92">i write software. mostly on purpose.</text>
    <text x="{x + 4}" y="{y + name_size * 0.95 + gap + line_size * 1.35}" font-family="{A.SERIF}" font-style="italic" font-size="{line_size}" fill="{A.TEXT_SOFT}">powered by tea, supervised by a cat.</text>"""


def header():
    W, H = 900, 250
    top, front = 198, 236
    corner = 744
    light = A.window_light(470, 34, pane_w=62, pane_h=64, gap=9, skew=0.22, slope=-0.06)
    body = f"""
    {A.wall(corner, top, patches=light)}
    {A.side_window(corner, W - corner, 26, top)}
    {A.sill(W, top, front, H, sun_from=0.55, grain_seed=2)}
    {A.cast_shadow(782, 214, 0.5)}
    {A.byte("fine", 782, 214, 0.5)}
    {A.tea(642, 240, 0.92)}
    {intro(50, 62, 72, 18, 34)}"""
    return svg(W, H, "hi, i'm mehmet. tea on the sill, byte the cat behind it.", body)


def header_narrow():
    """Phone layout: the intro on top, the sill scene underneath."""
    W, H = 600, 470
    top, front = 380, 428
    corner = 446
    light = A.window_light(196, 236, pane_w=74, pane_h=56, gap=9, skew=0.22, slope=-0.06)
    body = f"""
    {A.wall(corner, top, patches=light)}
    {A.side_window(corner, W - corner, 150, top)}
    {A.sill(W, top, front, H, sun_from=0.6, grain_seed=2)}
    {A.cast_shadow(470, 398, 0.62)}
    {A.byte("fine", 470, 398, 0.62)}
    {A.tea(300, 424, 1.1)}
    {intro(40, 58, 84, 24, 42)}"""
    return svg(W, H, "hi, i'm mehmet. tea on the sill, byte the cat behind it.", body)


# ------------------------------------------------------------- buttons

ICONS = {
    # a small fish, its head towards the label
    "feed": f"""<g filter="url(#gouache)">
        <path d="M-15 0 C-9 -9 5 -9 12 0 C5 9 -9 9 -15 0z" fill="#d9c7a6"/>
        <path d="M-15 0 C-9 -9 5 -9 12 0z" fill="#efe1c4"/>
        <path d="M12 0 L20 -7 L19 7z" fill="#c9b08a"/></g>
      <path d="M-15 0 C-9 -9 5 -9 12 0 C5 9 -9 9 -15 0z M12 0 L20 -7 L19 7z" fill="none" stroke="{A.INK}" stroke-width="1.4"/>
      <circle cx="-8" cy="-1.5" r="1.4" fill="{A.INK}"/>
      {A.stroke((-3, -5), (0, 0), (-3, 5), 1.1, A.INK, .6)}""",
    "play": f"""<g filter="url(#gouache)"><circle r="11" fill="#5d6f96"/>
        <path d="M0 -11 A11 11 0 0 1 11 0 A11 11 0 0 1 4 10 C7 2 6 -6 0 -11z" fill="#8193b8"/></g>
      <path d="M-9 -6 Q0 2 9 -7 M-10 1 Q0 9 10 0 M-3 -10 Q5 -1 2 10" stroke="#33406a" stroke-width="1.1" fill="none"/>
      <circle r="11" fill="none" stroke="{A.INK}" stroke-width="1.4"/>
      {A.stroke((-10, 7), (-16, 10), (-22, 8), 1.4, "#5d6f96")}""",
    # an open hand would be odd here; a paw print says "pet" in cat
    "pet": f"""<g filter="url(#gouache)">
        <ellipse cx="0" cy="4" rx="7.5" ry="6.5" fill="#e0a38a"/>
        <ellipse cx="-8" cy="-4" rx="3" ry="3.8" fill="#e0a38a"/><ellipse cx="-2.6" cy="-8.4" rx="3" ry="3.8" fill="#e0a38a"/>
        <ellipse cx="3.6" cy="-8.4" rx="3" ry="3.8" fill="#e0a38a"/><ellipse cx="8.8" cy="-4" rx="3" ry="3.8" fill="#e0a38a"/></g>
      <g fill="none" stroke="{A.INK}" stroke-width="1.3">
        <ellipse cx="0" cy="4" rx="7.5" ry="6.5"/><ellipse cx="-8" cy="-4" rx="3" ry="3.8"/><ellipse cx="-2.6" cy="-8.4" rx="3" ry="3.8"/>
        <ellipse cx="3.6" cy="-8.4" rx="3" ry="3.8"/><ellipse cx="8.8" cy="-4" rx="3" ry="3.8"/></g>""",
}


def button(kind, label):
    W, H = 150, 48
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{label}">
  <defs>{A.defs()}</defs>
  <g filter="url(#gouache)">
    <rect x="3" y="4" width="{W - 6}" height="{H - 7}" rx="20" fill="#24160f"/>
    <rect x="3" y="2" width="{W - 6}" height="{H - 7}" rx="20" fill="{A.WALL_MID}"/>
  </g>
  <rect x="3" y="2" width="{W - 6}" height="{H - 7}" rx="20" fill="none" stroke="{A.INK}" stroke-width="1.5" opacity=".9"/>
  {A.stroke((24, 4.5), (75, 3.5), (126, 4.5), 1.6, A.WOOD_EDGE, .55)}
  <g transform="translate(34 {(H - 5) / 2})">{ICONS[kind]}</g>
  <text x="62" y="{(H - 5) / 2 + 6}" font-family="{A.SERIF}" font-style="italic" font-size="19" fill="{A.TEXT}">{label}</text>
</svg>
"""


def main():
    files = {
        "header.svg": header(),
        "header-narrow.svg": header_narrow(),
    }
    for kind in ("feed", "play", "pet"):
        files[f"btn-{kind}.svg"] = button(kind, kind)
    for name, content in files.items():
        with open(os.path.join(ASSETS, name), "w") as f:
            f.write(content)
    print("ok")


if __name__ == "__main__":
    main()

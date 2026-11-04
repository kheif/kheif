#!/usr/bin/env python3
"""Draws the parts of the profile that never change: header and buttons."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sprites as S  # noqa: E402
from byte import INK, MONO, MUTED, PAPER, frames, layers  # noqa: E402
from pixel import sprite, word  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")


def header():
    W, H = 900, 230
    name, end = word("mehmet", 48, 70, 10, INK)
    shadow, _ = word("mehmet", 53, 75, 10, "#e8964a")

    # tea glass with three frames of steam
    gx, gy, gp = 540, 78, 7
    steam = "".join(
        f'<g class="steam{i}">{sprite(f, gx + 5 * gp, gy - 6 * gp, gp)}</g>' for i, f in enumerate(S.STEAM)
    )

    # byte peeking in from the bottom edge
    px = 6
    bx, by = 700, H - 3 - 12 * px
    head = S.BODY[:12]
    peek = (
        sprite(head, bx, by, px)
        + f'<g class="blink0">{layers(S.EYES["open"], bx, by, px)}</g>'
        + f'<g class="blink1">{layers(S.EYES["shut"], bx, by, px)}</g>'
        + layers([(12, 11, ["pp"])], bx, by, px)
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="hi, i'm mehmet" shape-rendering="crispEdges">
  <style>
    {frames("steam", 3, 1.5, [0, 1, 2])}
    {frames("blink", 2, 5, [0] * 16 + [1] + [0] * 6 + [1])}
    {frames("cur", 2, 1.1, [0, 1])}
  </style>
  <defs><clipPath id="card"><rect x="4.5" y="4.5" width="{W - 9}" height="{H - 9}" rx="13"/></clipPath></defs>
  <rect x="3" y="3" width="{W - 6}" height="{H - 6}" rx="14" fill="{PAPER}"/>

  <text x="50" y="52" font-family="{MONO}" font-size="16" fill="{MUTED}">hi, i'm</text>
  {shadow}
  {name}
  <rect class="cur0" x="{end + 14}" y="130" width="22" height="10" fill="{INK}"/>
  <text x="50" y="182" font-family="{MONO}" font-size="16" fill="{INK}">i write software. mostly on purpose.</text>
  <text x="50" y="204" font-family="{MONO}" font-size="16" fill="{MUTED}">powered by tea, supervised by a cat.</text>

  {steam}
  {sprite(S.TEA, gx, gy, gp)}

  <g clip-path="url(#card)">{peek}</g>
  <rect x="3" y="3" width="{W - 6}" height="{H - 6}" rx="14" fill="none" stroke="{INK}" stroke-width="3"/>
</svg>
"""


ICONS = {
    "feed": S.FISH,
    "play": [r[:7] for r in S.YARN[:7]],
    "pet": S.HEART,
}
COLORS = {"feed": "#e8964a", "play": "#6f8fd1", "pet": "#e05a6b"}


def button(kind, label):
    W, H = 34 + 14 * 2 + 9.6 * len(label) + 40, 52
    W = int(W)
    icon = ICONS[kind]
    ip = 3
    ih = len(icon) * ip
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{label}" shape-rendering="crispEdges">
  <rect x="7" y="7" width="{W - 8}" height="{H - 8}" fill="{INK}"/>
  <rect x="1.5" y="1.5" width="{W - 9}" height="{H - 9}" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>
  <rect x="1.5" y="1.5" width="8" height="{H - 9}" fill="{COLORS[kind]}" stroke="{INK}" stroke-width="3"/>
  {sprite(icon, 22, int((H - 6 - ih) / 2), ip)}
  <text x="{22 + len(icon[0]) * ip + 12}" y="{(H - 6) / 2 + 6}" font-family="{MONO}" font-size="16" font-weight="700" fill="{INK}">{label}</text>
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

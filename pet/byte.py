#!/usr/bin/env python3
"""Byte the README cat.

Visitors open an issue titled "byte|feed", "byte|play" or "byte|pet".
The GitHub Action runs this script, which updates pet/state.json,
redraws assets/byte.svg, refreshes the visitor list in README.md and
writes a thank-you comment to pet/reply.md.

Usage:
  python pet/byte.py tick                 # time passes, nothing else
  python pet/byte.py <action> <username>  # action: feed | play | pet
"""
import html
import json
import os
import re
import sys
import time
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = os.path.join(ROOT, "pet", "state.json")
SVG = os.path.join(ROOT, "assets", "byte.svg")
README = os.path.join(ROOT, "README.md")
REPLY = os.path.join(ROOT, "pet", "reply.md")

ACTIONS = {
    # action: (fullness, joy, energy)
    "feed": (28, 6, 4),
    "play": (-6, 26, -16),
    "pet": (0, 14, 12),
}
VERBS = {"feed": "fed", "play": "played with", "pet": "petted"}
EMOJI = {"feed": "🐟", "play": "🧶", "pet": "🤗"}

REPLIES = {
    "feed": [
        "*nom nom nom* 🐟 Byte devoured it in 0.3 seconds and is now staring at you for seconds.",
        "Byte ate the fish, then knocked your coffee off the table as a thank you. 🐟☕",
        "Delicious! Byte gives this fish 5 stars and a slow blink. 🐟⭐",
    ],
    "play": [
        "Byte went full zoomies mode and attacked the yarn ball like it owed rent. 🧶💨",
        "The yarn is destroyed. Byte is victorious. You are now Byte's favourite human. 🧶🏆",
        "Byte did a backflip (probably). 10/10 play session. 🧶✨",
    ],
    "pet": [
        "*purrrrrrrrr* 🤗 Byte headbutted your hand and decided you may stay.",
        "Byte rolled over to show the belly. It is a trap. You fell for it. It was worth it. 🤗",
        "Purr level: maximum. Byte is now a loaf of happiness. 🍞🤗",
    ],
}


def clamp(v):
    return max(0, min(100, int(round(v))))


def load():
    with open(STATE, encoding="utf-8") as f:
        return json.load(f)


def save(state):
    with open(STATE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
        f.write("\n")


def decay(state, now):
    hours = max(0.0, (now - state.get("updated", now)) / 3600)
    state["fullness"] = clamp(state["fullness"] - 2.0 * hours)
    state["joy"] = clamp(state["joy"] - 1.2 * hours)
    state["energy"] = clamp(state["energy"] + 2.5 * hours)
    state["updated"] = int(now)


def mood(state):
    if state["fullness"] < 30:
        return "hungry"
    if state["energy"] < 25:
        return "sleepy"
    if state["joy"] >= 70:
        return "happy"
    if state["joy"] < 30:
        return "bored"
    return "chill"


MOOD_TEXT = {
    "hungry": "is HUNGRY. please. a fish. any fish.",
    "sleepy": "is sleepy. shhh... zzz",
    "happy": "is very happy and purring",
    "bored": "is bored. throw the yarn!",
    "chill": "is chilling on the cushion",
}


# --------------------------------------------------------------------------- svg


def eyes(m):
    if m == "happy":
        return (
            '<path d="M-26 -6 q8 -10 16 0" class="ln"/>'
            '<path d="M10 -6 q8 -10 16 0" class="ln"/>'
        )
    if m == "sleepy":
        return (
            '<path d="M-26 -4 q8 6 16 0" class="ln"/>'
            '<path d="M10 -4 q8 6 16 0" class="ln"/>'
        )
    big = 9 if m == "hungry" else 7
    shine = 3 if m == "hungry" else 2.2
    return (
        '<g class="blink">'
        f'<circle cx="-18" cy="-6" r="{big}" fill="#2b2141"/>'
        f'<circle cx="18" cy="-6" r="{big}" fill="#2b2141"/>'
        f'<circle cx="-15" cy="-9" r="{shine}" fill="#fff"/>'
        f'<circle cx="21" cy="-9" r="{shine}" fill="#fff"/>'
        "</g>"
    )


def mouth(m):
    if m == "hungry":
        return '<ellipse cx="0" cy="12" rx="5" ry="6" fill="#7a2e3a"/>'
    if m == "bored":
        return '<path d="M-6 12 h12" class="ln"/>'
    return '<path d="M-9 9 q4.5 6 9 0 q4.5 6 9 0" class="ln"/>'


def extras(m):
    if m == "happy":
        hearts = []
        for i, (x, d) in enumerate([(-70, 0), (60, 1.2), (-40, 2.4)]):
            hearts.append(
                f'<g transform="translate({x} -70)"><path class="heart" style="animation-delay:{d}s" '
                'd="M0 4 C-8 -6 -18 2 0 14 C18 2 8 -6 0 4z" fill="#ff7aa8"/></g>'
            )
        return "".join(hearts)
    if m == "sleepy":
        return (
            '<text class="zz" x="56" y="-60" font-size="22">z</text>'
            '<text class="zz" style="animation-delay:1s" x="70" y="-74" font-size="16">z</text>'
            '<text class="zz" style="animation-delay:2s" x="82" y="-86" font-size="12">z</text>'
        )
    if m == "hungry":
        return (
            '<g class="bubble" transform="translate(62 -92)">'
            '<rect x="-4" y="-22" width="70" height="40" rx="18" fill="#fff4e6"/>'
            '<path d="M6 14 l-10 14 l18 -10z" fill="#fff4e6"/>'
            '<path d="M14 -2 q14 -14 30 0 q-16 14 -30 0z" fill="#6ec6ff"/>'
            '<path d="M44 -2 l10 -8 v16z" fill="#6ec6ff"/>'
            '<circle cx="22" cy="-4" r="2" fill="#2b2141"/>'
            "</g>"
        )
    if m == "bored":
        return (
            '<g transform="translate(-100 70)">'
            '<circle r="16" fill="#ff9ec7"/>'
            '<path d="M-12 -8 q12 8 24 0 M-14 2 q14 8 28 0 M-10 10 q10 5 20 0" '
            'stroke="#e46b9d" stroke-width="2" fill="none"/>'
            "</g>"
        )
    return ""


def bar(y, label, value, color):
    w = int(260 * value / 100)
    return (
        f'<text x="0" y="{y}" class="lbl">{label}</text>'
        f'<rect x="96" y="{y - 13}" width="260" height="16" rx="8" fill="#ffffff" fill-opacity=".08"/>'
        f'<rect class="fill" x="96" y="{y - 13}" width="{max(w, 16)}" height="16" rx="8" fill="{color}"/>'
        f'<text x="368" y="{y}" class="num">{value}</text>'
    )


def render(state):
    m = mood(state)
    c = state["counts"]
    last = state["visitors"][0] if state["visitors"] else None
    if last:
        who = html.escape(last["user"])
        last_line = f'last visitor: @{who} {VERBS[last["action"]]} Byte'
    else:
        last_line = "no visitors yet. be the first!"
    breath = "3.2s" if m != "sleepy" else "5s"
    tail = "1.4s" if m in ("happy", "bored") else "3s"

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="900" height="300" viewBox="0 0 900 300" role="img" aria-label="Byte the cat {html.escape(MOOD_TEXT[m])}">
  <style>
    .sans {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; }}
    .mono {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .ln {{ stroke: #2b2141; stroke-width: 3.5; fill: none; stroke-linecap: round; }}
    .lbl {{ font: 600 15px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; fill: #c9b8ff; }}
    .num {{ font: 700 15px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; fill: #fff4e6; }}
    @keyframes breathe {{ 0%,100% {{ transform: scale(1,1) }} 50% {{ transform: scale(1.03,.97) }} }}
    .body {{ transform-box: fill-box; transform-origin: 50% 100%; animation: breathe {breath} ease-in-out infinite; }}
    @keyframes tail {{ 0%,100% {{ transform: rotate(-10deg) }} 50% {{ transform: rotate(14deg) }} }}
    .tail {{ transform-box: fill-box; transform-origin: 0% 100%; animation: tail {tail} ease-in-out infinite; }}
    @keyframes blink {{ 0%,92%,100% {{ transform: scaleY(1) }} 95% {{ transform: scaleY(.1) }} }}
    .blink {{ transform-box: fill-box; transform-origin: center; animation: blink 4s infinite; }}
    @keyframes ear {{ 0%,86%,100% {{ transform: rotate(0) }} 90% {{ transform: rotate(-12deg) }} 94% {{ transform: rotate(4deg) }} }}
    .ear {{ transform-box: fill-box; transform-origin: 50% 100%; animation: ear 5s infinite; }}
    @keyframes float {{ 0% {{ opacity: 0; transform: translateY(10px) scale(.6) }} 25% {{ opacity: 1 }} 100% {{ opacity: 0; transform: translateY(-40px) scale(1.1) }} }}
    .heart {{ transform-box: fill-box; animation: float 3.6s ease-out infinite; opacity: 0; }}
    .zz {{ font: 700 20px -apple-system, "Segoe UI", Arial, sans-serif; fill: #c9b8ff; animation: float 3s ease-out infinite; opacity: 0; }}
    @keyframes bob {{ 0%,100% {{ transform: translate(62px,-92px) }} 50% {{ transform: translate(62px,-98px) }} }}
    .bubble {{ animation: bob 1.6s ease-in-out infinite; }}
    @keyframes grow {{ from {{ transform: scaleX(0) }} to {{ transform: scaleX(1) }} }}
    .fill {{ transform-box: fill-box; transform-origin: 0 50%; animation: grow 1.2s cubic-bezier(.2,.9,.3,1.2) both; }}
  </style>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#2b2141"/><stop offset="1" stop-color="#16182b"/>
    </linearGradient>
  </defs>
  <rect width="900" height="300" rx="24" fill="url(#bg)"/>

  <!-- the cat -->
  <g transform="translate(220 196)">
    <ellipse cx="0" cy="62" rx="150" ry="22" fill="#6f4ea8"/>
    <ellipse cx="0" cy="54" rx="140" ry="20" fill="#8b6cc4"/>
    {extras(m)}
    <path class="tail" d="M70 40 q50 -10 46 -60 q-2 -16 12 -14 q14 4 6 30 q-8 50 -60 60z" fill="#f4a259"/>
    <g class="body">
      <ellipse cx="0" cy="22" rx="92" ry="44" fill="#f4a259"/>
      <path d="M-40 -6 q8 18 0 40 M-16 -12 q8 20 0 46 M40 -6 q-8 18 0 40" stroke="#e08a3e" stroke-width="6" fill="none" stroke-linecap="round"/>
      <ellipse cx="-50" cy="58" rx="20" ry="10" fill="#fbd3a6"/>
      <ellipse cx="50" cy="58" rx="20" ry="10" fill="#fbd3a6"/>
      <g transform="translate(0 -30)">
        <path class="ear" d="M-58 -20 l6 -46 l34 26z" fill="#f4a259"/>
        <path class="ear" d="M-50 -26 l4 -28 l18 16z" fill="#ffb3c7"/>
        <path d="M58 -20 l-6 -46 l-34 26z" fill="#f4a259"/>
        <path d="M50 -26 l-4 -28 l-18 16z" fill="#ffb3c7"/>
        <ellipse cx="0" cy="0" rx="64" ry="50" fill="#f4a259"/>
        <path d="M-10 -48 q4 12 0 20 M0 -50 q4 12 0 22 M10 -48 q4 12 0 20" stroke="#e08a3e" stroke-width="4" fill="none" stroke-linecap="round"/>
        <ellipse cx="-36" cy="12" rx="10" ry="6" fill="#ff8fab" fill-opacity=".6"/>
        <ellipse cx="36" cy="12" rx="10" ry="6" fill="#ff8fab" fill-opacity=".6"/>
        {eyes(m)}
        <path d="M-4 4 h8 l-4 5z" fill="#ff6f91"/>
        {mouth(m)}
        <path d="M-30 6 h-26 M-30 12 l-24 6 M30 6 h26 M30 12 l24 6" stroke="#2b2141" stroke-width="1.6" stroke-linecap="round" opacity=".6"/>
      </g>
    </g>
  </g>

  <!-- stats -->
  <g transform="translate(470 0)">
    <text x="0" y="62" class="sans" font-size="34" font-weight="800" fill="#fff4e6">Byte</text>
    <text x="96" y="62" class="sans" font-size="16" fill="#a99dd0">{html.escape(MOOD_TEXT[m])}</text>
    <g transform="translate(0 112)">
      {bar(0, "food", state["fullness"], "#ffb86b")}
      {bar(36, "love", state["joy"], "#ff7aa8")}
      {bar(72, "nap", state["energy"], "#7ad0ff")}
    </g>
    <text x="0" y="236" class="mono" font-size="14" fill="#a99dd0">{last_line}</text>
    <text x="0" y="262" class="mono" font-size="14" fill="#8b7fb8">fish {c["feed"]}  ·  yarn {c["play"]}  ·  pets {c["pet"]}  ·  friends {len(state["friends"])}</text>
  </g>
</svg>
"""


# ---------------------------------------------------------------------- readme


def update_readme(state):
    if not os.path.exists(README):
        return
    with open(README, encoding="utf-8") as f:
        text = f.read()
    rows = []
    for v in state["visitors"][:5]:
        user = v["user"]
        date = datetime.fromtimestamp(v["at"], timezone.utc).strftime("%b %d")
        rows.append(
            f"{EMOJI[v['action']]} [@{user}](https://github.com/{user}) "
            f"{VERBS[v['action']]} Byte <sub>{date}</sub>"
        )
    body = "<br>\n".join(rows) if rows else "<i>nobody yet. be the first one!</i>"
    block = f"<!-- BYTE:START -->\n{body}\n<!-- BYTE:END -->"
    text = re.sub(r"<!-- BYTE:START -->.*?<!-- BYTE:END -->", lambda _: block, text, flags=re.S)
    with open(README, "w", encoding="utf-8") as f:
        f.write(text)


# ------------------------------------------------------------------------ main


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)
    action = args[0].strip().lower()
    now = time.time()
    state = load()
    decay(state, now)

    if action in ACTIONS:
        user = args[1] if len(args) > 1 else "someone"
        if not re.fullmatch(r"[A-Za-z0-9-]{1,39}(\[bot\])?", user):
            user = "someone"
        df, dj, de = ACTIONS[action]
        state["fullness"] = clamp(state["fullness"] + df)
        state["joy"] = clamp(state["joy"] + dj)
        state["energy"] = clamp(state["energy"] + de)
        state["counts"][action] += 1
        if user not in state["friends"]:
            state["friends"].append(user)
        state["visitors"].insert(0, {"user": user, "action": action, "at": int(now)})
        state["visitors"] = state["visitors"][:10]

        total = sum(state["counts"].values())
        pick = REPLIES[action][total % len(REPLIES[action])]
        m = mood(state)
        with open(REPLY, "w", encoding="utf-8") as f:
            f.write(
                f"Hey @{user}! {pick}\n\n"
                f"| food | love | nap |\n|:-:|:-:|:-:|\n"
                f"| {state['fullness']} | {state['joy']} | {state['energy']} |\n\n"
                f"Byte {MOOD_TEXT[m]}. You are friend **#{state['friends'].index(user) + 1}** "
                f"and this was interaction **#{total}**. "
                f"Your name is on the [profile](https://github.com/kheif) now, go take a look! 🐾\n"
            )
    elif action != "tick":
        print(f"unknown action: {action}")
        sys.exit(2)

    save(state)
    with open(SVG, "w", encoding="utf-8") as f:
        f.write(render(state))
    update_readme(state)
    print(f"ok: {action} -> {mood(state)}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Byte, the cat that lives on this profile.

Visitors open an issue titled "byte|feed", "byte|play" or "byte|pet".
A GitHub Action runs this script, which updates pet/state.json, redraws
assets/byte.svg, refreshes README.md and writes the issue reply to
pet/reply.md.

  python pet/byte.py tick               time passes
  python pet/byte.py <action> <user>    action is feed, play or pet
"""
import html
import json
import os
import re
import sys
import time
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sprites as S  # noqa: E402
from pixel import sprite, word  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = os.path.join(ROOT, "pet", "state.json")
SVG = os.path.join(ROOT, "assets", "byte.svg")
README = os.path.join(ROOT, "README.md")
REPLY = os.path.join(ROOT, "pet", "reply.md")

INK, PAPER, MUTED = "#2a2320", "#f4ecdf", "#8a7f74"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"

ACTIONS = {
    # action: (food, love, energy)
    "feed": (30, 5, 0),
    "play": (-5, 25, -20),
    "pet": (0, 15, 10),
}
NOUN = {"feed": "fish", "play": "yarn", "pet": "pets"}

# Byte writes in a diary. Byte is not impressed by much.
DIARY = {
    "feed": [
        "{u} brought a fish. i ate it. no further comment.",
        "fish from {u}. adequate.",
        "{u} fed me. i will be hungry again in four hours. this is not a threat.",
        "{u} gave me a fish. i ate half and looked at the other half for a while.",
    ],
    "play": [
        "{u} threw the yarn. i caught it. then i ignored it.",
        "played with {u}. i won.",
        "{u} has a string. i had no choice.",
        "{u} wanted to play. i pretended not to, then did.",
    ],
    "pet": [
        "{u} pet me. i allowed it.",
        "{u} scratched behind my ears. correct location.",
        "{u} tried the belly. bold. i respect it.",
        "{u} pet me exactly three times. i counted.",
    ],
    "hungry": [
        "nobody came. i stared at the bowl until it got dark.",
        "the bowl is still empty. i am writing this down.",
    ],
    "idle": [
        "knocked a pen off the desk. it had it coming.",
        "sat in a sunbeam. the sunbeam moved. i did not.",
        "mehmet was typing. i sat on the keyboard. you are welcome.",
        "slept 14 hours. productive day.",
        "saw a bird through the window. told no one.",
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
    state["food"] = clamp(state["food"] - 2.0 * hours)
    state["love"] = clamp(state["love"] - 1.2 * hours)
    state["energy"] = clamp(state["energy"] + 2.5 * hours)
    state["updated"] = int(now)


def mood(state):
    if state["food"] < 30:
        return "hungry"
    if state["energy"] < 25:
        return "asleep"
    if state["love"] >= 70:
        return "happy"
    if state["love"] < 30:
        return "bored"
    return "fine"


STATUS = {
    "hungry": "hungry. staring at the bowl.",
    "asleep": "asleep. do not.",
    "happy": "purring. a rare event.",
    "bored": "bored. the yarn is right there.",
    "fine": "fine. tolerating everyone.",
}


def write_diary(state, kind, user=None):
    lines = DIARY[kind]
    n = state["counts"].get("diary", 0)
    line = lines[n % len(lines)].format(u=user or "someone")
    state["counts"]["diary"] = n + 1
    state["diary"].insert(0, {"at": state["updated"], "text": line})
    state["diary"] = state["diary"][:12]
    return line


# --------------------------------------------------------------------- drawing


def frames(name, n, dur, seq):
    """CSS that shows sprite frame seq[i] during slot i of a loop."""
    css = []
    slots = len(seq)
    for f in range(n):
        on = [i for i, s in enumerate(seq) if s == f]
        stops = []
        for i in range(slots):
            a, b = i * 100 / slots, (i + 1) * 100 / slots - 0.01
            v = 1 if i in on else 0
            stops.append(f"{a:.2f}%,{b:.2f}% {{ opacity: {v} }}")
        css.append(
            f"@keyframes {name}{f} {{ {' '.join(stops)} }} "
            f".{name}{f} {{ opacity: 0; animation: {name}{f} {dur}s step-end infinite; }}"
        )
    return "\n    ".join(css)


def layers(items, ox, oy, px):
    return "".join(sprite(r, ox + x * px, oy + y * px, px) for x, y, r in items)


def draw_cat(m, ox, oy, px):
    eyes = {"hungry": "big", "asleep": "sleep", "happy": "happy", "bored": "meh", "fine": "open"}[m]
    mouth = {"hungry": "open", "asleep": "flat", "happy": "smile", "bored": "flat", "fine": "smile"}[m]
    out = []

    # tail behind the body, three frames
    tx, ty = ox + 23 * px, oy + 13 * px
    for i, t in enumerate(S.TAIL):
        out.append(f'<g class="tail{i}">{sprite(t, tx, ty, px)}</g>')

    out.append(sprite(S.BODY, ox, oy, px))
    out.append(layers(S.NOSE, ox, oy, px))

    if m == "hungry":
        # mouth goes "mew", eyes stay big
        out.append(layers(S.EYES[eyes], ox, oy, px))
        out.append(f'<g class="mew0">{layers(S.MOUTH["smile"], ox, oy, px)}</g>')
        out.append(f'<g class="mew1">{layers(S.MOUTH["open"], ox, oy, px)}</g>')
    elif m in ("asleep", "happy"):
        out.append(layers(S.EYES[eyes], ox, oy, px))
        out.append(layers(S.MOUTH[mouth], ox, oy, px))
    else:
        out.append(f'<g class="blink0">{layers(S.EYES[eyes], ox, oy, px)}</g>')
        out.append(f'<g class="blink1">{layers(S.EYES["shut"], ox, oy, px)}</g>')
        out.append(layers(S.MOUTH[mouth], ox, oy, px))
    return "".join(out)


def props(m, ox, oy, px):
    """Things around the cat that depend on the mood."""
    if m == "hungry":
        bowl = sprite(S.BOWL, ox - 15 * px, oy + 21 * px, px)
        mew = (
            f'<text class="mew1" x="{ox - 12 * px}" y="{oy + 6 * px}" '
            f'font-family="{MONO}" font-size="18" font-weight="700" fill="{INK}">mew.</text>'
        )
        return bowl + mew
    if m == "bored":
        return sprite(S.YARN, ox - 12 * px, oy + 17 * px, px)
    if m == "happy":
        out = []
        for i, (x, y) in enumerate([(-8, 2), (28, -1), (-4, -3)]):
            out.append(
                f'<g class="rise" style="animation-delay:{i * 1.1:.1f}s">'
                f"{sprite(S.HEART, ox + x * px, oy + y * px, px // 2)}</g>"
            )
        return "".join(out)
    if m == "asleep":
        return (
            f'<g class="rise">{sprite(S.ZED, ox + 27 * px, oy + 2 * px, px // 2 + 1)}</g>'
            f'<g class="rise" style="animation-delay:1.6s">{sprite(S.ZED_S, ox + 31 * px, oy - 2 * px, px // 2)}</g>'
        )
    return ""


def meter(x, y, label, value, color):
    filled = round(value / 10)
    out = [
        f'<text x="{x}" y="{y + 13}" font-family="{MONO}" font-size="14" fill="{MUTED}">{label}</text>'
    ]
    for i in range(10):
        sx = x + 64 + i * 22
        if i < filled:
            out.append(f'<rect x="{sx}" y="{y}" width="18" height="18" fill="{color}"/>')
            out.append(f'<rect x="{sx}" y="{y + 14}" width="18" height="4" fill="{INK}" fill-opacity=".18"/>')
        else:
            out.append(
                f'<rect x="{sx + 1.5}" y="{y + 1.5}" width="15" height="15" fill="none" '
                f'stroke="{INK}" stroke-opacity=".25" stroke-width="3"/>'
            )
    return "".join(out)


def render(state):
    m = mood(state)
    c = state["counts"]
    px = 8
    W, H = 900, 290
    cx, cy = 150, 38  # cat origin

    tail_speed = {"happy": 0.9, "asleep": 4.0, "bored": 2.6}.get(m, 1.6)
    name, _ = word("byte", 470, 30, 6, INK)

    last = ""
    if state["visitors"]:
        v = state["visitors"][0]
        when = datetime.fromtimestamp(v["at"], timezone.utc).strftime("%b %d").lower()
        last = f"last visit: {html.escape(v['user'])}, {NOUN[v['action']]}, {when}"
    else:
        last = "no visitors yet."

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="byte the cat is {html.escape(STATUS[m])}" shape-rendering="crispEdges">
  <style>
    {frames("tail", 3, tail_speed, [0, 1, 0, 2])}
    {frames("blink", 2, 4.5, [0] * 14 + [1])}
    {frames("mew", 2, 1.8, [0, 0, 1])}
    @keyframes rise {{ 0% {{ transform: translateY(0); opacity: 0 }} 15% {{ opacity: 1 }} 100% {{ transform: translateY(-40px); opacity: 0 }} }}
    .rise {{ opacity: 0; animation: rise 3.2s steps(10) infinite; }}
  </style>
  <rect x="3" y="3" width="{W - 6}" height="{H - 6}" rx="14" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>

  {sprite(S.RUG, cx - 4 * px, cy + 23 * px, px)}
  {props(m, cx, cy, px)}
  {draw_cat(m, cx, cy, px)}

  <g>
    {name}
    <text x="470" y="104" font-family="{MONO}" font-size="15" fill="{INK}">{html.escape(STATUS[m])}</text>
    {meter(470, 128, "food", state["food"], "#e8964a")}
    {meter(470, 158, "love", state["love"], "#e05a6b")}
    {meter(470, 188, "nap", state["energy"], "#6f8fd1")}
    <text x="470" y="242" font-family="{MONO}" font-size="13" fill="{MUTED}">{last}</text>
    <text x="470" y="264" font-family="{MONO}" font-size="13" fill="{MUTED}">{c["feed"]} fish, {c["play"]} yarn, {c["pet"]} pets, {len(state["friends"])} {"friend" if len(state["friends"]) == 1 else "friends"} so far</text>
  </g>
</svg>
"""


# ---------------------------------------------------------------------- readme


def replace_block(text, tag, body):
    return re.sub(
        rf"<!-- {tag}:START -->.*?<!-- {tag}:END -->",
        lambda _: f"<!-- {tag}:START -->\n{body}\n<!-- {tag}:END -->",
        text,
        flags=re.S,
    )


def update_readme(state):
    if not os.path.exists(README):
        return
    with open(README, encoding="utf-8") as f:
        text = f.read()

    seen, people = set(), []
    for v in state["visitors"]:
        if v["user"] not in seen:
            seen.add(v["user"])
            people.append(f'<a href="https://github.com/{v["user"]}"><img src="https://github.com/{v["user"]}.png?size=64" width="32" height="32" alt="{v["user"]}" title="{v["user"]}"></a>')
        if len(people) == 12:
            break
    regulars = " ".join(people) if people else "<sub>nobody yet.</sub>"

    if state["diary"]:
        lines = []
        for d in state["diary"][:8]:
            day = datetime.fromtimestamp(d["at"], timezone.utc).strftime("%b %d").lower()
            lines.append(f"{day}  {d['text']}")
        diary = "```text\n" + "\n".join(lines) + "\n```"
    else:
        diary = "```text\n(empty. byte has not written anything yet.)\n```"

    text = replace_block(text, "BYTE", regulars)
    text = replace_block(text, "DIARY", diary)
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
        user = args[1] if len(args) > 1 else ""
        if not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})", user):
            print("refusing: not a github login")
            sys.exit(2)
        df, dl, de = ACTIONS[action]
        state["food"] = clamp(state["food"] + df)
        state["love"] = clamp(state["love"] + dl)
        state["energy"] = clamp(state["energy"] + de)
        state["counts"][action] += 1
        if user not in state["friends"]:
            state["friends"].append(user)
        state["visitors"].insert(0, {"user": user, "action": action, "at": int(now)})
        state["visitors"] = state["visitors"][:30]
        line = write_diary(state, action, user)

        def bar(v):
            return "▮" * round(v / 10) + "▯" * (10 - round(v / 10))

        with open(REPLY, "w", encoding="utf-8") as f:
            f.write(
                f"from byte's diary:\n\n> {line}\n\n"
                f"```text\nfood {bar(state['food'])}\nlove {bar(state['love'])}\nnap  {bar(state['energy'])}\n```\n\n"
                f"<sub>you're on the profile now, top of the regulars list. come back when byte gets hungry.</sub>\n"
            )
    elif action == "tick":
        # at most one diary entry a day when nobody shows up
        last = state["diary"][0]["at"] if state["diary"] else 0
        if now - last > 20 * 3600:
            write_diary(state, "hungry" if mood(state) == "hungry" else "idle")
    else:
        print(f"unknown action: {action}")
        sys.exit(2)

    save(state)
    with open(SVG, "w", encoding="utf-8") as f:
        f.write(render(state))
    update_readme(state)
    print(f"ok: {action} -> {mood(state)}")


if __name__ == "__main__":
    main()

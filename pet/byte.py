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
import art as A  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = os.path.join(ROOT, "pet", "state.json")
SVG = os.path.join(ROOT, "assets", "byte.svg")
SVG_NARROW = os.path.join(ROOT, "assets", "byte-narrow.svg")
README = os.path.join(ROOT, "README.md")
REPLY = os.path.join(ROOT, "pet", "reply.md")


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
    "hungry": "hungry. the last fish did not last.",
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


def props(m, x, y, s=1.0):
    """Small things on the sill that depend on the mood."""
    if m == "hungry":
        return A.dish(x, y, s, bones=True)
    if m == "bored":
        return A.yarn(x, y, s)
    return ""


def meter(x, y, label, value, color, size=16, w=220):
    """A painted bar: a dark groove in the wall and a gouache fill."""
    fill = max(6, round(w * value / 100))
    lx = x + size * 3.6
    h = max(8, size * 0.55)
    return f"""
    <text x="{x}" y="{y + h}" font-family="{A.SERIF}" font-style="italic" font-size="{size}" fill="{A.TEXT_SOFT}">{label}</text>
    <rect x="{lx}" y="{y + 1}" width="{w}" height="{h}" rx="{h / 2}" fill="#1e130e" opacity=".75"/>
    <rect x="{lx}" y="{y}" width="{fill}" height="{h}" rx="{h / 2}" fill="{color}"/>
    <text x="{lx + w + 16}" y="{y + h}" font-family="{A.SERIF}" font-size="{size - 1}" fill="{A.TEXT}">{value}</text>"""


def readout(state, m, x, y, k=1.0):
    """Name, mood and the three meters, laid out from (x, y)."""
    c = state["counts"]
    if state["visitors"]:
        v = state["visitors"][0]
        when = datetime.fromtimestamp(v["at"], timezone.utc).strftime("%b %d").lower()
        last = f"last visit: {html.escape(v['user'])}, {NOUN[v['action']]}, {when}"
    else:
        last = "no visitors yet."
    friends = len(state["friends"])
    tally = (
        f'{c["feed"]} fish, {c["play"]} yarn, {c["pet"]} pets, '
        f'{friends} {"friend" if friends == 1 else "friends"} so far'
    )
    f = lambda v: round(v * k, 1)  # noqa: E731
    return f"""
    <g transform="translate({x} {y})">
      <text x="0" y="{f(42)}" font-family="{A.SERIF}" font-style="italic" font-size="{f(46)}" fill="{A.TEXT}">Byte</text>
      <text x="{f(2)}" y="{f(72)}" font-family="{A.SERIF}" font-style="italic" font-size="{f(18)}" fill="{A.TEXT_SOFT}">{html.escape(STATUS[m])}</text>
      {meter(f(2), f(94), "food", state["food"], "#d9924f", f(16), f(210))}
      {meter(f(2), f(120), "love", state["love"], "#c4606a", f(16), f(210))}
      {meter(f(2), f(146), "nap", state["energy"], "#7f93bb", f(16), f(210))}
      <text x="{f(2)}" y="{f(186)}" font-family="{A.SERIF}" font-size="{f(15)}" fill="{A.TEXT_FAINT}">{last}</text>
      <text x="{f(2)}" y="{f(207)}" font-family="{A.SERIF}" font-size="{f(15)}" fill="{A.TEXT_FAINT}">{tally}</text>
    </g>"""


def snooze(x, y, k=1.0):
    return "".join(
        f'<text class="rise" style="animation-delay:{i * 1.4:.1f}s" x="{x + dx * k}" y="{y + dy * k}" font-family="{A.SERIF}" '
        f'font-style="italic" font-size="{size * k}" fill="{A.TEXT_SOFT}">z</text>'
        for i, (dx, dy, size) in enumerate([(0, 0, 22), (16, -22, 17), (28, -40, 13)])
    )


def frame(W, H, m, body):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="byte the cat, lying on the sill: {html.escape(STATUS[m])}">
  <defs>
    {A.defs()}
    <clipPath id="card"><rect width="{W}" height="{H}" rx="16"/></clipPath>
  </defs>
  <style>{A.CSS}</style>
  <g clip-path="url(#card)"><rect width="{W}" height="{H}" fill="{A.WOOD_DARK}"/>{body}</g>
  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="none" stroke="#1c100a" stroke-opacity=".6" stroke-width="2"/>
</svg>
"""


def render(state):
    """Desktop: a closer look at the same sill, Byte on the left."""
    m = mood(state)
    W, H = 900, 340
    top, front = 240, 308
    light = A.window_light(30, 34, pane_w=132, pane_h=90, gap=13, skew=0.24, slope=-0.06)
    body = f"""
    {A.wall(W, top, patches=light)}
    <rect x="{W - 34}" y="-10" width="44" height="{top + 10}" fill="#2a1c18"/>
    {A.stroke((W - 34, 0), (W - 33, top / 2), (W - 34, top), 2.4, A.WOOD_EDGE, .6)}
    {A.sill(W, top, front, H, sun_from=0.7, grain_seed=5)}
    {A.cast_shadow(262, 294)}
    {props(m, 440, 298)}
    {A.byte(m, 262, 294)}
    {snooze(390, 92) if m == "asleep" else ""}
    {readout(state, m, 540, 22)}"""
    return frame(W, H, m, body)


def render_narrow(state):
    """Phone: the readout on top in larger type, Byte underneath."""
    m = mood(state)
    W, H = 600, 700
    top, front = 590, 652
    light = A.window_light(40, 404, pane_w=120, pane_h=74, gap=12, skew=0.24, slope=-0.06)
    body = f"""
    {A.wall(W, top, patches=light)}
    {A.sill(W, top, front, H, sun_from=0.7, grain_seed=5)}
    {A.cast_shadow(300, 646, 1.05)}
    {props(m, 500, 650, 1.1)}
    {A.byte(m, 300, 646, 1.05)}
    {snooze(430, 430, 1.1) if m == "asleep" else ""}
    {readout(state, m, 44, 52, 1.45)}"""
    return frame(W, H, m, body)


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
    with open(SVG_NARROW, "w", encoding="utf-8") as f:
        f.write(render_narrow(state))
    update_readme(state)
    print(f"ok: {action} -> {mood(state)}")


if __name__ == "__main__":
    main()

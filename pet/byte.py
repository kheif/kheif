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
import cat as C  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = os.path.join(ROOT, "pet", "state.json")
SVG = os.path.join(ROOT, "assets", "byte.svg")
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


def props(m):
    """Things around the cat that depend on the mood."""
    if m == "hungry":
        return f"""
  <g transform="translate(190 300)">
    <ellipse cx="0" cy="0" rx="30" ry="6" fill="#000" opacity=".35"/>
    <path class="ln" d="M-28 -16 Q0 -8 28 -16 L22 -2 Q0 4 -22 -2z" fill="#8a9aa6" stroke-width="3"/>
    <ellipse class="ln" cx="0" cy="-16" rx="28" ry="6" fill="#3a3530" stroke-width="3"/>
    <path d="M-24 -12 Q-12 -6 0 -8" stroke="#dfe8ee" stroke-width="2" fill="none" opacity=".6"/>
  </g>
  <text x="392" y="70" font-family="{C.SERIF}" font-style="italic" font-size="22" fill="{C.TEXT}" class="rise" style="animation-duration:2.6s">mew.</text>"""
    if m == "bored":
        return f"""
  <g transform="translate(186 284)">
    <ellipse cx="2" cy="16" rx="22" ry="5" fill="#000" opacity=".35"/>
    <circle class="ln" r="18" fill="#5f7fb8" stroke-width="3"/>
    <path d="M-14 -8 Q0 4 14 -10 M-17 2 Q0 14 16 0 M-10 12 Q2 18 12 10 M-4 -17 Q8 -2 6 16" stroke="#2f4a7a" stroke-width="2" fill="none"/>
    <path d="M-6 -12 Q2 -14 8 -10" stroke="#a9c3ef" stroke-width="2.5" fill="none" stroke-linecap="round"/>
    <path d="M16 8 C40 20 60 4 84 14" stroke="#5f7fb8" stroke-width="2.5" fill="none" stroke-linecap="round"/>
  </g>"""
    if m == "happy":
        out = []
        for i, (x, y, sc) in enumerate([(392, 92, 1), (360, 60, 0.7), (410, 40, 0.55)]):
            out.append(
                f'<g transform="translate({x} {y}) scale({sc})"><path class="rise ln" style="animation-delay:{i * 1.1:.1f}s" '
                'd="M0 6 C-6 -6 -22 -2 -18 10 C-15 18 -4 22 0 28 C4 22 15 18 18 10 C22 -2 6 -6 0 6z" fill="#e0606e" stroke-width="3"/></g>'
            )
        return "".join(out)
    if m == "asleep":
        out = []
        for i, (x, y, size) in enumerate([(380, 96, 30), (400, 70, 22), (416, 50, 16)]):
            out.append(
                f'<text class="rise" style="animation-delay:{i * 1.1:.1f}s" x="{x}" y="{y}" font-family="{C.SERIF}" '
                f'font-style="italic" font-weight="700" font-size="{size}" fill="{C.TEXT}">z</text>'
            )
        return "".join(out)
    return ""


def meter(y, label, value, color):
    w = 250
    fill = max(10, round(w * value / 100))
    return f"""
    <text x="0" y="{y + 12}" font-family="{C.SERIF}" font-style="italic" font-size="16" fill="{C.MUTED}">{label}</text>
    <rect x="58" y="{y}" width="{w}" height="14" rx="7" fill="#000" opacity=".35"/>
    <rect x="58" y="{y}" width="{fill}" height="14" rx="7" fill="{color}"/>
    <rect x="62" y="{y + 2.5}" width="{max(0, fill - 8)}" height="3.5" rx="1.75" fill="#fff" opacity=".28"/>
    <text x="{58 + w + 14}" y="{y + 12}" font-family="{C.SERIF}" font-size="14" fill="{C.MUTED}">{value}</text>"""


def render(state):
    m = mood(state)
    c = state["counts"]
    W, H = 900, 340
    stack, top = C.books(86, 300)

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

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="byte the cat is {html.escape(STATUS[m])}">
  <defs>
    {C.defs()}
    <clipPath id="card"><rect width="{W}" height="{H}" rx="18"/></clipPath>
  </defs>
  <style>{C.CSS}</style>
  <g clip-path="url(#card)">
    {C.backdrop(W, H, table_y=290)}
    {C.frame(770, 34, 96, 74)}
    {stack}
    {C.candle(86, top + 2)}
    <ellipse cx="300" cy="300" rx="120" ry="16" fill="#000" opacity=".4" filter="url(#blur)"/>
    {props(m)}
    {C.cat(m, x=300, y=298)}
    {C.motes(22, 480, H)}{C.motes(6, W, H, seed=5)}

    <g transform="translate(500 0)">
      <text x="0" y="86" font-family="{C.SERIF}" font-style="italic" font-size="50" fill="{C.TEXT}">Byte</text>
      <text x="0" y="118" font-family="{C.SERIF}" font-style="italic" font-size="17" fill="{C.MUTED}">{html.escape(STATUS[m])}</text>
      {meter(150, "food", state["food"], "#e89a52")}
      {meter(180, "love", state["love"], "#d9606c")}
      {meter(210, "nap", state["energy"], "#7f9cc9")}
      <text x="0" y="262" font-family="{C.SERIF}" font-size="14" fill="{C.MUTED}">{last}</text>
      <text x="0" y="284" font-family="{C.SERIF}" font-size="14" fill="{C.MUTED}">{tally}</text>
    </g>
    {C.overlay(W, H)}
  </g>
  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="18" fill="none" stroke="#000" stroke-opacity=".5" stroke-width="2"/>
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

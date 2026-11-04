"""Byte, drawn as a cartoon in a warm, candle lit room.

Everything is plain SVG paths, gradients and CSS animation so it works
inside a GitHub README (no scripts, no external files).
"""

LINE = "#1c110b"      # outline
FUR = "#e89a52"
FUR_SHADE = "#b8612c"
FUR_LIGHT = "#ffc07a"
STRIPE = "#a8541f"
CREAM = "#f6dcb4"
CREAM_SHADE = "#d6ad80"
PINK = "#e58a7d"
IRIS = "#c9b23a"
IRIS_DARK = "#7e7a1e"
TEXT = "#f1e3c8"
MUTED = "#a88f72"
SERIF = "Georgia, 'Iowan Old Style', 'Palatino Linotype', 'Times New Roman', serif"


def defs(uid=""):
    """Gradients and filters shared by the scenes."""
    return f"""
    <radialGradient id="glow{uid}" cx="0.3" cy="0.55" r="0.75">
      <stop offset="0" stop-color="#7a4a26"/>
      <stop offset="0.45" stop-color="#3d2416"/>
      <stop offset="1" stop-color="#160d08"/>
    </radialGradient>
    <radialGradient id="candle{uid}" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="#ffcf7a" stop-opacity=".55"/>
      <stop offset="0.4" stop-color="#ff9a3c" stop-opacity=".18"/>
      <stop offset="1" stop-color="#ff9a3c" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="vignette{uid}" cx="0.5" cy="0.5" r="0.75">
      <stop offset="0.55" stop-color="#000" stop-opacity="0"/>
      <stop offset="1" stop-color="#000" stop-opacity=".6"/>
    </radialGradient>
    <linearGradient id="fur{uid}" x1="0" y1="0" x2="1" y2="0.3">
      <stop offset="0" stop-color="{FUR_LIGHT}"/>
      <stop offset="0.45" stop-color="{FUR}"/>
      <stop offset="1" stop-color="{FUR_SHADE}"/>
    </linearGradient>
    <linearGradient id="cream{uid}" x1="0" y1="0" x2="1" y2="0.2">
      <stop offset="0" stop-color="#fff0d6"/>
      <stop offset="0.5" stop-color="{CREAM}"/>
      <stop offset="1" stop-color="{CREAM_SHADE}"/>
    </linearGradient>
    <radialGradient id="iris{uid}" cx="0.4" cy="0.65" r="0.7">
      <stop offset="0" stop-color="#f0e07a"/>
      <stop offset="0.6" stop-color="{IRIS}"/>
      <stop offset="1" stop-color="{IRIS_DARK}"/>
    </radialGradient>
    <linearGradient id="wood{uid}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#5a3520"/>
      <stop offset="0.15" stop-color="#3e2415"/>
      <stop offset="1" stop-color="#1e110a"/>
    </linearGradient>
    <linearGradient id="cushion{uid}" x1="0" y1="0" x2="1" y2="0.4">
      <stop offset="0" stop-color="#8a3b3b"/>
      <stop offset="1" stop-color="#4a1c22"/>
    </linearGradient>
    <filter id="grain{uid}" x="0" y="0" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" seed="7" result="n"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0.5  0 0 0 0 0.35  0 0 0 0 0.2  0 0 0 .55 0"/>
    </filter>
    <filter id="soft{uid}"><feGaussianBlur stdDeviation="1.4"/></filter>
    <filter id="blur{uid}"><feGaussianBlur stdDeviation="6"/></filter>
    """


CSS = """
    .ln { stroke: #1c110b; stroke-width: 4; stroke-linejoin: round; stroke-linecap: round; }
    .thin { stroke: #1c110b; stroke-width: 2.6; fill: none; stroke-linecap: round; stroke-linejoin: round; }
    @keyframes breathe { 0%,100% { transform: scale(1,1) } 50% { transform: scale(1.015,.985) } }
    .breathe { transform-box: fill-box; transform-origin: 50% 100%; animation: breathe var(--breath, 3.6s) ease-in-out infinite; }
    @keyframes swish { 0%,100% { transform: rotate(-6deg) } 50% { transform: rotate(9deg) } }
    .tail { transform-box: fill-box; transform-origin: 0% 100%; animation: swish var(--tail, 2.8s) ease-in-out infinite; }
    @keyframes twitch { 0%,88%,100% { transform: rotate(0) } 91% { transform: rotate(-9deg) } 95% { transform: rotate(3deg) } }
    .ear { transform-box: fill-box; transform-origin: 70% 100%; animation: twitch 6.5s ease-in-out infinite; }
    @keyframes flicker { 0%,100% { opacity: .95; transform: scale(1) } 20% { opacity: .8; transform: scale(.97,1.03) } 45% { opacity: 1; transform: scale(1.02,.98) } 70% { opacity: .85; transform: scale(.98,1.02) } }
    .flame { transform-box: fill-box; transform-origin: 50% 100%; animation: flicker 1.7s ease-in-out infinite; }
    .light { animation: flicker 2.3s ease-in-out infinite; }
    @keyframes drift { 0% { transform: translate(0,0); opacity: 0 } 15% { opacity: .9 } 85% { opacity: .7 } 100% { transform: translate(var(--dx), -90px); opacity: 0 } }
    .mote { animation: drift var(--d, 11s) linear infinite; }
    @keyframes rise { 0% { transform: translateY(8px) scale(.6); opacity: 0 } 20% { opacity: 1 } 100% { transform: translateY(-50px) scale(1.05); opacity: 0 } }
    .rise { transform-box: fill-box; transform-origin: center; animation: rise 3.4s ease-out infinite; opacity: 0; }
    @keyframes steam { 0% { transform: translateY(6px) scaleX(1); opacity: 0 } 35% { opacity: .55 } 100% { transform: translateY(-30px) scaleX(1.5); opacity: 0 } }
    .steam { transform-box: fill-box; transform-origin: 50% 100%; animation: steam 3.2s ease-out infinite; opacity: 0; }
"""


def blink_css(lid, eye_h=36, period=5.0):
    """Upper lid sits at `lid` px down, closes fully for a moment."""
    return (
        f"@keyframes blink {{ 0%,90%,100% {{ transform: translateY({lid}px) }} "
        f"93%,95% {{ transform: translateY({eye_h}px) }} }}\n"
        f"    .lid {{ transform: translateY({lid}px); animation: blink {period}s ease-in-out infinite; }}\n"
        f"    .lid2 {{ animation-delay: .04s }}"
    )


# ----------------------------------------------------------------- the cat


def eye(cx, cy, mood, uid, side):
    """One eye. side is -1 for left, 1 for right (mirrors the shine)."""
    rx, ry = 15, 18
    if mood == "happy":
        return f'<path class="thin" d="M{cx - 13} {cy + 4} Q{cx} {cy - 12} {cx + 13} {cy + 4}" stroke-width="4"/>'
    if mood == "asleep":
        return (
            f'<path class="thin" d="M{cx - 13} {cy} Q{cx} {cy + 10} {cx + 13} {cy}" stroke-width="4"/>'
            f'<path class="thin" d="M{cx + 9 * side} {cy + 5} l{5 * side} 5" stroke-width="2.4"/>'
        )
    pupil_rx, pupil_ry = (9, 13) if mood == "hungry" else (5.5, 12)
    clip = f"eye{uid}{side}"
    lid_group = (
        f'<g class="lid{" lid2" if side > 0 else ""}">'
        f'<rect x="{cx - rx - 2}" y="{cy - ry - 40}" width="{2 * rx + 4}" height="40" fill="url(#fur{uid})"/>'
        f'<path d="M{cx - rx - 2} {cy - ry} Q{cx} {cy - ry + 5} {cx + rx + 2} {cy - ry}" stroke="{LINE}" stroke-width="4" fill="none"/>'
        f"</g>"
    )
    return f"""
      <clipPath id="{clip}"><ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}"/></clipPath>
      <ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="url(#iris{uid})"/>
      <g clip-path="url(#{clip})">
        <ellipse cx="{cx + 1.5 * side}" cy="{cy + 1}" rx="{pupil_rx}" ry="{pupil_ry}" fill="{LINE}"/>
        <circle cx="{cx - 5}" cy="{cy - 6}" r="{4.5 if mood == 'hungry' else 3.6}" fill="#fff8ea"/>
        <circle cx="{cx + 5}" cy="{cy + 7}" r="1.8" fill="#fff8ea" opacity=".8"/>
        {lid_group}
      </g>
      <ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="{LINE}" stroke-width="3.6"/>
    """


def mouth(mood):
    if mood == "hungry":
        return (
            '<path d="M-9 -126 Q0 -132 9 -126 Q8 -110 0 -108 Q-8 -110 -9 -126z" fill="#6e2a2a" class="ln" stroke-width="3"/>'
            '<path d="M-5 -114 Q0 -118 5 -114 Q3 -110 0 -110 Q-3 -110 -5 -114z" fill="#d06a6a"/>'
        )
    if mood == "bored":
        return '<path class="thin" d="M-9 -125 Q0 -123 9 -126"/>'
    if mood == "asleep":
        return '<path class="thin" d="M-6 -126 Q0 -123 6 -126"/>'
    return '<path class="thin" d="M-13 -128 Q-7 -121 0 -127 Q7 -121 13 -128"/>'


def cat(mood, uid="", x=0, y=0, scale=1.0, tail=True):
    """Byte sitting, origin at the middle of the bottom of the body."""
    lid = {"fine": 11, "bored": 17, "hungry": 2}.get(mood, 11)
    head_tilt = {"asleep": 7, "happy": -5, "bored": 3, "hungry": -3}.get(mood, -2)
    breath = "5.5s" if mood == "asleep" else "3.6s"
    tail_speed = {"happy": "1.2s", "asleep": "6s", "bored": "4.5s", "hungry": "1.8s"}.get(mood, "2.8s")

    tail_svg = ""
    if tail:
        tail_d = "M48 -14 C98 -6 128 -40 116 -86 C110 -110 120 -128 136 -122"
        tail_svg = f"""
    <g class="tail" style="--tail:{tail_speed}">
      <path d="{tail_d}" stroke="{LINE}" stroke-width="30" fill="none" stroke-linecap="round"/>
      <path d="{tail_d}" stroke="url(#fur{uid})" stroke-width="22" fill="none" stroke-linecap="round"/>
      <path d="M112 -58 q10 2 14 -4 M114 -86 q9 4 14 -2 M120 -112 q8 4 12 -1" stroke="{STRIPE}" stroke-width="4" fill="none" stroke-linecap="round"/>
    </g>"""

    return f"""
  <g transform="translate({x} {y}) scale({scale})">
    {tail_svg}
    <g class="breathe" style="--breath:{breath}">
      <!-- body -->
      <clipPath id="bodyclip{uid}"><path d="M-74 -4 C-86 -52 -70 -104 -40 -122 L40 -122 C70 -104 86 -52 74 -4 Q0 6 -74 -4z"/></clipPath>
      <path fill="url(#fur{uid})" d="M-74 -4 C-86 -52 -70 -104 -40 -122 L40 -122 C70 -104 86 -52 74 -4 Q0 6 -74 -4z"/>
      <g clip-path="url(#bodyclip{uid})">
        <path fill="url(#cream{uid})" d="M-28 -116 C-44 -76 -38 -34 -22 -4 L22 -4 C38 -34 44 -76 28 -116z"/>
        <path d="M18 -130 C46 -96 40 -40 14 10 L100 10 L100 -130z" fill="#5a2410" opacity=".45"/>
        <path d="M-70 -100 C-84 -60 -80 -30 -72 0" stroke="#ffe0a8" stroke-width="7" fill="none" opacity=".55" filter="url(#soft{uid})"/>
      </g>
      <path class="ln" fill="none" d="M-74 -4 C-86 -52 -70 -104 -40 -122 L40 -122 C70 -104 86 -52 74 -4 Q0 6 -74 -4z"/>
      <path d="M-74 -40 q10 -4 16 2 M-78 -62 q10 -4 16 2 M76 -40 q-10 -4 -16 2 M78 -62 q-10 -4 -16 2" stroke="{STRIPE}" stroke-width="5" fill="none" stroke-linecap="round"/>
      <!-- front legs and paws -->
      <path class="thin" d="M-10 -66 C-12 -40 -10 -22 -8 -10 M10 -66 C12 -40 10 -22 8 -10"/>
      <ellipse class="ln" cx="-26" cy="-6" rx="22" ry="11" fill="url(#cream{uid})" stroke-width="3.4"/>
      <ellipse class="ln" cx="26" cy="-6" rx="22" ry="11" fill="url(#cream{uid})" stroke-width="3.4"/>
      <path class="thin" d="M-32 -10 v5 M-21 -10 v5 M21 -10 v5 M32 -10 v5" stroke-width="2"/>

      <!-- head -->
      <g transform="rotate({head_tilt} 0 -150)">
        <g class="ear">
          <path class="ln" fill="url(#fur{uid})" d="M-66 -180 L-74 -252 Q-72 -258 -66 -254 L-16 -214z"/>
          <path fill="{PINK}" d="M-60 -192 L-66 -238 L-30 -212z" opacity=".85"/>
          <path d="M-58 -200 l-6 -14 M-52 -204 l-4 -10" stroke="{CREAM}" stroke-width="2" stroke-linecap="round"/>
        </g>
        <path class="ln" fill="url(#fur{uid})" d="M66 -180 L74 -252 Q72 -258 66 -254 L16 -214z"/>
        <path fill="{PINK}" d="M60 -192 L66 -238 L30 -212z" opacity=".55"/>

        <clipPath id="headclip{uid}"><path d="M-72 -152 C-76 -196 -48 -226 0 -228 C48 -226 76 -196 72 -152 L84 -144 L70 -138 L78 -126 L60 -124 C46 -110 24 -104 0 -104 C-24 -104 -46 -110 -60 -124 L-78 -126 L-70 -138 L-84 -144z"/></clipPath>
        <path fill="url(#fur{uid})" d="M-72 -152 C-76 -196 -48 -226 0 -228 C48 -226 76 -196 72 -152 L84 -144 L70 -138 L78 -126 L60 -124 C46 -110 24 -104 0 -104 C-24 -104 -46 -110 -60 -124 L-78 -126 L-70 -138 L-84 -144z"/>
        <g clip-path="url(#headclip{uid})">
          <path d="M30 -240 C58 -200 52 -140 20 -98 L100 -98 L100 -240z" fill="#5a2410" opacity=".4"/>
          <path d="M-66 -196 C-78 -170 -78 -150 -72 -134" stroke="#ffe0a8" stroke-width="6" fill="none" opacity=".6" filter="url(#soft{uid})"/>
        </g>
        <path class="ln" fill="none" d="M-72 -152 C-76 -196 -48 -226 0 -228 C48 -226 76 -196 72 -152 L84 -144 L70 -138 L78 -126 L60 -124 C46 -110 24 -104 0 -104 C-24 -104 -46 -110 -60 -124 L-78 -126 L-70 -138 L-84 -144z"/>
        <path d="M-12 -226 q2 14 -2 24 M0 -228 q2 16 -1 30 M12 -226 q2 14 -2 24" stroke="{STRIPE}" stroke-width="5" fill="none" stroke-linecap="round"/>
        <path d="M-72 -168 q12 2 18 10 M72 -168 q-12 2 -18 10" stroke="{STRIPE}" stroke-width="4" fill="none" stroke-linecap="round"/>

        <!-- muzzle -->
        <ellipse cx="-12" cy="-128" rx="16" ry="12" fill="url(#cream{uid})"/>
        <ellipse cx="12" cy="-128" rx="16" ry="12" fill="url(#cream{uid})"/>
        <ellipse cx="-40" cy="-136" rx="10" ry="6" fill="{PINK}" opacity=".35"/>
        <ellipse cx="40" cy="-136" rx="10" ry="6" fill="{PINK}" opacity=".35"/>

        <style>{blink_css(lid)}</style>
        {eye(-28, -160, mood, uid, -1)}
        {eye(28, -160, mood, uid, 1)}

        <path d="M-7 -140 Q0 -144 7 -140 Q4 -133 0 -132 Q-4 -133 -7 -140z" fill="{PINK}" class="ln" stroke-width="2.6"/>
        {mouth(mood)}
        <g stroke="#f6e6cc" stroke-width="1.6" stroke-linecap="round" opacity=".75">
          <path d="M-26 -130 Q-56 -136 -86 -132 M-26 -125 Q-56 -124 -84 -116"/>
          <path d="M26 -130 Q56 -136 86 -132 M26 -125 Q56 -124 84 -116"/>
        </g>
      </g>
    </g>
  </g>"""


# ------------------------------------------------------------- the room


def candle(x, y, uid=""):
    return f"""
  <g class="light"><circle cx="{x}" cy="{y - 70}" r="190" fill="url(#candle{uid})"/></g>
  <g transform="translate({x} {y})">
    <ellipse cx="0" cy="0" rx="30" ry="7" fill="#2a1a10"/>
    <path class="ln" d="M-26 -4 Q0 6 26 -4 L24 -10 Q0 -2 -24 -10z" fill="#6b4a2c" stroke-width="3"/>
    <path class="ln" d="M-13 -8 L-13 -60 Q0 -64 13 -60 L13 -8 Q0 -4 -13 -8z" fill="#efe0c0" stroke-width="3"/>
    <path d="M-13 -60 Q0 -64 13 -60 Q11 -52 13 -44 Q8 -50 4 -42 Q2 -52 -3 -48 Q-8 -54 -13 -50z" fill="#fff6e0"/>
    <path d="M5 -50 v28" stroke="#d8c39a" stroke-width="5" stroke-linecap="round" opacity=".6"/>
    <path d="M0 -62 v-6" stroke="{LINE}" stroke-width="2"/>
    <g class="flame">
      <path d="M0 -94 C8 -82 8 -70 0 -66 C-8 -70 -8 -82 0 -94z" fill="#ffb347"/>
      <path d="M0 -84 C4 -78 4 -71 0 -69 C-4 -71 -4 -78 0 -84z" fill="#fff3c4"/>
    </g>
  </g>"""


def books(x, y):
    """A small stack of old books, origin at bottom centre."""
    spec = [(-58, 58, 22, "#6b2f2a", "#4a1f1c"), (-50, 52, 18, "#3f4a35", "#2b3324"), (-54, 60, 20, "#7a5a32", "#55401f")]
    out, cy = [], y
    for x0, w, h, c, dark in spec:
        cy -= h
        out.append(
            f'<rect class="ln" x="{x + x0}" y="{cy}" width="{w * 2}" height="{h}" rx="4" fill="{c}" stroke-width="3"/>'
            f'<rect x="{x + x0 + 4}" y="{cy + 5}" width="{w * 2 - 22}" height="{h - 10}" rx="2" fill="#d9c49a" opacity=".55"/>'
            f'<path d="M{x + x0 + 4} {cy + 3} h{w * 2 - 20}" stroke="#ffe0a8" stroke-width="2" opacity=".35"/>'
            f'<rect x="{x + x0 + w * 2 - 12}" y="{cy}" width="12" height="{h}" rx="3" fill="{dark}"/>'
        )
    return "".join(out), cy


def frame(x, y, w, h, uid=""):
    """A dim painting on the back wall, a little crooked."""
    return f"""
  <g transform="rotate(-2 {x + w / 2} {y + h / 2})" opacity=".55">
    <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="#4a2c18" stroke="#1c110b" stroke-width="3"/>
    <rect x="{x + 9}" y="{y + 9}" width="{w - 18}" height="{h - 18}" fill="#2a2a24"/>
    <circle cx="{x + w * 0.62}" cy="{y + h * 0.38}" r="{h * 0.13}" fill="#c9b886" opacity=".7"/>
    <path d="M{x + 9} {y + h - 22} Q{x + w * 0.35} {y + h * 0.5} {x + w * 0.6} {y + h - 26} T{x + w - 9} {y + h - 30} V{y + h - 9} H{x + 9}z" fill="#3b4632"/>
  </g>"""


def motes(n, w, h, seed=3):
    """Dust floating in the candle light. Deterministic pseudo random."""
    out = []
    s = seed
    for i in range(n):
        s = (s * 1103515245 + 12345) % 2**31
        x = 30 + s % (w - 60)
        s = (s * 1103515245 + 12345) % 2**31
        y = 60 + s % (h - 80)
        s = (s * 1103515245 + 12345) % 2**31
        r = 0.8 + (s % 100) / 70
        d = 9 + (s % 9)
        dx = (s % 41) - 20
        delay = -(s % 13)
        out.append(
            f'<circle class="mote" cx="{x}" cy="{y}" r="{r:.1f}" fill="#ffd9a0" '
            f'style="--d:{d}s;--dx:{dx}px;animation-delay:{delay}s"/>'
        )
    return "".join(out)


def backdrop(w, h, uid="", table_y=None):
    table = ""
    if table_y is not None:
        table = (
            f'<rect x="0" y="{table_y}" width="{w}" height="{h - table_y}" fill="url(#wood{uid})"/>'
            f'<path d="M0 {table_y} H{w}" stroke="#7a4a2a" stroke-width="2" opacity=".7"/>'
        )
    return f'<rect width="{w}" height="{h}" fill="url(#glow{uid})"/>{table}'


def overlay(w, h, uid=""):
    return (
        f'<rect width="{w}" height="{h}" filter="url(#grain{uid})" opacity=".22"/>'
        f'<rect width="{w}" height="{h}" fill="url(#vignette{uid})"/>'
    )

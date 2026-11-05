"""Byte, painted as a close up portrait.

Style notes (from the reference the profile owner picked):
  * angular, planar construction: straight runs that break into short
    curves, sharp corners at every joint, no bubbly shapes
  * thin, dark brown, tapered brush lines instead of a uniform outline
  * hard edged cel shadows cut along the planes, shadows drift to maroon
  * small eyes, heavy upper lids, sideways glance: droll, a bit tired
  * muted warm palette, near empty dark background, shallow depth of field

Everything is plain SVG so it renders inside a GitHub README.
"""
import math

LINE = "#2a1610"
FUR_LIT = "#e2a46a"
FUR = "#c47d45"
FUR_SHADE = "#a2593a"
FUR_DEEP = "#6e342a"
STRIPE = "#9a5532"
CREAM_LIT = "#eed6b4"
CREAM = "#cfb08e"
CREAM_SHADE = "#9a7663"
EAR_IN = "#8c5250"
IRIS = "#b99a3c"
TEXT = "#eadbc2"
MUTED = "#9c8670"
SERIF = "Georgia, 'Iowan Old Style', 'Palatino Linotype', 'Times New Roman', serif"


# ------------------------------------------------------------------ brush


def _quad(p0, p1, p2, t):
    a = (1 - t) ** 2
    b = 2 * (1 - t) * t
    c = t * t
    return a * p0[0] + b * p1[0] + c * p2[0], a * p0[1] + b * p1[1] + c * p2[1]


def brush(p0, p1, p2, w, color=LINE, opacity=1.0, start=0.0, end=0.0, n=14):
    """A tapered stroke along a quadratic curve, thickest in the middle.

    start/end thin one end more than the other, like a real brush mark.
    """
    left, right = [], []
    for i in range(n + 1):
        t = i / n
        x, y = _quad(p0, p1, p2, t)
        x2, y2 = _quad(p0, p1, p2, min(1, t + 0.01))
        x1, y1 = _quad(p0, p1, p2, max(0, t - 0.01))
        dx, dy = x2 - x1, y2 - y1
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy / ln, dx / ln
        k = math.sin(math.pi * t) ** 0.7
        k *= 1 - start * (1 - t) - end * t
        h = w / 2 * max(k, 0.06)
        left.append((x + nx * h, y + ny * h))
        right.append((x - nx * h, y - ny * h))
    pts = left + right[::-1]
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + "z"
    op = f' opacity="{opacity}"' if opacity != 1 else ""
    return f'<path d="{d}" fill="{color}"{op}/>'


def shape(points, bends, fill="none", extra=""):
    """Closed path whose edges bow outward by bends[i] * edge length.

    0 keeps an edge straight (sharp joints), small values give the
    "straight that breaks into a curve" feel of the reference.
    """
    d = [f"M{points[0][0]} {points[0][1]}"]
    for i in range(len(points)):
        a, b = points[i], points[(i + 1) % len(points)]
        k = bends[i] if i < len(bends) else 0
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        dx, dy = b[0] - a[0], b[1] - a[1]
        cx, cy = mx + dy * k, my - dx * k
        d.append(f"Q{cx:.1f} {cy:.1f} {b[0]} {b[1]}")
    return f'<path d="{" ".join(d)}z" fill="{fill}" {extra}/>'


def poly(points, fill, extra=""):
    d = "M" + " L".join(f"{x} {y}" for x, y in points) + "z"
    return f'<path d="{d}" fill="{fill}" {extra}/>'


# ------------------------------------------------------------------ defs


def defs(uid=""):
    return f"""
    <radialGradient id="bg{uid}" cx="0.32" cy="0.42" r="0.85">
      <stop offset="0" stop-color="#5a3622"/>
      <stop offset="0.38" stop-color="#3a2216"/>
      <stop offset="1" stop-color="#140b07"/>
    </radialGradient>
    <radialGradient id="vignette{uid}" cx="0.45" cy="0.5" r="0.8">
      <stop offset="0.5" stop-color="#000" stop-opacity="0"/>
      <stop offset="1" stop-color="#000" stop-opacity=".65"/>
    </radialGradient>
    <linearGradient id="key{uid}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#ffd9a0" stop-opacity=".22"/>
      <stop offset="0.5" stop-color="#ffd9a0" stop-opacity="0"/>
    </linearGradient>
    <radialGradient id="iris{uid}" cx="0.35" cy="0.7" r="0.8">
      <stop offset="0" stop-color="#e6cf74"/>
      <stop offset="0.65" stop-color="{IRIS}"/>
      <stop offset="1" stop-color="#6e5a1e"/>
    </radialGradient>
    <linearGradient id="facepaint{uid}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#ffe2b0" stop-opacity=".28"/>
      <stop offset="0.45" stop-color="#ffe2b0" stop-opacity="0"/>
      <stop offset="0.7" stop-color="#3a140c" stop-opacity="0"/>
      <stop offset="1" stop-color="#3a140c" stop-opacity=".35"/>
    </linearGradient>
    <filter id="paint{uid}" x="0" y="0" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency=".012 .02" numOctaves="3" seed="4"/>
      <feColorMatrix type="matrix" values="0 0 0 0 .55  0 0 0 0 .34  0 0 0 0 .2  0 0 0 .9 -.3"/>
      <feGaussianBlur stdDeviation="6"/>
    </filter>
    <filter id="grain{uid}" x="0" y="0" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="9"/>
      <feColorMatrix type="matrix" values="0 0 0 0 .5  0 0 0 0 .38  0 0 0 0 .26  0 0 0 .5 0"/>
    </filter>
    <filter id="dof{uid}" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="5"/></filter>
    <filter id="dof2{uid}" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="2.2"/></filter>
    <filter id="glow{uid}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="22"/></filter>
    """


CSS = """
    @keyframes breathe { 0%,100% { transform: translateY(0) } 50% { transform: translateY(1.6px) } }
    .breathe { animation: breathe 4.2s ease-in-out infinite; }
    @keyframes nod { 0%,100% { transform: rotate(0) } 50% { transform: rotate(1.2deg) } }
    .head { transform-box: fill-box; transform-origin: 50% 90%; animation: nod 6s ease-in-out infinite; }
    @keyframes twitch { 0%,90%,100% { transform: rotate(0) } 92% { transform: rotate(-7deg) } 95% { transform: rotate(2deg) } }
    .ear { transform-box: fill-box; transform-origin: 60% 100%; animation: twitch 7s ease-in-out infinite; }
    @keyframes glance { 0%,40%,100% { transform: translateX(0) } 48%,70% { transform: translateX(-4px) } }
    .pupil { animation: glance 9s ease-in-out infinite; }
    @keyframes waver { 0%,100% { opacity: .9 } 30% { opacity: .75 } 60% { opacity: 1 } }
    .keylight { animation: waver 3.1s ease-in-out infinite; }
    @keyframes fade { 0% { opacity: 0; transform: translateY(6px) } 25% { opacity: .9 } 100% { opacity: 0; transform: translateY(-34px) } }
    .rise { animation: fade 4s ease-out infinite; opacity: 0; }
    @keyframes steam { 0% { transform: translateY(6px) scaleX(1); opacity: 0 } 35% { opacity: .45 } 100% { transform: translateY(-30px) scaleX(1.5); opacity: 0 } }
    .steam { transform-box: fill-box; transform-origin: 50% 100%; animation: steam 3.4s ease-out infinite; opacity: 0; }
"""


def blink_css(lid, closed=38, period=5.5):
    return (
        f"@keyframes blink {{ 0%,91%,100% {{ transform: translateY({lid}px) }} "
        f"93.5%,95% {{ transform: translateY({closed}px) }} }}\n"
        f"    .lid {{ transform: translateY({lid}px); animation: blink {period}s ease-in-out infinite; }}"
    )


# ------------------------------------------------------------------ head

# The head is designed straight on and symmetric, then turned a little
# towards the viewer's left with one transform, so every feature agrees
# on the same angle: the far (left) half is narrowed, the centre line
# moves left with it. Light comes from the upper left; the near (right)
# side falls into shadow.
TURN_CENTRE = -6
FAR_SCALE = 0.92   # left half, turning away
NEAR_SCALE = 1.0   # right half, closer to us


def T(p):
    x, y = p
    return (round(TURN_CENTRE + x * (FAR_SCALE if x < 0 else NEAR_SCALE), 1), y)


def TT(points):
    return [T(p) for p in points]


def mirror(points):
    """Mirror a clockwise point list to the other side, keeping it clockwise."""
    return [(-x, y) for x, y in reversed(points)]


_RIGHT = [(0, -92), (38, -86), (104, -148), (100, -40), (110, -6), (132, 16),
          (106, 32), (124, 52), (98, 64), (52, 88)]
_RIGHT_BENDS = [0.03, 0.02, 0.06, 0.06, 0, 0, 0, 0, 0.08, 0.06]
HEAD = TT(_RIGHT + [(0, 100)] + [(-x, y) for x, y in reversed(_RIGHT[1:])])
HEAD_BENDS = _RIGHT_BENDS + _RIGHT_BENDS[::-1]

EAR_R = [(38, -86), (104, -148), (100, -40), (70, -64)]
EAR_IN_R = [(50, -84), (96, -128), (92, -54)]

SHADOW = [(44, -94), (104, -148), (100, -40), (110, -6), (132, 16), (106, 32), (124, 52),
          (98, 64), (52, 88), (30, 98), (46, 66), (56, 40), (40, 14), (30, -20), (36, -56)]
SHADOW_BENDS = [0] * 9 + [0.04, -0.06, 0.06, -0.06, -0.06, -0.06]
CORE = [(36, -56), (30, -20), (40, 14), (56, 40), (46, 66), (30, 98), (42, 96), (62, 62), (60, 16), (48, -18), (48, -60)]

MUZZLE = [(0, 18), (30, 22), (52, 40), (48, 66), (28, 86), (0, 94), (-28, 86), (-48, 66), (-52, 40), (-30, 22)]
MUZZLE_LIT = [(-52, 40), (-30, 22), (0, 18), (-10, 34), (-44, 58)]
MUZZLE_SHADE = [(14, 22), (30, 22), (52, 40), (48, 66), (28, 86), (6, 92), (20, 66), (26, 44)]
CHIN_SHADE = [(-28, 86), (0, 94), (28, 86), (18, 98), (0, 104), (-22, 98)]
NOSE = [(-16, 14), (16, 14), (0, 30)]

EYE_X, EYE_Y, EYE_W, EYE_H = 46, -8, 25, 17


def eye(cx, cy, w, h, mood, uid, name, look):
    """An almond eye with a heavy upper lid. look shifts the pupil."""
    if mood in ("happy", "asleep"):
        bend = -7 if mood == "happy" else 7
        return (
            brush((cx - w, cy + 2), (cx, cy + bend), (cx + w, cy - 1), 4.6)
            + brush((cx - w + 4, cy + 7), (cx, cy + 9 + bend / 2), (cx + w - 4, cy + 6), 1.6, LINE, 0.6)
        )
    top = f"Q{cx - w * 0.2} {cy - h * 1.3} {cx + w} {cy - h * 0.25}"
    bottom = f"Q{cx + w * 0.1} {cy + h * 1.15} {cx - w} {cy + h * 0.1}"
    almond = f"M{cx - w} {cy + h * 0.1} {top} {bottom}z"
    pr = 7.5 if mood == "hungry" else 5.5
    px = cx + look
    return f"""
      <clipPath id="{name}{uid}"><path d="{almond}"/></clipPath>
      <path d="{almond}" fill="url(#iris{uid})"/>
      <g clip-path="url(#{name}{uid})">
        <g class="pupil">
          <ellipse cx="{px}" cy="{cy + 1}" rx="{pr * 0.62}" ry="{pr * 1.55}" fill="{LINE}"/>
          <circle cx="{px - 4}" cy="{cy - 4}" r="2.6" fill="#fff6e4" opacity=".9"/>
        </g>
        <path d="M{cx - w} {cy - h * 0.6} H{cx + w}" stroke="#000" stroke-opacity=".35" stroke-width="{h * 0.9}"/>
        <g class="lid">
          <rect x="{cx - w - 4}" y="{cy - h - 34}" width="{2 * w + 8}" height="34" fill="{FUR}"/>
          <path d="M{cx - w - 4} {cy - h} Q{cx} {cy - h + 7} {cx + w + 4} {cy - h - 2}" stroke="{LINE}" stroke-width="5" fill="none"/>
        </g>
      </g>
      <path d="{almond}" fill="none" stroke="{LINE}" stroke-width="1.6"/>
      {brush((cx - w * 0.6, cy + h * 0.95), (cx + w * 0.1, cy + h * 1.25), (cx + w * 0.8, cy + h * 0.6), 1.8, LINE, .55)}
      {brush((cx - w - 3, cy + h * 0.05), (cx - w * 0.1, cy - h * 1.35), (cx + w + 3, cy - h * 0.3), 4.2)}
    """


def head(mood, uid):
    lid = {"fine": 15, "bored": 20, "hungry": 2}.get(mood, 15)
    look = {"fine": 5, "bored": 7, "hungry": 0}.get(mood, 4)
    out = []
    line = f'stroke="{LINE}" stroke-width="2.6" stroke-linejoin="round"'

    def b(p0, p1, p2, *args, **kw):
        out.append(brush(T(p0), T(p1), T(p2), *args, **kw))

    # ears behind the head
    out.append(
        f'<g class="ear">{shape(TT(mirror(EAR_R)), [0, 0.06, 0.02, 0], FUR, line)}'
        f'{shape(TT(mirror(EAR_IN_R)), [0.04, 0.03, 0], EAR_IN)}'
        f'{brush(T((-90, -58)), T((-94, -94)), T((-98, -120)), 3, CREAM_LIT, .7)}'
        f'{brush(T((-80, -60)), T((-82, -88)), T((-86, -110)), 2.4, CREAM_LIT, .55)}</g>'
    )
    out.append(shape(TT(EAR_R), [0.02, 0.06, 0, 0], FUR_SHADE, line)
               + shape(TT(EAR_IN_R), [0.03, 0.04, 0], FUR_DEEP))

    # face planes
    out.append(shape(HEAD, HEAD_BENDS, FUR))
    out.append(f'<clipPath id="hc{uid}">{shape(HEAD, HEAD_BENDS, "#000")}</clipPath>')
    out.append(f'<g clip-path="url(#hc{uid})">')
    out.append(shape(TT([(-104, -84), (10, -96), (18, -46), (-30, -40), (-118, -8)]),
                     [0.04, 0.12, 0.1, 0.12, 0.04], FUR_LIT, 'opacity=".8"'))
    out.append(shape(TT(SHADOW), SHADOW_BENDS, FUR_SHADE))
    out.append(shape(TT(CORE), [-0.06] * 11, FUR_DEEP, 'opacity=".5"'))
    brow = [(-84, -30), (-28, -40), (-20, -30), (-82, -20)]
    out.append(shape(TT(brow), [0.12, 0, -0.1, 0], FUR_SHADE, 'opacity=".55"'))
    out.append(shape(TT(mirror(brow)), [0, -0.1, 0, 0.12], FUR_DEEP, 'opacity=".45"'))
    out.append(shape(TT(MUZZLE), [0.08] * 10, CREAM))
    out.append(shape(TT(MUZZLE_LIT), [0.08, 0.05, -0.1, -0.1, 0.08], CREAM_LIT, 'opacity=".9"'))
    out.append(shape(TT(MUZZLE_SHADE), [0.06, 0.08, 0.08, 0.06, -0.06, -0.08, -0.08, -0.06], CREAM_SHADE))
    out.append(poly(TT(CHIN_SHADE), FUR_DEEP, 'opacity=".45"'))
    out.append(f'<rect x="-150" y="-160" width="300" height="270" fill="url(#facepaint{uid})"/>')
    # loose fur, light on the lit side and dark in the shadow
    for p0, p1, p2, col, op in [
        ((-118, 30), (-98, 20), (-78, 26), CREAM_LIT, .5),
        ((-120, 54), (-100, 46), (-80, 54), CREAM_LIT, .45),
        ((-56, -72), (-38, -80), (-20, -78), CREAM_LIT, .35),
        ((118, 30), (98, 20), (78, 26), FUR_DEEP, .6),
        ((120, 54), (100, 46), (80, 54), FUR_DEEP, .5),
    ]:
        b(p0, p1, p2, 3, col, op)
    for x, w, ln in [(-18, 6, 40), (0, 7, 46), (18, 6, 40)]:
        b((x, -94), (x + 1, -94 + ln * 0.45), (x, -94 + ln), w, STRIPE, 0.9, start=-0.2, end=0.6)
    for y in (-6, 14):
        b((-130, y + 4), (-112, y), (-90, y + 6), 5, STRIPE, 0.75)
        b((130, y + 4), (112, y), (90, y + 6), 5, FUR_DEEP, 0.6)
    out.append("</g>")

    # silhouette: a thin even line, heavier brush accents on the shadow side
    out.append(shape(HEAD, HEAD_BENDS, "none", line))
    for p0, p1, p2, w in [
        ((104, -148), (104, -94), (100, -40), 4), ((100, -40), (108, -24), (110, -6), 5),
        ((98, 64), (76, 78), (52, 88), 5), ((52, 88), (26, 98), (0, 100), 4.4),
    ]:
        b(p0, p1, p2, w)

    # eyes: same design both sides, the far one narrowed by the turn
    out.append(f"<style>{blink_css(lid)}</style>")
    lx, _ = T((-EYE_X, 0))
    rx, _ = T((EYE_X, 0))
    out.append(eye(lx, EYE_Y, EYE_W * FAR_SCALE, EYE_H, mood, uid, "eyeN", look))
    out.append(eye(rx, EYE_Y, EYE_W * NEAR_SCALE, EYE_H, mood, uid, "eyeF", look))

    # nose bridge and nose
    b((10, -32), (8, -10), (6, 10), 2.4, LINE, 0.7)
    out.append(poly(TT(NOSE), "#8e4a48"))
    out.append(poly(TT([(-16, 14), (-2, 13), (-4, 20)]), "#c07a6c"))
    b((-18, 14), (0, 10), (18, 14), 2.6)
    b((0, 30), (0, 38), (0, 44), 2.2)

    if mood == "hungry":
        out.append(poly(TT([(-18, 52), (0, 46), (18, 52), (10, 70), (-10, 70)]), "#4a1d1c"))
        out.append(poly(TT([(-8, 68), (8, 68), (0, 62)]), "#a5504c"))
        out.append(poly(TT([(-13, 51), (-10, 58), (-7, 50)]), "#efe2c8"))
        out.append(poly(TT([(7, 50), (10, 58), (13, 51)]), "#efe2c8"))
        b((-20, 52), (0, 44), (20, 52), 2.6)
    elif mood == "happy":
        b((-26, 48), (-13, 57), (0, 46), 2.6)
        b((0, 46), (13, 57), (26, 48), 2.6)
    elif mood == "bored":
        b((-22, 53), (0, 51), (22, 53), 2.6)
    else:
        b((-24, 50), (-12, 55), (0, 46), 2.6)
        b((0, 46), (12, 55), (24, 50), 2.4)

    for p0, p1, p2 in [((-50, 44), (-108, 34), (-158, 40)), ((-48, 52), (-106, 54), (-150, 68))]:
        b(p0, p1, p2, 1.8, "#efe2c8", 0.7)
        b((-p0[0], p0[1]), (-p1[0], p1[1]), (-p2[0], p2[1]), 1.8, "#efe2c8", 0.7)
    return "".join(out)


def body(uid):
    """Shoulders and chest ruff, out of focus like the reference's foreground."""
    return f"""
      <g filter="url(#dof2{uid})">
        <path d="M-210 230 C-200 140 -150 78 -70 70 L70 66 C140 66 196 130 206 230z" fill="{FUR}"/>
        <path d="M60 66 C140 66 196 130 206 230 L80 230 C96 160 90 100 60 66z" fill="{FUR_SHADE}"/>
        <path d="M-200 200 C-188 140 -150 90 -110 76 C-140 110 -160 160 -166 220z" fill="{FUR_LIT}" opacity=".55"/>
        <path d="M-84 70 C-80 100 -96 116 -70 128 C-86 146 -64 160 -44 156 C-48 178 -20 186 -6 172 C4 196 34 184 34 164 C58 172 72 150 58 134 C84 124 80 96 64 70z" fill="{CREAM}"/>
        <path d="M30 72 C40 100 50 120 58 134 C72 150 58 172 34 164 C40 140 34 100 24 74z" fill="{CREAM_SHADE}"/>
        <path d="M-210 230 C-200 140 -150 78 -70 70 M70 66 C140 66 196 130 206 230" stroke="{LINE}" stroke-width="3" fill="none"/>
      </g>"""


def cat(mood, uid="", x=0, y=0, scale=1.0, with_body=True):
    tilt = {"asleep": 9, "happy": -6, "bored": 4, "hungry": -2}.get(mood, 0)
    drop = 14 if mood == "asleep" else 0
    parts = []
    if with_body:
        parts.append(body(uid))
    parts.append(
        f'<g transform="translate(0 {drop}) rotate({tilt} 0 60)"><g class="head">{head(mood, uid)}</g></g>'
    )
    return f'<g transform="translate({x} {y}) scale({scale})"><g class="breathe">{"".join(parts)}</g></g>'


# ------------------------------------------------------------------ room


def backdrop(w, h, uid=""):
    return (
        f'<rect width="{w}" height="{h}" fill="url(#bg{uid})"/>'
        f'<rect width="{w}" height="{h}" filter="url(#paint{uid})" opacity=".3"/>'
        f'<ellipse cx="{w * 0.3}" cy="{h * 0.45}" rx="{w * 0.22}" ry="{h * 0.4}" fill="#6b4128" opacity=".45" filter="url(#glow{uid})"/>'
    )


def overlay(w, h, uid=""):
    return (
        f'<rect class="keylight" width="{w}" height="{h}" fill="url(#key{uid})"/>'
        f'<rect width="{w}" height="{h}" filter="url(#grain{uid})" opacity=".14"/>'
        f'<rect width="{w}" height="{h}" fill="url(#vignette{uid})"/>'
    )


def fish_bones(x, y, uid=""):
    """Memento mori for a hungry cat. Sits in the blurred foreground."""
    ribs = "".join(
        brush((x + dx, y - 2), (x + dx + 6, y - 14), (x + dx + 2, y - 24), 3.2, "#d9c9a8")
        + brush((x + dx, y + 2), (x + dx + 6, y + 14), (x + dx + 2, y + 24), 3.2, "#d9c9a8")
        for dx in range(-30, 34, 12)
    )
    return f"""
    <g filter="url(#dof{uid})" opacity=".9">
      <ellipse cx="{x}" cy="{y + 30}" rx="110" ry="22" fill="#6e6a64"/>
      <ellipse cx="{x}" cy="{y + 24}" rx="96" ry="16" fill="#8f8a82"/>
      {brush((x - 60, y), (x, y - 3), (x + 50, y), 5, "#e6d8ba")}
      {ribs}
      {poly([(x - 60, y), (x - 90, y - 22), (x - 84, y), (x - 90, y + 22)], "#e6d8ba")}
      <path d="M{x + 46} {y - 16} Q{x + 80} {y - 18} {x + 84} {y} Q{x + 80} {y + 18} {x + 46} {y + 16}z" fill="#e6d8ba"/>
      <circle cx="{x + 68}" cy="{y - 4}" r="5" fill="#2a1610"/>
    </g>"""


def yarn(x, y, uid=""):
    return f"""
    <g filter="url(#dof{uid})">
      <circle cx="{x}" cy="{y}" r="46" fill="#4d5f86"/>
      <path d="M{x - 40} {y - 10} Q{x} {y + 20} {x + 38} {y - 22} M{x - 44} {y + 12} Q{x} {y + 40} {x + 42} {y + 4} M{x - 10} {y - 44} Q{x + 20} {y} {x + 6} {y + 44}" stroke="#34436a" stroke-width="5" fill="none"/>
      <path d="M{x - 26} {y - 30} Q{x - 6} {y - 40} {x + 14} {y - 34}" stroke="#8ea3cc" stroke-width="5" fill="none" stroke-linecap="round"/>
    </g>"""

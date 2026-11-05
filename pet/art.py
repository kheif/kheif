"""One evening corner of Mehmet's desk, painted for the profile README.

Technique: gouache and coloured pencil on warm paper.
  * gouache: wide matte colour fields whose edges wobble a little
    (a gentle displacement filter, only on painted shapes)
  * pencil: thin grainy lines with slightly varying weight, used for
    outlines, wood grain and a few hatch marks
  * the lightest cream is reserved for Byte's muzzle, the glass rim and
    the important text

Light: low, warm evening sun from a window on the right. It throws the
window frame onto the back wall and catches the front edge of the sill.

Everything is plain SVG (no scripts, no external files) so GitHub can
render it inside an <img>.
"""
import math

# ---------------------------------------------------------------- palette

INK = "#3a2218"          # pencil line
WALL = "#3b2925"         # wall in shade
WALL_MID = "#4a3229"
WALL_LIT = "#b9703e"     # sun patch on the wall
WOOD = "#8a5634"
WOOD_LIT = "#b77744"
WOOD_DARK = "#5a3420"
WOOD_EDGE = "#f0b778"    # light caught on the sill edge
FUR = "#d6853f"
FUR_LIT = "#f2a95e"
FUR_SHADE = "#9c5434"
FUR_DEEP = "#6c3628"
STRIPE = "#a3542c"
CREAM = "#f7ead2"        # the lightest cream, reserved
CREAM_MID = "#e2c9a4"
CREAM_SHADE = "#b08f74"
EAR = "#c98a74"
GOLD = "#dcab3c"
GOLD_LIT = "#f3d273"
NOSE = "#c86f5c"
PORCELAIN = "#ece3d3"
PORCELAIN_SHADE = "#b8ab98"
TEA_DEEP = "#6a240e"
TEA = "#93391a"
TEA_COPPER = "#cf5f30"
TEXT = CREAM
TEXT_SOFT = "#dcc8aa"
TEXT_FAINT = "#c7b193"
SERIF = "Georgia, 'Iowan Old Style', 'Palatino Linotype', 'Times New Roman', serif"


# ------------------------------------------------------------------ geometry


def _cubic(p0, p1, p2, p3, t):
    u = 1 - t
    return (
        u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
        u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1],
    )


def _quad(p0, p1, p2, t):
    u = 1 - t
    return (u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0], u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1])


def _ribbon(pts, widths):
    left, right = [], []
    n = len(pts)
    for i, (x, y) in enumerate(pts):
        a = pts[max(0, i - 1)]
        b = pts[min(n - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy / ln, dx / ln
        h = widths[i] / 2
        left.append((x + nx * h, y + ny * h))
        right.append((x - nx * h, y - ny * h))
    poly = left + right[::-1]
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in poly) + "z"


def stroke(p0, p1, p2, w, color=INK, opacity=1.0, taper=(1, 1), n=14, extra=""):
    """A pencil or brush mark along a quadratic curve.

    The weight swells in the middle and thins towards the ends; taper
    sets how thin each end gets (1 = to a point, 0 = full weight).
    """
    pts, ws = [], []
    for i in range(n + 1):
        t = i / n
        pts.append(_quad(p0, p1, p2, t))
        k = math.sin(math.pi * t) ** 0.6
        ends = 1 - taper[0] * (1 - t) ** 3 - taper[1] * t ** 3
        ws.append(w * max(0.12, min(1, k * 0.7 + 0.3) * ends))
    op = f' opacity="{opacity}"' if opacity != 1 else ""
    return f'<path d="{_ribbon(pts, ws)}" fill="{color}"{op} {extra}/>'


def tube(p0, p1, p2, p3, w0, w1, n=24):
    """Outline of a soft tube along a cubic, used for the tail."""
    pts, ws = [], []
    for i in range(n + 1):
        t = i / n
        pts.append(_cubic(p0, p1, p2, p3, t))
        tip = 1 - max(0, (t - 0.86) / 0.14) ** 2 * 0.55
        ws.append((w0 * (1 - t) + w1 * t) * tip)
    return _ribbon(pts, ws)


def path(d, fill="none", extra=""):
    return f'<path d="{d}" fill="{fill}" {extra}/>'


# ------------------------------------------------------------------ filters


def defs():
    return f"""
    <filter id="gouache" x="-5%" y="-5%" width="110%" height="110%">
      <feTurbulence type="fractalNoise" baseFrequency=".035" numOctaves="2" seed="3" result="n"/>
      <feDisplacementMap in="SourceGraphic" in2="n" scale="3.2" xChannelSelector="R" yChannelSelector="G"/>
    </filter>
    <filter id="gouache-fine" x="-5%" y="-20%" width="110%" height="140%">
      <feTurbulence type="fractalNoise" baseFrequency=".05" numOctaves="1" seed="6" result="n"/>
      <feDisplacementMap in="SourceGraphic" in2="n" scale="1.4" xChannelSelector="R" yChannelSelector="G"/>
    </filter>
    <filter id="pencil" x="-5%" y="-5%" width="110%" height="110%">
      <feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="1" seed="8" result="grain"/>
      <feColorMatrix in="grain" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 2.2 -.55" result="mask"/>
      <feComposite in="SourceGraphic" in2="mask" operator="in" result="g"/>
      <feTurbulence type="fractalNoise" baseFrequency=".06" numOctaves="1" seed="2" result="w"/>
      <feDisplacementMap in="g" in2="w" scale="1.6" xChannelSelector="R" yChannelSelector="G"/>
    </filter>
    <filter id="drybrush" x="-5%" y="-5%" width="110%" height="110%">
      <feTurbulence type="fractalNoise" baseFrequency=".05 .6" numOctaves="2" seed="5" result="streak"/>
      <feColorMatrix in="streak" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 2.6 -.9" result="mask"/>
      <feComposite in="SourceGraphic" in2="mask" operator="in"/>
    </filter>
    <filter id="paper" x="0" y="0" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency=".7" numOctaves="3" seed="11"/>
      <feColorMatrix type="matrix" values="0 0 0 0 .96  0 0 0 0 .86  0 0 0 0 .7  0 0 0 .55 -.18"/>
    </filter>
    <filter id="softedge" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="2.2"/></filter>
    <filter id="haze" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="9"/></filter>
    <radialGradient id="iris" cx=".55" cy=".35" r=".75">
      <stop offset="0" stop-color="{GOLD_LIT}"/>
      <stop offset=".7" stop-color="{GOLD}"/>
      <stop offset="1" stop-color="#9c7420"/>
    </radialGradient>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#7c6a86"/>
      <stop offset=".45" stop-color="#d98f6a"/>
      <stop offset="1" stop-color="#f6c48a"/>
    </linearGradient>
    <linearGradient id="walltone" x1="1" y1="0" x2="0" y2="0">
      <stop offset="0" stop-color="{WALL_MID}"/>
      <stop offset="1" stop-color="{WALL}"/>
    </linearGradient>
    <linearGradient id="sidewall" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#000" stop-opacity=".25"/>
      <stop offset="1" stop-color="#000" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="sill" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{WOOD}"/>
      <stop offset="1" stop-color="#9a6139"/>
    </linearGradient>
    <linearGradient id="sunfloor" x1="1" y1="0" x2="0" y2="0">
      <stop offset="0" stop-color="#e79a58" stop-opacity=".55"/>
      <stop offset=".7" stop-color="#e79a58" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="teaglass" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{TEA_DEEP}"/>
      <stop offset=".55" stop-color="{TEA}"/>
      <stop offset=".85" stop-color="{TEA_COPPER}"/>
      <stop offset="1" stop-color="#e98a52"/>
    </linearGradient>
    """


CSS = """
    @keyframes breathe { 0%,100% { transform: scale(1,1) } 50% { transform: scale(1.006,1.018) } }
    .breathe { transform-box: fill-box; transform-origin: 50% 100%; animation: breathe 4.6s ease-in-out infinite; }
    @keyframes twitch { 0%,86%,100% { transform: rotate(0) } 89% { transform: rotate(9deg) } 93% { transform: rotate(-3deg) } }
    .ear-listen { transform-box: fill-box; transform-origin: 30% 100%; animation: twitch 6.8s ease-in-out infinite; }
    @keyframes flick { 0%,78%,100% { transform: rotate(0) } 84% { transform: rotate(-4deg) } 90% { transform: rotate(1.5deg) } }
    .tail { transform-box: fill-box; transform-origin: 0% 30%; animation: flick 7.5s ease-in-out infinite; }
    @keyframes steam { 0% { transform: translate(0,6px) scale(.9,1); opacity: 0 } 25% { opacity: .55 } 100% { transform: translate(5px,-34px) scale(1.4,1.2); opacity: 0 } }
    .steam { transform-box: fill-box; transform-origin: 50% 100%; animation: steam 4.2s ease-out infinite; opacity: 0; }
    @keyframes drift { 0%,100% { opacity: .9 } 50% { opacity: 1 } }
    .sun { animation: drift 9s ease-in-out infinite; }
    @keyframes fade { 0% { opacity: 0; transform: translate(0,6px) } 30% { opacity: .85 } 100% { opacity: 0; transform: translate(8px,-28px) } }
    .rise { animation: fade 4.4s ease-out infinite; opacity: 0; }
"""


def blink_css(rest, closed, period=6.0):
    """The upper lid rests at `rest` and closes to `closed` (px down)."""
    return (
        f"@keyframes blink {{ 0%,90%,100% {{ transform: translateY({rest}px) }} "
        f"92.5%,94% {{ transform: translateY({closed}px) }} }}\n"
        f"    .lid {{ transform: translateY({rest}px); animation: blink {period}s ease-in-out infinite; }}"
    )


# ------------------------------------------------------------------- room


def wall(w, top, patches=(), shadow_bars=()):
    """Back wall with the sun's window shape thrown on it.

    patches are quads of sunlight, shadow_bars the frame shadows that
    cut through them.
    """
    out = [f'<rect x="-20" y="-20" width="{w + 40}" height="{top + 60}" fill="{WALL}"/>',
           f'<rect width="{w}" height="{top}" fill="url(#walltone)"/>']
    out.append('<g class="sun" filter="url(#softedge)">')
    for quad in patches:
        d = "M" + " L".join(f"{x} {y}" for x, y in quad) + "z"
        out.append(path(d, WALL_LIT, 'opacity=".62"'))
    for quad in shadow_bars:
        d = "M" + " L".join(f"{x} {y}" for x, y in quad) + "z"
        out.append(path(d, WALL, 'opacity=".85"'))
    out.append("</g>")
    # paper tooth only on the wall, where it reads as painted plaster
    out.append(f'<rect width="{w}" height="{top}" filter="url(#paper)" opacity=".16"/>')
    return "".join(out)


def sill(w, top, front, bottom, sun_from=0.5, grain_seed=1):
    """Wooden surface: top plane, a lit front edge and a darker front face."""
    out = [
        f'<g filter="url(#gouache)">',
        f'<rect x="-10" y="{top}" width="{w + 20}" height="{front - top}" fill="url(#sill)"/>',
        f'<rect x="-10" y="{top - 2}" width="{w + 20}" height="8" fill="{WOOD}"/>',
        f'<rect x="{w * (1 - sun_from)}" y="{top}" width="{w * sun_from + 10}" height="{front - top}" fill="url(#sunfloor)"/>',
        f'<rect x="-10" y="{front}" width="{w + 20}" height="{bottom - front + 10}" fill="{WOOD_DARK}"/>',
        "</g>",
        # the thin line of light on the edge
        stroke((-10, front + 1), (w / 2, front - 0.5), (w + 10, front + 1), 3.2, WOOD_EDGE, 0.85, taper=(0.9, 0.1), n=30),
        f'<rect x="-10" y="{top}" width="{w + 20}" height="2.4" fill="{INK}" opacity=".45"/>',
    ]
    # sparse wood grain: long, directional pencil marks
    s = grain_seed * 7919
    g = []
    rows = max(3, int((front - top) / 14))
    for i in range(rows):
        s = (s * 1103515245 + 12345) % 2 ** 31
        y = top + 8 + i * (front - top - 12) / rows + (s % 5)
        s = (s * 1103515245 + 12345) % 2 ** 31
        x0 = -20 + s % 120
        while x0 < w:
            s = (s * 1103515245 + 12345) % 2 ** 31
            ln = 140 + s % 220
            sag = (s % 7) - 3
            g.append(stroke((x0, y), (x0 + ln / 2, y + sag), (x0 + ln, y + sag * 0.3), 1.3, WOOD_DARK, 0.55, n=10))
            s = (s * 1103515245 + 12345) % 2 ** 31
            x0 += ln + 40 + s % 160
    for i in range(3):
        s = (s * 1103515245 + 12345) % 2 ** 31
        y = front + 10 + i * 9
        g.append(stroke((-10, y), (w / 2, y + 2), (w + 10, y), 1.1, "#3a2014", 0.6, n=20))
    out.append(f'<g filter="url(#pencil)">{"".join(g)}</g>')
    return "".join(out)


def window_light(x0, y0, pane_w=118, pane_h=78, gap=12, skew=0.2, slope=-0.07):
    """The window's shape thrown onto the back wall: a 2 x 2 grid of
    skewed panes with the frame's soft shadow running between them."""
    quads = []
    for r in range(2):
        for c in range(2):
            u0, v0 = c * (pane_w + gap), r * (pane_h + gap)
            corners = [(u0, v0), (u0 + pane_w, v0), (u0 + pane_w, v0 + pane_h), (u0, v0 + pane_h)]
            quads.append([(round(x0 + u + v * skew, 1), round(y0 + v + u * slope, 1)) for u, v in corners])
    return quads


def side_window(x_corner, w, top, sill_y):
    """The right hand side wall, seen at an angle, with its window.

    x_corner is where the back wall meets the side wall. The side wall
    recedes from the viewer, so the window is a trapezoid that grows
    taller towards the right edge.
    """
    x1 = x_corner + w            # right edge of the panel
    near_t, near_b = top - 26, sill_y + 6
    far_t, far_b = top + 10, sill_y - 8
    wx0, wx1 = x_corner + w * 0.24, x1 - w * 0.08
    def at(x, a, b):
        t = (x - x_corner) / w
        return a + (b - a) * t
    pane = [(wx0, at(wx0, far_t, near_t)), (wx1, at(wx1, far_t, near_t)),
            (wx1, at(wx1, far_b, near_b) - 18), (wx0, at(wx0, far_b, near_b) - 14)]
    pd = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pane) + "z"
    mx = (wx0 + wx1) / 2
    my_top, my_bot = at(mx, far_t, near_t), at(mx, far_b, near_b) - 16
    ty0 = at(wx0, far_t, near_t) * 0.55 + (at(wx0, far_b, near_b) - 14) * 0.45
    ty1 = at(wx1, far_t, near_t) * 0.55 + (at(wx1, far_b, near_b) - 18) * 0.45
    return f"""
    <g filter="url(#gouache)">
      <path d="M{x_corner} -10 L{x1 + 10} -10 L{x1 + 10} {sill_y + 20} L{x_corner} {sill_y + 20}z" fill="#33231f"/>
      <path d="{pd}" fill="url(#sky)"/>
      <clipPath id="paneclip"><path d="{pd}"/></clipPath>
      <ellipse cx="{wx1 - 10}" cy="{my_bot - 10}" rx="{w * 0.35}" ry="30" fill="#ffd9a0" opacity=".7" filter="url(#haze)" clip-path="url(#paneclip)"/>
      <path d="M{mx - 4} {my_top} L{mx + 4} {my_top - 2} L{mx + 4} {my_bot + 2} L{mx - 4} {my_bot}z" fill="#6b4029"/>
      <path d="M{wx0} {ty0 - 4} L{wx1} {ty1 - 5} L{wx1} {ty1 + 5} L{wx0} {ty0 + 4}z" fill="#6b4029"/>
    </g>
    <path d="{pd}" fill="none" stroke="#7a4a2d" stroke-width="9" stroke-linejoin="round"/>
    <path d="{pd}" fill="none" stroke="{INK}" stroke-width="1.4" opacity=".7"/>
    {stroke(pane[0], ((pane[0][0] + pane[3][0]) / 2 + 1, (pane[0][1] + pane[3][1]) / 2), pane[3], 3, WOOD_EDGE, .8, taper=(0.3, 0.3))}
    {stroke((x_corner, -4), (x_corner + 1, sill_y / 2), (x_corner, sill_y), 1.6, INK, .55)}
    <rect x="{x_corner}" y="0" width="{w}" height="{sill_y}" fill="url(#sidewall)" opacity=".5"/>"""


# ------------------------------------------------------------------ tea


def tea(x, y, s=1.0, steam=True):
    """A real ince belli glass on a small porcelain saucer.

    Origin is where the saucer meets the wood. The view is slightly from
    above, so every ellipse (saucer, base, tea surface, rim) shares the
    same squash ratio.
    """
    q = 0.28  # ellipse squash, same for every round thing in the set
    # glass profile (half widths) from rim to base, measured down from rim
    rim_w, rim_y = 21, -86
    tea_y = rim_y + 9
    waist_w, waist_y = 10, rim_y + 44
    belly_w, belly_y = 16.5, rim_y + 64
    base_w, base_y = 14, -12

    def side(sign):
        return (
            f"{sign * rim_w} {rim_y} "
            f"C{sign * (rim_w - 1)} {rim_y + 20} {sign * waist_w} {waist_y - 14} {sign * waist_w} {waist_y} "
            f"C{sign * waist_w} {waist_y + 10} {sign * belly_w} {belly_y - 10} {sign * belly_w} {belly_y} "
            f"C{sign * belly_w} {belly_y + 8} {sign * base_w} {base_y - 6} {sign * base_w} {base_y}"
        )

    glass = f"M{side(-1)} L{base_w} {base_y} " + "".join(
        []) + f"C{base_w} {base_y - 6} {belly_w} {belly_y + 8} {belly_w} {belly_y} " \
        f"C{belly_w} {belly_y - 10} {waist_w} {waist_y + 10} {waist_w} {waist_y} " \
        f"C{waist_w} {waist_y - 14} {rim_w - 1} {rim_y + 20} {rim_w} {rim_y}"

    # tea: the same profile, a hair inside the glass, from the surface to
    # the top of the thick base
    k = 0.9
    tw = rim_w - 1.6
    inner = (
        f"M{-tw} {tea_y} "
        f"C{-(rim_w - 2.4)} {rim_y + 22} {-(waist_w - 2)} {waist_y - 14} {-(waist_w - 2)} {waist_y} "
        f"C{-(waist_w - 2)} {waist_y + 10} {-(belly_w - 2.4)} {belly_y - 10} {-(belly_w - 2.4)} {belly_y} "
        f"C{-(belly_w - 2.4)} {belly_y + 5} {-(base_w - 3)} {base_y - 12} {-(base_w - 3)} {base_y - 9} "
        f"Q0 {base_y - 6} {base_w - 3} {base_y - 9} "
        f"C{base_w - 3} {base_y - 12} {belly_w - 2.4} {belly_y + 5} {belly_w - 2.4} {belly_y} "
        f"C{belly_w - 2.4} {belly_y - 10} {waist_w - 2} {waist_y + 10} {waist_w - 2} {waist_y} "
        f"C{waist_w - 2} {waist_y - 14} {rim_w - 2.4} {rim_y + 22} {tw} {tea_y}z"
    )

    wisps = ""
    if steam:
        for i, (dx, h, d) in enumerate([(-6, 40, 0), (4, 48, 1.4), (12, 34, 2.8)]):
            wisps += (
                f'<g class="steam" style="animation-delay:{d}s">'
                + stroke((dx, rim_y - 6), (dx - 9, rim_y - 6 - h * 0.5), (dx + 3, rim_y - 6 - h), 2.6, CREAM, 0.65, n=16)
                + "</g>"
            )

    return f"""
  <g transform="translate({x} {y}) scale({s})">
    <!-- contact shadow, thrown left by the sun on the right -->
    <ellipse cx="-14" cy="2" rx="52" ry="{52 * q * 0.5}" fill="#2a160c" opacity=".45" filter="url(#softedge)"/>
    <!-- saucer -->
    <g filter="url(#gouache)">
      <ellipse cx="0" cy="-3" rx="46" ry="{46 * q}" fill="{PORCELAIN_SHADE}"/>
      <ellipse cx="0" cy="-6" rx="46" ry="{46 * q}" fill="{PORCELAIN}"/>
      <ellipse cx="0" cy="-6.5" rx="27" ry="{27 * q}" fill="#d9cdb9"/>
      <path d="M-46 -6 A46 {46 * q} 0 0 0 46 -6 L46 -3 A46 {46 * q} 0 0 1 -46 -3z" fill="#cfc2ad"/>
    </g>
    <path d="M-44 -2.5 A46 {46 * q} 0 0 0 30 4" stroke="{INK}" stroke-width="1.3" fill="none" opacity=".55"/>
    <path d="M14 -18 A46 {46 * q} 0 0 1 44 -9" stroke="#fffaf0" stroke-width="2" fill="none" opacity=".9"/>
    <!-- glass contact shadow on the saucer -->
    <ellipse cx="-4" cy="-10" rx="18" ry="{18 * q}" fill="#8a7a66" opacity=".55" filter="url(#softedge)"/>
    {wisps}
    <!-- back of the rim, seen through the tea gap -->
    <ellipse cx="0" cy="{rim_y}" rx="{rim_w}" ry="{rim_w * q}" fill="#f0e6d6" fill-opacity=".1" stroke="{CREAM}" stroke-width="1.1" stroke-opacity=".7"/>
    <!-- tea -->
    <path d="{inner}" fill="url(#teaglass)"/>
    <ellipse cx="0" cy="{tea_y}" rx="{tw}" ry="{tw * q}" fill="#a2421c"/>
    <ellipse cx="3" cy="{tea_y + 0.6}" rx="{tw * 0.72}" ry="{tw * q * 0.6}" fill="{TEA_DEEP}" opacity=".65"/>
    <path d="M{tw * 0.25} {tea_y - tw * q * 0.85} A{tw} {tw * q} 0 0 1 {tw} {tea_y}" stroke="#f08a52" stroke-width="1.4" fill="none" opacity=".9"/>
    <path d="M{waist_w - 3} {waist_y - 8} C{waist_w - 2} {waist_y + 6} {belly_w - 3} {belly_y - 8} {belly_w - 3.5} {belly_y + 4}" stroke="#f3874c" stroke-width="2.2" fill="none" opacity=".75"/>
    <!-- thick glass base -->
    <path d="M{-base_w} {base_y} Q0 {base_y + 4} {base_w} {base_y} L{base_w - 0.5} {base_y - 9} Q0 {base_y - 5} {-(base_w - 0.5)} {base_y - 9}z" fill="#efe4d0" fill-opacity=".28"/>
    <ellipse cx="6" cy="{base_y - 4}" rx="3.2" ry="1.4" fill="#fff7e8"/>
    <path d="M-9 {base_y - 2} q6 2 12 0" stroke="#ffcf9a" stroke-width="1.2" fill="none" opacity=".8"/>
    <!-- glass walls and the front of the rim -->
    <path d="{glass}" fill="none" stroke="{INK}" stroke-width="1.3" opacity=".8"/>
    <path d="M{-rim_w} {rim_y} A{rim_w} {rim_w * q} 0 0 0 {rim_w} {rim_y}" stroke="{CREAM}" stroke-width="1.8" fill="none"/>
    <path d="M{-rim_w} {rim_y} A{rim_w} {rim_w * q} 0 0 0 {rim_w} {rim_y}" stroke="{INK}" stroke-width=".8" fill="none" opacity=".5" transform="translate(0 1.4)"/>
    <!-- one thin, sharp reflection on the lit side -->
    <path d="M{rim_w - 4} {rim_y + 5} C{rim_w - 5} {rim_y + 20} {waist_w + 1} {waist_y - 12} {waist_w - 0.5} {waist_y - 2}" stroke="#fffaf0" stroke-width="1.6" fill="none" stroke-linecap="round"/>
    <path d="M{-(rim_w - 5)} {rim_y + 8} C{-(rim_w - 6)} {rim_y + 16} {-(waist_w + 2)} {waist_y - 18} {-(waist_w + 1)} {waist_y - 10}" stroke="#fffaf0" stroke-width=".9" fill="none" opacity=".45" stroke-linecap="round"/>
  </g>"""


# ------------------------------------------------------------------ Byte

# Byte lies loaf style on the sill in three quarter view: head at the
# front right, body running back and to the left behind it, paws tucked.
# Local units, ground at y = 0. The sun comes from the right.

BODY = (
    "M100 -6 "
    "L-150 -6 "
    "C-182 -8 -192 -56 -170 -90 "                   # rump
    "C-146 -130 -76 -162 10 -156 "                  # one soft back arc
    "C56 -152 108 -116 116 -66 "                    # behind the head down to the chest
    "C120 -36 114 -12 100 -6z"
)

HAUNCH = "M-98 -6 C-94 -56 -124 -94 -166 -82"
HAUNCH_SHADE = "M-170 -90 C-192 -56 -182 -8 -150 -6 L-104 -6 C-98 -44 -118 -86 -164 -86z"
BELLY_SHADE = "M-150 -6 L100 -6 C112 -10 118 -20 118 -28 C40 -22 -60 -22 -170 -30z"

# the tail leaves the hip, wraps round the rump and curls along the front
TAIL_A = ((-146, -30), (-182, -30), (-194, -2), (-150, 2))
TAIL_B = ((-150, 2), (-106, 5), (-54, 6), (-20, -12))

HEAD_X, HEAD_Y, HEAD_S = 50, -96, 1.2


def tail():
    pts, ws = [], []
    for seg, w0, w1, n in [(TAIL_A, 27, 24, 12), (TAIL_B, 24, 15, 18)]:
        for i in range(n + (seg is TAIL_B)):
            t = i / n
            pts.append(_cubic(*seg, t))
            ws.append(w0 * (1 - t) + w1 * t)
    for k, f in zip(range(1, 6), (0.3, 0.55, 0.72, 0.85, 0.94)):
        ws[-k] *= f
    d = _ribbon(pts, ws)
    # rings sit across the tail, following its direction
    rings = []
    for idx in (6, 13, 19, 25):
        (x, y), (x2, y2) = pts[idx], pts[idx + 1]
        ang = math.atan2(y2 - y, x2 - x) + math.pi / 2
        hw = ws[idx] / 2
        c, s_ = math.cos(ang) * hw, math.sin(ang) * hw
        rings.append(stroke((x - c, y - s_), (x + 3, y), (x + c, y + s_), 5.5, STRIPE, .7, taper=(0.6, 0.6)))
    tip = pts[-3]
    return f"""
    <mask id="tailmask" maskUnits="userSpaceOnUse" x="-260" y="-200" width="420" height="240">
      <rect x="-260" y="-200" width="420" height="240" fill="#fff"/>
      <path d="{BODY}" fill="#000"/>
      <rect x="-150" y="-12" width="200" height="30" fill="#fff"/>
      <path d="M-60 -12 L10 -12 L10 -30 L-60 -30z" fill="#fff"/>
    </mask>
    <g class="tail" mask="url(#tailmask)">
      <g filter="url(#gouache)"><path d="{d}" fill="{FUR}"/></g>
      {"".join(rings)}
      {stroke((tip[0] - 2, tip[1] + 2), (tip[0] + 4, tip[1] - 2), pts[-1], 6, FUR_DEEP, .75)}
      {stroke(pts[14], pts[20], pts[26], 2.4, FUR_LIT, .8)}
      <path d="{d}" fill="none" stroke="{INK}" stroke-width="1.7" opacity=".8"/>
    </g>"""


def body_stripes():
    """Tabby bands that wrap around the barrel, following its volume."""
    out = []
    for x, y, dx, ln, w in [
        (-14, -156, -4, 48, 12), (-48, -150, -8, 52, 12), (-82, -138, -12, 50, 11),
        (-114, -122, -14, 44, 10), (-142, -102, -12, 36, 9),
    ]:
        out.append(stroke((x, y + 2), (x + dx * 0.4 - 6, y + ln * 0.55), (x + dx, y + ln), w, STRIPE, .55, taper=(0.4, 1)))
    for x, y in [(-150, -66), (-140, -44)]:
        out.append(stroke((x, y), (x + 14, y - 8), (x + 30, y - 4), 7, STRIPE, .5))
    return "".join(out)


def paw():
    """Tip of the near front paw, peeking from under the chest."""
    return f"""
    <g filter="url(#gouache)">
      <path d="M50 -4 C50 -20 66 -26 84 -24 C100 -22 110 -14 108 -4z" fill="{CREAM_MID}"/>
      <path d="M58 -14 C66 -22 84 -24 98 -18 C92 -20 70 -20 58 -14z" fill="{CREAM}" opacity=".9"/>
      <path d="M50 -4 C52 -10 60 -12 70 -10 L66 -4z" fill="{CREAM_SHADE}" opacity=".8"/>
    </g>
    <path d="M50 -4 C50 -20 66 -26 84 -24 C100 -22 110 -14 108 -4" stroke="{INK}" stroke-width="1.7" fill="none" opacity=".85"/>
    {stroke((74, -5), (75, -11), (76, -16), 1.6, INK, .7)}
    {stroke((88, -5), (89, -11), (90, -16), 1.6, INK, .7)}"""


def chest():
    """Cream bib under the chin, spread along the fur direction."""
    return f"""
    <g filter="url(#gouache)">
      <path d="M30 -78 C22 -54 34 -34 40 -24 C48 -12 60 -14 64 -22 C76 -14 92 -16 100 -24 C110 -20 120 -28 122 -40
               C126 -60 118 -84 100 -98z" fill="{CREAM_MID}"/>
      <path d="M86 -96 C106 -84 120 -62 120 -42 C112 -36 104 -40 98 -36 C104 -56 98 -76 86 -96z" fill="{CREAM}" opacity=".85"/>
      <path d="M30 -78 C22 -54 34 -34 40 -24 C44 -18 50 -16 54 -18 C44 -36 40 -56 46 -84z" fill="{CREAM_SHADE}" opacity=".7"/>
    </g>
    {stroke((46, -40), (52, -30), (50, -22), 2, CREAM_SHADE, .8)}
    {stroke((70, -44), (76, -32), (74, -22), 2, CREAM_SHADE, .7)}
    {stroke((96, -52), (102, -40), (100, -30), 2, "#fff6e4", .8)}"""


# head, built straight on and symmetric, then turned a little to the
# viewer's right so it agrees with the body
TURN_C, SCALE_L, SCALE_R = 4, 1.0, 0.9


def T(p):
    x, y = p
    return (round(TURN_C + x * (SCALE_L if x < 0 else SCALE_R), 2), y)


def head_outline():
    """Soft head: rounded crown, cheek fluff in a few tufts, small chin."""
    crown = (0, -60)
    right = [
        ((30, -60), (56, -50), (66, -30)),    # crown to cheek top
        ((74, -16), (80, -2), (80, 6)),       # upper cheek
        ((86, 12), (90, 16), (88, 18)),       # tuft 1
        ((82, 20), (84, 26), (86, 30)),
        ((78, 34), (76, 36), (70, 38)),       # tuft 2
        ((58, 50), (30, 58), (0, 58)),        # jaw to chin
    ]
    d = [f"M{T(crown)[0]} {crown[1]}"]
    for c1, c2, e in right:
        a, b, c = T(c1), T(c2), T(e)
        d.append(f"C{a[0]} {a[1]} {b[0]} {b[1]} {c[0]} {c[1]}")
    # left half: mirror and reverse
    pts = [crown] + [seg[2] for seg in right]
    for i in range(len(right) - 1, -1, -1):
        c1, c2, e = right[i]
        start = pts[i]
        m = lambda p: (-p[0], p[1])  # noqa: E731
        a, b, c = T(m(c2)), T(m(c1)), T(m(start))
        d.append(f"C{a[0]} {a[1]} {b[0]} {b[1]} {c[0]} {c[1]}")
    return " ".join(d) + "z"


def ear(side, mood, uid):
    """side -1 is the viewer's left ear, 1 the right one (turned to listen)."""
    m = (lambda p: (side * p[0], p[1]))
    base_in, tip, base_out = m((20, -56)), m((50, -94)), m((66, -32))
    tipL = m((45, -89))
    tipR = m((54, -89))
    pts = [T(base_in), T(tipL), T(tipR), T(base_out)]
    d = (f"M{pts[0][0]} {pts[0][1]} Q{T(m((30, -76)))[0]} {T(m((30, -76)))[1]} {pts[1][0]} {pts[1][1]} "
         f"Q{T(tip)[0]} {tip[1] - 4} {pts[2][0]} {pts[2][1]} "
         f"Q{T(m((64, -64)))[0]} {T(m((64, -64)))[1]} {pts[3][0]} {pts[3][1]}z")
    inner = (f"M{T(m((27, -56)))[0]} -56 Q{T(m((34, -74)))[0]} -74 {T(m((48, -85)))[0]} -85 "
             f"Q{T(m((56, -66)))[0]} -66 {T(m((57, -42)))[0]} -42z")
    lit = side > 0
    fill_in = "#e0a38a" if lit else EAR
    rot = {"bored": 10, "asleep": 14}.get(mood, 0) * side
    listen = 'class="ear-listen"' if lit else ""
    tufts = "".join(
        stroke(T(m((40 + k, -48))), T(m((42 + k, -62))), T(m((44 + k * 0.5, -75))), 2, CREAM, .75 if lit else .5)
        for k in (0, 7)
    )
    return f"""
      <g transform="rotate({rot + (-8 if lit else 0)} {T(base_out)[0]} {base_out[1]})">
       <g {listen}>
        <g filter="url(#gouache)"><path d="{d}" fill="{FUR_LIT if lit else FUR_SHADE}"/><path d="{inner}" fill="{fill_in}"/></g>
        {tufts}
        <path d="{d}" stroke="{INK}" stroke-width="1.8" fill="none" opacity=".85"/>
        {stroke(T(m((48, -90))), T(m((58, -64))), T(m((66, -34))), 2.6, INK, .55) if not lit else ""}
       </g>
      </g>"""


def eye(side, mood, uid):
    """Almond eye, outer corner a touch higher, heavy upper lid.

    Built in its own little coordinate system so the lid can slide down
    without changing shape.
    """
    cx, cy = T((side * 30, -8))
    sx = SCALE_L if side < 0 else SCALE_R
    w, h = 17, 11.5
    tilt = side * 5
    look = {"bored": 5}.get(mood, -1.5)  # pupils turn slightly towards us
    name = f"eye{'L' if side < 0 else 'R'}"
    g = f'transform="translate({cx} {cy}) rotate({tilt}) scale({sx * side} 1)"'

    if mood in ("happy", "asleep"):
        if mood == "happy":
            # content, squeezed shut: an upward arch
            return f"""
      <g {g}>
        {stroke((-w * 0.95, 3), (0, -9), (w * 0.95, 1), 3.4, INK)}
        {stroke((-w * 0.6, 6), (0, 4), (w * 0.6, 5), 1.1, INK, .35)}
      </g>"""
        return f"""
      <g {g}>
        {stroke((-w, -1), (0, 7), (w, -2), 3.2, INK)}
        {stroke((-w * 0.5, 7), (0, 10), (w * 0.6, 6), 1.1, INK, .3)}
      </g>"""

    rest = {"fine": 0.55, "bored": 0.68, "hungry": 0.18}.get(mood, 0.5) * h * 2
    pupil_r = 3.4 if mood == "hungry" else 2.6
    almond = f"M{-w} 0 Q{-w * 0.2} {-h * 1.45} {w} {-h * 0.2} Q{w * 0.15} {h * 1.05} {-w} 0z"
    return f"""
      <g {g}>
        <style>{blink_css(rest, h * 2.1)}</style>
        <clipPath id="{name}{uid}"><path d="{almond}"/></clipPath>
        <path d="{almond}" fill="url(#iris)"/>
        <g clip-path="url(#{name}{uid})">
          <ellipse cx="{look}" cy="1" rx="{pupil_r}" ry="{pupil_r * 2.1}" fill="#24130c"/>
          <circle cx="{look + 3}" cy="-3" r="1.7" fill="#fffaf0"/>
          <g class="lid">
            <rect x="{-w - 4}" y="{-h * 3.4}" width="{2 * w + 8}" height="{h * 2.2}" fill="{FUR}"/>
            <path d="M{-w - 4} {-h * 1.2} Q{-w * 0.1} {-h * 1.2 + 4} {w + 4} {-h * 1.4}" stroke="{FUR_SHADE}" stroke-width="5" fill="none"/>
            {stroke((-w - 3, -h * 1.15), (-w * 0.1, -h * 0.95), (w + 3, -h * 1.35), 3.6, INK, taper=(0.8, 0.3))}
          </g>
        </g>
        {stroke((-w, 0.5), (w * 0.15, h * 1.1), (w, -h * 0.2), 1.6, INK, .8, taper=(1, 0.5))}
        {stroke((-w * 0.8, -h * 1.0), (-w * 0.1, -h * 1.75), (w * 0.9, -h * 0.9), 1.2, FUR_DEEP, .45)}
      </g>"""


def face(mood, uid):
    out = []
    # whisker pads, chin, nose
    pad_l, pad_r = T((-11, 22)), T((11, 22))
    out.append('<g filter="url(#gouache)">')
    out.append(f'<ellipse cx="{T((0, 38))[0]}" cy="38" rx="16" ry="9" fill="{CREAM_MID}"/>')
    out.append(f'<ellipse cx="{pad_l[0]}" cy="{pad_l[1]}" rx="{14 * SCALE_L}" ry="10.5" fill="{CREAM}"/>')
    out.append(f'<ellipse cx="{pad_r[0]}" cy="{pad_r[1]}" rx="{14 * SCALE_R}" ry="10.5" fill="{CREAM}"/>')
    out.append("</g>")
    out.append(f'<ellipse cx="{pad_l[0] - 2}" cy="{pad_l[1] + 3}" rx="9" ry="5" fill="{CREAM_SHADE}" opacity=".35" filter="url(#softedge)"/>')
    # whisker dots
    for side in (-1, 1):
        for dx, dy in [(8, 18), (13, 23), (9, 26)]:
            p = T((side * dx, dy))
            out.append(f'<circle cx="{p[0]}" cy="{p[1]}" r=".9" fill="{CREAM_SHADE}"/>')
    nx = T((0, 0))[0]
    out.append(f'<path d="M{nx - 6} 10 Q{nx} 8 {nx + 6} 10 Q{nx + 5} 15 {nx} 18 Q{nx - 5} 15 {nx - 6} 10z" fill="{NOSE}"/>')
    out.append(f'<ellipse cx="{nx + 2}" cy="11" rx="2" ry="1" fill="#eaa18e"/>')
    out.append(stroke((nx, 18), (nx, 21), (nx, 25), 1.4, INK, .8))

    if mood == "hungry":
        out.append(f'<path d="M{nx - 7} 26 Q{nx} 24 {nx + 7} 26 Q{nx + 4} 35 {nx} 35 Q{nx - 4} 35 {nx - 7} 26z" fill="#5a2018"/>')
        out.append(f'<path d="M{nx - 3} 33 Q{nx} 30 {nx + 3} 33z" fill="#c26658"/>')
        out.append(stroke((nx - 9, 26), (nx, 23), (nx + 9, 26), 1.6, INK, .85))
    elif mood == "happy":
        out.append(stroke((nx - 10, 25), (nx - 5, 30), (nx, 25), 1.6, INK, .85))
        out.append(stroke((nx, 25), (nx + 5, 30), (nx + 10, 25), 1.6, INK, .85))
    elif mood == "bored":
        out.append(stroke((nx - 8, 27), (nx, 26), (nx + 8, 27), 1.5, INK, .8))
    else:
        # a small smug curl at one corner
        out.append(stroke((nx - 9, 26), (nx - 5, 29), (nx, 25), 1.5, INK, .85))
        out.append(stroke((nx, 25), (nx + 5, 29), (nx + 10, 25), 1.5, INK, .85))

    # whiskers: thin, different lengths, a slight droop
    for side in (-1, 1):
        sc = SCALE_L if side < 0 else SCALE_R
        for dy, ln, droop, op in [(18, 70, -4, .8), (23, 82, 4, .7), (27, 58, 10, .55)]:
            a = T((side * 16, dy))
            b = (a[0] + side * ln * 0.5 * sc, a[1] + droop * 0.3 - 2)
            c = (a[0] + side * ln * sc, a[1] + droop)
            out.append(stroke(a, b, c, 1.3, CREAM, op, taper=(0.3, 1)))
    return "".join(out)


def head(mood, uid):
    outline = head_outline()
    out = [ear(-1, mood, uid), ear(1, mood, uid)]
    out.append(f'<clipPath id="headclip{uid}"><path d="{outline}"/></clipPath>')
    out.append(f'<g filter="url(#gouache)"><path d="{outline}" fill="{FUR}"/></g>')
    out.append(f'<g clip-path="url(#headclip{uid})">')
    # light from the right: lit cheek and brow, shade on the far left side
    out.append(f'<path d="M14 -70 C60 -66 96 -30 92 20 C70 0 40 -20 14 -40z" fill="{FUR_LIT}" opacity=".8" filter="url(#softedge)"/>')
    out.append(f'<path d="M-90 -40 C-70 -20 -60 20 -40 64 L-100 64z" fill="{FUR_SHADE}" opacity=".75" filter="url(#softedge)"/>')
    out.append(f'<path d="M-60 40 C-30 52 30 54 70 40 L70 70 L-60 70z" fill="{FUR_SHADE}" opacity=".6" filter="url(#softedge)"/>')
    # forehead M and the three crown lines: Byte's signature
    for x0, top, ln, w in [(-9, -60, 22, 4.6), (0, -62, 28, 5.2), (9, -60, 22, 4.6)]:
        a, c = T((x0, top)), T((x0 * 0.7, top + ln))
        out.append(stroke(a, ((a[0] + c[0]) / 2 + 0.5, (top + top + ln) / 2), c, w, STRIPE, .9, taper=(0.3, 1)))
    for side in (-1, 1):
        out.append(stroke(T((side * 6, -34)), T((side * 14, -26)), T((side * 22, -34)), 3.4, STRIPE, .8))
        out.append(stroke(T((side * 22, -34)), T((side * 30, -42)), T((side * 38, -30)), 3.4, STRIPE, .8))
        # cheek bands curve back along the cheek's volume
        out.append(stroke(T((side * 44, -4)), T((side * 58, 0)), T((side * 74, -6)), 4.4, STRIPE, .75))
        out.append(stroke(T((side * 46, 10)), T((side * 62, 16)), T((side * 78, 12)), 4, STRIPE, .65))
    # soft fur tufts at the cheeks
    for side, col, op in [(-1, FUR_DEEP, .55), (1, CREAM, .6)]:
        for y in (12, 24):
            out.append(stroke(T((side * 70, y)), T((side * 80, y + 4)), T((side * 86, y + 2)), 3, col, op))
    out.append("</g>")
    out.append(f'<path d="{outline}" stroke="{INK}" stroke-width="1.9" fill="none" opacity=".88"/>')
    out.append(stroke(T((-78, 0)), T((-70, 44)), T((0, 58)), 3.4, INK, .7))
    out.append(eye(-1, mood, uid))
    out.append(eye(1, mood, uid))
    out.append(face(mood, uid))
    return "".join(out)


def byte(mood, x, y, s=1.0, uid="", with_body=True):
    """Byte at (x, y), ground under the paws, scale s."""
    tilt = {"asleep": 8, "happy": -3, "bored": 3, "hungry": -6}.get(mood, -2)
    drop = {"asleep": 12, "hungry": -6}.get(mood, 0)
    parts = []
    if with_body:
        parts.append(f"""
            <clipPath id="bodyclip{uid}"><path d="{BODY}"/></clipPath>
      <g class="breathe">
        <g filter="url(#gouache)"><path d="{BODY}" fill="{FUR}"/></g>
        <g clip-path="url(#bodyclip{uid})">
          <path d="{HAUNCH_SHADE}" fill="{FUR_SHADE}" opacity=".8" filter="url(#softedge)"/>
          <path d="{BELLY_SHADE}" fill="{FUR_DEEP}" opacity=".55" filter="url(#softedge)"/>
          <path d="M-40 -160 C30 -164 104 -122 118 -66 L140 -66 L140 -190z" fill="{FUR_LIT}" opacity=".55" filter="url(#softedge)"/>
          {body_stripes()}
          <g filter="url(#drybrush)">{stroke((-150, -112), (-80, -160), (6, -150), 12, FUR_LIT, .85, n=24)}</g>
        </g>
        {stroke((-166, -98), (-86, -166), (14, -157), 2.8, "#ffd59a", .85, taper=(1, 0.6), n=26)}
        <path d="{HAUNCH}" stroke="{INK}" stroke-width="1.8" fill="none" opacity=".7"/>
        <path d="{BODY}" stroke="{INK}" stroke-width="1.9" fill="none" opacity=".85"/>
        {stroke((-170, -90), (-190, -50), (-150, -6), 3.2, INK, .6)}
        {chest()}
        {paw()}
      </g>
      {tail()}""")
    parts.append(
        f'<g transform="translate({HEAD_X} {HEAD_Y + drop}) rotate({tilt}) scale({HEAD_S})">{head(mood, uid)}</g>'
    )
    return f'<g transform="translate({x} {y}) scale({s})">{"".join(parts)}</g>'


def cast_shadow(x, y, s=1.0):
    """Byte's shadow on the sill, thrown to the left by the low sun."""
    return (
        f'<g transform="translate({x} {y}) scale({s})">'
        f'<path d="M106 0 C80 8 -110 14 -260 10 C-290 6 -280 -4 -240 -6 L100 -6z" fill="#2a1409" opacity=".42" filter="url(#softedge)"/>'
        f'<path d="M104 -1 L-196 -1" stroke="#1e0e06" stroke-width="3" opacity=".5" filter="url(#softedge)"/>'
        "</g>"
    )


# ----------------------------------------------------------------- props


def dish(x, y, s=1.0, bones=False):
    """An empty saucer, licked clean. Same porcelain as the tea set."""
    fish = ""
    if bones:
        ribs = "".join(
            stroke((dx, -9), (dx + 2, -13), (dx + 1, -16), 1.3, "#efe4cc")
            + stroke((dx, -7), (dx + 2, -4), (dx + 1, -1), 1.3, "#efe4cc")
            for dx in range(-8, 9, 4)
        )
        fish = (
            stroke((-14, -8), (0, -9), (13, -8), 1.6, "#efe4cc") + ribs
            + '<path d="M-14 -8 L-21 -13 L-19 -8 L-21 -3z" fill="#efe4cc"/>'
            + '<path d="M12 -12 Q20 -11 21 -8 Q20 -5 12 -4z" fill="#efe4cc"/>'
            + f'<circle cx="16.5" cy="-8.4" r="1.2" fill="{INK}"/>'
        )
    q = 0.28
    return f"""
  <g transform="translate({x} {y}) scale({s})">
    <ellipse cx="-10" cy="2" rx="40" ry="6" fill="#2a160c" opacity=".4" filter="url(#softedge)"/>
    <g filter="url(#gouache)">
      <ellipse cx="0" cy="-3" rx="36" ry="{36 * q}" fill="{PORCELAIN_SHADE}"/>
      <ellipse cx="0" cy="-6" rx="36" ry="{36 * q}" fill="{PORCELAIN}"/>
      <ellipse cx="0" cy="-6.5" rx="22" ry="{22 * q}" fill="#ddd2bf"/>
    </g>
    <path d="M10 -15 A36 {36 * q} 0 0 1 34 -8" stroke="#fffaf0" stroke-width="1.8" fill="none"/>
    {fish if bones else stroke((-10, -7), (-4, -8), (4, -7), 1.4, "#b39a7a", .8)}
  </g>"""


def yarn(x, y, s=1.0):
    return f"""
  <g transform="translate({x} {y}) scale({s})">
    <ellipse cx="-8" cy="1" rx="30" ry="5" fill="#2a160c" opacity=".4" filter="url(#softedge)"/>
    <g filter="url(#gouache)">
      <circle cx="0" cy="-22" r="22" fill="#5d6f96"/>
      <path d="M0 -44 A22 22 0 0 1 22 -22 A22 22 0 0 1 8 -1 C14 -16 12 -32 0 -44z" fill="#8193b8"/>
    </g>
    <g filter="url(#pencil)">
      <path d="M-18 -34 Q0 -18 18 -36 M-21 -20 Q0 -2 20 -22 M-12 -6 Q4 -12 14 -4 M-6 -43 Q10 -24 4 -1" stroke="#33406a" stroke-width="1.6" fill="none"/>
    </g>
    <circle cx="0" cy="-22" r="22" fill="none" stroke="{INK}" stroke-width="1.5" opacity=".8"/>
    {stroke((-20, -6), (-50, 2), (-84, -1), 1.8, "#5d6f96")}
  </g>"""

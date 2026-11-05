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


LIGHT_EDGE = "#ffd9a0"

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
    return byte_defs() + f"""
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
    <filter id="shade" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="3.6"/></filter>
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
    @keyframes blink { 0%,91%,100% { transform: scaleY(1) } 93.5%,94.5% { transform: scaleY(.08) } }
    .blink { transform-box: fill-box; transform-origin: 50% 85%; animation: blink 6.5s ease-in-out infinite; }
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
        out.append(path(d, WALL_LIT, 'opacity=".3"'))
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

# ------------------------------------------------------------------ Byte
#
# Byte follows the look of soft, textured cat illustrations:
#   * no closed outline: an edge is where one colour meets another, and
#     that edge is grainy, like crayon on paper
#   * a thin, broken dark line only where one form overlaps another,
#     on the underside of that overlap (chin over chest, paw, ear back)
#   * big simple shapes: a wide cheeked head, a bean shaped body
#   * colour runs in soft gradients and darkens towards the extremities;
#     cream on the muzzle and chest fades into orange through the grain
#   * stripes are broad soft bands, not ink strokes
#   * big round eyes with a dark pupil, a tiny pink nose, freckle dots,
#     long thin whiskers
#
# He lies loaf style on the sill in three quarter view: head at the
# front right, body running back and to the left, paws tucked. The sun
# comes from the window on the right. Local units, ground at y = 0.

B_FUR = "#e48a46"
B_FUR_LIT = "#f6ad66"
B_FUR_DARK = "#b8592c"
B_DEEP = "#7a3220"
B_STRIPE = "#bd5c2b"
B_CREAM = "#f8dcb4"
B_CREAM_LIT = "#fff1dc"
B_PINK = "#eda08e"
B_NOSE = "#d8787a"
B_LINE = "#2c140d"
B_WHISKER = "#f7dfb0"
B_EYE = "#e2b544"
B_EYE_LIT = "#f6dc80"

BODY = (
    "M100 -6 "
    "L-150 -6 "
    "C-182 -8 -192 -56 -170 -90 "
    "C-146 -130 -76 -162 10 -156 "
    "C56 -152 108 -116 116 -66 "
    "C120 -36 114 -12 100 -6z"
)
TAIL_A = ((-136, -36), (-178, -36), (-198, -4), (-152, 3))
TAIL_B = ((-152, 3), (-106, 9), (-54, 10), (-22, -16))
HEAD_X, HEAD_Y, HEAD_S = 44, -104, 1.18

# head turned three quarters to the viewer's left: the right side is
# the near one, wider and lit; the left side narrower
TURN_C, SCALE_L, SCALE_R = -10, 0.78, 1.0

EXPR = {
    "fine":   dict(eyes={-1: ("open", .5), 1: ("open", .46)}, look=2, turned_ear=-1, brow=False, tilt=0, drop=0),
    "happy":  dict(eyes={-1: ("content", 0), 1: ("open", .62)}, look=3, turned_ear=-1, brow=True, tilt=5, drop=8),
    "bored":  dict(eyes={-1: ("open", .64), 1: ("open", .6)}, look=-4, turned_ear=-1, brow=False, tilt=3, drop=4),
    "hungry": dict(eyes={-1: ("open", .08), 1: ("open", .05)}, look=2, turned_ear=0, brow=True, tilt=-5, drop=-6),
    "asleep": dict(eyes={-1: ("shut", 0), 1: ("shut", 0)}, look=0, turned_ear=0, brow=False, tilt=8, drop=12),
}


def byte_defs():
    """Filters and gradients for Byte's soft, grainy painting."""
    return f"""
    <filter id="crayon" x="-10%" y="-10%" width="120%" height="120%">
      <feMorphology in="SourceGraphic" operator="dilate" radius="1" result="wide"/>
      <feGaussianBlur in="SourceGraphic" stdDeviation="1.1" result="soft"/>
      <feTurbulence type="fractalNoise" baseFrequency="1.1" numOctaves="2" seed="21" result="n"/>
      <feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  1 0 0 0 0" result="na"/>
      <feComposite in="soft" in2="na" operator="arithmetic" k2="3" k3="1" k4="-1.95" result="mask"/>
      <feComposite in="wide" in2="mask" operator="in"/>
    </filter>
    <filter id="crayon-soft" x="-20%" y="-20%" width="140%" height="140%">
      <feMorphology in="SourceGraphic" operator="dilate" radius="2" result="wide"/>
      <feGaussianBlur in="SourceGraphic" stdDeviation="5" result="soft"/>
      <feTurbulence type="fractalNoise" baseFrequency=".8" numOctaves="2" seed="33" result="n"/>
      <feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  1 0 0 0 0" result="na"/>
      <feComposite in="soft" in2="na" operator="arithmetic" k2="1.9" k3="1.1" k4="-1.45" result="mask"/>
      <feComposite in="wide" in2="mask" operator="in"/>
    </filter>
    <filter id="speckle" x="0" y="0" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency=".95" numOctaves="1" seed="5" result="n"/>
      <feColorMatrix in="n" type="matrix" values="0 0 0 0 .36  0 0 0 0 .13  0 0 0 0 .07  6 0 0 0 -3.4"/>
    </filter>
    <filter id="speckle-light" x="0" y="0" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="1" seed="13" result="n"/>
      <feColorMatrix in="n" type="matrix" values="0 0 0 0 1  0 0 0 0 .9  0 0 0 0 .74  6 0 0 0 -3.5"/>
    </filter>
    <filter id="line" x="-5%" y="-5%" width="110%" height="110%">
      <feTurbulence type="fractalNoise" baseFrequency=".7" numOctaves="1" seed="2" result="g"/>
      <feColorMatrix in="g" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  2.4 0 0 0 -.7" result="m"/>
      <feComposite in="SourceGraphic" in2="m" operator="in"/>
    </filter>
    <filter id="blurband" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="1.6"/></filter>
    <linearGradient id="b-body" x1=".85" y1="0" x2=".1" y2="1">
      <stop offset="0" stop-color="{B_FUR_LIT}"/>
      <stop offset=".45" stop-color="{B_FUR}"/>
      <stop offset="1" stop-color="{B_FUR_DARK}"/>
    </linearGradient>
    <linearGradient id="b-tail" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{B_FUR_DARK}"/>
      <stop offset=".45" stop-color="{B_FUR}"/>
      <stop offset=".85" stop-color="{B_FUR_DARK}"/>
      <stop offset="1" stop-color="{B_DEEP}"/>
    </linearGradient>
    <radialGradient id="b-head" cx=".66" cy=".3" r=".8">
      <stop offset="0" stop-color="{B_FUR_LIT}"/>
      <stop offset=".55" stop-color="{B_FUR}"/>
      <stop offset="1" stop-color="{B_FUR_DARK}"/>
    </radialGradient>
    <linearGradient id="b-cream" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{B_CREAM_LIT}"/>
      <stop offset="1" stop-color="{B_CREAM}"/>
    </linearGradient>
    <radialGradient id="b-iris" cx=".5" cy=".62" r=".6">
      <stop offset="0" stop-color="{B_EYE_LIT}"/>
      <stop offset=".75" stop-color="{B_EYE}"/>
      <stop offset="1" stop-color="#b9862a"/>
    </radialGradient>
    """


def T(p):
    x, y = p
    return (round(TURN_C + x * (SCALE_L if x < 0 else SCALE_R), 2), y)


def TP(*pts):
    return [T(p) for p in pts]


def smooth(points, k=0.18, closed=True):
    """A soft path through points: every edge bows a little outward."""
    q = points
    d = [f"M{q[0][0]:.1f} {q[0][1]:.1f}"]
    n = len(q) if closed else len(q) - 1
    for i in range(n):
        p0, p1 = q[i], q[(i + 1) % len(q)]
        mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
        dx, dy = p1[0] - p0[0], p1[1] - p0[1]
        kk = k[i] if isinstance(k, (list, tuple)) else k
        d.append(f"Q{mx + dy * kk:.1f} {my - dx * kk:.1f} {p1[0]:.1f} {p1[1]:.1f}")
    return " ".join(d) + ("z" if closed else "")


def hair(p0, p1, p2, w=1.3, color=B_LINE, opacity=0.85):
    """A thin, grainy pencil hair line."""
    return f'<g filter="url(#line)">{stroke(p0, p1, p2, w, color, opacity)}</g>'


# ---- head

def head_shape():
    """Wide cheeks with three soft tufts each, a flat crown, small chin."""
    right = [(0, -62), (30, -63), (56, -54), (70, -34), (80, -10), (86, 8), (92, 18), (84, 22),
             (88, 30), (78, 33), (78, 42), (64, 46), (46, 56), (22, 62), (0, 63)]
    bends = [0.05, 0.08, 0.1, 0.08, 0.1, 0.06, 0.04, 0.02, 0.04, 0.02, 0.04, 0.08, 0.1, 0.06]
    left = [(-x, y) for x, y in reversed(right[1:-1])]
    pts = TP(*(right + left))
    return smooth(pts, bends + [0.06] + bends[::-1][:len(left)])


def b_ear(side, mood):
    e = EXPR[mood]
    m = (lambda p: (side * p[0], p[1]))
    shape = TP(m((14, -58)), m((44, -96)), m((60, -114)), m((66, -88)), m((68, -40)))
    inner = TP(m((24, -58)), m((48, -92)), m((58, -104)), m((60, -82)), m((60, -46)))
    near = side > 0
    turned = e["turned_ear"] == side
    pivot = T(m((42, -48)))
    if turned:
        xf = f"rotate({-24 * side} {pivot[0]} {pivot[1]}) translate({pivot[0]} 0) scale(.7 1) translate({-pivot[0]} 0)"
    else:
        xf = f"rotate({3 * side} {pivot[0]} {pivot[1]})"
    hairs = "".join(
        hair(T(m((40 + k, -54))), T(m((44 + k, -70))), T(m((48 + k * 0.6, -88))), 1.1, B_DEEP, .55)
        for k in (0, 6, 12)
    )
    fur = "url(#b-head)" if near else B_FUR_DARK
    rim = (stroke(T(m((58, -110))), T(m((66, -80))), T(m((68, -42))), 3, LIGHT_EDGE, .75, taper=(0.5, 1))
           if near else hair(T(m((60, -112))), T(m((66, -80))), T(m((68, -42))), 1.4, B_LINE, .7))
    listen = ' class="ear-listen"' if turned else ""
    return f"""
      <g transform="{xf}"><g{listen}>
        <g filter="url(#crayon)">
          <path d="{smooth(shape, [0.02, 0.08, 0.1, 0.04, 0])}" fill="{fur}"/>
          <path d="{smooth(inner, [0.02, 0.08, 0.1, 0.04, 0])}" fill="{B_PINK}" opacity="{.45 if turned else .95}"/>
        </g>
        {hairs if not turned else ""}
        {rim}
      </g></g>"""


def b_eye(side, mood, uid):
    """A big round eye. The upper lid is a curved line across it; only
    the part below the lid is painted, so the lid is the face's fur."""
    e = EXPR[mood]
    kind, lid = e["eyes"][side]
    r = 18
    cx, cy = T((side * 34, -12))
    sx = SCALE_L if side < 0 else SCALE_R
    near = side > 0
    g = f'transform="translate({cx} {cy}) scale({sx} 1)"'
    if kind == "content":
        return f"""<g {g}>{hair((-r * 0.9, 3), (0, -9), (r * 0.9, 2), 3, B_LINE, .95)}
          {hair((-r * 0.5, 7), (0, 6), (r * 0.5, 6.5), 1, B_LINE, .35)}</g>"""
    if kind == "shut":
        return f"""<g {g}>{hair((-r, -1), (0, 7), (r, -2), 2.8, B_LINE, .95)}
          {hair((-r * 0.5, 8), (0, 10), (r * 0.6, 7), 1, B_LINE, .3)}</g>"""
    lid_y = -r + 2 * r * lid               # height of the lid line at the centre
    tilt = 3                               # the lid sinks a touch towards the outer corner
    name = f"bey{'N' if near else 'F'}{uid}"
    look = e["look"]
    below = f"M{-r - 6} {lid_y - tilt} Q0 {lid_y - 2.5} {r + 6} {lid_y + tilt} L{r + 6} {r + 6} L{-r - 6} {r + 6}z"
    pupil = r * (0.58 if mood != "hungry" else 0.66)
    lid_light = (stroke((-r * 0.6, lid_y - 7), (0, lid_y - 9.5), (r * 0.7, lid_y - 5), 3, LIGHT_EDGE, .65)
                 if near and lid > 0.2 else "")
    return f"""
      <g {g}>
        {lid_light}
        <clipPath id="{name}c"><circle r="{r}"/></clipPath>
        <clipPath id="{name}l"><path d="{below}"/></clipPath>
        <g class="blink">
          <g clip-path="url(#{name}c)"><g clip-path="url(#{name}l)">
            <circle r="{r}" fill="url(#b-iris)"/>
            <circle cx="{look}" cy="1.5" r="{pupil}" fill="#2a130c"/>
            <circle cx="{look + 4.5}" cy="{max(lid_y + 4.5, -4)}" r="2.6" fill="#fffaf0"/>
            <circle cx="{look - 4}" cy="7" r="1.2" fill="#fffaf0" opacity=".7"/>
            <path d="M{-r} {lid_y + 1} Q0 {lid_y + 4} {r} {lid_y + 3}" stroke="#000" stroke-opacity=".25" stroke-width="5" fill="none"/>
            <circle r="{r}" fill="none" stroke="{B_LINE}" stroke-width="1.6" opacity=".8"/>
          </g></g>
          {hair((-r - 1.5, lid_y - tilt + 1), (0, lid_y - 3), (r + 2, lid_y + tilt), 2.8, B_LINE, .95)}
        </g>
      </g>"""


def b_face(mood):
    out = []
    n = T((0, 0))[0]
    # tiny pink nose with a darker underside
    out.append(f'<path d="M{n - 6} 12 Q{n + 1} 8.5 {n + 8} 12 Q{n + 6} 17 {n + 1} 20 Q{n - 4} 17 {n - 6} 12z" fill="{B_NOSE}"/>')
    out.append(f'<path d="M{n - 1} 18 Q{n + 1} 20 {n + 3} 18" stroke="#9a4a4c" stroke-width="1.6" fill="none"/>')
    out.append(f'<ellipse cx="{n + 2}" cy="11.8" rx="2.2" ry="1" fill="#f6c0b0"/>')
    mouth = {
        "hungry": f'<path d="M{n - 7} 27 Q{n + 1} 24 {n + 9} 27 Q{n + 5} 37 {n + 1} 37 Q{n - 3} 37 {n - 7} 27z" fill="#6a2422"/>'
                  f'<path d="M{n - 2} 35 Q{n + 1} 32 {n + 4} 35z" fill="#d07070"/>',
        "happy": "",
        "bored": "",
    }.get(mood, "")
    out.append(mouth)
    out.append(hair((n + 1, 20), (n + 1, 23), (n + 1, 25.5), 1.2, "#6a2c2a", .9))
    if mood == "bored":
        out.append(hair((n - 7, 28), (n + 1, 27), (n + 10, 28.5), 1.3, "#6a2c2a", .85))
    elif mood == "hungry":
        out.append(hair((n - 9, 27), (n + 1, 23), (n + 11, 27), 1.4, "#6a2c2a", .9))
    else:
        lift = 3 if mood == "happy" else 1
        out.append(hair((n - 8, 27), (n - 3.5, 30.5), (n + 1, 25.5), 1.3, "#6a2c2a", .9))
        out.append(hair((n + 1, 25.5), (n + 6, 31), (n + 12, 26 - lift), 1.4, "#6a2c2a", .9))
    # freckle dots on the muzzle, as in the references
    for dx, dy in [(13, 27), (19, 30.5), (13.5, 34), (-13, 27), (-19, 30.5), (-13.5, 34)]:
        p = T((dx, dy))
        out.append(f'<circle cx="{p[0]}" cy="{p[1]}" r="1.4" fill="{B_FUR_DARK}" opacity=".75"/>')
    # whiskers: long, thin, slightly curved; each one different
    for (sx_, sy), ln, ang, sag, op in [((22, 26), 88, -6, 6, .85), ((24, 30), 104, 4, 12, .8),
                                        ((22, 34), 86, 13, 14, .65), ((18, 37), 62, 24, 8, .5)]:
        a = T((sx_, sy))
        rr = math.radians(ang)
        c = (a[0] + ln * math.cos(rr), a[1] + ln * math.sin(rr) + sag)
        b = ((a[0] + c[0]) / 2, (a[1] + c[1]) / 2 - sag * 0.9)
        out.append(stroke(a, b, c, 1.15, B_WHISKER, op, taper=(0.15, 1)))
    for (sx_, sy), ln, ang, sag, op in [((-18, 27), 56, 188, 6, .55), ((-19, 32), 48, 174, 9, .45)]:
        a = T((sx_, sy))
        rr = math.radians(ang)
        c = (a[0] + ln * math.cos(rr), a[1] + ln * math.sin(rr) + sag)
        b = ((a[0] + c[0]) / 2, (a[1] + c[1]) / 2 - sag)
        out.append(stroke(a, b, c, 1, B_WHISKER, op, taper=(0.15, 1)))
    return "".join(out)


def b_head(mood, uid):
    e = EXPR[mood]
    hd = head_shape()
    out = [b_ear(-1, mood), b_ear(1, mood)]
    out.append(f'<clipPath id="bhc{uid}"><path d="{hd}"/></clipPath>')
    lower = smooth(TP((-40, 22), (-22, 14), (-6, 14), (8, 13), (26, 14), (46, 18), (60, 30),
                      (54, 46), (30, 58), (0, 64), (-30, 58), (-46, 42)), 0.12)
    body = f"""
        <path d="{hd}" fill="url(#b-head)"/>
        <g clip-path="url(#bhc{uid})">
          <path d="{smooth(TP((-120, -80), (-30, -70), (-22, -20), (-30, 30), (-60, 80), (-130, 80)), 0.12)}" fill="{B_FUR_DARK}" opacity=".45" filter="url(#haze)"/>
          <path d="{lower}" fill="{B_CREAM}" opacity=".95" filter="url(#crayon-soft)"/>
          <path d="{smooth(TP((6, 16), (24, 16), (38, 24), (34, 36), (16, 40), (4, 32)), 0.15)}" fill="{B_CREAM_LIT}" opacity=".7" filter="url(#crayon-soft)"/>
          <g filter="url(#blurband)" opacity=".9">
            {stroke(T((-12, -63)), T((-11, -54)), T((-9, -42)), 7, B_STRIPE, 1, taper=(0.1, 1))}
            {stroke(T((2, -64)), T((3, -52)), T((3, -38)), 8, B_STRIPE, 1, taper=(0.1, 1))}
            {stroke(T((16, -63)), T((15, -54)), T((13, -42)), 7, B_STRIPE, 1, taper=(0.1, 1))}
            {stroke(T((48, -10)), T((66, -6)), T((86, -14)), 7, B_STRIPE, .8)}
            {stroke(T((-50, -8)), T((-64, -4)), T((-80, -10)), 6, B_STRIPE, .7)}
          </g>
        </g>"""
    out.append(f'<g filter="url(#crayon)">{body}</g>')
    out.append(f'<rect x="-140" y="-80" width="280" height="160" filter="url(#speckle)" opacity=".22" clip-path="url(#bhc{uid})"/>')
    # lines only where the head overlaps something: the chin over the
    # chest, the far cheek over the back
    out.append(hair(T((-46, 56)), T((-4, 70)), T((48, 56)), 2.2, B_LINE, .75))
    out.append(hair(T((-88, 34)), T((-76, 48)), T((-56, 54)), 1.6, B_LINE, .6))
    out.append(hair(T((-70, -30)), T((-84, -4)), T((-92, 14)), 1.3, B_LINE, .45))
    out.append(b_eye(-1, mood, uid))
    out.append(b_eye(1, mood, uid))
    if e["brow"]:
        a = T((38, -32))
        out.append(stroke(a, (a[0] + 26, a[1] - 22), (a[0] + 64, a[1] - 26), 1.1, B_WHISKER, .85, taper=(0.15, 1)))
        out.append(stroke((a[0] + 6, a[1] + 3), (a[0] + 32, a[1] - 12), (a[0] + 62, a[1] - 8), 1, B_WHISKER, .6, taper=(0.15, 1)))
    out.append(b_face(mood))
    return "".join(out)


# ---- body

def b_tail():
    """The tail leaves the hip from behind the rump and curls along the
    front of the body. Its start fades into the fur through a feathered
    mask, so there is no cut where it emerges."""
    pts, ws = [], []
    for seg, w0, w1, n in [(TAIL_A, 26, 24, 14), (TAIL_B, 24, 15, 20)]:
        for i in range(n + (seg is TAIL_B)):
            t = i / n
            pts.append(_cubic(*seg, t))
            ws.append(w0 * (1 - t) + w1 * t)
    for k, f in zip(range(1, 7), (0.35, 0.6, 0.76, 0.87, 0.94, 0.98)):
        ws[-k] *= f
    d = _ribbon(pts, ws)

    def edge(i, side):
        (x, y), (x2, y2) = pts[i], pts[min(i + 1, len(pts) - 1)]
        if i == len(pts) - 1:
            (x, y), (x2, y2) = pts[i - 1], pts[i]
        ang = math.atan2(y2 - y, x2 - x) + math.pi / 2
        h = ws[i] / 2 * side
        return (pts[i][0] + math.cos(ang) * h, pts[i][1] + math.sin(ang) * h)

    # soft bands that wrap round the tail
    rings = "".join(
        stroke(edge(i, -1), ((edge(i, -1)[0] + edge(i, 1)[0]) / 2 + 4, (edge(i, -1)[1] + edge(i, 1)[1]) / 2),
               edge(i, 1), 9, B_STRIPE, .75, taper=(0.2, 0.2))
        for i in (10, 17, 23, 28)
    )
    under = "".join(stroke(edge(a, 1), edge((a + b) // 2, 1), edge(b, 1), 6, B_FUR_DARK, .7)
                    for a, b in [(6, 16), (16, 26), (26, 33)])
    top_light = stroke(edge(16, -1), edge(24, -1), edge(32, -1), 4, B_FUR_LIT, .7)
    # the kesisim line: where the tail lies in front of the body
    overlap = hair(edge(15, -1), edge(22, -1), edge(30, -1), 1.5, B_LINE, .6)
    return f"""
    <clipPath id="tailbody"><path d="{BODY}"/></clipPath>
    <filter id="tailfeather" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="2.4"/></filter>
    <linearGradient id="b-tailfur" x1="-200" y1="0" x2="-20" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{B_FUR_DARK}"/>
      <stop offset=".3" stop-color="{B_FUR}"/>
      <stop offset=".75" stop-color="{B_FUR}"/>
      <stop offset="1" stop-color="{B_FUR_DARK}"/>
    </linearGradient>
    <mask id="tailmask" maskUnits="userSpaceOnUse" x="-260" y="-200" width="420" height="240">
      <rect x="-260" y="-200" width="420" height="240" fill="#fff"/>
      <!-- hidden: the part inside the body that is not in front of it -->
      <g filter="url(#tailfeather)"><g clip-path="url(#tailbody)">
        <rect x="-260" y="-200" width="160" height="186" fill="#000"/>
      </g></g>
    </mask>
    <g class="tail" mask="url(#tailmask)">
      <g filter="url(#crayon)">
        <path d="{d}" fill="url(#b-tailfur)"/>
        <clipPath id="tailclip"><path d="{d}"/></clipPath>
        <g clip-path="url(#tailclip)"><g filter="url(#blurband)">{under}{rings}{top_light}</g></g>
      </g>
      {overlap}
    </g>"""


def b_body(uid):
    stripes = "".join(
        stroke((x, y + 2), (x + dx * 0.4 - 6, y + ln * 0.55), (x + dx, y + ln), w, B_STRIPE, .85, taper=(0.3, 1))
        for x, y, dx, ln, w in [(-14, -156, -4, 52, 15), (-50, -149, -9, 56, 15), (-86, -136, -13, 54, 14),
                                (-118, -118, -14, 46, 13), (-146, -96, -12, 38, 11)]
    ) + stroke((-150, -60), (-132, -70), (-112, -64), 10, B_STRIPE, .7) + stroke((-140, -36), (-122, -44), (-102, -38), 9, B_STRIPE, .6)
    bib = smooth([(28, -84), (60, -100), (98, -96), (120, -66), (122, -36), (112, -14), (90, -8),
                  (60, -8), (38, -18), (26, -44)], 0.12)
    thigh_shade = smooth([(-172, -92), (-150, -100), (-118, -86), (-100, -50), (-104, -8), (-152, -6), (-184, -30)], 0.1)
    return f"""
      <clipPath id="bbody{uid}"><path d="{BODY}"/></clipPath>
      <g class="breathe">
        <g filter="url(#crayon)">
          <path d="{BODY}" fill="url(#b-body)"/>
          <g clip-path="url(#bbody{uid})">
            <path d="{thigh_shade}" fill="{B_FUR_DARK}" opacity=".5" filter="url(#haze)"/>
            <path d="M-170 -20 C-80 -30 40 -30 120 -20 L120 10 L-170 10z" fill="{B_DEEP}" opacity=".35" filter="url(#haze)"/>
            <g filter="url(#blurband)">{stripes}</g>
            <path d="{bib}" fill="url(#b-cream)" filter="url(#crayon-soft)"/>
          </g>
        </g>
        <rect x="-200" y="-170" width="330" height="170" filter="url(#speckle)" opacity=".4" clip-path="url(#bbody{uid})"/>
        {stroke((-160, -100), (-86, -164), (10, -158), 3, LIGHT_EDGE, .55, taper=(1, 0.7), n=26)}
        {hair((-104, -10), (-104, -40), (-116, -62), 1.4, B_LINE, .45)}
        {hair((-182, -40), (-184, -18), (-160, -7), 1.6, B_LINE, .5)}
        <g filter="url(#crayon)">
          <path d="{smooth([(48, -4), (52, -20), (72, -26), (96, -22), (110, -12), (108, -3)], 0.12)}" fill="url(#b-cream)"/>
        </g>
        {hair((48, -4), (60, -1), (108, -3), 1.8, B_LINE, .7)}
        {hair((74, -5), (75, -11), (76, -16), 1.2, B_LINE, .65)}
        {hair((89, -5), (90, -11), (91, -16), 1.2, B_LINE, .65)}
      </g>
      {b_tail()}"""


def byte(mood, x, y, s=1.0, uid="", with_body=True):
    """Byte at (x, y), ground under the paws, scale s."""
    e = EXPR[mood]
    parts = [b_body(uid)] if with_body else []
    if with_body:
        # the head sits on the body: a soft occlusion shadow where they meet
        parts.append(f'<g clip-path="url(#bbody{uid})"><ellipse cx="{HEAD_X - 40}" cy="{HEAD_Y + e["drop"] + 10}" rx="70" ry="78" '
                     f'fill="{B_DEEP}" opacity=".45" filter="url(#haze)"/></g>')
    parts.append(
        f'<g transform="translate({HEAD_X} {HEAD_Y + e["drop"]}) rotate({e["tilt"]}) scale({HEAD_S})">{b_head(mood, uid)}</g>'
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

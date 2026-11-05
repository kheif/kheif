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


# head, built straight on and symmetric, then turned three quarters to
# the viewer's left: the right cheek is the near one and catches the
# window light, the left one is narrower and falls into shadow.
TURN_C, SCALE_L, SCALE_R = -12, 0.74, 1.0

SHADOW_RED = "#8a4030"     # the far cheek, red brown
LIGHT_EDGE = "#ffd9a0"     # where the low sun touches an edge

# Byte's expressions. Each eye can be: half (heavy lidded), slit (one
# eye just cracked open), wide, content (squeezed shut, arched), shut.
EXPR = {
    "fine":   dict(eyes={-1: ("half", .55), 1: ("half", .52)}, look=2, turned_ear=-1, brow=False, tilt=0, drop=0),
    "happy":  dict(eyes={-1: ("content", 0), 1: ("slit", .8)}, look=3.5, turned_ear=-1, brow=True, tilt=5, drop=8),
    "bored":  dict(eyes={-1: ("half", .7), 1: ("half", .68)}, look=-4, turned_ear=-1, brow=False, tilt=3, drop=4),
    "hungry": dict(eyes={-1: ("wide", .15), 1: ("wide", .12)}, look=2.5, turned_ear=0, brow=True, tilt=-5, drop=-6),
    "asleep": dict(eyes={-1: ("shut", 0), 1: ("shut", 0)}, look=0, turned_ear=0, brow=False, tilt=8, drop=12),
}


def T(p):
    x, y = p
    return (round(TURN_C + x * (SCALE_L if x < 0 else SCALE_R), 2), y)


def TP(*pts):
    return [T(p) for p in pts]


def head_outline():
    """Soft head: rounded crown, cheek fluff in a few tufts, small chin."""
    crown = (0, -60)
    right = [
        ((30, -60), (56, -50), (66, -30)),    # crown to cheek top
        ((74, -16), (80, -2), (80, 6)),       # upper cheek
        ((86, 12), (92, 16), (90, 19)),       # tuft 1
        ((84, 21), (86, 27), (87, 31)),
        ((79, 35), (77, 38), (70, 40)),       # tuft 2
        ((58, 52), (30, 59), (0, 59)),        # jaw to chin
    ]
    d = [f"M{T(crown)[0]} {crown[1]}"]
    for c1, c2, e in right:
        a, b, c = T(c1), T(c2), T(e)
        d.append(f"C{a[0]} {a[1]} {b[0]} {b[1]} {c[0]} {c[1]}")
    pts = [crown] + [seg[2] for seg in right]
    for i in range(len(right) - 1, -1, -1):
        c1, c2, e = right[i]
        start = pts[i]
        m = lambda p: (-p[0], p[1])  # noqa: E731
        a, b, c = T(m(c2)), T(m(c1)), T(m(start))
        d.append(f"C{a[0]} {a[1]} {b[0]} {b[1]} {c[0]} {c[1]}")
    return " ".join(d) + "z"


def ear(side, mood, uid):
    """side 1 is the near ear, lit by the window; side -1 the far one.

    The turned ear swings outward towards a sound and shows more of its
    back, so it gets narrower and darker.
    """
    e = EXPR[mood]
    m = (lambda p: (side * p[0], p[1]))
    base_in, tip, base_out = m((20, -56)), m((50, -94)), m((66, -32))
    pts = [T(base_in), T(m((45, -89))), T(m((54, -89))), T(base_out)]
    d = (f"M{pts[0][0]} {pts[0][1]} Q{T(m((30, -76)))[0]} -76 {pts[1][0]} {pts[1][1]} "
         f"Q{T(tip)[0]} {tip[1] - 4} {pts[2][0]} {pts[2][1]} "
         f"Q{T(m((64, -64)))[0]} -64 {pts[3][0]} {pts[3][1]}z")
    inner = (f"M{T(m((27, -56)))[0]} -56 Q{T(m((34, -74)))[0]} -74 {T(m((48, -85)))[0]} -85 "
             f"Q{T(m((56, -66)))[0]} -66 {T(m((57, -42)))[0]} -42z")
    near = side > 0
    turned = e["turned_ear"] == side
    pivot = T(m((44, -46)))
    if turned:
        xf = f"rotate({-26 * side} {pivot[0]} {pivot[1]}) translate({pivot[0]} 0) scale(.72 1) translate({-pivot[0]} 0)"
    else:
        xf = f"rotate({4 * side if near else 0} {pivot[0]} {pivot[1]})"
    if near:
        body = f"""
        <g filter="url(#gouache)"><path d="{d}" fill="{FUR_LIT}"/><path d="{inner}" fill="#eaa58c"/></g>
        <path d="{inner}" fill="#ffc9a8" opacity=".45" filter="url(#softedge)"/>
        {stroke(T(m((40, -48))), T(m((43, -64))), T(m((45, -78))), 2, CREAM, .8)}
        {stroke(T(m((48, -48))), T(m((50, -62))), T(m((49, -74))), 1.6, CREAM, .7)}
        {stroke(T(m((54, -86))), T(m((62, -60))), T(m((66, -34))), 2.6, LIGHT_EDGE, .9, taper=(0.6, 1))}
        <path d="{d}" stroke="{INK}" stroke-width="1.3" fill="none" opacity=".8"/>"""
    else:
        body = f"""
        <g filter="url(#gouache)"><path d="{d}" fill="{FUR_SHADE}"/><path d="{inner}" fill="{EAR}" opacity="{.35 if turned else .8}"/></g>
        {stroke(T(m((40, -48))), T(m((42, -62))), T(m((44, -75))), 1.8, CREAM, .4)}
        <path d="{d}" stroke="{INK}" stroke-width="1.7" fill="none" opacity=".85"/>
        {stroke(T(m((48, -90))), T(m((58, -64))), T(m((66, -34))), 2.8, INK, .55)}"""
    listen = ' class="ear-listen"' if turned else ""
    return f'<g transform="{xf}"><g{listen}>{body}</g></g>'


def eye(side, mood, uid):
    """One eye in its own little coordinate system, so the lid can slide
    down without changing shape. side 1 is the near (lit) eye."""
    e = EXPR[mood]
    kind, lid = e["eyes"][side]
    cx, cy = T((side * 30, -8))
    sx = SCALE_L if side < 0 else SCALE_R
    w, h = 17, 11.5
    near = side > 0
    g = f'transform="translate({cx} {cy}) rotate({side * 4}) scale({sx * side} 1)"'
    ink = 1 if near else 0.85

    if kind == "content":
        return f"""
      <g {g}>
        {stroke((-w * 0.9, 3), (0, -8), (w * 0.9, 1), 3.2 * ink, INK)}
        {stroke((-w * 0.55, 6), (0, 4.5), (w * 0.5, 5), 1, INK, .3)}
      </g>"""
    if kind == "shut":
        return f"""
      <g {g}>
        {stroke((-w, -1), (0, 7), (w, -2), 3 * ink, INK)}
        {stroke((-w * 0.5, 7), (0, 10), (w * 0.6, 6), 1, INK, .3)}
      </g>"""

    # Only the opening between the lid line and the lower lid is drawn;
    # the lid itself is the face's own fur, so it shares its light.
    look = e["look"] * side
    pupil_r = 3.4 if kind == "wide" else (2.3 if kind == "slit" else 2.6)
    top_y = -h * 1.45 * (1 - lid) + h * 0.55 * lid     # lid curve control
    lower = f"Q{w * 0.15} {h * 1.05} {-w} 0"
    opening = f"M{-w} 0 Q{-w * 0.1} {top_y:.1f} {w} {-h * 0.2} {lower}z"
    name = f"eye{'N' if near else 'F'}{uid}"
    fold = stroke((-w * 0.8, -h * 0.95), (-w * 0.1, -h * 1.8), (w * 0.85, -h * 1.05), 1.3,
                  FUR_DEEP if near else INK, .45 if near else .35)
    lid_light = (stroke((-w * 0.55, top_y * 0.5 - 4), (0, top_y * 0.62 - 6), (w * 0.7, top_y * 0.45 - 5), 3.2, LIGHT_EDGE, .75)
                 if near else "")
    return f"""
      <g {g}>
        {fold}
        {lid_light}
        <g class="blink">
          <clipPath id="{name}"><path d="{opening}"/></clipPath>
          <path d="{opening}" fill="url(#iris)"/>
          <g clip-path="url(#{name})">
            <ellipse cx="{look}" cy="2.5" rx="{pupil_r}" ry="{pupil_r * 2.1}" fill="#24130c"/>
            <circle cx="{look + 2.6 * side}" cy="{0.5 if kind == 'slit' else -2.5}" r="1.5" fill="#fffaf0"/>
            <path d="M{-w} {top_y * 0.5} Q0 {top_y * 0.5 + 3} {w} {top_y * 0.5 - 2}" stroke="#000" stroke-opacity=".28" stroke-width="5" fill="none"/>
          </g>
          {stroke((-w - 3, 0.5), (-w * 0.1, top_y + 1.5), (w + 3, -h * 0.25), 3.4 * ink, INK, taper=(0.7, 0.35))}
        </g>
        {stroke((-w * 0.95, 0.8), (w * 0.15, h * 1.05), (w, -h * 0.15), 1.4, INK, .7, taper=(1, 0.6))}
      </g>"""


def face(mood, uid):
    """Muzzle, nose, mouth and whiskers. Nothing here is mirrored: the
    near side is wider and lit, the far side short and in shadow."""
    out = []
    # one matte cream field that grows out of the cheeks: tufted where it
    # meets the orange fur, wider on the near side, no separate pads
    edge = [(-10, 13), (-20, 17), (-28, 24), (-34, 31), (-27, 34), (-26, 43), (-14, 50), (0, 55),
            (18, 54), (32, 50), (38, 44), (46, 40), (40, 34), (46, 27), (36, 22), (26, 16), (14, 13), (6, 12)]
    q = TP(*edge)
    parts = [f"M{q[0][0]} {q[0][1]}"]
    for i in range(len(q)):
        p0, p1 = q[i], q[(i + 1) % len(q)]
        # bow every edge a little outward, more on the long smooth ones
        mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
        dx, dy = p1[0] - p0[0], p1[1] - p0[1]
        k = 0.18 if i % 2 else 0.05
        parts.append(f"Q{mx + dy * k:.1f} {my - dx * k:.1f} {p1[0]} {p1[1]}")
    muzzle = " ".join(parts) + "z"
    core = TP((4, 16), (18, 15), (30, 20), (34, 30), (28, 38), (14, 41), (5, 35), (2, 25))
    core_d = "M" + " L".join(f"{x} {y}" for x, y in core) + "z"
    out.append(f'<g filter="url(#gouache)"><path d="{muzzle}" fill="{CREAM_MID}"/><path d="{core_d}" fill="{CREAM}" opacity=".9"/></g>')
    out.append(f'<path d="{core_d}" fill="{CREAM}" opacity=".5" filter="url(#softedge)"/>')
    # cream fur running back along the near cheek, following its form
    for a, b, c, op in [((46, 30), (60, 26), (74, 16), .7), ((44, 40), (58, 40), (72, 32), .6),
                        ((20, 52), (34, 56), (50, 50), .5)]:
        out.append(stroke(T(a), T(b), T(c), 2.4, CREAM, op))
    # whisker roots, near side only
    for dx, dy in [(16, 22), (22, 27), (17, 31), (28, 24)]:
        p = T((dx, dy))
        out.append(f'<circle cx="{p[0]}" cy="{p[1]}" r=".9" fill="{CREAM_SHADE}"/>')

    # nose: small, warm, its top catching the light
    n = T((0, 0))[0]
    out.append(f'<path d="M{n - 5} 10 Q{n + 1} 7.5 {n + 7} 10 Q{n + 6} 15 {n + 1} 18 Q{n - 4} 15 {n - 5} 10z" fill="{NOSE}"/>')
    out.append(f'<path d="M{n - 2} 9.6 Q{n + 2} 8.4 {n + 5} 9.8" stroke="#f3b19e" stroke-width="1.6" fill="none" stroke-linecap="round"/>')
    out.append(stroke((n + 1, 18), (n + 1, 21), (n, 24.5), 1.3, INK, .8))

    if mood == "hungry":
        out.append(f'<path d="M{n - 6} 26 Q{n + 1} 24 {n + 9} 26 Q{n + 5} 35 {n + 1} 35 Q{n - 3} 35 {n - 6} 26z" fill="#5a2018"/>')
        out.append(f'<path d="M{n - 2} 33 Q{n + 1} 30 {n + 4} 33z" fill="#c26658"/>')
        out.append(stroke((n - 8, 26), (n + 1, 23), (n + 11, 26), 1.6, INK, .85))
    elif mood == "happy":
        # content: the near corner curls up, the far one barely moves
        out.append(stroke((n - 6, 26), (n - 3, 28.5), (n, 25), 1.4, INK, .8))
        out.append(stroke((n, 25), (n + 7, 31), (n + 14, 24), 1.6, INK, .9, taper=(0.6, 1)))
    elif mood == "bored":
        out.append(stroke((n - 6, 27), (n + 2, 26), (n + 11, 27.5), 1.4, INK, .8))
    else:
        out.append(stroke((n - 6, 26), (n - 3, 28.5), (n, 25), 1.4, INK, .8))
        out.append(stroke((n, 25), (n + 6, 29), (n + 12, 25.5), 1.5, INK, .85))

    # whiskers: a handful of curved hairs, each with its own length and
    # angle; the far ones are short and mostly hidden by the muzzle
    near = [((18, 22), 78, -8, 7, .8), ((20, 26), 96, 2, 12, .75), ((19, 30), 84, 10, 16, .6), ((16, 33), 60, 18, 10, .45)]
    for (sx, sy), ln, ang, sag, op in near:
        a = T((sx, sy))
        r = math.radians(ang)
        c = (a[0] + ln * math.cos(r), a[1] + ln * math.sin(r) + sag)
        b = ((a[0] + c[0]) / 2, (a[1] + c[1]) / 2 - sag * 0.9)
        out.append(stroke(a, b, c, 1.25, CREAM, op, taper=(0.2, 1)))
    for (sx, sy), ln, ang, sag, op in [((-16, 23), 44, 186, 4, .5), ((-17, 28), 36, 172, 7, .4)]:
        a = T((sx, sy))
        r = math.radians(ang)
        c = (a[0] + ln * math.cos(r), a[1] + ln * math.sin(r) + sag)
        b = ((a[0] + c[0]) / 2, (a[1] + c[1]) / 2 - sag)
        out.append(stroke(a, b, c, 1.05, CREAM, op, taper=(0.2, 1)))
    return "".join(out)


def far_shade():
    """The far cheek's shadow. Its edge bends round the brow, dips into
    the eye socket beside the nose and follows the muzzle down."""
    pts = [(-110, -70), (-36, -66), (-4, -56), (-10, -34), (-24, -22), (-10, -6), (-2, 6), (-12, 16),
           (-26, 30), (-36, 50), (-44, 62), (-50, 70)]
    q = TP(*pts)
    d = f"M{q[0][0]} {q[0][1]} L{q[1][0]} {q[1][1]}"
    for i in range(2, len(q) - 1, 2):
        c, e = q[i], q[i + 1]
        d += f" Q{c[0]} {c[1]} {e[0]} {e[1]}"
    d += f" L{T((-120, 70))[0]} 70"
    return d + f" L{q[-1][0]} {q[-1][1]}z"


def head(mood, uid):
    e = EXPR[mood]
    outline = head_outline()
    out = [ear(-1, mood, uid), ear(1, mood, uid)]
    out.append(f'<clipPath id="headclip{uid}"><path d="{outline}"/></clipPath>')
    far = TP((-120, -80), (-6, -80), (-2, -40), (-6, 12), (-12, 40), (-20, 70), (-120, 70))
    out.append(f'<clipPath id="farside{uid}"><path d="M' + " L".join(f"{x} {y}" for x, y in far) + 'z"/></clipPath>')
    out.append(f'<g filter="url(#gouache)"><path d="{outline}" fill="{FUR}"/></g>')
    out.append(f'<g clip-path="url(#headclip{uid})">')
    # near side in the window light
    out.append(f'<path d="M{T((0, -70))[0]} -70 C{T((50, -68))[0]} -66 {T((96, -30))[0]} -30 {T((92, 22))[0]} 22 '
               f'C{T((70, 4))[0]} 2 {T((30, -20))[0]} -24 {T((6, -36))[0]} -36z" fill="{FUR_LIT}" opacity=".85" filter="url(#softedge)"/>')
    # far cheek in red brown shade, cut along the nose bridge
    out.append(f'<path d="{far_shade()}" fill="{SHADOW_RED}" opacity=".78" filter="url(#shade)"/>')
    # under the jaw, where the head meets the chest
    out.append(f'<path d="M{T((-70, 36))[0]} 36 C{T((-30, 54))[0]} 52 {T((40, 54))[0]} 52 {T((80, 34))[0]} 34 L{T((80, 70))[0]} 70 L{T((-70, 70))[0]} 70z" fill="{FUR_DEEP}" opacity=".5" filter="url(#softedge)"/>')
    # forehead M and three crown lines: Byte's signature
    for x0, top, ln, w in [(-9, -60, 22, 4.4), (0, -62, 28, 5), (10, -60, 22, 4.6)]:
        a, c = T((x0, top)), T((x0 * 0.7, top + ln))
        out.append(stroke(a, ((a[0] + c[0]) / 2 + 0.5, (top + top + ln) / 2), c, w, STRIPE, .9, taper=(0.3, 1)))
    for side in (-1, 1):
        col = STRIPE if side > 0 else FUR_DEEP
        out.append(stroke(T((side * 6, -34)), T((side * 14, -26)), T((side * 22, -34)), 3.2, col, .8))
        out.append(stroke(T((side * 22, -34)), T((side * 30, -42)), T((side * 38, -30)), 3.2, col, .8))
    # cheek bands curving back around the near cheek; one on the far side
    out.append(stroke(T((46, -4)), T((62, 0)), T((80, -8)), 4.4, STRIPE, .75))
    out.append(stroke(T((50, 10)), T((66, 14)), T((84, 8)), 3.8, STRIPE, .6))
    out.append(stroke(T((-48, -2)), T((-60, 2)), T((-74, -4)), 4, FUR_DEEP, .55))
    # nose bridge catching the light
    out.append(stroke(T((4, -14)), T((5, -4)), T((4, 6)), 3.4, LIGHT_EDGE, .5))
    # loose fur at the cheeks
    out.append(stroke(T((72, 18)), T((82, 22)), T((88, 20)), 2.6, CREAM, .6))
    out.append(stroke(T((-70, 18)), T((-80, 22)), T((-86, 20)), 2.6, FUR_DEEP, .55))
    out.append("</g>")

    # line weight follows the light: thin on the lit cheek, heavier on
    # the shaded side and where the chin sits in front of the chest
    out.append(f'<path d="{outline}" stroke="{INK}" stroke-width="1.1" fill="none" opacity=".8"/>')
    out.append(stroke(T((-62, -36)), T((-84, -6)), T((-86, 22)), 3, INK, .75))
    out.append(stroke(T((-86, 24)), T((-78, 44)), T((-44, 54)), 3.4, INK, .8))
    out.append(stroke(T((-50, 52)), T((-4, 64)), T((50, 50)), 4.6, INK, .85, taper=(0.7, 0.9)))
    out.append(eye(-1, mood, uid))
    out.append(eye(1, mood, uid))
    if e["brow"]:
        # one eyebrow whisker raised over the near eye
        a = T((36, -26))
        out.append(stroke(a, (a[0] + 30, a[1] - 22), (a[0] + 70, a[1] - 24), 1.2, CREAM, .8, taper=(0.2, 1)))
        out.append(stroke((a[0] + 6, a[1] + 3), (a[0] + 34, a[1] - 12), (a[0] + 64, a[1] - 6), 1, CREAM, .55, taper=(0.2, 1)))
    out.append(face(mood, uid))
    out.append(f'<g clip-path="url(#headclip{uid})"><path d="{far_shade()}" fill="{SHADOW_RED}" opacity=".3" filter="url(#shade)"/></g>')
    return "".join(out)


def byte(mood, x, y, s=1.0, uid="", with_body=True):
    """Byte at (x, y), ground under the paws, scale s."""
    tilt = EXPR[mood]["tilt"]
    drop = EXPR[mood]["drop"]
    parts = []
    if with_body:
        parts.append(f"""
            <clipPath id="bodyclip{uid}"><path d="{BODY}"/></clipPath>
      <g class="breathe">
        <g filter="url(#gouache)"><path d="{BODY}" fill="{FUR}"/></g>
        <g clip-path="url(#bodyclip{uid})">
          <path d="{HAUNCH_SHADE}" fill="{FUR_SHADE}" opacity=".55" filter="url(#haze)"/>
          <path d="{BELLY_SHADE}" fill="{FUR_DEEP}" opacity=".55" filter="url(#softedge)"/>
          <path d="M-40 -160 C30 -164 104 -122 118 -66 L140 -66 L140 -190z" fill="{FUR_LIT}" opacity=".55" filter="url(#softedge)"/>
          {body_stripes()}
          <g filter="url(#drybrush)">{stroke((-150, -112), (-80, -160), (6, -150), 12, FUR_LIT, .85, n=24)}</g>
        </g>
        {stroke((-166, -98), (-86, -166), (14, -157), 2.8, "#ffd59a", .85, taper=(1, 0.6), n=26)}
        {stroke((-104, -12), (-104, -36), (-114, -56), 3, FUR_DEEP, .45)}
        {stroke((-126, -70), (-140, -80), (-158, -82), 2.6, FUR_DEEP, .35)}
        {stroke((-112, -64), (-128, -74), (-146, -74), 2.4, FUR_LIT, .5)}
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

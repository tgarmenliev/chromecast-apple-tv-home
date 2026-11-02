"""12 more dark landscape wallpapers in the style of themes/scenes, drawn from code (SVG 1280x720).

    python3 new_scenes.py out_dir        # writes 15-....svg ... 26-....svg

The helpers (ridge, hills, stars, water, ripples, radial, grad, svg) come from the launcher repo's
tools/scenes_wallpapers.py. Every scene gets the same dark scrim over its lower third, because the dock, the
grid and the text sit there.
"""
import math
import os
import random
import sys

REPO_TOOLS = os.path.expanduser("~/Documents/LimitMe/екран/launcher-src/repo/tools")
sys.path.insert(0, REPO_TOOLS)
import scenes_wallpapers as S  # noqa: E402

W, H = S.W, S.H
grad, radial, ridge, hills, stars, water, ripples = S.grad, S.radial, S.ridge, S.hills, S.stars, S.water, S.ripples

SCRIM = (grad("scrim", [(0, "#04050a", 0), (.55, "#04050a", .35), (1, "#04050a", .92)]))
SCRIM_RECT = f'<rect y="330" width="{W}" height="{H - 330}" fill="url(#scrim)"/>'


def scene(defs, body):
    return S.svg(defs + SCRIM, body + SCRIM_RECT)


def pines(seed, y, h, n, color, spread=(0, W), lean=0.0):
    """A row of pine silhouettes standing on y, about h tall."""
    rnd = random.Random(seed)
    out = []
    for _ in range(n):
        x = rnd.uniform(*spread)
        th = h * rnd.uniform(.55, 1.15)
        tw = th * rnd.uniform(.22, .3)
        tiers = 5
        pts = [f"{x:.0f},{y - th:.0f}"]
        right, left = [], []
        for i in range(1, tiers + 1):
            yy = y - th + th * i / tiers
            ww = tw * i / tiers
            right += [f"{x + ww * .55:.0f},{yy - th / tiers * .35:.0f}", f"{x + ww:.0f},{yy:.0f}"]
            left = [f"{x - ww * .55:.0f},{yy - th / tiers * .35:.0f}", f"{x - ww:.0f},{yy:.0f}"] + left
        pts += right + [f"{x:.0f},{y + 40:.0f}"] + left
        out.append(f'<polygon points="{" ".join(pts)}" fill="{color}"/>')
    return "".join(out)


def pine_forest_aurora():
    d = grad("sky", [(0, "#03060f"), (.5, "#0a1c2e"), (.75, "#12384a")]) + radial("g1", "#3dffb0", .55, .18) + \
        radial("g2", "#7a5cff", .45, .12)
    b = ('<rect width="1280" height="720" fill="url(#sky)"/>' + stars(51, 230, 330) +
         '<ellipse cx="520" cy="170" rx="520" ry="120" fill="url(#g1)" filter="url(#b24)" transform="rotate(-8 520 170)"/>'
         '<ellipse cx="820" cy="130" rx="380" ry="80" fill="url(#g2)" filter="url(#b24)" transform="rotate(6 820 130)"/>'
         f'<path d="{ridge(53, 520, 40, 1.4)}" fill="#07131c"/>' +
         pines(55, 560, 120, 38, "#050d14") + pines(57, 640, 190, 26, "#030910") + pines(59, 760, 260, 14, "#02060b"))
    return scene(d, b)


def desert_milky_way():
    d = grad("sky", [(0, "#050816"), (.4, "#171a3a"), (.62, "#3a2a55"), (.7, "#b0587a")]) + \
        grad("band", [(0, "#cfd8ff", 0), (.5, "#cfd8ff", .5), (1, "#cfd8ff", 0)], vertical=False) + \
        radial("core", "#ffd6f2", .75, .25)
    b = ('<rect width="1280" height="720" fill="url(#sky)"/>' + stars(61, 420, 420, 1.5) +
         '<g transform="rotate(-32 640 280)"><rect x="-200" y="215" width="1700" height="110" fill="url(#band)" '
         'filter="url(#b24)" opacity=".85"/><ellipse cx="780" cy="270" rx="230" ry="60" fill="url(#core)"/></g>' +
         stars(63, 140, 300, 1.2) +
         f'<path d="{hills(65, 560, 26, 1.4)}" fill="#26162b"/>'
         f'<path d="{hills(67, 610, 34, 1.1)}" fill="#160d1c"/>'
         f'<path d="{hills(69, 670, 22, 1.8)}" fill="#0a0610"/>'
         '<path d="M840,610 l0,-70 M840,580 q-20,0 -20,-22 M840,568 q22,0 22,-20" stroke="#0a0610" stroke-width="9" '
         'fill="none" stroke-linecap="round"/>')
    return scene(d, b)


def synthwave():
    lines = "".join(f'<line x1="640" y1="470" x2="{640 + k * 120}" y2="720" stroke="#ff4fd8" stroke-width="1.4" opacity=".55"/>'
                    for k in range(-12, 13))
    horiz = "".join(f'<line x1="0" y1="{470 + (i * i) * 3.6:.0f}" x2="1280" y2="{470 + (i * i) * 3.6:.0f}" '
                    'stroke="#ff4fd8" stroke-width="1.3" opacity=".5"/>' for i in range(1, 8))
    d = grad("sky", [(0, "#0a0220"), (.5, "#3a0f63"), (.68, "#ff4f9a")]) + \
        grad("sun", [(0, "#ffe66d"), (.55, "#ff6ec4"), (1, "#8a2be2")]) + radial("halo", "#ff6ec4", .55, .15) + \
        grad("floor", [(0, "#1a0638"), (1, "#05010d")])
    bands = "".join(f'<rect x="300" y="{330 + k * 22 + k * k * 1.6:.0f}" width="680" height="{3 + k * 1.4:.1f}" fill="#0a0220"/>'
                    for k in range(1, 8))
    b = ('<rect width="1280" height="720" fill="url(#sky)"/>' + stars(71, 120, 300, 1.2) +
         '<circle cx="640" cy="430" r="260" fill="url(#halo)"/><circle cx="640" cy="420" r="130" fill="url(#sun)"/>' + bands +
         f'<path d="{ridge(73, 470, 38, 1.5)}" fill="#12052b"/>'
         '<rect y="470" width="1280" height="250" fill="url(#floor)"/>' + lines + horiz)
    return scene(d, b)


def foggy_forest():
    d = grad("sky", [(0, "#1b2733"), (.5, "#3d5163"), (.7, "#8da3b3")]) + grad("mist", [(0, "#a9bdca", 0), (.5, "#a9bdca", .55), (1, "#a9bdca", 0)])
    layers = ""
    cols = ["#6b8396", "#506879", "#38505f", "#233a49", "#12222d", "#08121a"]
    for i, c in enumerate(cols):
        y = 420 + i * 48
        layers += pines(80 + i, y, 110 + i * 38, 26 - i * 2, c)
        layers += f'<rect y="{y - 70}" width="1280" height="120" fill="url(#mist)" opacity="{.75 - i * .09:.2f}"/>'
    b = '<rect width="1280" height="720" fill="url(#sky)"/><circle cx="930" cy="190" r="60" fill="#e6eef3" opacity=".35" filter="url(#b24)"/>' + layers
    return scene(d, b)


def snowy_twilight():
    d = grad("sky", [(0, "#101a4a"), (.45, "#4a5a9a"), (.66, "#e9a7b4"), (.72, "#ffd6c0")])
    snow = lambda seed, base, amp, fill, shade: (  # noqa: E731
        f'<path d="{ridge(seed, base, amp, 1.0)}" fill="{fill}"/>')
    b = ('<rect width="1280" height="720" fill="url(#sky)"/>' + stars(91, 110, 220) +
         snow(93, 440, 120, "#7f8fc0", "") + snow(95, 500, 110, "#56669b", "") + snow(97, 570, 90, "#303c6e", "") +
         snow(99, 640, 60, "#161d40", "") + pines(101, 690, 120, 18, "#070a1a", (0, W)))
    return scene(d, b)


def rila_dawn():
    d = grad("sky", [(0, "#1c2757"), (.4, "#6e5a96"), (.6, "#f3987a"), (.7, "#ffd18c")]) + radial("sun", "#ffe2a8", .9, .25)
    rn = random.Random(111)
    peaks = "".join(f'<polygon points="{x},{y} {x - w},{y + h} {x + w},{y + h}" fill="#fff" opacity=".12"/>' for x, y, w, h in
                    [(rn.randint(80, 1200), rn.randint(300, 380), rn.randint(40, 90), rn.randint(70, 110)) for _ in range(6)])
    b = ('<rect width="1280" height="720" fill="url(#sky)"/><circle cx="360" cy="470" r="260" fill="url(#sun)"/>'
         f'<path d="{ridge(113, 430, 110, 0.95)}" fill="#8a6f9c"/>' +
         f'<path d="{ridge(115, 510, 90, 1.1)}" fill="#5a4a82"/>'
         f'<path d="{ridge(117, 580, 75, 1.2)}" fill="#33295a"/>' +
         pines(119, 620, 90, 24, "#161232") + f'<path d="{hills(121, 680, 24, 1.6)}" fill="#0b0a1c"/>')
    return scene(d, b)


def lavender_dusk():
    rows = ""
    for i in range(14):
        y = 470 + i * 19
        rows += (f'<path d="{hills(130 + i, y, 6 + i * .8, 1.5 + i * .05)}" fill="{["#5b3f8c", "#4d3478", "#40296a", "#331f58", "#281848", "#1c1036"][min(i // 3, 5)]}" '
                 f'opacity=".96"/>')
    d = grad("sky", [(0, "#1d1148"), (.45, "#5a2f7a"), (.65, "#e0698f"), (.72, "#ffb27a")]) + radial("sun", "#ffc58f", .85, .25)
    b = ('<rect width="1280" height="720" fill="url(#sky)"/><circle cx="880" cy="450" r="220" fill="url(#sun)"/>'
         f'<path d="{ridge(129, 460, 30, 1.6)}" fill="#3b2166"/>' + rows)
    return scene(d, b)


def tropical_sunset():
    def palm(x, y, lean, h, c):
        top = (x + lean, y - h)
        fronds = "".join(
            f'<path d="M{top[0]},{top[1]} q{math.cos(a) * 60:.0f},{math.sin(a) * 40 - 30:.0f} {math.cos(a) * 110:.0f},{math.sin(a) * 70 + 14:.0f}" '
            f'stroke="{c}" stroke-width="7" fill="none" stroke-linecap="round"/>'
            for a in [-2.9, -2.4, -1.9, -1.2, -0.7, -0.2, 0.35, 2.8])
        return f'<path d="M{x},{y} Q{x + lean * .2},{y - h * .6} {top[0]},{top[1]}" stroke="{c}" stroke-width="9" fill="none"/>' + fronds
    gd, gb = water(450, "#7a3f6a", "#0a0716")
    d = grad("sky", [(0, "#241256"), (.4, "#8a2f7a"), (.58, "#ff6a5c"), (.66, "#ffc15a")]) + radial("sun", "#ffd27a", .95, .3) + gd + \
        grad("streak", [(0, "#ffd27a", .8), (1, "#ffd27a", 0)])
    b = ('<rect width="1280" height="720" fill="url(#sky)"/><circle cx="640" cy="452" r="230" fill="url(#sun)"/>'
         '<circle cx="640" cy="450" r="46" fill="#fff2c4"/>' + gb +
         '<path d="M600,452 L680,452 L760,720 L520,720 Z" fill="url(#streak)" opacity=".6"/>' + ripples(141, 456, "#ffd7a0") +
         '<path d="M0,600 C140,560 260,570 330,640 L330,720 L0,720 Z" fill="#0b0712"/>' +
         palm(150, 610, 40, 250, "#0b0712") + palm(250, 640, -30, 190, "#0b0712") +
         '<path d="M1280,610 C1160,590 1100,620 1050,680 L1050,720 L1280,720 Z" fill="#0b0712"/>' + palm(1170, 640, -50, 220, "#0b0712"))
    return scene(d, b)


def nebula():
    rnd = random.Random(151)
    blobs = "".join(
        f'<circle cx="{rnd.randint(100, 1180)}" cy="{rnd.randint(40, 420)}" r="{rnd.randint(110, 240)}" '
        f'fill="url(#{rnd.choice(["n1", "n2", "n3"])})" filter="url(#b24)"/>' for _ in range(9))
    d = grad("sky", [(0, "#02030a"), (1, "#0a0820")]) + radial("n1", "#6a3dff", .55, .2) + radial("n2", "#ff3d9a", .5, .15) + \
        radial("n3", "#2fd6ff", .45, .12) + radial("planet", "#ffb77a", .9, .3)
    b = ('<rect width="1280" height="720" fill="url(#sky)"/>' + blobs + stars(153, 520, 560, 1.6) +
         '<circle cx="1020" cy="300" r="120" fill="url(#planet)"/><circle cx="1020" cy="300" r="62" fill="#2a1830"/>'
         '<ellipse cx="1020" cy="300" rx="160" ry="22" fill="none" stroke="#ffd7a8" stroke-width="3" opacity=".6" transform="rotate(-18 1020 300)"/>')
    return scene(d, b)


def volcano_embers():
    rnd = random.Random(161)
    sparks = "".join(f'<circle cx="{rnd.randint(480, 800)}" cy="{rnd.randint(40, 330)}" r="{rnd.choice([1.2, 1.8, 2.4])}" '
                     f'fill="#ffb347" opacity="{rnd.uniform(.3, .9):.2f}"/>' for _ in range(90))
    d = grad("sky", [(0, "#0a0508"), (.55, "#2a0f14"), (.7, "#7a2a1a")]) + radial("glow", "#ff6a1a", .85, .3) + \
        grad("lava", [(0, "#ffb347"), (1, "#c2210a")])
    b = ('<rect width="1280" height="720" fill="url(#sky)"/>' + stars(163, 160, 260) +
         '<circle cx="640" cy="330" r="300" fill="url(#glow)" filter="url(#b24)"/>' + sparks +
         '<path d="M180,720 L520,360 L585,325 L695,325 L760,360 L1100,720 Z" fill="#150a0c"/>'
         '<path d="M585,325 L695,325 L670,345 L610,345 Z" fill="url(#lava)"/>'
         '<path d="M630,345 L650,345 L640,450 L660,540 L600,720 L575,720 L625,540 L615,450 Z" fill="url(#lava)" opacity=".85"/>'
         f'<path d="{ridge(165, 600, 40, 1.4)}" fill="#0a0507" opacity=".95"/>')
    return scene(d, b)


def crescent_sea():
    gd, gb = water(470, "#13244a", "#04070f")
    d = grad("sky", [(0, "#050a1c"), (.5, "#14285a"), (.66, "#3b5b9a")]) + radial("glow", "#c8d8ff", .5, .15) + gd + \
        grad("streak", [(0, "#e8efff", .6), (1, "#e8efff", 0)])
    b = ('<rect width="1280" height="720" fill="url(#sky)"/>' + stars(171, 300, 420) +
         '<circle cx="330" cy="190" r="200" fill="url(#glow)"/>'
         '<path d="M330,140 a52,52 0 1,0 40,92 a42,42 0 1,1 -40,-92 Z" fill="#f6f1de"/>' + gb +
         '<path d="M315,472 L345,472 L420,720 L240,720 Z" fill="url(#streak)" opacity=".55"/>' + ripples(173, 478, "#cfe0ff", 3, (.05, .22)) +
         f'<path d="{ridge(175, 478, 20, 1.5)}" fill="#050912"/>')
    return scene(d, b)


SCENES = [("15-pine-aurora", pine_forest_aurora), ("16-desert-milky-way", desert_milky_way), ("17-synthwave", synthwave),
          ("18-foggy-forest", foggy_forest), ("19-snowy-twilight", snowy_twilight), ("20-rila-dawn", rila_dawn),
          ("21-lavender-dusk", lavender_dusk), ("22-tropical-sunset", tropical_sunset), ("23-nebula", nebula),
          ("24-volcano-embers", volcano_embers), ("25-crescent-sea", crescent_sea)]

if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    for name, fn in SCENES:
        with open(os.path.join(out, name + ".svg"), "w") as f:
            f.write(fn())
    print(len(SCENES), "scenes written to", out)

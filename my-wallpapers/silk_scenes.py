"""Abstract wallpapers in the style of Apple's own: soft light orbs and silk ribbons on a deep dark base (SVG 1280x720).

    python3 silk_scenes.py out_dir

Every picture keeps its lower third dark for the dock, the grid and the text.
"""
import math
import os
import random
import sys

W, H = 1280, 720


def blur(name, n):
    return f'<filter id="{name}" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="{n}"/></filter>'


DEFS = blur("b30", 30) + blur("b60", 60) + blur("b110", 110) + blur("b6", 6) + blur("b14", 14)
SCRIM = ('<linearGradient id="scrim" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#030409" stop-opacity=".25"/>'
         '<stop offset=".35" stop-color="#030409" stop-opacity="0"/><stop offset=".6" stop-color="#030409" stop-opacity=".35"/>'
         '<stop offset="1" stop-color="#030409" stop-opacity=".93"/></linearGradient>')


def page(base_top, base_bottom, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><defs>{DEFS}{SCRIM}'
            f'<linearGradient id="base" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{base_top}"/>'
            f'<stop offset="1" stop-color="{base_bottom}"/></linearGradient></defs>'
            f'<rect width="{W}" height="{H}" fill="url(#base)"/>{body}'
            f'<rect y="0" width="{W}" height="{H}" fill="url(#scrim)"/></svg>')


def orbs(seed, colors, n=7, rmin=170, rmax=360, ymax=470, op=(.45, .85)):
    rmin, rmax = rmin * 1.25, rmax * 1.3
    rnd = random.Random(seed)
    out = []
    for i in range(n):
        c = colors[i % len(colors)]
        out.append(f'<circle cx="{rnd.uniform(-60, W + 60):.0f}" cy="{rnd.uniform(-60, ymax):.0f}" r="{rnd.uniform(rmin, rmax):.0f}" '
                   f'fill="{c}" opacity="{rnd.uniform(*op):.2f}" filter="url(#b110)"/>')
    return "".join(out)


def ribbon(seed, y, amp, thick, c1, c2, op=.6, tilt=0, blur_id="b14"):
    """One flowing band across the picture, a gradient along its length."""
    rnd = random.Random(seed)
    ph = [rnd.uniform(0, 6.28) for _ in range(3)]
    top, bot = [], []
    for x in range(-40, W + 41, 20):
        t = x / W
        yy = y + tilt * (t - .5) + amp * (math.sin(t * 5.1 + ph[0]) * .6 + math.sin(t * 9.7 + ph[1]) * .25 + math.sin(t * 2.3 + ph[2]) * .5)
        th = thick * (.55 + .45 * math.sin(t * 3.4 + ph[1]))
        top.append(f"{x},{yy - th / 2:.1f}")
        bot.append(f"{x},{yy + th / 2:.1f}")
    gid = f"rg{seed}"
    d = "M" + " L".join(top) + " L" + " L".join(reversed(bot)) + " Z"
    return (f'<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{c1}" stop-opacity="0"/>'
            f'<stop offset=".25" stop-color="{c1}"/><stop offset=".75" stop-color="{c2}"/><stop offset="1" stop-color="{c2}" stop-opacity="0"/></linearGradient>'
            f'<path d="{d}" fill="url(#{gid})" opacity="{op}" filter="url(#{blur_id})"/>')


def stars_fine(seed, n, ymax):
    rnd = random.Random(seed)
    return "".join(f'<circle cx="{rnd.uniform(0, W):.0f}" cy="{ymax * rnd.random() ** 1.3:.0f}" r="{rnd.choice([.5, .7, .9, 1.2])}" '
                   f'fill="#fff" opacity="{rnd.uniform(.25, .8):.2f}"/>' for _ in range(n))


def aurora_sea():
    return page("#02141c", "#031a2a", orbs(1, ["#00e0b0", "#0a8fd6", "#5b3df5"], 6, 160, 320, 300) +
                ribbon(11, 190, 70, 150, "#00ffc8", "#3d7bff", .55) + ribbon(12, 250, 60, 90, "#7cf5ff", "#9a5bff", .4))


def ember_dusk():
    return page("#14060c", "#1c0a10", orbs(2, ["#ff5a36", "#ff9a3c", "#c21e56"], 6, 160, 340, 330) +
                ribbon(21, 210, 60, 140, "#ffb454", "#ff3d6e", .5) + ribbon(22, 280, 50, 80, "#ffd9a0", "#ff6a3d", .35))


def violet_bloom():
    return page("#0b0720", "#12082b", orbs(3, ["#8a4dff", "#ff5ad1", "#3d6bff"], 7, 150, 330, 360) +
                ribbon(31, 200, 80, 130, "#c58bff", "#ff6ad5", .5))


def midnight_gold():
    return page("#05070f", "#0a0e1c", orbs(4, ["#1d3a8a", "#2a56c8", "#e8b657"], 6, 150, 300, 330, (.35, .75)) +
                ribbon(41, 230, 50, 110, "#f5d38a", "#4f7bff", .5) + stars_fine(43, 160, 330))


def forest_mist():
    return page("#06120d", "#0a1c14", orbs(5, ["#1f8a5b", "#6bd68a", "#0f5a4a"], 7, 150, 320, 340, (.35, .75)) +
                ribbon(51, 220, 65, 120, "#b8ffcf", "#27c28a", .4))


def rose_gold():
    return page("#150a12", "#1f0f1a", orbs(6, ["#ff8fa3", "#ffbe8a", "#b04a8a"], 6, 160, 330, 340, (.4, .8)) +
                ribbon(61, 190, 60, 130, "#ffd2c0", "#ff7fa8", .5) + ribbon(62, 260, 40, 70, "#fff0e0", "#ff9ec0", .3))


def deep_ocean():
    return page("#020b1a", "#041428", orbs(7, ["#0a4bd6", "#12c8e0", "#2a2fa8"], 7, 150, 330, 360, (.4, .8)) +
                ribbon(71, 210, 90, 140, "#5ce8ff", "#2f6bff", .45) + ribbon(72, 300, 70, 90, "#9ef0ff", "#4a7bff", .3))


def sunset_candy():
    return page("#160a2a", "#210d33", orbs(8, ["#ff6a88", "#ffb347", "#7a5cff"], 7, 150, 330, 360, (.45, .85)) +
                ribbon(81, 200, 70, 130, "#ffc2a0", "#b27bff", .5))


def northern_lights():
    return page("#030914", "#06101f", stars_fine(9, 200, 420) +
                ribbon(91, 160, 80, 190, "#38ff9a", "#2a9bff", .55, 40, "b30") + ribbon(92, 215, 60, 120, "#a5ffd6", "#7a4dff", .45, -30, "b30") +
                ribbon(93, 130, 50, 70, "#d8ffe8", "#46c8ff", .35, 10, "b14"))


def amber_haze():
    return page("#120a05", "#1a0f08", orbs(10, ["#ffae42", "#ff7a2f", "#a8431f"], 6, 170, 340, 330, (.4, .75)) +
                ribbon(101, 220, 55, 120, "#ffe3a8", "#ff8a3d", .4))


def ice_blue():
    return page("#050d18", "#08162a", orbs(11, ["#7fd4ff", "#4a8bff", "#b8f0ff"], 6, 150, 320, 330, (.3, .65)) +
                ribbon(111, 200, 70, 110, "#e8fbff", "#7fb8ff", .45))


def magenta_night():
    return page("#0c0617", "#14091f", stars_fine(12, 120, 300) + orbs(12, ["#ff2fa8", "#6a3dff", "#00c8ff"], 6, 150, 320, 330, (.4, .75)) +
                ribbon(121, 210, 75, 120, "#ff9ae0", "#7a8dff", .5))


def emerald_dusk():
    return page("#04120f", "#071d19", orbs(13, ["#00c896", "#2a7bff", "#ffd36a"], 6, 150, 320, 330, (.35, .7)) +
                ribbon(131, 215, 60, 110, "#9bffe0", "#4fa8ff", .45))


SCENES = [("30-aurora-sea", aurora_sea), ("31-ember-dusk", ember_dusk), ("32-violet-bloom", violet_bloom),
          ("33-midnight-gold", midnight_gold), ("34-forest-mist", forest_mist), ("35-rose-gold", rose_gold),
          ("36-deep-ocean", deep_ocean), ("37-sunset-candy", sunset_candy), ("38-northern-lights", northern_lights),
          ("39-amber-haze", amber_haze), ("40-ice-blue", ice_blue), ("41-magenta-night", magenta_night),
          ("42-emerald-dusk", emerald_dusk)]

if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    for name, fn in SCENES:
        with open(os.path.join(out, name + ".svg"), "w") as f:
            f.write(fn())
    print(len(SCENES), "written to", out)

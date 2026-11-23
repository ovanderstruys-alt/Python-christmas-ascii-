"""Crackling Fireplace: flames dance in a brick hearth below a mantel hung with stockings.

Run it in a terminal with:  python fireplace.py   (Ctrl+C to stop)
"""
import random

TITLE = "Crackling Fireplace"
BLURB = "A brick hearth with a living fire simulation, stockings on the mantel and a garland above."
FPS = 12

RESET = "\033[0m"


def paint(code, text):
    return "\033[" + code + "m" + text + RESET


FIRE_W = 28
FIRE_H = 9
HEAT_CHARS = " .:-=+*#%@"
HEAT_COLOURS = ["2", "31", "31", "91", "91", "33", "93", "93;1", "97;1", "97;1"]

STOCKING = [
    " [##]",
    "  ##",
    "  ##",
    " ###",
    "###",
]
STOCKING_COLOURS = ["91", "92", "94"]


def fire_step(heat, rng):
    """Classic cellular fire: each cell takes the heat below it, minus a little, drifting sideways."""
    for x in range(FIRE_W):
        heat[FIRE_H - 1][x] = rng.choice([7, 8, 9, 9, 9]) if 3 < x < FIRE_W - 4 else rng.choice([0, 3, 5])
    for y in range(FIRE_H - 1):
        for x in range(FIRE_W):
            src = heat[y + 1][min(FIRE_W - 1, max(0, x + rng.choice([-1, 0, 1])))]
            heat[y][x] = max(0, src - rng.choice([0, 1, 1, 2]))


def garland(t):
    out = ""
    for i in range(46):
        if i % 6 == 3:
            out += paint(["91;1", "93;1", "94;1"][(i // 6 + t // 4) % 3], "o")
        else:
            out += paint("32", "~" if i % 2 else "^")
    return out


def frames():
    rng = random.Random()
    heat = [[0] * FIRE_W for _ in range(FIRE_H)]
    t = 0
    while True:
        fire_step(heat, rng)
        pad = "  "
        lines = [pad + garland(t)]
        mantel = paint("33", "=" * 46)
        lines.append(pad + mantel)
        # stockings hang from the mantel, swaying a little in the warm air
        for dy in range(len(STOCKING)):
            row = pad + " " * 3
            for i, colour in enumerate(STOCKING_COLOURS):
                sway = 1 if (t // 8 + i) % 4 == 0 and dy > 2 else 0
                part = (" " * sway + STOCKING[dy]).ljust(7)
                row += paint("97" if dy == 0 else colour, part) + " " * 7
            lines.append(row)
        lines.append(pad + paint("31", "|" + "_" * 44 + "|"))
        for y in range(FIRE_H):
            flame = ""
            for x in range(FIRE_W):
                h = heat[y][x]
                flame += paint(HEAT_COLOURS[h], HEAT_CHARS[h]) if h else " "
            side = paint("31", "[__][__]" if y % 2 == 0 else "_][__][_")
            wall = paint("31", "|")
            lines.append(pad + side + wall + flame + wall + side)
        logs = paint("33", "(@)====(@)")
        lines.append(pad + paint("31", "[__][__]|") + "   " + logs + "  " + logs + "   " + paint("31", "|[__][__]"))
        lines.append(pad + paint("37", "#" * 46))
        lines.append("")
        lines.append(pad + " " * 11 + paint("93", "Warm wishes by the fire"))
        yield "\n".join(lines)
        t += 1


if __name__ == "__main__":
    import time
    try:
        print("\033[?25l", end="")
        for frame in frames():
            print("\033[H\033[2J" + frame, flush=True)
            time.sleep(1 / FPS)
    except KeyboardInterrupt:
        pass
    finally:
        print("\033[?25h" + RESET)

"""Twinkle Tree: a fir tree with blinking lights, shifting baubles and a pulsing star.

Run it in a terminal with:  python tree.py   (Ctrl+C to stop)
"""
import random

TITLE = "Twinkle Tree"
BLURB = "A fir tree with blinking lights, colour-shifting baubles and a star that pulses."
FPS = 5

RESET = "\033[0m"


def paint(code, text):
    return "\033[" + code + "m" + text + RESET


ROWS = 13          # height of the tree's branches
CENTER = 24        # column of the trunk
BAUBLE_COLOURS = ["91", "93", "94", "95", "96"]


def build_layout():
    """Decide once where the decorations go, so they stay put between frames."""
    rng = random.Random(25)
    layout = {}
    for row in range(1, ROWS):
        for k in range(1, 2 * row):
            x = CENTER - row + k
            if (x - 3 * row) % 15 < 3:
                layout[(row, x)] = "tinsel"
            elif rng.random() < 0.11:
                layout[(row, x)] = "bauble"
            elif rng.random() < 0.12:
                layout[(row, x)] = "light"
    return layout


def draw_tree(layout, t, rng):
    lines = []
    star = paint("93;1" if t % 2 else "33", "*")
    glow = paint("93", "\\ | /") if t % 2 else "     "
    lines.append(" " * (CENTER - 2) + glow)
    lines.append(" " * CENTER + star)
    for row in range(1, ROWS):
        line = " " * (CENTER - row) + paint("32", "/")
        for k in range(1, 2 * row):
            x = CENTER - row + k
            kind = layout.get((row, x))
            if kind == "tinsel":
                bright = (x + row + t) % 4 == 0
                line += paint("93;1" if bright else "33", "~")
            elif kind == "bauble":
                colour = BAUBLE_COLOURS[(x + row * 3 + t // 2) % len(BAUBLE_COLOURS)]
                line += paint(colour + ";1", "o")
            elif kind == "light":
                line += paint("97;1", "*") if rng.random() < 0.55 else paint("2", ".")
            else:
                line += paint("92" if (x + row) % 3 else "32", "^")
        line += paint("32", "\\")
        lines.append(line)
    base = " " * (CENTER - ROWS) + paint("32", "/" + "_" * (2 * ROWS - 1) + "\\")
    lines.append(base)
    trunk = paint("33", "|###|")
    gift_a = paint("91", "[") + paint("93", "#") + paint("91", "]")
    gift_b = paint("94", "[=") + paint("97", "+") + paint("94", "=]")
    gift_c = paint("95", "[") + paint("92", "*") + paint("95", "]")
    lines.append(" " * (CENTER - 2) + trunk)
    lines.append(" " * (CENTER - 10) + gift_a + "     " + trunk + "  " + gift_b + " " + gift_c)
    lines.append(paint("97", "~" * (2 * CENTER + 1)))
    return lines


def greeting(t):
    words = "M E R R Y   C H R I S T M A S"
    out = ""
    for i, ch in enumerate(words):
        out += paint("91;1" if (i // 2 + t) % 2 else "92;1", ch) if ch != " " else " "
    pad = (2 * CENTER + 1 - len(words)) // 2
    return " " * pad + out


def frames():
    layout = build_layout()
    rng = random.Random()
    t = 0
    while True:
        lines = draw_tree(layout, t, rng)
        lines.append("")
        lines.append(greeting(t))
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

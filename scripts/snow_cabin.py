"""Snowed-In Cabin: snow drifts down over a log cabin while smoke curls from the chimney.

Run it in a terminal with:  python snow_cabin.py   (Ctrl+C to stop)
"""
import random

TITLE = "Snowed-In Cabin"
BLURB = "Snowflakes drift past a log cabin with glowing windows and smoke curling from the chimney."
FPS = 8

RESET = "\033[0m"


def paint(code, text):
    return "\033[" + code + "m" + text + RESET


WIDTH = 52
HEIGHT = 22

# Each scene row is (text, colour key). Colour keys map characters to ANSI codes below.
CABIN = [
    "          ||",
    "  ________||______________",
    " /,,,,,,,,,,,,,,,,,,,,,,,,\\",
    "/__________________________\\",
    " |  ___    _____    ___   |",
    " | |WW|   |     |  |WW|   |",
    " | |WW|   |    o|  |WW|   |",
    " |________|_____|_________|",
]

PINE = [
    "   *",
    "   ^",
    "  ^^^",
    " ^^^^^",
    "  ^^^",
    " ^^^^^",
    "^^^^^^^",
    "   |",
]


def blank():
    return [[(" ", None) for _ in range(WIDTH)] for _ in range(HEIGHT)]


def stamp(grid, art, top, left, colours):
    """Draw art onto the grid. Gaps inside a row stay solid so snow can't fall through walls."""
    for dy, row in enumerate(art):
        first = len(row) - len(row.lstrip())
        for dx, ch in enumerate(row):
            y, x = top + dy, left + dx
            if dx < first or not (0 <= y < HEIGHT and 0 <= x < WIDTH):
                continue
            grid[y][x] = (ch, "solid") if ch == " " else (ch, colours.get(ch, "37"))


def make_flakes(rng, count):
    return [[rng.uniform(0, WIDTH), rng.uniform(0, HEIGHT), rng.choice([0.35, 0.5, 0.8])]
            for _ in range(count)]


def frames():
    rng = random.Random()
    flakes = make_flakes(rng, 55)
    smoke = []
    cabin_top = HEIGHT - len(CABIN) - 2
    cabin_left = (WIDTH - len(CABIN[3])) // 2
    chimney_x = cabin_left + 10
    t = 0
    while True:
        grid = blank()
        # moon
        stamp(grid, [" _ ", "( `", " ~ "], 1, 4, {"_": "93", "(": "93", "`": "93", "~": "93"})
        # pines on either side
        pine_colours = {"^": "32", "|": "33"}
        stamp(grid, PINE, HEIGHT - len(PINE) - 2, 1, {"*": "93;1", **pine_colours})
        stamp(grid, PINE, HEIGHT - len(PINE) - 2, WIDTH - 8, {"*": "93;1", **pine_colours})
        # cabin, windows flicker like firelight
        window = "93;1" if rng.random() < 0.8 else "33"
        stamp(grid, CABIN, cabin_top, cabin_left, {
            ",": "97", "_": "33", "/": "33", "\\": "33", "|": "33",
            "W": window, "o": "93",
        })
        # snow on the ground
        for y in (HEIGHT - 2, HEIGHT - 1):
            for x in range(WIDTH):
                grid[y][x] = ("~" if (x + y + t // 6) % 5 else "-", "97" if y == HEIGHT - 2 else "37")
        # smoke rises from the chimney and drifts right
        if t % 3 == 0:
            smoke.append([float(chimney_x), float(cabin_top - 1)])
        for puff in smoke:
            puff[1] -= 0.5
            puff[0] += rng.choice([0, 0.3, 0.6])
        smoke = [p for p in smoke if p[1] > 0]
        for x, y in smoke:
            xi, yi = int(x), int(y)
            if 0 <= xi < WIDTH and grid[yi][xi] == (" ", None):
                grid[yi][xi] = ("(" if yi % 2 else ")", "2" if yi < 4 else "37")
        # falling snow, drawn only on open sky
        for flake in flakes:
            flake[1] += flake[2]
            flake[0] += rng.choice([-0.4, 0, 0.4])
            if flake[1] >= HEIGHT - 2:
                flake[0], flake[1] = rng.uniform(0, WIDTH), 0
            xi, yi = int(flake[0]) % WIDTH, int(flake[1])
            if grid[yi][xi] == (" ", None):
                grid[yi][xi] = ("*" if flake[2] > 0.6 else "." if flake[2] < 0.4 else "+", "97" if flake[2] > 0.4 else "37")
        yield "\n".join(
            "".join(paint(code, ch) if code and code != "solid" else ch for ch, code in row).rstrip()
            for row in grid
        )
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

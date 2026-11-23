"""Midnight Sleigh Ride: Santa's sleigh and reindeer fly over a sleeping town.

Run it in a terminal with:  python sleigh_ride.py   (Ctrl+C to stop)
"""
import random

TITLE = "Midnight Sleigh Ride"
BLURB = "Santa and his reindeer fly across a starry sky over a sleeping town, leaving a trail of sparkles."
FPS = 10

RESET = "\033[0m"


def paint(code, text):
    return "\033[" + code + "m" + text + RESET


WIDTH = 56
HEIGHT = 20

SLEIGH = [
    r"     ,^.          \/       \/",
    r"    (o o)     ___/o>    ___/o@",
    r" \==|___|=/~~(___)~~~~~(___)",
    r"  \_______/   /  \      /  \ ",
    r" ==`======'==",
]
SLEIGH_COLOURS = {
    ",": "91", "^": "97;1", ".": "91", "(": "33", ")": "33", "o": "97",
    "|": "91", "_": "33", "=": "93", "\\": "33", "/": "33", "~": "2",
    "`": "93", "'": "93", ">": "33", "@": "91;1",
}

MOON = [
    r"  _.._",
    r".' .-'`",
    r"/  /",
    r"|  |",
    r"\  '.___.;",
    r" '._  _.'",
    r"    ``",
]

TOWN = [
    r"      ||                  ||                  ||",
    r"   ___||___     /\     ___||____      /\   ___||___",
    r"  /,,,,,,,,\   /,,\   /,,,,,,,,,\    /,,\ /,,,,,,,,\ ",
    r"  | #   #  |  /,,,,\  |  #    # |   /,,,,\|  #   # |",
    r"  |   _    |  | #  |  | #   _   |   | #  ||    _   |",
    r"~~|__| |___|~~|____|~~|____| |__|~~~|____||___| |__|~~",
]
TOWN_COLOURS = {",": "97", "#": "93", "~": "97", "|": "34", "_": "34", "/": "34", "\\": "34"}


def frames():
    rng = random.Random()
    stars = []
    while len(stars) < 34:
        sx, sy = rng.randrange(WIDTH), rng.randrange(HEIGHT - len(TOWN) - 1)
        if not (sx >= WIDTH - 13 and sy < len(MOON)):  # keep stars off the moon
            stars.append((sx, sy))
    sleigh_w = max(len(r) for r in SLEIGH)
    sparkles = []
    x = -sleigh_w
    t = 0
    while True:
        grid = [[(" ", None)] * WIDTH for _ in range(HEIGHT)]

        def put(px, py, ch, code):
            if 0 <= px < WIDTH and 0 <= py < HEIGHT and ch != " ":
                grid[py][px] = (ch, code)

        def solid(px, py, row):
            """Blank out the sky behind a sprite row so stars don't show through it."""
            start = len(row) - len(row.lstrip())
            for dx in range(start, len(row.rstrip())):
                if 0 <= px + dx < WIDTH and 0 <= py < HEIGHT:
                    grid[py][px + dx] = (" ", None)

        for sx, sy in stars:
            roll = rng.random()
            put(sx, sy, "*" if roll < 0.15 else "+" if roll < 0.35 else ".", "97" if roll < 0.35 else "2")
        for dy, row in enumerate(MOON):
            for dx, ch in enumerate(row):
                put(WIDTH - 12 + dx, dy, ch, "93")
        town_top = HEIGHT - len(TOWN)
        for dy, row in enumerate(TOWN):
            for dx, ch in enumerate(row):
                code = TOWN_COLOURS.get(ch, "37")
                if ch == "#" and rng.random() < 0.1:
                    code = "33"
                put(dx, town_top + dy, ch, code)

        # the sleigh bobs gently as it flies
        top = 8 + (1 if (t // 4) % 2 else 0)
        sparkles.append([x + 1, top + 4, 6])
        for s in sparkles:
            s[2] -= 1
        sparkles = [s for s in sparkles if s[2] > 0]
        for sx, sy, life in sparkles:
            put(sx - (6 - life) * 2, sy + rng.choice([-1, 0, 0, 1]),
                "*" if life > 3 else ".", "93;1" if life > 3 else "33")
        for dy, row in enumerate(SLEIGH):
            solid(x, top + dy, row)
            for dx, ch in enumerate(row):
                put(x + dx, top + dy, ch, SLEIGH_COLOURS.get(ch, "97"))
        if (t // 6) % 3 == 0 and 0 < x < WIDTH - 10:
            for i, ch in enumerate("Ho ho ho!"):
                put(x + 2 + i, top - 2, ch, "91;1")

        yield "\n".join(
            "".join(paint(code, ch) if code else ch for ch, code in row).rstrip()
            for row in grid
        )
        x += 1
        if x > WIDTH + 4:
            x = -sleigh_w
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

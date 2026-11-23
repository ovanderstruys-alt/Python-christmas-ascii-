"""Christmas Countdown: giant ticking digits counting down to 25 December.

Run it in a terminal with:  python countdown.py   (Ctrl+C to stop)
"""
import datetime

TITLE = "Christmas Countdown"
BLURB = "Big block digits tick down the days, hours, minutes and seconds until Christmas morning."
FPS = 2

RESET = "\033[0m"


def paint(code, text):
    return "\033[" + code + "m" + text + RESET


# Each digit is 5 rows tall, drawn with "#" and turned into solid blocks when printed.
DIGITS = {
    "0": ["###", "# #", "# #", "# #", "###"],
    "1": [" # ", "## ", " # ", " # ", "###"],
    "2": ["###", "  #", "###", "#  ", "###"],
    "3": ["###", "  #", " ##", "  #", "###"],
    "4": ["# #", "# #", "###", "  #", "  #"],
    "5": ["###", "#  ", "###", "  #", "###"],
    "6": ["###", "#  ", "###", "# #", "###"],
    "7": ["###", "  #", " # ", " # ", " # "],
    "8": ["###", "# #", "###", "# #", "###"],
    "9": ["###", "# #", "###", "  #", "###"],
    ":": [" ", "#", " ", "#", " "],
    " ": [" ", " ", " ", " ", " "],
}

WIDTH = 54


def big(text, colour, blink_colon=False):
    rows = []
    for r in range(5):
        row = ""
        for ch in text:
            glyph = DIGITS[ch][r]
            if ch == ":" and blink_colon:
                glyph = " "
            row += glyph.replace("#", "██").replace(" ", "  ") + "  "
        rows.append(row.rstrip())
    width = max(len(r) for r in rows)
    pad = " " * max(0, (WIDTH - width) // 2)
    return [pad + paint(colour, r) for r in rows]


def centre(text, colour):
    return " " * max(0, (WIDTH - len(text)) // 2) + paint(colour, text)


def next_christmas(now):
    target = datetime.datetime(now.year, 12, 25)
    if now >= target + datetime.timedelta(days=1):
        target = datetime.datetime(now.year + 1, 12, 25)
    return target


def candles(t):
    flames = "".join(paint("93;1" if (i + t) % 3 else "91", "^" if (i + t) % 2 else "'") + "   " for i in range(5))
    return [
        " " * 19 + flames,
        " " * 19 + paint("97", "|   " * 5),
        " " * 19 + paint("91", "|   " * 5),
        " " * 17 + paint("32", "~" * 21),
    ]


def frames():
    t = 0
    while True:
        now = datetime.datetime.now()
        target = next_christmas(now)
        lines = [centre("* * *  COUNTDOWN TO CHRISTMAS  * * *", "93;1"), ""]
        if now >= target:
            lines += [centre("IT'S CHRISTMAS DAY!", "91;1"), "", centre("Merry Christmas to all,", "92"),
                      centre("and to all a good night.", "92")]
        else:
            left = target - now
            hours, rest = divmod(left.seconds, 3600)
            minutes, seconds = divmod(rest, 60)
            lines += big(str(left.days), "91;1")
            lines.append(centre("days" if left.days != 1 else "day", "97"))
            lines.append("")
            lines += big("%02d:%02d:%02d" % (hours, minutes, seconds), "92;1", blink_colon=t % 2 == 1)
            labels = "hours".center(14) + " " * 6 + "minutes".center(14) + " " * 6 + "seconds".center(14)
            lines.append(centre(labels, "97"))
        lines.append("")
        lines += candles(t)
        lines.append("")
        lines.append(centre("Christmas morning: " + target.strftime("%A %d %B %Y"), "2"))
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

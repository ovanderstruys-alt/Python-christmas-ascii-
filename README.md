# Tinsel Terminal

A little website that's a library of Christmas ASCII-art Python scripts. Click a script and it runs right in the page (using [Brython](https://brython.info), Python for the browser), with colour, animation and a "Source" button to read the code.

Every script also runs in a normal terminal:

```sh
python scripts/tree.py        # Ctrl+C to stop
```

## The scripts

| File | What it draws |
| --- | --- |
| `scripts/tree.py` | Twinkle Tree: blinking lights, colour-shifting baubles, a pulsing star |
| `scripts/snow_cabin.py` | Snowed-In Cabin: falling snow, glowing windows, chimney smoke |
| `scripts/sleigh_ride.py` | Midnight Sleigh Ride: Santa and reindeer fly over a sleeping town |
| `scripts/fireplace.py` | Crackling Fireplace: a fire simulation under a mantel of stockings |
| `scripts/countdown.py` | Christmas Countdown: giant digits ticking down to 25 December |

## Open the website

Browsers won't let a page opened straight from disk read other files, so serve the folder:

```sh
python -m http.server 8000
```

Then open <http://localhost:8000>. It also works as-is on GitHub Pages.

## Add a script

1. Create `scripts/your_script.py` with:
   - `TITLE`, `BLURB` and `FPS` constants (the site reads these for the card)
   - a `frames()` generator that `yield`s each picture as a string
   - ANSI colour codes like `"\033[91m"` (red) for colour
2. Add `"your_script.py"` to `scripts/library.json`.

Copy the `if __name__ == "__main__":` block from any existing script so it also animates in a terminal.

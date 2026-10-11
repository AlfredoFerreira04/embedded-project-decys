#!/usr/bin/env python3
"""Plot median timing deltas for the 1- and 2-letter candidate combinations.

Usage: plot_timing.py [-o out.png] [-l 1 2] timing_results_1.txt [timing_results_2.txt ...]

Each input file has sections like:
    2 Letter(s), 208 candidates, 7 repetitions, beam 8
    jz 166 us median delta (range -4 to 2381 us)
"""
import argparse
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

HEADER = re.compile(r"^(\d+) Letter\(s\)")
ROW = re.compile(r"^(\S+) (-?\d+) us median delta \(range (-?\d+) to (-?\d+) us\)")


POSITION = re.compile(r"^Position (\d+):")
CAND = re.compile(r"^\s+(\S+): (-?\d+) us median")


def parse(path):
    """Handles both 'N Letter(s)' sections and 'Position N:' sweep blocks.

    For position blocks, the label is the character being varied at that position.
    """
    sections, cur, pos = {}, None, 0
    for line in Path(path).read_text().splitlines():
        if m := POSITION.match(line):
            pos = int(m[1])
            cur = sections.setdefault(pos, [])
        elif pos and cur is not None and (m := CAND.match(line)):
            v = int(m[2])
            cur.append((m[1][pos - 1], v, v, v))
        elif m := HEADER.match(line):
            pos = 0
            cur = sections.setdefault(int(m[1]), [])
        elif cur is not None and (m := ROW.match(line)):
            cur.append((m[1], int(m[2]), int(m[3]), int(m[4])))
    return sections


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("files", nargs="+")
    ap.add_argument("-l", "--lengths", type=int, nargs="+", default=[1, 2])
    ap.add_argument("--range", action="store_true", help="draw min/max error bars")
    ap.add_argument("-o", "--output", default="timing_plot.png")
    args = ap.parse_args()

    panels = [(f, n) for f in args.files for n in args.lengths]
    fig, axes = plt.subplots(
        len(args.files), len(args.lengths), squeeze=False,
        figsize=(7 * len(args.lengths), 4 * len(args.files)),
    )
    for ax, (f, n) in zip(axes.flat, panels):
        rows = sorted(parse(f).get(n, []), key=lambda r: -r[1])
        ax.set_title(f"{Path(f).name}: {n} letter(s)")
        if not rows:
            ax.text(0.5, 0.5, "no data", ha="center", va="center")
            continue
        names = [r[0] for r in rows]
        med = [r[1] for r in rows]
        err = [[r[1] - r[2] for r in rows], [r[3] - r[1] for r in rows]]
        ax.bar(names, med, yerr=err if args.range else None, capsize=2, color="tab:blue", ecolor="gray")
        ax.set_ylabel("median delta (us)")
        ax.tick_params(axis="x", rotation=90)
    fig.tight_layout()
    fig.savefig(args.output, dpi=150)
    print(f"saved {args.output}")


if __name__ == "__main__":
    main()

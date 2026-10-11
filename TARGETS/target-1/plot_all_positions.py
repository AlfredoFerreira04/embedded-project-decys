#!/usr/bin/env python3
"""Plot median timing per candidate letter for every position of the sweep.

Usage: plot_all_positions.py [-o out.png] timing_results_11.txt

Reads 'Position N: <best> (<us> us median)' blocks followed by
'  <candidate>: <us> us median' lines. One subplot per position, letters in
alphabetical order, the winning letter highlighted.
"""
import argparse
import math
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

POSITION = re.compile(r"^Position (\d+): (\S+)")
CAND = re.compile(r"^\s+(\S+): (-?\d+) us median")


def parse(path):
    data, best, pos = {}, {}, 0
    for line in Path(path).read_text().splitlines():
        if m := POSITION.match(line):
            pos = int(m[1])
            data[pos] = []
            best[pos] = m[2][pos - 1]
        elif pos and (m := CAND.match(line)):
            data[pos].append((m[1][pos - 1], int(m[2])))
    return data, best


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("file")
    ap.add_argument("-o", "--output", default="timing_all_positions.png")
    ap.add_argument("--cols", type=int, default=3)
    args = ap.parse_args()

    data, best = parse(args.file)
    if not data:
        raise SystemExit("no 'Position N:' blocks found")

    rows = math.ceil(len(data) / args.cols)
    fig, axes = plt.subplots(rows, args.cols, squeeze=False,
                             figsize=(6 * args.cols, 2.8 * rows))
    for ax in axes.flat:
        ax.axis("off")
    for ax, pos in zip(axes.flat, sorted(data)):
        ax.axis("on")
        items = sorted(data[pos])
        letters = [c for c, _ in items]
        vals = [v for _, v in items]
        colors = ["tab:red" if c == best[pos] else "tab:blue" for c in letters]
        ax.bar(letters, vals, color=colors)
        ax.set_title(f"Position {pos} (best: {best[pos]})")
        ax.set_ylabel("median (us)")
    fig.tight_layout()
    fig.savefig(args.output, dpi=150)
    print(f"saved {args.output}")


if __name__ == "__main__":
    main()

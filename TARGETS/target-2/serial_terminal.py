#!/usr/bin/env python3
"""Interactive serial terminal with one newline sent per entered line."""

from __future__ import annotations

import argparse
import select
import sys

from extract_memory_mapping import PORT, SerialDevice


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", default=PORT)
    args = parser.parse_args()

    with SerialDevice(args.port) as device:
        print(f"Connected to {args.port}. Type a line and press Enter once.")
        print("Press Ctrl-C or Ctrl-D to exit.")

        while True:
            ready, _, _ = select.select([sys.stdin, device.fd], [], [])
            if sys.stdin in ready:
                line = sys.stdin.readline()
                if not line:
                    return
                device.write(line.rstrip("\r\n").encode("ascii") + b"\n")
            if device.fd in ready:
                received = device.read()
                if received:
                    sys.stdout.write(received.decode("replace"))
                    sys.stdout.flush()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nDisconnected.")

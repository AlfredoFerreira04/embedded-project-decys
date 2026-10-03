#!/usr/bin/env python3
"""Send exact lines to the target serial device without forwarding keypresses."""

from __future__ import annotations

import argparse
import sys

from extract_memory_mapping import PORT, SerialDevice


def send_line(device: SerialDevice, value: str) -> None:
    device.write(value.encode("ascii") + b"\n")
    print(f"Sent: {value!r}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("value", nargs="?", help="send one value and exit")
    parser.add_argument("--port", default=PORT)
    args = parser.parse_args()

    with SerialDevice(args.port) as device:
        if args.value is not None:
            send_line(device, args.value)
            return

        print("Type one value per line. Each line sends exactly one newline.")
        print("Press Ctrl-D to exit.")
        for value in sys.stdin:
            send_line(device, value.rstrip("\r\n"))


if __name__ == "__main__":
    main()

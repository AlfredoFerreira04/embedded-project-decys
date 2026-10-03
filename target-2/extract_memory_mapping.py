#!/usr/bin/env python3
"""Log in to target 1 and dump all three memory locations."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import select
import termios
import time

PORT = "/dev/ttyUSB0"
BAUD_RATE = 115200
PASSWORD = "danprzjzumfgn"
MENU_MARKER = b"DEVELOPMENT MENU"
LOCATION_MARKER = b"MEMORY LOCATION TO PRINT"
DUMP_STOP_MARKER = b"Press Enter to stop"


class SerialDevice:
    """Small standard-library serial client for Linux."""

    def __init__(self, port: str, timeout: float = 0.2) -> None:
        self.timeout = timeout
        self.fd = os.open(port, os.O_RDWR | os.O_NOCTTY)
        settings = termios.tcgetattr(self.fd)
        settings[0] &= ~(
            termios.BRKINT
            | termios.ICRNL
            | termios.INPCK
            | termios.ISTRIP
            | termios.IXON
        )
        settings[1] &= ~termios.OPOST
        settings[2] &= ~(termios.CSIZE | termios.PARENB)
        settings[2] |= termios.CS8
        settings[3] &= ~(termios.ECHO | termios.ICANON | termios.IEXTEN | termios.ISIG)
        settings[6][termios.VMIN] = 0
        settings[6][termios.VTIME] = 2
        settings[4] = termios.B115200
        settings[5] = termios.B115200
        settings[2] |= termios.CLOCAL | termios.CREAD
        termios.tcsetattr(self.fd, termios.TCSANOW, settings)

    def __enter__(self) -> "SerialDevice":
        return self

    def __exit__(self, *_: object) -> None:
        os.close(self.fd)

    def read(self) -> bytes:
        ready, _, _ = select.select([self.fd], [], [], self.timeout)
        return os.read(self.fd, 4096) if ready else b""

    def write(self, data: bytes) -> None:
        view = memoryview(data)
        while view:
            written = os.write(self.fd, view)
            view = view[written:]


def read_until(
    device: SerialDevice, marker: bytes, timeout: float
) -> bytes:
    """Read and return data through marker, or fail with the partial output."""
    deadline = time.monotonic() + timeout
    received = bytearray()
    while marker not in received:
        if time.monotonic() >= deadline:
            preview = bytes(received).decode("replace")
            raise TimeoutError(
                f"Timed out waiting for {marker!r}. Received:\n{preview}"
            )
        chunk = device.read()
        if chunk:
            received.extend(chunk)
    return bytes(received)


def send_line(device: SerialDevice, value: str) -> None:
    device.write(value.encode("ascii") + b"\n")


def dump_memory(
    device: SerialDevice, location: int, dump_seconds: float
) -> bytes:
    """Select a location, stream it briefly, then send one stop newline."""
    send_line(device, "1")
    menu_response = read_until(device, LOCATION_MARKER, timeout=5)
    send_line(device, str(location))
    dump_response = read_until(device, DUMP_STOP_MARKER, timeout=5)
    time.sleep(dump_seconds)
    device.write(b"\n")
    dump_response += read_until(device, MENU_MARKER, timeout=30)
    return menu_response + dump_response


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", default=PORT)
    parser.add_argument("--output-dir", type=Path, default=Path("memory_dumps"))
    parser.add_argument(
        "--dump-seconds",
        type=float,
        default=10,
        help="seconds to stream each memory dump before sending one Enter",
    )
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)

    with SerialDevice(args.port) as device:
        read_until(device, b"Enter password", timeout=10)
        send_line(device, PASSWORD)
        read_until(device, MENU_MARKER, timeout=10)

        for location in range(3):
            output = dump_memory(device, location, args.dump_seconds)
            destination = args.output_dir / f"memory_{location}.txt"
            destination.write_bytes(output)
            print(f"Saved memory location {location} to {destination}")


if __name__ == "__main__":
    main()
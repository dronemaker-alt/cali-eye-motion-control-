#!/usr/bin/env python3
"""Guided Cali-Eye rotary-stage bench test for PD-Stepper Serial_Control firmware."""

from __future__ import annotations

import argparse
import csv
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import serial


FLOAT_LINE = re.compile(r"^\s*([-+]?(?:\d+(?:\.\d*)?|\.\d+))\s*$")


class PDStepper:
    def __init__(self, port: str, baud: int = 115200, timeout: float = 0.15):
        self.serial = serial.Serial(port, baudrate=baud, timeout=timeout)
        time.sleep(1.0)
        self.serial.reset_input_buffer()

    def close(self) -> None:
        self.serial.close()

    def command(self, text: str, overall_timeout: float = 2.0) -> list[str]:
        self.serial.reset_input_buffer()
        self.serial.write((text.strip() + "\n").encode("ascii"))
        self.serial.flush()

        lines: list[str] = []
        deadline = time.monotonic() + overall_timeout
        quiet_deadline = None
        while time.monotonic() < deadline:
            raw = self.serial.readline()
            if raw:
                lines.append(raw.decode("utf-8", errors="replace").strip())
                quiet_deadline = time.monotonic() + 0.25
            elif quiet_deadline is not None and time.monotonic() >= quiet_deadline:
                break
        return lines

    def angle(self) -> tuple[float, list[str]]:
        lines = self.command("get_angle")
        for line in reversed(lines):
            match = FLOAT_LINE.match(line)
            if match:
                return float(match.group(1)), lines
        raise RuntimeError(f"No numeric angle returned. Raw response: {lines!r}")


def require_enter(message: str) -> None:
    input(f"\n{message}\nPress Enter to continue, or Ctrl-C to stop: ")


def show(command: str, lines: list[str]) -> None:
    print(f"\n> {command}")
    if lines:
        for line in lines:
            print(line)
    else:
        print("[no response]")


def run_move(
    node: PDStepper,
    writer: csv.DictWriter,
    move_deg: float,
    speed_deg_s: float,
    settle_s: float,
    tolerance_deg: float,
) -> bool:
    require_enter(
        f"Ready for installed-stage move {move_deg:+.1f} deg. "
        "Confirm the travel path and coupling marks are clear."
    )
    start, raw_start = node.angle()
    command = f"deg_rel={move_deg}"
    response = node.command(command)
    travel_s = abs(move_deg) / max(speed_deg_s, 0.1)
    time.sleep(travel_s + settle_s)
    end, raw_end = node.angle()

    measured = end - start
    error = measured - move_deg
    passed = abs(error) <= tolerance_deg
    print(
        f"Command {move_deg:+.3f} deg | measured {measured:+.3f} deg | "
        f"error {error:+.3f} deg | {'PASS' if passed else 'FAIL'}"
    )

    writer.writerow(
        {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "event": "move",
            "command_deg": f"{move_deg:.6f}",
            "start_deg": f"{start:.6f}",
            "end_deg": f"{end:.6f}",
            "measured_delta_deg": f"{measured:.6f}",
            "error_deg": f"{error:.6f}",
            "tolerance_deg": f"{tolerance_deg:.6f}",
            "result": "PASS" if passed else "FAIL",
            "raw": repr(
                {
                    "start": raw_start,
                    "command": response,
                    "end": raw_end,
                }
            ),
        }
    )
    return passed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Guided USB bench test for the installed Cali-Eye rotary stage."
    )
    parser.add_argument("--port", required=True, help="Serial port, e.g. COM5 or /dev/ttyACM0")
    parser.add_argument("--log", default="rotary-stage-test.csv", help="CSV evidence file")
    parser.add_argument("--voltage", type=int, default=12)
    parser.add_argument("--current", type=int, default=10, dest="current_percent")
    parser.add_argument("--speed", type=float, default=30.0, dest="speed_deg_s")
    parser.add_argument("--steps-per-rev", type=int, default=200)
    parser.add_argument("--microsteps", type=int, default=64)
    parser.add_argument("--tolerance", type=float, default=2.0, dest="tolerance_deg")
    parser.add_argument("--settle", type=float, default=1.0, dest="settle_s")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    log_path = Path(args.log)
    fields = [
        "timestamp_utc",
        "event",
        "command_deg",
        "start_deg",
        "end_deg",
        "measured_delta_deg",
        "error_deg",
        "tolerance_deg",
        "result",
        "raw",
    ]

    print("Cali-Eye Motion Node bench test CMN-BT-001")
    print("Target: installed rotary sensor stage")
    print(f"Port: {args.port}")
    print(f"Evidence: {log_path.resolve()}")

    node = PDStepper(args.port)
    passed_moves: list[bool] = []
    try:
        show("enable=0", node.command("enable=0"))
        show("help", node.command("help"))
        show("values", node.command("values"))

        idle = []
        for _ in range(3):
            angle, raw = node.angle()
            idle.append(angle)
            print(f"Idle encoder angle: {angle:.3f} deg | raw={raw!r}")
            time.sleep(0.25)
        print(f"Idle encoder spread: {max(idle) - min(idle):.3f} deg")

        before, _ = node.angle()
        require_enter("Driver is disabled. Rotate the installed stage slowly in its intended positive direction.")
        after, _ = node.angle()
        manual_delta = after - before
        print(f"Manual measured change: {manual_delta:+.3f} deg")
        if manual_delta <= 0:
            print("Direction convention does not agree. Record and correct mapping before acceptance.")

        print("\nProposed low-energy configuration:")
        print(
            f"{args.voltage} V, {args.current_percent}% current, "
            f"{args.speed_deg_s} deg/s, {args.microsteps} microsteps"
        )
        arm = input("Type ARM to configure and enable the installed stage: ").strip()
        if arm != "ARM":
            print("Not armed. Leaving the driver disabled.")
            return 2

        configuration = [
            f"voltage={args.voltage}",
            f"current={args.current_percent}",
            f"speed={args.speed_deg_s}",
            f"steps_per_rev={args.steps_per_rev}",
            f"microsteps={args.microsteps}",
            "closed_loop_type=MOVE_FROM_ENC",
            "enable=1",
        ]
        for command in configuration:
            show(command, node.command(command))

        log_path.parent.mkdir(parents=True, exist_ok=True)
        new_file = not log_path.exists() or log_path.stat().st_size == 0
        with log_path.open("a", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            if new_file:
                writer.writeheader()
            for move in (5.0, -5.0, 30.0, -30.0, 5.0, -5.0, 5.0, -5.0):
                passed_moves.append(
                    run_move(
                        node,
                        writer,
                        move,
                        args.speed_deg_s,
                        args.settle_s,
                        args.tolerance_deg,
                    )
                )

            show("enable=0", node.command("enable=0"))
            displaced_start, _ = node.angle()
            require_enter("Recovery check: move the disabled stage by hand about 10 degrees.")
            displaced_end, raw = node.angle()
            displacement = displaced_end - displaced_start
            print(f"Disabled manual displacement: {displacement:+.3f} deg")
            writer.writerow(
                {
                    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                    "event": "disabled_manual_displacement",
                    "command_deg": "",
                    "start_deg": f"{displaced_start:.6f}",
                    "end_deg": f"{displaced_end:.6f}",
                    "measured_delta_deg": f"{displacement:.6f}",
                    "error_deg": "",
                    "tolerance_deg": "",
                    "result": "OBSERVED",
                    "raw": repr(raw),
                }
            )

        if all(passed_moves):
            print("\nMOVE CRITERIA PASS. Complete coupling, power, reset and observation checks in CMN-BT-001.")
            return 0
        print("\nONE OR MORE MOVES FAILED TOLERANCE. Retain the CSV; this is useful evidence.")
        return 1
    except KeyboardInterrupt:
        print("\nTest interrupted.")
        return 130
    finally:
        try:
            node.command("enable=0")
        except Exception:
            pass
        node.close()


if __name__ == "__main__":
    sys.exit(main())

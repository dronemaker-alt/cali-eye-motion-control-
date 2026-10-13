# Cali-Eye Motion Control

Cali-Eye is the robotic inspection and bench-development project within **Æsir Autonomous Systems**, whose broader pantheon spans autonomous aircraft, ground vehicles, maritime systems, and robotic inspection.

This repository develops Cali-Eye's distributed smart motion-control architecture. Cali-Eye is intended to support component inspection, diagnostics, and engineering work across that pantheon.

## Scope and verification status

The repository remains focused on Cali Motion Node hardware, firmware, host interfaces, architecture documentation, test plans, and bench evidence. Reuse of its motion-control approach across other Æsir platforms is a future possibility, not a verified capability.

The assembled workstation and operational Lenovo/Linux Mint XFCE console are documented in the [October 11 bench evidence record](docs/evidence/2026-10-11-bench-assembly.md). Physical motion, encoder-based position verification, host-to-node control, automated scanning, and vision integration remain **unverified**; motion and vision integration are pending. The broader program scope does not establish autonomous operation or integration with aircraft, ground vehicles, or maritime systems.

## Reference architecture: PD-Stepper

Upstream project: **joshr120/PD-Stepper**

https://github.com/joshr120/PD-Stepper

PD-Stepper is being retained as a design/reference source for the Cali-Eye motion system. Preserve upstream attribution and licensing when incorporating upstream material.

### Architecture of interest

- ESP32-S3 local motion controller
- TMC2209 stepper driver
- AS5600 magnetic position feedback
- USB-C / USB-PD power architecture
- Distributed per-axis intelligence
- Local closed-loop position verification rather than relying solely on commanded step counts

## Cali-Eye direction

The intended architecture treats each motion axis as a smart actuator/node. A Pi/host controller would issue high-level position and scan commands while each node would handle local motion, feedback, limits, and telemetry. These responsibilities are design targets; their physical implementation and integration remain unverified.

Initial target axes (planned; physical motion remains unverified):

- X gantry
- Y / sensor positioning
- Z compact linear actuator
- Rotary sensor stage

Candidate Cali-specific additions include CAN or RS-485 networking, home/limit inputs, motor/driver temperature monitoring, current/voltage telemetry, standardized connectors, fault reporting, and integration with the Cali-Eye command/inspection stack.

## Repository strategy

Keep upstream PD-Stepper material identifiable and attributable. Develop Cali-specific hardware/firmware separately so upstream reference material can be compared against the evolving Cali Motion Node design.


## Repository layout

- `reference/PD-Stepper/` — complete upstream snapshot, preserved unchanged
- `hardware/cali-motion-node/` — Cali Motion Node electronics and mechanical integration
- `firmware/` — Cali-specific node firmware and host interfaces
- `docs/` — architecture decisions, interface definitions, and test plans

See `reference/PD-Stepper-UPSTREAM.md` for snapshot provenance and update procedure. PD-Stepper is GPL-3.0 licensed; retain its license and attribution in any derivative work.

## Bench assembly — October 11, 2026

The Cali-Eye bench is assembled and its Lenovo console is operational under Linux Mint XFCE. Motion and vision integration remain pending.

![Cali-Eye bench structure and Lenovo console](docs/evidence/2026-10-11-bench-assembly/1000040173.jpg)

[View all five original bench photographs and the evidence record](docs/evidence/2026-10-11-bench-assembly.md).

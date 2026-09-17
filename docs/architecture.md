# Motion-control architecture

## System boundary

The Cali-Eye host coordinates inspection jobs and issues high-level motion commands. Each axis node owns real-time motor control, encoder observation, limits, telemetry, and local fault response.

Initial nodes are X gantry, Y/sensor position, Z compact linear actuator, and rotary sensor stage.

## Design principle

Command, observe, and verify. A completed move requires measured position within tolerance—not merely the expected number of step pulses.

## Decisions still required

- CAN versus isolated RS-485, or support for both
- Network power topology and connector family
- Encoder placement and coupling-error limits
- Homing and absolute-position recovery strategy
- Maximum axis voltage/current and cooling requirements
- Host protocol and time synchronization
- Following-error thresholds and fault-recovery policy

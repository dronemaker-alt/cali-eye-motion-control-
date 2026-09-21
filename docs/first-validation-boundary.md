# First hardware/software validation boundary

## Boundary statement

Test zero validates this complete path:

```text
bench tool -> USB CDC -> ESP32-S3 command parser -> TMC2209 -> motor/coupling
                                                        |
                                             AS5600 measured angle
                                                        |
                                      USB response -> CSV evidence
```

The physical endpoint is the installed Cali-Eye rotary sensor stage, not an unloaded motor.

## Inside the boundary

- Host opens the selected USB serial port.
- Node accepts a command and reports its result.
- Power-good gating prevents an underpowered driver enable.
- TMC2209 configuration and enable control are functional.
- Step/direction motion reaches the motor.
- Coupling transfers motion to the rotary stage.
- AS5600 produces continuous signed angle feedback.
- Host compares commanded and measured change and records the result.
- Disable, manual displacement and measured-position recovery are demonstrated.

## Outside the boundary

- RS-485 transceiver, addressing, termination and collision handling
- Multi-node synchronization
- X/Y/Z linear accuracy
- Limit-switch and index-sensor integration
- Thermal endurance and maximum load
- Cable-chain EMI performance
- Unattended recovery
- Final connector and PCB decisions

## Why this boundary comes first

A USB-only parser test proves software but not motion. An unloaded motor test proves electronics but not the coupling or installed encoder geometry. Starting with the rotary stage includes the first real mechanism while keeping the measurement model native to the AS5600.

## Pass/fail measurements

Default provisional criteria:

| Measurement | Pass criterion |
| --- | --- |
| Encoder continuity | No jump larger than 180 deg between adjacent reads during slow manual rotation |
| Direction agreement | Positive and negative commands produce matching measured signs |
| Final position error | Absolute error <= 2.0 deg after each test move |
| Short-move repeatability | Spread <= 1.0 deg across repeated +5/-5 deg moves |
| Disable behavior | No commanded holding torque; angle remains readable |
| Recovery | After disabled manual displacement, next move is calculated from measured angle |
| Reliability | No reset, power-good dropout or unexplained fault during the sequence |

The tolerances are intentionally generous for first motion. Tightening them comes after backlash, magnet alignment, coupling compliance and load are measured.

## Evidence record

Each run should retain:

- date/time and operator
- board and firmware identity or commit
- motor part number
- USB-PD source and requested voltage
- driver-current percentage
- stage/coupling configuration
- commanded angle change
- measured start/end angle
- error and pass/fail result
- observations, photos and any scope/logic-analyzer captures

Link the retained evidence from the project Decision/Development Log.

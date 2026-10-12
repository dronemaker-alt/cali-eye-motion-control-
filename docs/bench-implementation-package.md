# Bench implementation package v0

This package turns the preserved PD-Stepper reference into a repeatable first Cali-Eye motion-node bench test.

## Selected direction

- First service transport: USB CDC serial at 115200 baud
- Later field transport: isolated RS-485 multidrop
- First installed axis: Cali-Eye rotary sensor stage
- Initial hardware profile: PD-Stepper-compatible ESP32-S3, TMC2209 and AS5600
- Upstream files under `reference/PD-Stepper/` remain unchanged

The rotary stage is the first target because the AS5600 directly observes rotary motion. Passing this test does not prove X/Y/Z carriage position; those axes will need load-side feedback or a separately justified coupling-error budget.

## Package contents

- [Motion-node interface](motion-node-interface-v0.md)
- [Hardware/software boundary](first-validation-boundary.md)
- [Rotary-stage bench sequence](rotary-stage-bench-test.md)
- `tools/cali_motion_bench.py` — guided USB serial test and CSV logger
- `tools/requirements.txt` — host dependency

## Firmware used for test zero

Flash:

`reference/PD-Stepper/Software/Serial_Control/Serial_Control.ino`

Required Arduino dependency:

- janelia-arduino/TMC2209

This is a reference bring-up image, not the final Cali Motion Node firmware. It is acceptable for test zero because it already exercises USB serial, the TMC2209, AS5600, USB-PD selection and power-good gating.

## Quick start

1. Flash the reference Serial Control sketch.
2. Attach the AS5600 magnet and confirm free mechanical rotation.
3. Install the motor on the rotary stage with hard stops clear.
4. Start with 12 V, 10% driver current and 30 deg/s.
5. Install the host dependency: `python -m pip install -r tools/requirements.txt`.
6. Run: `python tools/cali_motion_bench.py --port PORT --log rotary-stage-test.csv`.
7. Follow the prompts and retain the CSV with the node, motor, stage and coupling configuration.

## Exit criteria

Test zero passes when:

- USB commands and responses are repeatable.
- Manual shaft rotation produces signed, continuous encoder motion.
- Positive and negative motor commands agree with measured direction.
- Four installed-stage moves complete within the configured tolerance.
- Driver disable removes commanded torque.
- Moving the disabled stage by hand changes the measured angle.
- A subsequent position command uses measured position rather than assuming prior step count.
- No unexplained reset, power-good loss, stall, mechanical strike or encoder discontinuity occurs.

A pass authorizes development of the native Cali protocol/state machine. It does not authorize unattended motion or claim gantry accuracy.

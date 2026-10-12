# Rotary-stage bench test CMN-BT-001

## Objective

Demonstrate controlled, measured motion of one installed Cali-Eye rotary sensor stage using USB serial and the preserved PD-Stepper Serial Control firmware.

## Configuration

Initial values:

- Requested bus voltage: 12 V
- Driver current: 10%
- Position speed: 30 deg/s
- Microsteps: 64
- Steps/revolution: match the installed motor, normally 200
- Closed-loop type: `MOVE_FROM_ENC`
- Position tolerance: 2.0 deg
- Test moves: +5, -5, +30, -30 deg

Increase current only if the installed stage cannot move cleanly. Record every change.

## Sequence

### A. Power-off inspection

1. Record board, motor, stage, magnet and coupling identity.
2. Confirm the stage can complete every planned move without reaching a hard stop.
3. Confirm the encoder magnet is centered and retained.
4. Confirm the stage and encoder rotate together without visible slip.
5. Place an index mark across both sides of the coupling so slip is visible.

### B. Communications with torque disabled

1. Connect USB and open 115200 baud.
2. Send `help`, then `values`.
3. Send `enable=0`.
4. Send `get_angle` three times without moving the stage.
5. Record idle measurement spread.

### C. Encoder observation

1. With the driver disabled, rotate the installed stage slowly in the positive direction.
2. Read the angle and record the change.
3. Rotate back through the starting position and slightly negative.
4. Confirm continuous signed readings across the encoder wrap.
5. If sign is opposite the intended stage convention, record the needed `mappingDirection`; do not conceal a mechanical labeling error in software.

### D. Low-energy motion

1. Return the stage to the marked start region.
2. Set 12 V, 10% current, 30 deg/s and the correct motor steps/revolution.
3. Set `closed_loop_type=MOVE_FROM_ENC`.
4. Enable the driver.
5. Command +5 deg and compare start, end and commanded delta.
6. Command -5 deg and compare again.
7. Stop on unexpected direction, binding, coupling slip or encoder disagreement.

### E. Installed-stage acceptance moves

Run and log:

1. +5 deg
2. -5 deg
3. +30 deg
4. -30 deg
5. Repeat +5/-5 deg twice for repeatability

After each move, allow settling, obtain `get_angle`, calculate measured delta and compare it with the 2 deg provisional tolerance.

### F. Measured-position recovery

1. Send `enable=0`.
2. Move the stage by hand approximately 10 deg.
3. Read and record the new angle.
4. Re-enable the driver.
5. Command a small return move.
6. Confirm the result is based on the measured encoder position, not the previously commanded step count.

### G. Closeout

1. Send `enable=0`.
2. Inspect the coupling index mark.
3. Record resets, stalls, noise, heating, power-good changes and mechanical observations.
4. Save the CSV and supporting images.
5. Mark the run PASS only if every criterion in `first-validation-boundary.md` is met.

## Stop conditions

Stop the run for wrong direction, an approaching hard stop, loss of encoder continuity, coupling slip, repeated missed motion, node reset or loss of power-good. These are test findings, not invitations to solve the problem by increasing current until the mechanism develops an opinion.

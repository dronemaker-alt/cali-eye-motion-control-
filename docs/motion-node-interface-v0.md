# Cali Motion Node interface v0

## Purpose

Version 0 separates the immediately usable PD-Stepper bench interface from the durable Cali-Eye node contract. USB serial is the first service interface. Isolated RS-485 is the planned multidrop transport; it must carry the same command and state model rather than inventing a second controller personality.

## Transport v0A: reference compatibility

The first bench test uses the upstream Serial Control sketch unchanged.

- USB CDC serial
- 115200 baud
- 8 data bits, no parity, 1 stop bit
- UTF-8/ASCII commands terminated by newline
- One outstanding command at a time
- Host waits for the response before sending the next command

Minimum command subset:

| Command | Use in Cali-Eye test zero |
| --- | --- |
| `help` | Confirm parser and command set |
| `values` | Capture configuration |
| `enable=0/1` | Remove or apply motor torque |
| `voltage=12` | Select conservative initial PD voltage |
| `current=N` | Set conservative initial driver current |
| `speed=N` | Set position-move speed in deg/s |
| `mappingDirection=0/1` | Align motor and encoder sign |
| `closed_loop_type=MOVE_FROM_ENC` | Base each move on measured angle |
| `deg_rel=N` | Small signed test move |
| `get_angle` | Read accumulated encoder angle |

Reference responses are human-readable and are not a stable machine API. The bench tool therefore treats the final numeric line returned by `get_angle` as the measurement and records raw text for traceability.

## Transport v0B: native Cali contract

The first Cali-specific firmware shall preserve the following semantics on both USB and RS-485:

- Every command has a sequence number.
- Every accepted command receives an acknowledgement.
- Every rejected command returns a machine-readable fault code.
- Position commands are expressed in axis engineering units, not raw microsteps.
- Completion means measured position is within tolerance and velocity has settled.
- Node state and faults can be queried without causing motion.
- Disable and stop commands are idempotent.
- A communications timeout never initiates motion.
- Persistent settings are separate from ordinary motion commands.
- On RS-485, node address and frame integrity are mandatory.

Proposed line-oriented service representation:

```text
CMN1 seq=41 node=rotary verb=STATUS
CMN1 seq=42 node=rotary verb=MOVE_REL pos_deg=5.0 vel_deg_s=30 tol_deg=2.0
CMN1 seq=43 node=rotary verb=STOP
```

Response classes:

```text
ACK seq=42 state=MOVING
DONE seq=42 pos_cmd_deg=5.000 pos_meas_deg=4.82 error_deg=-0.18
ERR seq=42 code=LIMIT_ACTIVE state=FAULT
TEL node=rotary state=IDLE pos_deg=4.82 vbus_v=12.1
```

The exact framing and CRC for RS-485 remain a v1 decision. The command/state semantics above are fixed by test zero unless bench evidence shows they are wrong.

## Node state model

- `BOOT`: outputs safe; driver disabled
- `DISABLED`: communications and sensing active; no commanded torque
- `READY`: power, encoder and limits valid
- `MOVING`: command executing
- `SETTLING`: target reached by command estimate; measured result being checked
- `IDLE`: enabled and holding, with no active move
- `FAULT`: local inhibit latched until the fault is reported and explicitly cleared

## Authority split

The host owns job planning, scan sequencing and coordination among axes. The node owns step timing, driver enable, encoder observation, limit response, following-error detection and local stopping.

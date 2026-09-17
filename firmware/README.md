# Cali Motion Node firmware

Planned firmware responsibilities:

- Accept high-level absolute-position, relative-move, velocity, and scan commands
- Close the local verification loop using encoder feedback
- Execute homing and limit handling without host pulse generation
- Report commanded position, measured position, following error, current, voltage, temperature, and faults
- Stop locally and predictably if communications, limits, feedback, or power fail
- Expose a documented protocol for the Cali-Eye host and bench tools

Initial implementation decisions—framework, transport, message schema, and axis state machine—remain open and should be recorded under `docs/` before hardware is frozen.

# Cali Motion Node hardware

Development area for the Cali-Eye distributed smart-axis controller.

## Baseline under evaluation

- ESP32-S3 local controller
- TMC2209 stepper driver
- AS5600 absolute magnetic encoder
- USB-C Power Delivery input
- CAN and/or isolated RS-485 multidrop communications
- Dedicated home, minimum-limit, and maximum-limit inputs
- Motor, driver, bus-voltage, and current telemetry
- Standardized power, network, sensor, and service connectors

Hardware here is Cali-specific and must remain separate from the unchanged PD-Stepper snapshot in `reference/PD-Stepper/`.

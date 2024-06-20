# RPI cable tester concept
## Overview
This document provides a comprehensive guide to implementing a cable tester using a Raspberry Pi, MCP3008 ADC, and optocouplers for signal isolation. The tester is designed to validate the connectivity and voltage levels of three different connectors. It ensures safe operation by using optocouplers to step down high voltage signals to levels acceptable by the Raspberry Pi.

## Hardware Components
* Raspberry Pi
* MCP3008 ADC
* Optocouplers (PC817)
* LEDs
* Resistors
* Breadboard and connecting wires
* Schematic
The schematic includes connections for each connector to the Raspberry Pi via optocouplers for high voltage isolation and the MCP3008 for analog-to-digital conversion. The optocouplers ensure that signals above 5V do not directly interface with the Raspberry Pi.

## System Setup
### 1. Raspberry Pi SPI Setup:

* Enable SPI interface on the Raspberry Pi through the Raspberry Pi Configuration tool or by adding dtparam=spi=on to the /boot/config.txt file.
* Connect MCP3008 to the Raspberry Pi SPI pins:
- VDD to 3.3V
- VREF to 3.3V
- AGND to GND
- DGND to GND
- CLK to GPIO 11 (SCLK)
- DOUT to GPIO 9 (MISO)
- DIN to GPIO 10 (MOSI)
- CS to GPIO 8 (CE0)

### 2. Optocoupler Connections:

* High voltage input (42V or 12V) connected to the input side of the optocoupler.
* Output side of the optocoupler connected to a GPIO pin on the Raspberry Pi via a current-limiting resistor.
* Ensure proper biasing of the optocoupler input with appropriate resistors to handle 42V and 12V inputs.

### 3. MCP3008 ADC Connections:

* MCP3008 channels connected to the CAN High and CAN Low signal lines.
* Ensure proper voltage levels (between 2.5-3.5V for CAN High and 1.5-2.5V for CAN Low).

## Testing Procedure
### 1. Power Up:

* Ensure all connections are properly made.
* Power up the Raspberry Pi and ensure the MCP3008 and optocouplers are properly powered.

### 2. ## Run the Script:

Execute the script on the Raspberry Pi using:
```
python3 cable_tester.py
```

### 3. Observe Outputs:

* The script will print the state of each pin for each connector.
* LEDs will indicate the pass/fail status of each connector.

### 4. Validation:

* Ensure that the printed states match the expected values.
* If all tests pass, the respective LED for each connector will light up.
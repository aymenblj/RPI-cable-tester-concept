import spidev
import RPi.GPIO as GPIO
import time

# Setup SPI for MCP3008
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

# Function to read from MCP3008
def read_channel(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

# Setup GPIO
GPIO.setmode(GPIO.BCM)

# Connector 1 pins
connector1_LV_12v = 5
connector1_LIGTH_OUT = 6
connector1_HV_42v = 12
connector1_can_high_channel = 0
connector1_can_low_channel = 1
connector1_led_pin = 11

# Connector 2 pins
connector2_HV_42v = 19
connector2_LV_12v = 13
connector2_LIGTH_OUT = 16
connector2_can_high_channel = 2
connector2_can_low_channel = 3
connector2_led_pin = 13

# Connector 3 pins
connector3_LV_12v = 20
connector3_HV_42v = 26
connector3_LIGTH_OUT = 21
connector3_can_high_channel = 4
connector3_can_low_channel = 5
connector3_led_pin = 12

# Setup GPIO pins for connectors
GPIO.setup(connector1_LV_12v, GPIO.IN)
GPIO.setup(connector1_LIGTH_OUT, GPIO.IN)
GPIO.setup(connector1_HV_42v, GPIO.IN)
GPIO.setup(connector1_led_pin, GPIO.OUT)

GPIO.setup(connector2_HV_42v, GPIO.IN)
GPIO.setup(connector2_LV_12v, GPIO.IN)
GPIO.setup(connector2_LIGTH_OUT, GPIO.IN)
GPIO.setup(connector2_led_pin, GPIO.OUT)

GPIO.setup(connector3_LV_12v, GPIO.IN)
GPIO.setup(connector3_HV_42v, GPIO.IN)
GPIO.setup(connector3_LIGTH_OUT, GPIO.IN)
GPIO.setup(connector3_led_pin, GPIO.OUT)

# Function to read GPIO pin
def read_gpio(pin):
    return GPIO.input(pin)

# Read analog values
def read_analog(channel):
    value = read_channel(channel)
    voltage = (value * 5.0) / 1023  # Adjusted for 5V reference
    return voltage

# Main test function
def harness_test():
    all_tests_passed = True

    # Test Connector 1
    print("Testing Connector 1...")
    pin_LV_12v_state1 = read_gpio(connector1_LV_12v)
    pin_LIGTH_OUT_state1 = read_gpio(connector1_LIGTH_OUT)
    pin_HV_12v_state1 = read_gpio(connector1_HV_42v)
    can_high_voltage1 = read_analog(connector1_can_high_channel)
    can_low_voltage1 = read_analog(connector1_can_low_channel)

    print(f"Connector 1 Pin 3 (should be HIGH): {pin_LV_12v_state1}")
    print(f"Connector 1 Pin 4 (should be LOW): {pin_LIGTH_OUT_state1}")
    print(f"Connector 1 Pin 5 (should be HIGH): {pin_HV_12v_state1}")
    print(f"Connector 1 CAN High Voltage: {can_high_voltage1:.2f}V")
    print(f"Connector 1 CAN Low Voltage: {can_low_voltage1:.2f}V")

    try:
        assert pin_LV_12v_state1 == GPIO.HIGH, "Connector 1 Pin 3 is not HIGH"
        assert pin_LIGTH_OUT_state1 == GPIO.LOW, "Connector 1 Pin 4 is not LOW"
        assert pin_HV_12v_state1 == GPIO.HIGH, "Connector 1 Pin 5 is not HIGH"
        assert 2.5 <= can_high_voltage1 <= 3.5, "Connector 1 CAN High voltage out of range"
        assert 1.5 <= can_low_voltage1 <= 2.5, "Connector 1 CAN Low voltage out of range"
        print("Connector 1 test passed!")
        GPIO.output(connector1_led_pin, GPIO.HIGH)  # Turn on the LED to indicate pass
    except AssertionError as e:
        print(f"Connector 1 test failed: {e}")
        GPIO.output(connector1_led_pin, GPIO.LOW)  # Turn off the LED on failure
        all_tests_passed = False

    # Test Connector 2
    print("Testing Connector 2...")
    pin_HV_42v_state2 = read_gpio(connector2_HV_42v)
    pin_LV_12v_state2 = read_gpio(connector2_LV_12v)
    pin_LIGTH_state2 = read_gpio(connector2_LIGTH_OUT)
    can_high_voltage2 = read_analog(connector2_can_high_channel)
    can_low_voltage2 = read_analog(connector2_can_low_channel)

    print(f"Connector 2 Pin 1 (should be HIGH): {pin_HV_42v_state2}")
    print(f"Connector 2 Pin 4 (should be HIGH): {pin_LV_12v_state2}")
    print(f"Connector 2 Pin 6 (should be LOW): {pin_LIGTH_state2}")
    print(f"Connector 2 CAN High Voltage: {can_high_voltage2:.2f}V")
    print(f"Connector 2 CAN Low Voltage: {can_low_voltage2:.2f}V")

    try:
        assert pin_HV_42v_state2 == GPIO.HIGH, "Connector 2 Pin 1 is not HIGH"
        assert pin_LV_12v_state2 == GPIO.HIGH, "Connector 2 Pin 4 is not HIGH"
        assert pin_LIGTH_state2 == GPIO.LOW, "Connector 2 Pin 6 is not LOW"
        assert 2.5 <= can_high_voltage2 <= 3.5, "Connector 2 CAN High voltage out of range"
        assert 1.5 <= can_low_voltage2 <= 2.5, "Connector 2 CAN Low voltage out of range"
        print("Connector 2 test passed!")
        GPIO.output(connector2_led_pin, GPIO.HIGH)  # Turn on the LED to indicate pass
    except AssertionError as e:
        print(f"Connector 2 test failed: {e}")
        GPIO.output(connector2_led_pin, GPIO.LOW)  # Turn off the LED on failure
        all_tests_passed = False

    # Test Connector 3
    print("Testing Connector 3...")
    pin_LV_12v_state3 = read_gpio(connector3_LV_12v)
    pin_HV_42v_state3 = read_gpio(connector3_HV_42v)
    pin_LIGTH_state3 = read_gpio(connector3_LIGTH_OUT)
    can_high_voltage3 = read_analog(connector3_can_high_channel)
    can_low_voltage3 = read_analog(connector3_can_low_channel)

    print(f"Connector 3 Pin 1 (should be HIGH): {pin_LV_12v_state3}")
    print(f"Connector 3 Pin 2 (should be HIGH): {pin_HV_42v_state3}")
    print(f"Connector 3 Pin 3 (should be LOW): {pin_LIGTH_state3}")
    print(f"Connector 3 CAN High Voltage: {can_high_voltage3:.2f}V")
    print(f"Connector 3 CAN Low Voltage: {can_low_voltage3:.2f}V")

    try:
        assert pin_LV_12v_state3 == GPIO.HIGH, "Connector 3 Pin 1 is not HIGH"
        assert pin_HV_42v_state3 == GPIO.HIGH, "Connector 3 Pin 2 is not HIGH"
        assert pin_LIGTH_state3 == GPIO.LOW, "Connector 3 Pin 3 is not LOW"
        assert 2.5 <= can_high_voltage3 <= 3.5, "Connector 3 CAN High voltage out of range"
        assert 1.5 <= can_low_voltage3 <= 2.5, "Connector 3 CAN Low voltage out of range"
        print("Connector 3 test passed!")
        GPIO.output(connector3_led_pin, GPIO.HIGH)  # Turn on the LED to indicate pass
    except AssertionError as e:
        print(f"Connector 3 test failed: {e}")
        GPIO.output(connector3_led_pin, GPIO.LOW)  # Turn off the LED on failure
        all_tests_passed = False

    # Final result
    if all_tests_passed:
        print("All tests passed!")
    else:
        print("Some tests failed!")

if __name__ == "__main__":
    try:
        harness_test()
    finally:
        GPIO.cleanup()
        spi.close()

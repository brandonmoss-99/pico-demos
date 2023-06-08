import machine
import time

# Set to Pin GP5, NOT physically Pin 5 on the Pico
rxPin = machine.Pin(5, machine.Pin.OUT)
# Set to Pin GP4, NOT physically Pin 4 on the Pico
txPin = machine.Pin(4, machine.Pin.IN)

# Set LED to be the LED on the Pico
led = machine.Pin("LED", machine.Pin.OUT)

# Create UART configuration
uart = machine.UART(1, baudrate=9600, rx=rxPin, tx=txPin, bits=8, parity=None, stop=2)

# Send a 't' character over UART. If there's data back, read it, and if it's
# an 'm' character from the other end, toggle the LED, then sleep for 1 second
while True:
    uart.write('t')
    if uart.any():
        data = uart.read()
        if data == b'm':
            led.toggle()
    time.sleep(1)
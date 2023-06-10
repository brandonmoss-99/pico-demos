import machine

# Set to Pin GP5, NOT physically Pin 5 on the Pico
UART_rxPin = machine.Pin(5, machine.Pin.OUT)
# Set to Pin GP4, NOT physically Pin 4 on the Pico
UART_txPin = machine.Pin(4, machine.Pin.IN)
# Set LED to be the LED on the Pico
led = machine.Pin(25, machine.Pin.OUT)

# Create UART configuration
uart = machine.UART(1, baudrate=9600, rx=UART_rxPin, tx=UART_txPin, bits=8, parity=None, stop=2)

# Keep checking the UART bus, and set the LED to whatever value is received on
# the UART bus
while True:
    if uart.any():
        data = uart.readline()

        if data == b'0':
            led.value(0)
        else:
            led.value(1)



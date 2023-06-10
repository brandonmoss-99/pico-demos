import machine

# Set to Pin GP5, NOT physically Pin 5 on the Pico
UART_rxPin = machine.Pin(5, machine.Pin.OUT)
# Set to Pin GP4, NOT physically Pin 4 on the Pico
UART_txPin = machine.Pin(4, machine.Pin.IN)

# Set the button input to pin GP0, and activate the Pico's internal resistor
# to get the value to low when not pressed
button = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_DOWN)

# Create UART configuration
uart = machine.UART(1, baudrate=9600, rx=UART_rxPin, tx=UART_txPin, bits=8, parity=None, stop=2)

while True:
    # Send the value of the button over UART
    if button.value() == 0:
        uart.write(b'0')
    else:
        uart.write(b'1')

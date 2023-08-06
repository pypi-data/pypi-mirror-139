from telemetrix_rpi_pico import telemetrix_rpi_pico

# Constants
BCM = 1
OUT = 1
IN = 0
HIGH = 1
LOW = 0
PUD_OFF = 0
PUD_DOWN = 1
PUD_UP = 2

BCM_PORCUPINE_LOOKUP = {
    "TX": 13,
    "RX": 12,
    "SCLK": 27,
    "MISO": 26,
    "CE0": 6,
    12: 3,
    17: 20,
    18: 11,
    20: 1,
    21: 0,
    24: 9,
    25: 7,
    "SCL": 17,
    "ID_SD": 28
}

# if testing with a pi pico just use this
PI_PICO_LOOKUP = {x: x for x in range(28)}

PI_PICO = "PI_PICO_LOOKUP"
BCM_PORCUPINE = "BCM_PORCUPINE_LOOKUP"

pin_definitions = {
    "PI_PICO_LOOKUP": PI_PICO_LOOKUP,
    "BCM_PORCUPINE_LOOKUP": BCM_PORCUPINE_LOOKUP,
}

pin_definition = BCM_PORCUPINE

board = telemetrix_rpi_pico.TelemetrixRpiPico()

pinStates = dict()


def pinChange(data):
    pinStates[data[1]] = data[2]
    print(f"Pin {data[1]} changed to {data[2]}")
    pass


def setmode(pinType):
    global pin_definition
    pin_definition = pin_definitions[pinType]
    pass


def setup(pin, direction, pull_up_down=PUD_OFF):
    newPin = pin_definition[pin]
    if direction == OUT:
        board.set_pin_mode_digital_output(newPin)
        # print('mode set OUT')
    else:
        pinStates[newPin] = LOW
        if pull_up_down == PUD_DOWN:
            # TelemetrixRpiPico does not support pull-down
            # TODO: Implement pull-down support
            board.set_pin_mode_digital_input(newPin, pinChange)
            pass
        else:
            board.set_pin_mode_digital_input_pullup(newPin, pinChange)
            pass
        board.set_pin_mode_digital_input(newPin, pinChange)
    pass


def output(pin, value):
    newPin = pin_definition[pin]
    board.digital_write(newPin, value)
    pass


def input(pin):
    newPin = pin_definition[pin]
    if newPin in pinStates:
        return pinStates[newPin]
    else:
        pass


def cleanup():
    board.shutdown()
    pass

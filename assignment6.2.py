from machine import Pin, PWM
from time import sleep

# --- HARDWARE SETUP ---
# Motor A / Moottori A
e1 = PWM(Pin(28))
m1 = Pin(27, Pin.OUT)

# Motor B / Moottori B
e2 = PWM(Pin(26))
m2 = Pin(22, Pin.OUT)

# Set PWM frequency to 1000 Hz
e1.freq(1000)
e2.freq(1000)

# --- CALIBRATION CONSTANTS ---
# Adjust these values based on your robot's battery level and physical build
DUTY_CYCLE_SPEED = 32767  # 50% Speed

# How many seconds does it take the car to drive exactly 1 meter at 50% speed?
TIME_PER_METER = 2.0

# How many seconds does it take the car to spin exactly 90 degrees on the spot?
TIME_FOR_90_DEG = 0.8

# File that contains the movement instructions
ROUTE_FILE = "route.txt"


# --- CORE MOVEMENT FUNCTIONS ---

def stop_motors():
    """Immediately stops both motors."""
    e1.duty_u16(0)
    e2.duty_u16(0)
    sleep(0.5)  # Short pause to let kinetic energy dissipate

def move_forward(meters: float):
    """Drives forward for a specific distance."""
    m1.value(1)
    m2.value(1)
    duration = meters * TIME_PER_METER
    e1.duty_u16(DUTY_CYCLE_SPEED)
    e2.duty_u16(DUTY_CYCLE_SPEED)
    sleep(duration)
    stop_motors()

def reverse(meters: float):
    """Drives backward for a specific distance."""
    m1.value(0)
    m2.value(0)
    duration = meters * TIME_PER_METER
    e1.duty_u16(DUTY_CYCLE_SPEED)
    e2.duty_u16(DUTY_CYCLE_SPEED)
    sleep(duration)
    stop_motors()

def turn_left(degrees: float):
    """Pivots left on the spot by running motors in opposite directions."""
    m1.value(0)
    m2.value(1)
    duration = (degrees / 90.0) * TIME_FOR_90_DEG
    e1.duty_u16(DUTY_CYCLE_SPEED)
    e2.duty_u16(DUTY_CYCLE_SPEED)
    sleep(duration)
    stop_motors()

def turn_right(degrees: float):
    """Pivots right on the spot by running motors in opposite directions."""
    m1.value(1)
    m2.value(0)
    duration = (degrees / 90.0) * TIME_FOR_90_DEG
    e1.duty_u16(DUTY_CYCLE_SPEED)
    e2.duty_u16(DUTY_CYCLE_SPEED)
    sleep(duration)
    stop_motors()

def turn_around():
    """Rotates 180 degrees on the spot (to the right, mirroring the S-route)."""
    turn_right(180)


# --- READING INSTRUCTIONS FROM FILE ---

# Maps each command word in the file to the function that performs it
COMMANDS = {
    "forward": move_forward,
    "reverse": reverse,
    "left": turn_left,
    "right": turn_right,
}

def read_route(filename: str):
    """Reads movement instructions from a file.

    One instruction per line, e.g. 'forward 0.5', 'left 90', 'turn_around'.
    Empty lines and lines starting with '#' are ignored.
    Returns a list of (command, value) tuples.
    """
    route = []
    with open(filename, "r") as f:
        line_number = 0
        for line in f:
            line_number += 1
            line = line.strip()
            if line == "" or line.startswith("#"):
                continue

            parts = line.split()
            command = parts[0].lower()

            if command == "turn_around":
                route.append((command, None))
            elif command in COMMANDS and len(parts) == 2:
                try:
                    route.append((command, float(parts[1])))
                except ValueError:
                    print("Line " + str(line_number) + ": invalid number, skipped: " + line)
            else:
                print("Line " + str(line_number) + ": unknown instruction, skipped: " + line)
    return route

def drive_route(route):
    """Executes a list of (command, value) instructions in order."""
    for command, value in route:
        if command == "turn_around":
            print("turn_around")
            turn_around()
        else:
            print(command + " " + str(value))
            COMMANDS[command](value)


# --- EXECUTION ---

route = read_route(ROUTE_FILE)
print("Loaded " + str(len(route)) + " instructions from " + ROUTE_FILE)

# Safety timeout before starting
print("Starting in 5 seconds... Place the car on the floor.")
sleep(5)

print("Executing mirrored S-route...")
drive_route(route)
print("Route completed successfully!")
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
DUTY_CYCLE_SPEED = 32767  # 50% Speed
TIME_PER_METER = 2.0  
TIME_FOR_90_DEG = 0.8  

# --- CORE MOVEMENT FUNCTIONS ---

def stop_motors():
    """Immediately stops both motors."""
    e1.duty_u16(0)
    e2.duty_u16(0)
    sleep(0.5)

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

def turn_left(degrees: int):
    """Pivots left on the spot by running motors in opposite directions."""
    m1.value(0)
    m2.value(1)
    duration = (degrees / 90.0) * TIME_FOR_90_DEG
    e1.duty_u16(DUTY_CYCLE_SPEED)
    e2.duty_u16(DUTY_CYCLE_SPEED)
    sleep(duration)
    stop_motors()

def turn_right(degrees: int):
    """Pivots right on the spot by running motors in opposite directions."""
    m1.value(1)
    m2.value(0)
    duration = (degrees / 90.0) * TIME_FOR_90_DEG
    e1.duty_u16(DUTY_CYCLE_SPEED)
    e2.duty_u16(DUTY_CYCLE_SPEED)
    sleep(duration)
    stop_motors()

def turn_around():
    """Convenience function to rotate 180 degrees on the spot."""
    turn_left(180)

# --- INSTRUCTION FILE PARSER ---

def execute_instructions_from_file(filename: str = "route.txt"):
    """Reads movement instructions from a file and runs them."""
    print(f"Reading instructions from {filename}...")
    try:
        with open(filename, "r") as file:
            for line in file:
                # Strip spaces and ignore empty lines or comments
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                
                # Parse command and value
                parts = line.split()
                command = parts[0].lower()
                value = float(parts[1]) if len(parts) > 1 else 0
                
                if command == "forward":
                    move_forward(value)
                elif command == "reverse":
                    reverse(value)
                elif command == "left":
                    turn_left(int(value))
                elif command == "right":
                    turn_right(int(value))
                elif command == "around":
                    turn_around()
                else:
                    print(f"Unknown command: {command}")
        print("Route completed successfully!")
    except Exception as e:
        print(f"Error reading or executing file: {e}")

# --- EXECUTION ---

# Safety timeout before starting
print("Starting in 5 seconds... Place the car on the floor.")
sleep(5) 

# Execute the parsed path from the external file
execute_instructions_from_file("route.txt")

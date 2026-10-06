from machine import Pin, PWM
from time import sleep

# --- HARDWARE SETUP ---
# Motor A
e1 = PWM(Pin(28))
m1 = Pin(27, Pin.OUT)

# Motor B
e2 = PWM(Pin(26))
m2 = Pin(22, Pin.OUT)     

# Set PWM frequency to 1000 Hz
e1.freq(1000)
e2.freq(1000)

# --- CALIBRATION CONSTANTS ---
DUTY_CYCLE_SPEED = 32767  # 50% Speed
TIME_PER_METER = 2.0      # Seconds per meter
TIME_FOR_90_DEG = 0.8     # Seconds per 90 degrees


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
    """Pivots left on the spot."""
    m1.value(0)
    m2.value(1)
    duration = (degrees / 90.0) * TIME_FOR_90_DEG
    e1.duty_u16(DUTY_CYCLE_SPEED)
    e2.duty_u16(DUTY_CYCLE_SPEED)
    sleep(duration)
    stop_motors()

def turn_right(degrees: int):
    """Pivots right on the spot."""
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


# --- FILE READING ROUTINE ---

def execute_route_from_file(filename: str):
    """Reads a text file line-by-line and triggers respective movement functions."""
    print(f"Reading instructions from {filename}...")
    
    try:
        with open(filename, "r") as file:
            for line in file:
                # Clean up whitespace and skip empty lines or comments
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                
                # Split line into command and its optional parameter value
                parts = line.split()
                command = parts[0].lower()
                
                print(f"Executing: {line}")
                
                # Parse commands and trigger matching hardware functions
                if command == "forward":
                    move_forward(float(parts[1]))
                elif command == "reverse":
                    reverse(float(parts[1]))
                elif command == "left":
                    turn_left(int(parts[1]))
                elif command == "right":
                    turn_right(int(parts[1]))
                elif command == "around":
                    turn_around()
                else:
                    print(f"Unknown command skipped: {command}")
                    
        print("Route completed successfully!")
        
    except OSError:
        print(f"Error: Could not find or read file '{filename}'. Make sure it is saved onto the Pico.")


# --- EXECUTION ---

# Safety timeout before starting
print("Starting in 5 seconds... Place the car on the floor.")
sleep(5) 

# Execute the mirrored S route file
execute_route_from_file("route.txt")
from machine import Pin, PWM
from time import sleep

# Motor A / Moottori A
e1 = PWM(Pin(28))
m1 = Pin(27, Pin.OUT)

# Motor B / Moottori B
e2 = PWM(Pin(26))
m2 = Pin(22, Pin.OUT)     

# Set PWM frequency to 1000 Hz / Aseta PWM-taajuus 1000 Hz
e1.freq(1000)
e2.freq(1000)

# 5 second timeout / 5 sekunnin tauko
sleep(5)

# Move forward / Eteenpäin
m1.value(1)
m2.value(1)

# Speed to 50% / Nopeus 50%
e1.duty_u16(32767)
e2.duty_u16(32767)

# After 10 seconds stop / 10 sekunnin kuluttua pysäytys
sleep(10)
e1.duty_u16(0)
e2.duty_u16(0)

# Wait 1 second for motors to stop / Odota yksi sekunti moottoreiden pysähtymistä
sleep(1)
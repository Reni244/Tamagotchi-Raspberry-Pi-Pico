from machine import I2C, Pin
from i2c_lcd import I2cLcd
import time
import os
import utime

# Setup I2C and LCD
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
lcd = I2cLcd(i2c, 0x27, 2, 16)

button1 = Pin(15, Pin.IN, Pin.PULL_DOWN)
button2 = Pin(14, Pin.IN, Pin.PULL_DOWN)
button3 = Pin(13, Pin.IN, Pin.PULL_DOWN)
button4 = Pin(12, Pin.IN, Pin.PULL_DOWN)
egg1 = 0
egg2 = 0
true1 = 0

# Dino head char (slot 0)
dino_head = bytearray([
    0b00000,
    0b00000,
    0b00100,
    0b01010,
    0b10001,
    0b11001,
    0b10011,
    0b01110
])

# Canvas below (slot 1)
canvas_below = bytearray([
    0b00000,
    0b00000,
    0b00100,
    0b01010,
    0b10011,
    0b11001,
    0b10001,
    0b01110
])

# Cracked egg (slot 2)
cracked_egg = bytearray([
    0b00000,
    0b00000,
    0b00100,
    0b01010,
    0b10111,
    0b11001,
    0b10111,
    0b01110
])

egg_cracked2 = bytearray([ 
    0b00000,
    0b00100,
    0b01110,
    0b11111,
    0b11111,
    0b11111,
    0b11111,
    0b01110
])
small_dino = bytearray([
    0b00000,
    0b00000,
    0b01010,
    0b01110,
    0b10001,
    0b11011,
    0b10001,
    0b01110
])
small_dino1 = bytearray([
    0b00000,
    0b00000,
    0b10101,
    0b01010,
    0b10001,
    0b11011,
    0b10101,
    0b01110
])


# Load custom chars
def load_custom_chars(lcd_obj, fontdata):
    lcd_obj.send(0x40)
    for char in fontdata:
        for line in char:
            lcd_obj.send(line, mode=0x01)

# Load all characters into CGRAM
load_custom_chars(lcd, [dino_head, canvas_below, cracked_egg, egg_cracked2])

lcd.clear()

# Show dino at start
lcd.move_to(6, 0)
lcd.putchar(chr(0))  # dino head
lcd.move_to(8, 0)
lcd.putchar(chr(1))  # canvas

time.sleep(0.5)
lcd.move_to(6, 0)
lcd.putchar(' ')
lcd.move_to(8, 0)
lcd.putchar(' ')
lcd.move_to(6, 1)
lcd.putchar(chr(0))
lcd.move_to(8, 1)
lcd.putchar(chr(1))

time.sleep(1)
lcd.clear()
lcd.move_to(0, 0)
lcd.putstr("Choose one.")

while true1 == 0:
    if button1.value() == 1:
        egg1 = 1
        egg2 = 0
        true1 = 1
        lcd.move_to(8, 1)
        lcd.putchar(' ')
        time.sleep(0.3)
        lcd.move_to(7, 1)
        lcd.putchar(chr(0))  # head moves left
        lcd.move_to(6, 1)
        lcd.putchar(' ')
        dinovariant = 0

    if button2.value() == 1:
        egg2 = 1
        egg1 = 0
        true1 = 1
        lcd.move_to(6, 1)
        lcd.putchar(' ')
        time.sleep(0.3)
        lcd.move_to(7, 1)
        lcd.putchar(chr(1))  # head moves right
        lcd.move_to(8, 1)
        lcd.putchar(' ')
        dinovariant = 1

time.sleep(0.5)
lcd.move_to(0, 0)
lcd.putstr("Good choice")
time.sleep(1.5)

lcd.move_to(0, 0)
lcd.putstr("Crack it.    ")

# Wait until button press
while button1.value() == 0 and button2.value() == 0:
    time.sleep(0.1)

# Show cracked egg at (7, 1)
lcd.move_to(7, 1)
lcd.putchar(chr(2))

time.sleep(1)

lcd.move_to(7, 1)
lcd.putchar(chr(3))

time.sleep(1)

lcd.move_to(0, 0)
lcd.putstr(chr(255) * 16)  # fill top row
lcd.move_to(0, 1)
lcd.putstr(chr(255) * 16)  # fill top row

time.sleep(1)
lcd.move_to(0, 0)
lcd.putstr("[][][][][][][][]")
lcd.move_to(0, 1)
lcd.putstr("[][][][][][][][]")
time.sleep(0.5)

lcd.move_to(0, 0)
lcd.putstr("                ")
lcd.move_to(0, 1)
lcd.putstr("                ")

time.sleep(1)
if dinovariant == 0:
    load_custom_chars(lcd, [small_dino])
    
else:
    load_custom_chars(lcd, [small_dino1])
    

lcd.move_to(7, 1)
lcd.putstr((chr(0)))
time.sleep(1)
lcd.move_to(0, 0)
lcd.putstr("Hello little guy ")

time.sleep(2.3)
lcd.move_to(0, 0)
lcd.putstr("You need a name   ")
time.sleep(2)

from machine import Pin
import utime

matrix_keys = [['A', 'B', 'C', 'D'],
               ['E', 'F', 'G', 'H'],
               ['I', 'J', 'K', 'L'],
               ['*', 'M', '#', 'N']]

keypad_rows = [9, 8, 7, 6]
keypad_columns = [5, 4, 3, 2]


col_pins = []
row_pins = []

# Setup pins
for x in range(4):
    row_pins.append(Pin(keypad_rows[x], Pin.OUT))
    row_pins[x].value(1)
    col_pins.append(Pin(keypad_columns[x], Pin.IN, Pin.PULL_DOWN))

# Clear LCD
lcd.clear()
lcd.move_to(0, 0)
lcd.putstr("Enter name:         ")

name = []

def scankeys():
    global name

    # Alternative input using button1
    if button1.value():
        name = list("KIKI        ")
        lcd.move_to(0, 1)
        lcd.putstr(" " * 16)
        lcd.move_to(0, 1)
        lcd.putstr("".join(name))
        utime.sleep(0.5)
        return True
    if button2.value():
        name = list("KIWI           ")
        lcd.move_to(0, 1)
        lcd.putstr(" " * 16)
        lcd.move_to(0, 1)
        lcd.putstr("".join(name))
        utime.sleep(0.5)# debounce
        return True
    if button3.value():
        name = list("PIP           ")
        lcd.move_to(0, 1)
        lcd.putstr(" " * 16)
        lcd.move_to(0, 1)
        lcd.putstr("".join(name))
        utime.sleep(0.5)# debounce
        return True
    if button4.value():
        name = list("PIXIE           ")
        lcd.move_to(0, 1)
        lcd.putstr(" " * 16)
        lcd.move_to(0, 1)
        lcd.putstr("".join(name))
        utime.sleep(0.5)# debounce
        return True

    for row in range(4):
        row_pins[row].high()
        for col in range(4):
            if col_pins[col].value() == 1:
                key_press = matrix_keys[row][col]

                if key_press == '#':  # Finish input
                    row_pins[row].low()
                    utime.sleep(0.3)
                    return True
                elif key_press == '*':  # Backspace
                    if name:
                        name.pop()
                else:
                    if len(name) < 5:
                        name.append(key_press)

                # Show on LCD
                lcd.move_to(0, 1)
                lcd.putstr(" " * 16)
                lcd.move_to(0, 1)
                lcd.putstr("".join(name))

                utime.sleep(0.3)  # debounce
        row_pins[row].low()
    return False


# Main loop
done = False
while not done:
    done = scankeys()

# Save to file as string
with open("name.txt", "w") as f:
    f.write("".join(name))
    
with open("dinovariant.txt", "w") as f: f.write(str(dinovariant))




lcd.clear()
lcd.move_to(0, 0)
lcd.putstr("               ")
lcd.move_to(0, 1)
lcd.putstr("               ")

lcd.clear()
lcd.move_to(0, 0)
lcd.putstr("Hello, " + "".join(name))
lcd.move_to(7, 1)
lcd.putstr(chr(0))

time.sleep(2)

lcd.clear()
lcd.move_to(0, 0)
lcd.putstr("he needs good     ")
lcd.move_to(0, 1)
lcd.putstr("care             ")

time.sleep(2)

lcd.clear()
lcd.move_to(0, 0)
lcd.putstr("food, water,      ")
lcd.move_to(0, 1)
lcd.putstr("games..             ")

time.sleep(2)

lcd.clear()
lcd.move_to(0, 0)
lcd.putstr("take care of     ")
lcd.move_to(0, 1)
lcd.putstr(name)
lcd.clear()

time.sleep(2)

lcd.move_to(0, 0)
lcd.putstr("              ")
lcd.move_to(0, 1)
lcd.putstr("             ")

lcd.move_to(7, 1)
lcd.putstr((chr(0)))

def swap_main():
    # Make sure both files exist
    if 'main.py' in os.listdir() and 'alt.py' in os.listdir():
        print("Swapping main.py and alt.py...")
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr("wait a moment...")
        os.rename('main.py', 'old.py')   # rename current main.py to old.py
        os.rename('alt.py', 'main.py')   # rename alt.py to main.py
        # Optionally rename old.py to alt.py to keep the files swapped
        os.rename('old.py', 'alt.py')
        print("Swap complete. Rebooting now...")
        time.sleep(2)
        machine.reset()
    else:
        print("Required files not found. No swap done.")

# Call swap_main() to swap files and reboot
swap_main()

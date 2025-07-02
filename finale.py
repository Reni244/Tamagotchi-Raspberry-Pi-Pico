from machine import Pin
from machine import I2C, Pin, Timer, reset, ADC
from i2c_lcd import I2cLcd
import time
import time
import os
import uos
import machine  # Make sure this is imported
# Setup I2C and LCD
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
lcd = I2cLcd(i2c, 0x27, 2, 16)
button1 = Pin(15, Pin.IN, Pin.PULL_DOWN)

with open("name.txt", "r") as f:
    name = f.read().strip()


dino = bytearray([
    0b11011,
    0b01110,
    0b11011,
    0b10001,
    0b01110,
    0b00100,
    0b11111,
    0b01110
])
def load_custom_chars(lcd_obj, fontdata):
    lcd_obj.send(0x40)
    for char in fontdata:
        for line in char:
            lcd_obj.send(line, mode=0x01)
load_custom_chars(lcd, [dino])

def swap_main():
    if 'main.py' in os.listdir() and 'alt.py' in os.listdir():
        print("Swapping main.py and alt.py...")
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr("wait a moment...")

        # Do the renaming
        os.rename('main.py', 'finale.py')
        os.rename('oldmain.py', 'main.py')

        # Reset files
        with open("age.txt", "w") as f: f.write("0")
        with open("happy.txt", "w") as f: f.write("0")
        with open("hunger.txt", "w") as f: f.write("0")
        with open("thirst.txt", "w") as f: f.write("0")
        with open("coins.txt", "w") as f: f.write("15")
        with open("bigbottle.txt", "w") as f: f.write("0")
        with open("toy.txt", "w") as f: f.write("0")
        with open("dead.txt", "w") as f: f.write("0")

        uos.sync()  # ensure everything is written
        
        time.sleep(3)
        machine.reset()  # restart Pico
    else:
        print("Files missing.")

with open("birthdays.txt", "w") as f:
    f.write(f"0\n")
    f.write(f"0\n")
    f.write(f"0\n")
    f.write(f"0\n")
    f.write(f"0\n")

time.sleep(1.5)
lcd.move_to(0, 0)
lcd.putstr("               ")
lcd.move_to(7, 1)
lcd.putstr(chr(0))
lcd.move_to(0, 0)
time.sleep(4)
lcd.putstr("you did it.   ")
time.sleep(2)
lcd.move_to(0, 0)
lcd.putstr("you grew        ")
lcd.move_to(0, 1)
lcd.putstr(name + "...      ")
time.sleep(2)
lcd.move_to(0, 0)
lcd.putstr("he starts to        ")
lcd.move_to(0, 1)
lcd.putstr("speak...      ")
time.sleep(2)
lcd.move_to(0, 0)
lcd.putstr("-thank you.        ")
lcd.move_to(0, 1)
lcd.putstr("so much...      ")
time.sleep(2)
lcd.move_to(0, 0)
lcd.putstr("-im gonna go        ")
lcd.move_to(0, 1)
lcd.putstr("now...      ")
time.sleep(2)
lcd.move_to(0, 0)
lcd.putstr("-im gonna go        ")
lcd.move_to(0, 1)
lcd.putstr("now...      ")
time.sleep(2)
lcd.move_to(0, 0)
lcd.putstr(name +" left...")
lcd.move_to(0, 1)
lcd.putstr("              ")
time.sleep(2)
lcd.move_to(0, 0)
lcd.putstr("you can allways")
lcd.move_to(0, 1)
lcd.putstr("start again.")
time.sleep(2)
lcd.move_to(0, 0)
lcd.putstr("hold button 1      ")
lcd.move_to(0, 1)
lcd.putstr("when youre ready     ")
time.sleep(2)
while True:
    if button1.value() == 1:
        time.sleep(3)
        lcd.move_to(0, 0)
        lcd.putstr("resetting...      ")
        lcd.move_to(0, 1)
        lcd.putstr("                    ")
        time.sleep(2)
        swap_main()


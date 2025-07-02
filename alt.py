from machine import I2C, Pin, Timer, reset, ADC
from i2c_lcd import I2cLcd
import time
import os
import uos
import machine  # Make sure this is imported
import random

# Setup I2C and LCD
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
lcd = I2cLcd(i2c, 0x27, 2, 16)
# Constants for power and signal pins
POWER_PIN = 2        # Use a free GPIO pin, like GP2
SIGNAL_PIN = 26      # ADC0

vrx = ADC(Pin(27))        # X-axis
vry = ADC(Pin(28))        # Y-axis
sw = Pin(20, Pin.IN, Pin.PULL_UP)  # Button with pull-up resistor
pet_x = 0
pet_y = 0
moving = 0
Srandom = 0
Srandom2 = 0
maxsearch = 0
sticktime = 0
gonr = 0
sticknumber = 0
continuestick = 0
toytime = 0
buttonsecventa1 = 0
buttonsecventa2 = 0
buttonsecventa3 = 0

button1 = Pin(15, Pin.IN, Pin.PULL_DOWN)
button2 = Pin(14, Pin.IN, Pin.PULL_DOWN)
button3 = Pin(13, Pin.IN, Pin.PULL_DOWN)
button4 = Pin(12, Pin.IN, Pin.PULL_DOWN)
sitch = Pin(11, Pin.IN, Pin.PULL_DOWN)
REDLED = Pin(16, Pin.OUT)
GREENLED = Pin(17, Pin.OUT)
power = Pin(POWER_PIN, Pin.OUT)
power.value(0)  # Start with sensor off
vrx = ADC(Pin(27))        # X-axis
vry = ADC(Pin(28))        # Y-axis
sw = Pin(20, Pin.IN, Pin.PULL_UP)  # Button with pull-up resistor

# Setup ADC for reading the water sensor
signal = ADC(Pin(SIGNAL_PIN))  # Set up ADC on signal pin

holdingreset = 0  # global counter
true1 = 0
place = "home"
bh = 0
state = "normal"
hungermax = 1100
thirstmax = 900
happymax = 1200
enoughwater = 0

with open("dinovariant.txt", "r") as f:
    dinovariant = f.read().strip()
    
with open("name.txt", "r") as f:
    name = f.read().strip()
    
with open("hunger.txt", "r") as f:
    hunger = int(f.read())

with open("hungerbar.txt", "r") as f:
    hungerbar = float(f.read())
    
with open("thirst.txt", "r") as f:
    thirst = int(f.read())
    
with open("thirstbar.txt", "r") as f:
    thirstbar = float(f.read())
    
with open("happy.txt", "r") as f:
    happy = int(f.read())

with open("happybar.txt", "r") as f:
    happybar = float(f.read())
    
with open("age.txt", "r") as f:
    age = int(f.read())
    
with open("coins.txt", "r") as f:
    coins = int(f.read())
    
with open("bigbottle.txt", "r") as f:
    bigbottle = int(f.read())
    
with open("toy.txt", "r") as f:
    toy = int(f.read())
    
with open("dead.txt", "r") as f:
    dead = int(f.read())
    
with open("birthdays.txt", "r") as f:
    lines = f.readlines()
    trueage1 = int(lines[0].strip())
    trueage2 = int(lines[1].strip())
    trueage3 = int(lines[2].strip())
    trueage4 = int(lines[3].strip())
    trueage5 = int(lines[4].strip())
    
print(age)

if age >= 20000:
    hungermax = 1000
    thirstmax = 910
    happymax = 1110

if age >= 40000:
    hungermax = 950
    thirstmax = 950
    happymax = 1050

if age >= 60000:
    hungermax = 850
    thirstmax = 1000
    happymax = 900

if age >= 80000:
    hungermax = 830
    thirstmax = 950
    happymax = 860

if age >= 100000:
    hungermax = 750
    thirstmax = 900
    happymax = 800



# Custom character
if dinovariant == 0:
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
else:
    small_dino = bytearray([
        0b00000,
        0b00000,
        0b10101,
        0b01010,
        0b10001,
        0b11011,
        0b10101,
        0b01110
    ])
    
border = bytearray([
    0b11111,
    0b10001,
    0b10001,
    0b10001,
    0b10001,
    0b10001,
    0b10001,
    0b11111
])
sad = bytearray([
    0b00000,
    0b00100,
    0b10100,
    0b10100,
    0b10001,
    0b10001,
    0b00001,
    0b00001
])

def load_custom_chars(lcd_obj, fontdata):
    lcd_obj.send(0x40)
    for char in fontdata:
        for line in char:
            lcd_obj.send(line, mode=0x01)

load_custom_chars(lcd, [small_dino, border, sad])

def swap_main():
    if 'main.py' in os.listdir() and 'alt.py' in os.listdir():
        print("Swapping main.py and alt.py...")
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr("wait a moment...")

        # Do the renaming
        os.rename('main.py', 'old.py')
        os.rename('alt.py', 'main.py')
        os.rename('old.py', 'alt.py')

        # Reset files
        with open("age.txt", "w") as f: f.write("0")
        with open("happy.txt", "w") as f: f.write("0")
        with open("hunger.txt", "w") as f: f.write("0")
        with open("thirst.txt", "w") as f: f.write("0")
        with open("coins.txt", "w") as f: f.write("15")
        with open("bigbottle.txt", "w") as f: f.write("0")
        with open("toy.txt", "w") as f: f.write("0")
        with open("dead.txt", "w") as f: f.write("0")
        with open("birthdays.txt", "w") as f:
            f.write(f"0\n")
            f.write(f"0\n")
            f.write(f"0\n")
            f.write(f"0\n")
            f.write(f"0\n")

        uos.sync()  # ensure everything is written
        
        time.sleep(3)
        machine.reset()  # restart Pico
    else:
        print("Files missing.")

def background_task(timer):
    global holdingreset, hunger, thirst, happy, hungerbar, thirstbar, happybar, age, hungermax, thirstmax, happymax, coins, bigbottle, trueage1, trueage2, trueage3, trueage4, trueage5, toy, dead

    if button1.value():
        holdingreset += 1
    else:
        holdingreset = 0
    if holdingreset >= 30:
        swap_main()
        
    hunger += 1
    thirst += 1
    happy += 1
    age += 1
    
    if hunger >= hungermax:
        hunger = 0
        hungerbar += 1
        
    if thirst >= thirstmax:
        thirst = 0
        thirstbar += 1
        
    if happy >= happymax:
        happy = 0
        happybar += 1

    # 💡 Write integers as strings
    with open("hunger.txt", "w") as f: f.write(str(hunger))
    with open("hungerbar.txt", "w") as f: f.write(str(hungerbar))
    with open("thirst.txt", "w") as f: f.write(str(thirst))
    with open("thirstbar.txt", "w") as f: f.write(str(thirstbar))
    with open("happy.txt", "w") as f: f.write(str(happy))
    with open("happybar.txt", "w") as f: f.write(str(happybar))
    with open("age.txt", "w") as f: f.write(str(age))
    with open("coins.txt", "w") as f: f.write(str(coins))
    with open("bigbottle.txt", "w") as f: f.write(str(bigbottle))
    with open("toy.txt", "w") as f: f.write(str(toy))
    with open("dead.txt", "w") as f: f.write(str(dead))

    with open("birthdays.txt", "w") as f:
        f.write(f"{trueage1}\n")
        f.write(f"{trueage2}\n")
        f.write(f"{trueage3}\n")
        f.write(f"{trueage4}\n")
        f.write(f"{trueage5}\n")

    if age >= 20000:
        hungermax = 830
        thirstmax = 710
        happymax = 910

    if age >= 40000:
        hungermax = 750
        thirstmax = 750
        happymax = 950

    if age >= 60000:
        hungermax = 720
        thirstmax = 800
        happymax = 900

    if age >= 80000:
        hungermax = 650
        thirstmax = 750
        happymax = 800

    if age >= 100000:
        hungermax = 600
        thirstmax = 700
        happymax = 750


# Setup timer
timer = Timer()
timer.init(period=200, mode=Timer.PERIODIC, callback=background_task)

# Show ready screen
lcd.clear()
lcd.move_to(0, 0)
lcd.putstr("Saved!")
lcd.move_to(7, 1)
lcd.putchar(chr(0))
REDLED.value(1)
time.sleep(1)
print("Ready.")
REDLED.value(0)

lcd.move_to(0, 0)
lcd.putstr("          ")
if trueage5 == 1:
    def swap_main():
        # Make sure both files exist
        if 'main.py' in os.listdir() and 'finale.py' in os.listdir():
            print("Swapping main.py and finale.py...")
            lcd.clear()
            lcd.move_to(0, 0)
            lcd.putstr("wait a moment...")
            os.rename('main.py', 'old.py')        # rename current main.py to old.py
            os.rename('finale.py', 'main.py')     # rename finale.py to main.py
            os.rename('old.py', 'oldmain.py')     # rename old.py to oldmain.py
            print("Swap complete. Rebooting now...")
            time.sleep(2)
            machine.reset()
        else:
            print("Required files not found. No swap done.")
    swap_main()

while True:
    if happybar >= 6 or hungerbar >= 7 or thirstbar >= 7 or dead == 1:
        lcd.move_to(0, 0)
        lcd.putstr("i'm sorry, but         ")
        lcd.move_to(0, 1)
        lcd.putstr(name + " died...      ")
        time.sleep(2)
        lcd.move_to(0, 0)
        lcd.putstr("you didnt threat")
        lcd.move_to(0, 1)
        lcd.putstr("him well...      ")
        time.sleep(2)
        lcd.move_to(0, 0)
        lcd.putstr("goodbye...       ")
        lcd.move_to(0, 1)
        lcd.putstr("...             ")
        time.sleep(2)
        dead = 1
        break
    if true1 == 0 and place == "home":
        lcd.move_to(0, 0)
        lcd.putstr("                 ")
        lcd.move_to(0, 1)
        lcd.putstr("                 ")
        lcd.move_to(7, 1)
        lcd.putchar(chr(0))
        Srandom = random.randint(1, 8)
        time.sleep(1)
        if Srandom == 4:
            if place == "home":
                lcd.move_to(0, 0)
                lcd.putstr(name +" has a gift       ")
                lcd.move_to(0, 1)
                lcd.putstr("for you!           ")
                time.sleep(2)
                lcd.move_to(0, 0)
                lcd.putstr(".                ")
                lcd.move_to(0, 1)
                lcd.putstr("                   ")
                Srandom = random.randint(1, 10)
                time.sleep(0.4)
                lcd.move_to(0, 0)
                lcd.putstr("..         ")
                lcd.move_to(0, 1)
                lcd.putstr("                   ")
                time.sleep(0.4)
                lcd.move_to(0, 0)
                lcd.putstr("...               ")
                lcd.move_to(0, 1)
                lcd.putstr("                   ")
                time.sleep(1.2)
                if Srandom == 1 or Srandom == 2 or Srandom == 3:
                    lcd.move_to(0, 0)
                    lcd.putstr("it's 5 coins!     ")
                    lcd.move_to(0, 1)
                    lcd.putstr("                   ")
                    coins += 5
                    time.sleep(2)
                    lcd.move_to(0, 0)
                    lcd.putstr("                  ")
                    lcd.move_to(0, 1)
                    lcd.putstr("                   ")
                
                if Srandom == 4 or Srandom == 5:
                    lcd.move_to(0, 0)
                    lcd.putstr("it's 10 coins!     ")
                    lcd.move_to(0, 1)
                    lcd.putstr("                   ")
                    coins += 10
                    time.sleep(2)
                    lcd.move_to(0, 0)
                    lcd.putstr("                  ")
                    lcd.move_to(0, 1)
                    lcd.putstr("                   ")
                    
                if Srandom == 6:
                    lcd.move_to(0, 0)
                    lcd.putstr("it was actually         ")
                    lcd.move_to(0, 1)
                    lcd.putstr("a scrap              ")
                    bigbottle = 0
                    time.sleep(2)
                    lcd.move_to(0, 0)
                    lcd.putstr("you threw it          ")
                    lcd.move_to(0, 1)
                    lcd.putstr("away...             ")
                    time.sleep(2)
                    lcd.move_to(0, 0)
                    lcd.putstr("                  ")
                    lcd.move_to(0, 1)
                    lcd.putstr("                   ")
                    
                if Srandom == 7:
                    lcd.move_to(0, 0)
                    lcd.putstr("it's a ground          ")
                    lcd.move_to(0, 1)
                    lcd.putstr("special fruit!                 ")
                    time.sleep(2)
                    lcd.move_to(0, 0)
                    lcd.putstr("you give it to    ")
                    lcd.move_to(0, 1)
                    lcd.putstr(name + "...")
                    time.sleep(2)
                    lcd.move_to(0, 0)
                    lcd.putstr("he likes it!     ")
                    lcd.move_to(0, 1)
                    lcd.putstr("               ")
                    time.sleep(2)
                    lcd.move_to(0, 0)
                    lcd.putstr("+1 hunger!    ")
                    lcd.move_to(0, 1)
                    lcd.putstr("+0.5 thirst!")
                    hungerbar -= 1
                    thirstbar -= 0.5
                    time.sleep(2)
                    lcd.move_to(0, 0)
                    lcd.putstr("                  ")
                    lcd.move_to(0, 1)
                    lcd.putstr("                   ")
                    
                if Srandom == 8:
                    lcd.move_to(0, 0)
                    lcd.putstr("it's a special         ")
                    lcd.move_to(0, 1)
                    lcd.putstr("fruit juice!                 ")
                    time.sleep(2)
                    lcd.move_to(0, 0)
                    lcd.putstr("you give it to    ")
                    lcd.move_to(0, 1)
                    lcd.putstr(name + "...         ")
                    time.sleep(2)
                    lcd.move_to(0, 0)
                    lcd.putstr("he likes it     ")
                    lcd.move_to(0, 1)
                    lcd.putstr("a lot!               ")
                    time.sleep(2)
                    lcd.move_to(0, 0)
                    lcd.putstr("+1.5 thirst!    ")
                    lcd.move_to(0, 1)
                    lcd.putstr("               ")
                    thirstbar -= 1.5
                    time.sleep(2)
                    lcd.move_to(0, 0)
                    lcd.putstr("he aged faster!    ")
                    lcd.move_to(0, 1)
                    lcd.putstr("AGE BONUS!")
                    age += 2500
                    time.sleep(2)
                    lcd.move_to(0, 0)
                    lcd.putstr("                  ")
                    lcd.move_to(0, 1)
                    lcd.putstr("                   ")
                    
                if Srandom == 9:
                    lcd.move_to(0, 0)
                    lcd.putstr("it's a           ")
                    lcd.move_to(0, 1)
                    lcd.putstr("super meat!                 ")
                    time.sleep(2)
                    lcd.move_to(0, 0)
                    lcd.putstr("you give it to          ")
                    lcd.move_to(0, 1)
                    lcd.putstr(name + "...                 ")
                    time.sleep(2)
                    lcd.move_to(0, 0)
                    lcd.putstr("he likes it             ")
                    lcd.move_to(0, 1)
                    lcd.putstr("really much!!!                 ")
                    time.sleep(2)
                    lcd.move_to(0, 0)
                    lcd.putstr(name + " is happy          ")
                    lcd.move_to(0, 1)
                    lcd.putstr("now!                  ")
                    time.sleep(2)
                    lcd.move_to(0, 0)
                    lcd.putstr("+1.5 hunger           ")
                    lcd.move_to(0, 1)
                    lcd.putstr("+1 happiness                 ")
                    time.sleep(2)
                    lcd.move_to(0, 0)
                    lcd.putstr("                   ")
                    lcd.move_to(0, 1)
                    lcd.putstr("                     ")
                    hungerbar -= 1.5
                    happybar -= 1
                    time.sleep(2)
                    
                if Srandom == 10:
                    lcd.move_to(0, 0)
                    lcd.putstr("it's a              ")
                    lcd.move_to(0, 1)
                    lcd.putstr("water bottle!                 ")
                    time.sleep(2)
                    lcd.move_to(0, 0)
                    lcd.putstr("you give it to          ")
                    lcd.move_to(0, 1)
                    lcd.putstr(name + "...                 ")
                    time.sleep(2)
                    lcd.move_to(0, 0)
                    lcd.putstr("he drinks it.              ")
                    lcd.move_to(0, 1)
                    lcd.putstr("                    ")
                    time.sleep(2)
                    lcd.move_to(0, 0)
                    lcd.putstr("+1 thirst!             ")
                    lcd.move_to(0, 1)
                    lcd.putstr("                    ")
                    thirstbar -= 1
                    time.sleep(2)
                    lcd.move_to(0, 0)
                    lcd.putstr("                  ")
                    lcd.move_to(0, 1)
                    lcd.putstr("                    ")
        if hungerbar >= 5 or thirstbar >= 4 or happybar >= 5:
            lcd.move_to(8, 1)
            lcd.putchar(chr(2))
            lcd.move_to(6, 1)
            lcd.putchar(chr(2))
            lcd.move_to(7, 0)
            lcd.putchar(chr(2))
            
        if place == "home" and 20000 <= age < 40000 and trueage1 == 0:
            print("1 year old")
            lcd.clear()
            lcd.move_to(0, 0)
            lcd.putstr(" is now 1")
            lcd.move_to(0, 1)
            lcd.putstr("year old!")
            time.sleep(2)
            lcd.move_to(0, 0)
            lcd.putstr("+ 5 coins!")
            lcd.move_to(0, 1)
            lcd.putstr("            ")
            coins += 5
            time.sleep(2)
            lcd.clear()
            trueage1 = 1
            lcd.move_to(0, 0)
            lcd.putstr("                 ")
            lcd.move_to(0, 1)
            lcd.putstr("                 ")
            lcd.move_to(7, 1)
            lcd.putchar(chr(0))
            
        if place == "home" and 40000 <= age < 60000 and trueage2 == 0:
            print("2 years old")
            lcd.clear()
            lcd.move_to(0, 0)
            lcd.putstr(" is now 2")
            lcd.move_to(0, 1)
            lcd.putstr("years old!")
            time.sleep(2)
            lcd.clear()
            lcd.move_to(0, 0)
            lcd.putstr("+ 10 coins!")
            lcd.move_to(0, 1)
            lcd.putstr("            ")
            coins += 10
            time.sleep(2)
            lcd.clear()
            trueage2 = 1
            lcd.move_to(0, 0)
            lcd.putstr("                 ")
            lcd.move_to(0, 1)
            lcd.putstr("                 ")
            lcd.move_to(7, 1)
            lcd.putchar(chr(0))
        if place == "home" and 60000 <= age < 80000 and trueage3 == 0:
            print("3 years old")
            lcd.clear()
            lcd.move_to(0, 0)
            lcd.putstr(" is now 3")
            lcd.move_to(0, 1)
            lcd.putstr("years old!")
            time.sleep(2)
            lcd.move_to(0, 0)
            lcd.putstr("+ 15 coins!")
            lcd.move_to(0, 1)
            lcd.putstr("            ")
            coins += 15
            time.sleep(2)
            lcd.clear()
            trueage3 = 1
            lcd.move_to(0, 0)
            lcd.putstr("                 ")
            lcd.move_to(0, 1)
            lcd.putstr("                 ")
            lcd.move_to(7, 1)
            lcd.putchar(chr(0))
            
        if place == "home" and 80000 <= age < 100000 and trueage4 == 0:
            print("4 years old")
            lcd.clear()
            lcd.move_to(0, 0)
            lcd.putstr(" is now 4")
            lcd.move_to(0, 1)
            lcd.putstr("years old!")
            time.sleep(2)
            lcd.move_to(0, 0)
            lcd.putstr("+ 20 coins!")
            lcd.move_to(0, 1)
            lcd.putstr("            ")
            coins += 20
            time.sleep(2)
            lcd.clear()
            trueage4 = 1
            lcd.move_to(0, 0)
            lcd.putstr("                 ")
            lcd.move_to(0, 1)
            lcd.putstr("                 ")
            lcd.move_to(7, 1)
            lcd.putchar(chr(0))
            
        if place == "home" and 100000 <= age < 120000 and trueage5 == 0:
            print("4 years old")
            lcd.clear()
            lcd.move_to(0, 0)
            lcd.putstr(" is now 5")
            lcd.move_to(0, 1)
            lcd.putstr("years old!")
            time.sleep(2)
            lcd.move_to(0, 0)
            lcd.putstr("+ 30 coins!")
            lcd.move_to(0, 1)
            lcd.putstr("            ")
            coins += 30
            time.sleep(2)
            lcd.clear()
            trueage5 = 1
            lcd.move_to(0, 0)
            lcd.putstr("please restart")
            lcd.move_to(0, 1)
            lcd.putstr("the machine")
            break
            
        true1 = 1

    if place == "home" and button1.value() == 1:
        place = "info"
        print("sending to info")
        time.sleep(0.5)
        
    if place == "home" and button3.value() == 1:
        place = "thirstt"
        print("sending to thirst")
        time.sleep(0.5)
        
    if place == "home" and button4.value() == 1:
        place = "happyy"
        print("sending to happy")
        time.sleep(0.5)
        
    if place == "home" and button2.value() == 1:
            place = "hunger shop"
            print("sending to hunger")
            time.sleep(0.5)

    # INFO SCREEN
    while place == "info":
        lcd.move_to(0, 0)
        lcd.putstr("*hunger  *thirst")
        lcd.move_to(0, 1)
        lcd.putstr("*happyness  *->")
        time.sleep(0.8)

        while place == "info":
            if button1.value():
                place = "hunger"
                time.sleep(0.3)
            elif button2.value():
                place = "thirst"
                time.sleep(0.3)
            elif button3.value():
                place = "happy"
                time.sleep(0.3)
            elif button4.value():
                place = "home"
                true1 = 0
                time.sleep(0.3)
                
        
    while place == "hunger" and bh == 0:
        lcd.move_to(0, 0)
        lcd.putstr("hunger:            ")
        lcd.move_to(0, 1)
        lcd.putstr("                    ")
        if hungerbar <= -4:
            hungerbar = -3
            
        if hungerbar <= 0:
            lcd.move_to(0, 1)
            lcd.putstr(chr(255)*6 + "         ")

        elif hungerbar == 1:
            lcd.move_to(0, 1)
            lcd.putstr(chr(255)*5 + chr(1))

        elif hungerbar == 2:
            lcd.move_to(0, 1)
            lcd.putstr(chr(255)*4 + chr(1)*2)

        elif hungerbar == 3:
            lcd.move_to(0, 1)
            lcd.putstr(chr(255)*3 + chr(1)*3)

        elif hungerbar == 4:
            lcd.move_to(0, 1)
            lcd.putstr(chr(255)*2 + chr(1)*4)

        elif hungerbar == 5:
            lcd.move_to(0, 1)
            lcd.putstr(chr(255) + chr(1)*5)

        elif hungerbar >= 6:
            lcd.move_to(0, 1)
            lcd.putstr(chr(1)*6)
            
        bh = 1
            
    while (place == "hunger" or place == "thirst" or place == "happy") and button4.value() == 1:
        place = "info"
        print("back to info!")
        time.sleep(0.5)
        bh = 0
            
    while place == "thirst" and bh == 0:
        lcd.move_to(0, 0)
        lcd.putstr("Thirst:            ")
        lcd.move_to(0, 1)
        lcd.putstr("                    ")
        if thirstbar <= -4:
            thirstbar = -3
            
        if thirstbar <= 0:
            lcd.move_to(0, 1)
            lcd.putstr(chr(255)*7 + "         ")

        elif thirstbar == 1:
            lcd.move_to(0, 1)
            lcd.putstr(chr(255)*6 + chr(1))

        elif thirstbar == 2:
            lcd.move_to(0, 1)
            lcd.putstr(chr(255)*5 + chr(1)*2)

        elif thirstbar == 3:
            lcd.move_to(0, 1)
            lcd.putstr(chr(255)*4 + chr(1)*3)

        elif thirstbar == 4:
            lcd.move_to(0, 1)
            lcd.putstr(chr(255)*3 + chr(1)*4)
              
        elif thirstbar >= 5:
            lcd.move_to(0, 1)
            lcd.putstr(chr(255)*2 + chr(1)*5)
            
        elif thirstbar >= 6:
            lcd.move_to(0, 1)
            lcd.putstr(chr(255)*1 + chr(1)*6)
            
        elif thirstbar >= 7:
            lcd.move_to(0, 1)
            lcd.putstr(chr(1)*7)
                
                
        bh = 1
                
    while place == "happy" and bh == 0:
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr("Happiness:            ")
        lcd.move_to(0, 1)
        lcd.putstr("                    ")
        if happybar <= -4:
            happybar = -3
            
        if happybar <= 0:
            lcd.move_to(0, 1)
            lcd.putstr(chr(255)*6 + "         ")

        elif happybar == 1:
            lcd.move_to(0, 1)
            lcd.putstr(chr(255)*5 + chr(1))

        elif happybar == 2:
            lcd.move_to(0, 1)
            lcd.putstr(chr(255)*4 + chr(1)*2)

        elif happybar == 3:
            lcd.move_to(0, 1)
            lcd.putstr(chr(255)*3 + chr(1)*3)

        elif happybar == 4:
            lcd.move_to(0, 1)
            lcd.putstr(chr(255)*2 + chr(1)*4)

        elif happybar == 5:
            lcd.move_to(0, 1)
            lcd.putstr(chr(255) + chr(1)*5)

        elif happybar >= 6:
            lcd.move_to(0, 1)
            lcd.putstr(chr(1)*6)
            
        bh = 1
        
    if place == "thirstt":
        lcd.move_to(0, 0)
        lcd.putstr("you went to take    ")
        lcd.move_to(0, 1)
        lcd.putstr("water        ")
        time.sleep(2)
        
        if bigbottle == 0:
            lcd.move_to(0, 0)
            lcd.putstr("you have a tiny   ")
            lcd.move_to(0, 1)
            lcd.putstr("bottle    ")
            time.sleep(2)
        if bigbottle == 1:
            lcd.move_to(0, 0)
            lcd.putstr("you have a big   ")
            lcd.move_to(0, 1)
            lcd.putstr("bottle    ")
            time.sleep(2)
        
        lcd.move_to(0, 0)
        lcd.putstr("<---lake           ")
        lcd.move_to(0, 1)
        lcd.putstr("shop--->    ")
        time.sleep(0.3)
        
        while place == "thirstt" and (button1.value() == 0 or button2.value() == 0):
            if button1.value() == 1:
                place = "lake"
                lcd.move_to(0, 0)
                lcd.putstr("you went to the")
                lcd.move_to(0, 1)
                lcd.putstr("lake...   ")
                REDLED.value(1)
                print("going to lake")
                time.sleep(1)
                REDLED.value(0)
                
            if button2.value() == 1:
                place = "thirst shop"
                lcd.move_to(0, 0)
                lcd.putstr("you went to the")
                lcd.move_to(0, 1)
                lcd.putstr("shop...   ")
                GREENLED.value(1)
                time.sleep(2)
                GREENLED.value(0)
        print("lake?")
    while place == "lake":
        lcd.move_to(0, 0)
        lcd.putstr("put water in     ")
        lcd.move_to(0, 1)
        lcd.putstr("the bottle...     ")
        time.sleep(0.1)
        power.value(1)        # Turn on the sensor
        time.sleep(1)         # Wait for sensor to stabilize

        value = signal.read_u16()  # Read analog value (0 to 65535)
        print("Water sensor reading:", value)

        power.value(0)        # Turn off sensor
        
        if value >= 20000:
            enoughwater += 1
            print("enough +1")
            if enoughwater >= 3:
            
                place = "afterlake"
        time.sleep(0.1)
        
    if place == "afterlake":
        power.value(0)
        print("gathered water")
        lcd.move_to(0, 0)
        lcd.putstr("you filled your    ")
        lcd.move_to(0, 1)
        lcd.putstr("bottle!!      ")
        time.sleep(2)
        lcd.move_to(0, 0)
        lcd.putstr("you give it to   ")
        lcd.move_to(0, 1)
        lcd.putstr(name + "        ")
        time.sleep(2)
        if bigbottle == 0:
            lcd.move_to(0, 0)
            lcd.putstr("+1 thirst!    ")
            lcd.move_to(0, 1)
            lcd.putstr("              ")
            thirstbar -= 1
            time.sleep(2)
            place = "home"
            true1 = 0
            print("going home")
            print(thirstbar)
            
        if bigbottle == 1:
            lcd.move_to(0, 0)
            lcd.putstr("you have a big    ")
            lcd.move_to(0, 1)
            lcd.putstr("bottle!")
            
            lcd.move_to(0, 0)
            lcd.putstr("+2 thirst!    ")
            lcd.move_to(0, 1)
            lcd.putstr("              ")
            thirstbar -= 2
            time.sleep(2)
            place = "home"
            true1 = 0
            print("going home")
            print(thirstbar)
        
    while place == "thirst shop":
        print("in shop")
        lcd.move_to(0, 0)
        lcd.putstr("welcome to the  ")
        lcd.move_to(0, 1)
        lcd.putstr("shop!           ")
        time.sleep(2)
        lcd.move_to(0, 0)
        lcd.putstr("you have           ")
        lcd.move_to(0, 1)
        lcd.putstr(str(coins) +" coins")
        time.sleep(2)
        lcd.move_to(0, 0)
        lcd.putstr("*big water - 5$")
        lcd.move_to(0, 1)
        lcd.putstr("*<<          *->")
        place = "big water"
        time.sleep(1)
        
#-----------------------------------------------------------------------------
        
    while place == "big water":
        if button3.value() == 1:
            print("go back home")
            place = "home"
            true1 = 0
            
        if button4.value() == 1:
            print("next: big bottle")
            lcd.move_to(0, 0)
            lcd.putstr("*big bottle-15$   ")
            lcd.move_to(0, 1)
            lcd.putstr("*<-          *->   ")
            time.sleep(1)
            place = "big bottle"
            
        if button1.value() == 1:
            print("buying it")
            place = "Bbig water"
            lcd.move_to(0, 0)
            lcd.putstr("do you want it?  ")
            lcd.move_to(0, 1)
            lcd.putstr("*yes         *no")
            
    while place == "Bbig water" and button1.value() == 0:
        if button4.value() == 1:
            print("back home")
            place = "home"
            true1 = 0
            
        if button3.value() == 1:
            if coins >= 5:
                print("bought it")
                coins -= 5
                lcd.move_to(0, 0)
                lcd.putstr("thanks for      ")
                lcd.move_to(0, 1)
                lcd.putstr("buying!              ")
                time.sleep(2)
                lcd.move_to(0, 0)
                lcd.putstr("you give it to   ")
                lcd.move_to(0, 1)
                lcd.putstr("".join(name) + "           ")
                time.sleep(2)
                lcd.move_to(0, 0)
                lcd.putstr("he likes it a      ")
                lcd.move_to(0, 1)
                lcd.putstr("lot!                ")
                time.sleep(2)
                lcd.move_to(0, 0)
                lcd.putstr("+ 3 thirst!     ")
                lcd.move_to(0, 1)
                lcd.putstr("- 500 TD!       ")
                thirstbar -= 3
                thirst -= 500
                print(thirstbar)
                time.sleep(2)
                place = "home"
                true1 = 0
            else:
                print("no money :P")
                lcd.move_to(0, 0)
                lcd.putstr("i'm sorry, you         ")
                lcd.move_to(0, 1)
                lcd.putstr("dont have enough      ")
                time.sleep(2)
                place = "home"
                true1 = 0
                time.sleep(2)
                
#--------------------------------------------------------------------------------
                
    while place == "big bottle":
        if button3.value() == 1:
            print("big ater")
            lcd.move_to(0, 0)
            lcd.putstr("*big water - 5$")
            lcd.move_to(0, 1)
            lcd.putstr("*<<          *->")
            place = "big water"
            time.sleep(1)
            
        if button4.value() == 1:
            print("super ater")
            lcd.move_to(0, 0)
            lcd.putstr("*superwater-25$")
            lcd.move_to(0, 1)
            lcd.putstr("*<-          *>>")
            place = "super water"
            time.sleep(1)
            
        if button1.value() == 1:
            print("buying it")
            place = "Bbig bottle"
            lcd.move_to(0, 0)
            lcd.putstr("do you want it?  ")
            lcd.move_to(0, 1)
            lcd.putstr("*yes         *no")
            
    while place == "Bbig bottle" and button1.value() == 0:
        if button4.value() == 1:
            print("back home")
            place = "home"
            true1 = 0
            
        if button3.value() == 1:
            if coins >= 15:
                print("bought it")
                coins -= 15
                lcd.move_to(0, 0)
                lcd.putstr("thanks for      ")
                lcd.move_to(0, 1)
                lcd.putstr("buying!              ")
                time.sleep(2)
                lcd.move_to(0, 0)
                lcd.putstr("you can fill up")
                lcd.move_to(0, 1)
                lcd.putstr("more water now")
                time.sleep(2)
                bigbottle = 1
                print(thirstbar)
                time.sleep(2)
                place = "home"
                true1 = 0
            else:
                print("no money :P")
                lcd.move_to(0, 0)
                lcd.putstr("i'm sorry, you         ")
                lcd.move_to(0, 1)
                lcd.putstr("dont have enough      ")
                time.sleep(2)
                place = "home"
                true1 = 0
                time.sleep(2)
                
#------------------------------------------------------------------------------------------
                
    while place == "super water":
        if button4.value() == 1:
            print("go back home")
            place = "home"
            true1 = 0
            
        if button3.value() == 1:
            print("next: big bottle")
            lcd.move_to(0, 0)
            lcd.putstr("*big bottle-15$   ")
            lcd.move_to(0, 1)
            lcd.putstr("*<-          *->   ")
            time.sleep(1)
            place = "big bottle"
            
        if button1.value() == 1:
            print("buying it")
            place = "Bsuper water"
            lcd.move_to(0, 0)
            lcd.putstr("do you want it?  ")
            lcd.move_to(0, 1)
            lcd.putstr("*yes         *no")
            
    while place == "Bsuper water" and button1.value() == 0:
        if button4.value() == 1:
            print("back home")
            place = "home"
            true1 = 0
            
        if button3.value() == 1:
            if coins >= 25:
                print("bought it")
                coins -= 20
                lcd.move_to(0, 0)
                lcd.putstr("thanks for      ")
                lcd.move_to(0, 1)
                lcd.putstr("buying!              ")
                time.sleep(2)
                lcd.move_to(0, 0)
                lcd.putstr("you give it to   ")
                lcd.move_to(0, 1)
                lcd.putstr("".join(name) + "           ")
                time.sleep(2)
                lcd.move_to(0, 0)
                lcd.putstr("he likes it very      ")
                lcd.move_to(0, 1)
                lcd.putstr("very much!                ")
                time.sleep(2)
                lcd.move_to(0, 0)
                lcd.putstr("+ 7 thirst!     ")
                lcd.move_to(0, 1)
                lcd.putstr("- 1500 TD!       ")
                thirstbar -= 7
                thirst -= 1500
                print(thirstbar)
                time.sleep(2)
                place = "home"
                true1 = 0
            else:
                print("no money :P")
                lcd.move_to(0, 0)
                lcd.putstr("i'm sorry, you         ")
                lcd.move_to(0, 1)
                lcd.putstr("dont have enough      ")
                time.sleep(2)
                place = "home"
                true1 = 0
                time.sleep(2)
                
                
#-----------------------------------------------------------------------------
    if place == "happyy":
        lcd.move_to(0, 0)
        lcd.putstr("*go for a walk     ")
        lcd.move_to(0, 1)
        lcd.putstr("*<<          *->")
        time.sleep(1)
        place = "UIwalk"
        
    if place == "UIwalk":
        if button1.value() == 1:
            lcd.move_to(0, 0)
            lcd.putstr("going to the      ")
            lcd.move_to(0, 1)
            lcd.putstr("forest...                ")
            print("going for a alk")
            place = "walk"
            time.sleep(2)
            lcd.move_to(0, 0)
            lcd.putstr("                   ")
            lcd.move_to(0, 1)
            lcd.putstr("                    ")
            
        if button3.value() == 1:
            lcd.move_to(0, 0)
            lcd.putstr("                 ")
            lcd.move_to(0, 1)
            lcd.putstr("                 ")
            true1 = 0
            place = "home"
            
        if button4.value() == 1:
            lcd.move_to(0, 0)
            lcd.putstr("*play with stick      ")
            lcd.move_to(0, 1)
            lcd.putstr("*<-          *->")
            place = "UIstick"
            time.sleep(1)
            
    if place == "UIstick":
        if button1.value() == 1:
            lcd.move_to(0, 0)
            lcd.putstr("going to the      ")
            lcd.move_to(0, 1)
            lcd.putstr("forest...                ")
            print("going play stick")
            place = "stick"
            time.sleep(2)
            lcd.move_to(0, 0)
            lcd.putstr("throw stick        ")
            lcd.move_to(0, 1)
            lcd.putstr(" /                   ")
            
        if button3.value() == 1:
            lcd.move_to(0, 0)
            lcd.putstr("*go for a walk      ")
            lcd.move_to(0, 1)
            lcd.putstr("*<<          *->")
            time.sleep(1)
            place = "UIwalk"
            time.sleep(1)
            
        if button4.value() == 1:
            lcd.move_to(0, 0)
            lcd.putstr("*play with toy        ")
            lcd.move_to(0, 1)
            lcd.putstr("*<-          *>>")
            place = "UItoy"
            time.sleep(1)
            
    if place == "UItoy":
        if button1.value() == 1:
            if toy == 1:
                lcd.move_to(0, 0)
                lcd.putstr("going back      ")
                lcd.move_to(0, 1)
                lcd.putstr("home...                ")
                print("going play toy")
                place = "toy"
                time.sleep(2)
                lcd.move_to(0, 0)
                lcd.putstr("                   ")
                lcd.move_to(0, 1)
                lcd.putstr("                    ")
                lcd.move_to(0, 0)
                lcd.putstr("                   ")
                lcd.move_to(7, 1)
                lcd.putstr(chr(0))
            else:
                lcd.move_to(0, 0)
                lcd.putstr("im sorry, you      ")
                lcd.move_to(0, 1)
                lcd.putstr("don't have a toy                ")
                time.sleep(2)
                true1 = 0
                place = "home"
            
        if button4.value() == 1:
            lcd.move_to(0, 0)
            lcd.putstr("                 ")
            lcd.move_to(0, 1)
            lcd.putstr("                 ")
            true1 = 0
            place = "home"
            
        if button3.value() == 1:
            lcd.move_to(0, 0)
            lcd.putstr("*play with stick       ")
            lcd.move_to(0, 1)
            lcd.putstr("*<-          *->")
            place = "UIstick"
            time.sleep(1)
                
    if place == "walk":
        x_val = vrx.read_u16()
        y_val = vry.read_u16()
        is_pressed = sw.value() == 0
        lcd.move_to(pet_x, pet_y)
        lcd.putstr(chr(0))
        if not pet_x == 0:
            lcd.move_to(pet_x - 1, pet_y)
            lcd.putstr(" ")
        lcd.move_to(pet_x + 1, pet_y)
        lcd.putstr(" ")
        if not pet_y == 0:
            lcd.move_to(pet_x, pet_y + 1)
            lcd.putstr(" ")
        lcd.move_to(pet_x, pet_y - 1)
        lcd.putstr(" ")

            
        if pet_x <= -1:
            pet_x = 0
            
        if pet_x >= 16:
            pet_x = 15

        #print("X:", x_val, "Y:", y_val, "Button:", "Pressed" if is_pressed else "Released")
        time.sleep(0.2)
        if 0 <= x_val <= 10000 and 1000 <= y_val <= 40000:
            print("left")
            pet_x -= 1
            moving += 1
            
        if 50000 <= x_val <= 70000 and 1000 <= y_val <= 40000:
            print("right")
            pet_x += 1
            moving += 1
            
        if 50000 <= y_val <= 70000 and 1000 <= x_val <= 40000:
            print("don")
            pet_y -= 1
            moving += 1
            
        if 0 <= y_val <= 10000 and 1000 <= x_val <= 40000:
            print("up")
            pet_y += 1
            moving += 1

        time.sleep(0.01)
        
        if moving >= 28:
            lcd.move_to(0, 0)
            lcd.putstr(name +" is happy!")
            lcd.move_to(0, 1)
            lcd.putstr("")
            time.sleep(2)
            lcd.move_to(0, 0)
            lcd.putstr("+0.5 happiness!   ")
            lcd.move_to(0, 1)
            lcd.putstr("")
            time.sleep(2)
            happybar += 0.5
            moving = 0
            place = "home"
            maxsearch = 0
            true1 = 0
        
        if button1.value() == 1 and moving >= 5 and maxsearch <= 1:
            maxsearch += 1
            print(maxsearch)
            lcd.move_to(0, 0)
            lcd.putstr(name +" is                ")
            lcd.move_to(0, 1)
            lcd.putstr("searching.              ")
            time.sleep(0.4)
            lcd.move_to(0, 1)
            lcd.putstr("searching..")
            time.sleep(0.4)
            lcd.move_to(0, 1)
            lcd.putstr("searching...")
            random.randint(1, 4)
            time.sleep(1.2)

            Srandom = random.randint(1, 4)
            
            print(Srandom)
                
            
            if Srandom == 2:
                lcd.move_to(0, 0)
                lcd.putstr(name +" found       ")
                lcd.move_to(0, 1)
                lcd.putstr("something!           ")
                time.sleep(2)
                lcd.move_to(0, 0)
                lcd.putstr(".                ")
                lcd.move_to(0, 1)
                lcd.putstr("                   ")
                Srandom = random.randint(1, 10)
                time.sleep(0.4)
                lcd.move_to(0, 0)
                lcd.putstr("..         ")
                lcd.move_to(0, 1)
                lcd.putstr("                   ")
                time.sleep(0.4)
                lcd.move_to(0, 0)
                lcd.putstr("...               ")
                lcd.move_to(0, 1)
                lcd.putstr("                   ")
                time.sleep(1.2)
                if Srandom == 1 or Srandom == 2 or Srandom == 3:
                    lcd.move_to(0, 0)
                    lcd.putstr("it's 5 coins!     ")
                    lcd.move_to(0, 1)
                    lcd.putstr("                   ")
                    coins += 5
                    time.sleep(2)
                    lcd.move_to(0, 0)
                    lcd.putstr("                  ")
                    lcd.move_to(0, 1)
                    lcd.putstr("                   ")
                
                if Srandom == 4 or Srandom == 5:
                    lcd.move_to(0, 0)
                    lcd.putstr("it's 10 coins!     ")
                    lcd.move_to(0, 1)
                    lcd.putstr("                   ")
                    coins += 10
                    time.sleep(2)
                    lcd.move_to(0, 0)
                    lcd.putstr("                  ")
                    lcd.move_to(0, 1)
                    lcd.putstr("                   ")
                    
                if Srandom == 6:
                    lcd.move_to(0, 0)
                    lcd.putstr("it was actually         ")
                    lcd.move_to(0, 1)
                    lcd.putstr("a scrap              ")
                    bigbottle = 0
                    time.sleep(2)
                    lcd.move_to(0, 0)
                    lcd.putstr("you threw it          ")
                    lcd.move_to(0, 1)
                    lcd.putstr("away...             ")
                    time.sleep(2)
                    lcd.move_to(0, 0)
                    lcd.putstr("                  ")
                    lcd.move_to(0, 1)
                    lcd.putstr("                   ")
                    
                if Srandom == 7:
                    lcd.move_to(0, 0)
                    lcd.putstr("it's a ground          ")
                    lcd.move_to(0, 1)
                    lcd.putstr("special fruit!                 ")
                    time.sleep(2)
                    lcd.move_to(0, 0)
                    lcd.putstr("you give it to    ")
                    lcd.move_to(0, 1)
                    lcd.putstr(name + "...")
                    time.sleep(2)
                    lcd.move_to(0, 0)
                    lcd.putstr("he likes it!     ")
                    lcd.move_to(0, 1)
                    lcd.putstr("               ")
                    time.sleep(2)
                    lcd.move_to(0, 0)
                    lcd.putstr("+1 hunger!    ")
                    lcd.move_to(0, 1)
                    lcd.putstr("+0.5 thirst!")
                    hungerbar -= 1
                    thirstbar -= 0.5
                    time.sleep(2)
                    lcd.move_to(0, 0)
                    lcd.putstr("                  ")
                    lcd.move_to(0, 1)
                    lcd.putstr("                   ")
                    
                if Srandom == 8:
                    lcd.move_to(0, 0)
                    lcd.putstr("it's a special         ")
                    lcd.move_to(0, 1)
                    lcd.putstr("fruit juice!                 ")
                    time.sleep(2)
                    lcd.move_to(0, 0)
                    lcd.putstr("you give it to    ")
                    lcd.move_to(0, 1)
                    lcd.putstr(name + "...")
                    time.sleep(2)
                    lcd.move_to(0, 0)
                    lcd.putstr("he likes it     ")
                    lcd.move_to(0, 1)
                    lcd.putstr("a lot!               ")
                    time.sleep(2)
                    lcd.move_to(0, 0)
                    lcd.putstr("+1.5 thirst!    ")
                    lcd.move_to(0, 1)
                    lcd.putstr("               ")
                    thirstbar -= 1.5
                    time.sleep(2)
                    lcd.move_to(0, 0)
                    lcd.putstr("he aged faster!    ")
                    lcd.move_to(0, 1)
                    lcd.putstr("AGE BONUS!")
                    age += 2500
                    time.sleep(2)
                    lcd.move_to(0, 0)
                    lcd.putstr("                  ")
                    lcd.move_to(0, 1)
                    lcd.putstr("                   ")
                    
                if Srandom == 9:
                    lcd.move_to(0, 0)
                    lcd.putstr("it's a           ")
                    lcd.move_to(0, 1)
                    lcd.putstr("super meat!                 ")
                    time.sleep(2)
                    lcd.move_to(0, 0)
                    lcd.putstr("you give it to          ")
                    lcd.move_to(0, 1)
                    lcd.putstr(name + "...                 ")
                    time.sleep(2)
                    lcd.move_to(0, 0)
                    lcd.putstr("he likes it             ")
                    lcd.move_to(0, 1)
                    lcd.putstr("really much!!!                 ")
                    time.sleep(2)
                    lcd.move_to(0, 0)
                    lcd.putstr(name + " is happy          ")
                    lcd.move_to(0, 1)
                    lcd.putstr("now!                  ")
                    time.sleep(2)
                    lcd.move_to(0, 0)
                    lcd.putstr("+1.5 hunger           ")
                    lcd.move_to(0, 1)
                    lcd.putstr("+1 happiness                 ")
                    time.sleep(2)
                    lcd.move_to(0, 0)
                    lcd.putstr("                   ")
                    lcd.move_to(0, 1)
                    lcd.putstr("                     ")
                    hungerbar -= 1.5
                    happybar -= 1
                    time.sleep(2)
                    
                if Srandom == 10:
                    lcd.move_to(0, 0)
                    lcd.putstr("it's a              ")
                    lcd.move_to(0, 1)
                    lcd.putstr("water bottle!                 ")
                    time.sleep(2)
                    lcd.move_to(0, 0)
                    lcd.putstr("you give it to          ")
                    lcd.move_to(0, 1)
                    lcd.putstr(name + "...                 ")
                    time.sleep(2)
                    lcd.move_to(0, 0)
                    lcd.putstr("he drinks it.              ")
                    lcd.move_to(0, 1)
                    lcd.putstr("                    ")
                    time.sleep(2)
                    lcd.move_to(0, 0)
                    lcd.putstr("+1 thirst!             ")
                    lcd.move_to(0, 1)
                    lcd.putstr("                    ")
                    thirstbar -= 1
                    time.sleep(2)
                    lcd.move_to(0, 0)
                    lcd.putstr("                  ")
                    lcd.move_to(0, 1)
                    lcd.putstr("                    ")
                    
            else:
                lcd.move_to(0, 0)
                lcd.putstr(name +" did not    ")
                lcd.move_to(0, 1)
                lcd.putstr("find anything...")
                time.sleep(2)
                lcd.move_to(0, 0)
                lcd.putstr("                      ")
                lcd.move_to(0, 1)
                lcd.putstr("                     ")
                
                
    if place == "stick":
        if sitch.value() == 1 and sticktime <= 20 and sticknumber <= 2:
            sticktime += 1
            lcd.move_to(0, 0)
            lcd.putstr("                 ")
            lcd.move_to(0, 1)
            lcd.putstr("  /                    ")
            time.sleep(0.1)
            
        if 2 <= sticktime <= 20 and sitch.value() == 0:
            continuestick = 0
            sticktime = 0
            lcd.move_to(0, 0)
            lcd.putstr("                 ")
            lcd.move_to(0, 1)
            lcd.putstr(" /                    ")
            time.sleep(0.4)
            lcd.move_to(0, 0)
            lcd.putstr("                 ")
            lcd.move_to(0, 1)
            lcd.putstr("/                     ")
            time.sleep(1)
            lcd.move_to(0, 0)
            lcd.putstr("                 ")
            lcd.move_to(0, 1)
            lcd.putstr(" /                     ")
            time.sleep(0.3)
            lcd.move_to(0, 0)
            lcd.putstr("                 ")
            lcd.move_to(0, 1)
            lcd.putstr("    /                     ")
            time.sleep(0.4)
            lcd.move_to(0, 0)
            lcd.putstr("                 ")
            lcd.move_to(0, 1)
            lcd.putstr("     /                     ")
            time.sleep(0.3)
            lcd.move_to(0, 0)
            lcd.putstr("                 ")
            lcd.move_to(0, 1)
            lcd.putstr("          /            ")
            time.sleep(0.3)
            lcd.move_to(0, 0)
            lcd.putstr("                 ")
            lcd.move_to(0, 1)
            lcd.putstr("             /    ")
            time.sleep(1)
            gonr = 0
            while continuestick == 0:
                if button1.value() == 1:
                    continuestick = 1
                    
            while gonr <= 11:
                lcd.move_to(0, 0)
                lcd.putstr("                 ")
                lcd.move_to(0, 1)
                lcd.putstr(" " * gonr + chr(0) + " " * (11 - gonr) + "/") 
                gonr +=1
                time.sleep(0.2)
                
            time.sleep(1)
            gonr = 0
            continuestick = 0
            while continuestick == 0:
                if button1.value() == 1:
                    continuestick = 1
                    
                    
            continuestick = 0
            while gonr <= 11:
                lcd.move_to(0, 0)
                lcd.putstr("                 ")
                lcd.move_to(0, 1)
                lcd.putstr(" " * (11 - gonr) + chr(0) + "/" + " " * gonr + " ") 
                gonr +=1
                time.sleep(0.2)
                
            gonr = 0
            continuestick = 0
            time.sleep(1)
            sticknumber +=1
            continuestick = 0
            
        if sticknumber == 2:
            lcd.move_to(0, 0)
            lcd.putstr(name + " is happy!")
            lcd.move_to(0, 1)
            lcd.putstr("                  ")
            time.sleep(2)
            lcd.move_to(0, 0)
            lcd.putstr("+0.5 happiness!")
            lcd.move_to(0, 1)
            lcd.putstr("                  ")
            lcd.move_to(0, 0)
            time.sleep(2)
            lcd.putstr("                  ")
            lcd.move_to(0, 1)
            lcd.putstr("                  ")
            happybar -= 0.5
            true1 = 0
            place = "home"
            
    if place == "toy":
        if button1.value() == 1:
            if buttonsecventa2 == 0 and buttonsecventa3 == 0:
                buttonsecventa1 = 1
                lcd.move_to(0, 0)
                lcd.putstr("                  ")
                lcd.move_to(0, 1)
                lcd.putstr("                   ")
                lcd.move_to(8, 1)
                lcd.putstr(chr(0))
                time.sleep(0.4)
                lcd.move_to(0, 1)
                lcd.putstr("                   ")
                lcd.move_to(9, 1)
                lcd.putstr(chr(0))
                time.sleep(0.4)
                lcd.move_to(0, 1)
                lcd.putstr("                   ")
                lcd.move_to(10, 1)
                lcd.putstr(chr(0))
                time.sleep(0.4)
                lcd.move_to(0, 1)
                lcd.putstr("                   ")
                lcd.move_to(9, 0)
                lcd.putstr(chr(0))
                time.sleep(0.4)
                lcd.move_to(0, 0)
                lcd.putstr("                   ")
                lcd.move_to(8, 0)
                lcd.putstr(chr(0))
                time.sleep(0.4)
                lcd.move_to(0, 0)
                lcd.putstr("                   ")
                lcd.move_to(7, 1)
                lcd.putstr(chr(0))
                time.sleep(1)
            else:
                lcd.move_to(0, 0)
                lcd.putstr("wrong button!      ")
                lcd.move_to(0, 1)
                lcd.putstr("         ")
                time.sleep(2)
                buttonsecventa1 = 0
                buttonsecventa2 = 0
                buttonsecventa3 = 0
                lcd.move_to(0, 0)
                lcd.putstr(name + " is         ")
                lcd.move_to(0, 1)
                lcd.putstr("confused")
                time.sleep(2)
                lcd.move_to(0, 0)
                lcd.putstr("-0.5 happiness.     ")
                lcd.move_to(0, 1)
                lcd.putstr("                 ")
                happybar += 0.5
                true1 = 0
                place == "home"
            
        if button2.value() == 1:
            if buttonsecventa1 == 1 and buttonsecventa3 == 0:
                buttonsecventa2 = 1
                lcd.move_to(0, 0)
                lcd.putstr("               ")
                lcd.move_to(0, 1)
                lcd.putstr("               ")
                lcd.move_to(7, 0)
                lcd.putstr(chr(0))
                lcd.move_to(7, 1)
                lcd.putstr(chr(2))
                lcd.move_to(0, 0)
                time.sleep(0.4)
                lcd.putstr("               ")
                lcd.move_to(0, 1)
                lcd.putstr("               ")
                lcd.move_to(6, 0)
                lcd.putstr(chr(0))
                lcd.move_to(0, 0)
                time.sleep(0.3)
                lcd.putstr("               ")
                lcd.move_to(5, 0)
                lcd.putstr(chr(0))
                lcd.move_to(0, 0)
                time.sleep(0.3)
                lcd.putstr("               ")
                lcd.move_to(5, 1)
                lcd.putstr(chr(0))
                lcd.move_to(0, 0)
                time.sleep(0.3)
                        
            else:
                lcd.move_to(0, 0)
                lcd.putstr("wrong button!      ")
                lcd.move_to(0, 1)
                lcd.putstr("         ")
                time.sleep(2)
                buttonsecventa1 = 0
                buttonsecventa2 = 0
                buttonsecventa3 = 0
                lcd.move_to(0, 0)
                lcd.putstr(name + " is         ")
                lcd.move_to(0, 1)
                lcd.putstr("confused")
                time.sleep(2)
                lcd.move_to(0, 0)
                lcd.putstr("-0.5 happiness.     ")
                lcd.move_to(0, 1)
                lcd.putstr("                 ")
                happybar += 0.5
                true1 = 0
                place == "home"
                
        if button3.value() == 1:
            if buttonsecventa1 == 1 and buttonsecventa2 == 1:
                buttonsecventa3 = 1
                lcd.move_to(6, 1)
                lcd.putstr(chr(0))
                time.sleep(0.3)
                lcd.move_to(0, 1)
                lcd.putstr("            ")
                lcd.move_to(6, 0)
                lcd.putstr(chr(0))
                lcd.move_to(6, 1)
                lcd.putstr(chr(2))
                time.sleep(0.3)
                lcd.move_to(0, 1)
                lcd.putstr("                 ")
                lcd.move_to(0, 0)
                lcd.putstr("                 ")
                lcd.move_to(7, 0)
                lcd.putstr(chr(0))
                time.sleep(0.3)
                lcd.move_to(0, 1)
                lcd.putstr("                 ")
                lcd.move_to(0, 0)
                lcd.putstr("                 ")
                lcd.move_to(7, 1)
                lcd.putstr(chr(0))
                time.sleep(0.3)
                lcd.move_to(0, 1)
                lcd.putstr("                 ")
                lcd.move_to(0, 0)
                lcd.putstr("                 ")
                lcd.move_to(8, 0)
                lcd.putstr(chr(0))
                lcd.move_to(7, 1)
                lcd.putstr(chr(2))
                time.sleep(0.3)
                lcd.move_to(0, 1)
                lcd.putstr("                 ")
                lcd.move_to(0, 0)
                lcd.putstr("                 ")
                lcd.move_to(9, 0)
                lcd.putstr(chr(0))
                time.sleep(0.3)
                lcd.move_to(0, 1)
                lcd.putstr("                 ")
                lcd.move_to(0, 0)
                lcd.putstr("                 ")
                lcd.move_to(8, 1)
                lcd.putstr(chr(0))
                time.sleep(0.3)
                lcd.move_to(0, 1)
                lcd.putstr("                 ")
                lcd.move_to(0, 0)
                lcd.putstr("                 ")
                lcd.move_to(7, 1)
                lcd.putstr(chr(0))
                time.sleep(0.3)
                        
            else:
                lcd.move_to(0, 0)
                lcd.putstr("wrong button!      ")
                lcd.move_to(0, 1)
                lcd.putstr("         ")
                time.sleep(2)
                buttonsecventa1 = 0
                buttonsecventa2 = 0
                buttonsecventa3 = 0
                lcd.move_to(0, 0)
                lcd.putstr(name + " is         ")
                lcd.move_to(0, 1)
                lcd.putstr("confused")
                time.sleep(2)
                lcd.move_to(0, 0)
                lcd.putstr("-0.5 happiness.     ")
                lcd.move_to(0, 1)
                lcd.putstr("                 ")
                happybar += 0.5
                true1 = 0
                place == "home"
                
        
        if buttonsecventa1 == 1 and buttonsecventa2 == 1 and buttonsecventa3 == 1:
            if button4.value() == 1:
                lcd.move_to(0, 0)
                lcd.putstr(name + " is so happy!      ")
                lcd.move_to(0, 1)
                lcd.putstr("                 ")
                time.sleep(2)
                lcd.move_to(0, 0)
                lcd.putstr("+1.5 happiness!      ")
                lcd.move_to(0, 1)
                lcd.putstr("                    ")
                time.sleep(2)
                lcd.move_to(0, 0)
                lcd.putstr("              ")
                lcd.move_to(0, 1)
                lcd.putstr("                    ")
                happybar -= 1.5
                true1 = 0
                place = "home"


#---------------------------------------------------------------

    while place == "hunger shop":
        print("in shop")
        lcd.move_to(0, 0)
        lcd.putstr("welcome to the  ")
        lcd.move_to(0, 1)
        lcd.putstr("hunger shop!           ")
        time.sleep(2)
        lcd.move_to(0, 0)
        lcd.putstr("you have           ")
        lcd.move_to(0, 1)
        lcd.putstr(str(coins) +" coins        ")
        time.sleep(2)
        lcd.move_to(0, 0)
        lcd.putstr("*porkchop - 5$       ")
        lcd.move_to(0, 1)
        lcd.putstr("*<<          *->")
        place = "porkchop"
        time.sleep(1)
        
#-----------------------------------------------------------------------------
        
    while place == "porkchop":
        if button3.value() == 1:
            print("go back home")
            place = "home"
            true1 = 0
            
        if button4.value() == 1:
            print("super ater")
            lcd.move_to(0, 0)
            lcd.putstr("*toy - 25$         ")
            lcd.move_to(0, 1)
            lcd.putstr("*<-          *>>")
            place = "toyy"
            time.sleep(1)
            
        if button1.value() == 1:
            print("buying it")
            place = "Bporkchop"
            lcd.move_to(0, 0)
            lcd.putstr("do you want it?  ")
            lcd.move_to(0, 1)
            lcd.putstr("*yes         *no")
            
    while place == "Bporkchop" and button1.value() == 0:
        if button4.value() == 1:
            print("back home")
            place = "home"
            true1 = 0
            
        if button3.value() == 1:
            if coins >= 5:
                print("bought it")
                coins -= 5
                lcd.move_to(0, 0)
                lcd.putstr("thanks for      ")
                lcd.move_to(0, 1)
                lcd.putstr("buying!              ")
                time.sleep(2)
                lcd.move_to(0, 0)
                lcd.putstr("you give it to   ")
                lcd.move_to(0, 1)
                lcd.putstr("".join(name) + "           ")
                time.sleep(2)
                lcd.move_to(0, 0)
                lcd.putstr("he likes it!      ")
                lcd.move_to(0, 1)
                lcd.putstr("                   ")
                time.sleep(2)
                lcd.move_to(0, 0)
                lcd.putstr("+ 1 hunger!     ")
                lcd.move_to(0, 1)
                lcd.putstr("- 800 HD!       ")
                hungerbar -= 1
                hunger -= 800
                print(hungerbar)
                time.sleep(2)
                place = "home"
                true1 = 0
            else:
                print("no money :P")
                lcd.move_to(0, 0)
                lcd.putstr("i'm sorry, you         ")
                lcd.move_to(0, 1)
                lcd.putstr("dont have enough      ")
                time.sleep(2)
                place = "home"
                true1 = 0
                time.sleep(2)
                
#--------------------------------toy-----------------------------------
                
    while place == "toyy":
        if button3.value() == 1:
            print("super meat")
            lcd.move_to(0, 0)
            lcd.putstr("*porkchop - 5$")
            lcd.move_to(0, 1)
            lcd.putstr("*<<          *->")
            place = "porkchop"
            time.sleep(1)
            
        if button4.value() == 1:
            print("go back home")
            place = "home"
            true1 = 0
            
        if button1.value() == 1:
            print("buying it")
            place = "Btoy"
            lcd.move_to(0, 0)
            lcd.putstr("do you want it?  ")
            lcd.move_to(0, 1)
            lcd.putstr("*yes         *no")
            
    while place == "Btoy" and button1.value() == 0:
        if button4.value() == 1:
            print("back home")
            place = "home"
            true1 = 0
            
        if button3.value() == 1:
            if coins >= 25:
                print("bought it")
                coins -= 25
                lcd.move_to(0, 0)
                lcd.putstr("thanks for      ")
                lcd.move_to(0, 1)
                lcd.putstr("buying!              ")
                time.sleep(2)
                lcd.move_to(0, 0)
                lcd.putstr("you can play    ")
                lcd.move_to(0, 1)
                lcd.putstr("with ".join(name) + "...           ")
                time.sleep(2)
                lcd.move_to(0, 0)
                lcd.putstr("he will love it!      ")
                lcd.move_to(0, 1)
                lcd.putstr("                       ")
                time.sleep(2)
                toy = 1
                print(hungerbar)
                time.sleep(2)
                place = "home"
                true1 = 0
            else:
                print("no money :P")
                lcd.move_to(0, 0)
                lcd.putstr("i'm sorry, you         ")
                lcd.move_to(0, 1)
                lcd.putstr("dont have enough      ")
                time.sleep(2)
                place = "home"
                true1 = 0
                time.sleep(2)



# i2c_lcd.py
from lcd_api import LcdApi
from machine import I2C
from time import sleep_ms

class I2cLcd(LcdApi):
    # LCD commands
    LCD_CLR             = 0x01
    LCD_HOME            = 0x02
    LCD_ENTRY_MODE      = 0x04
    LCD_DISPLAY_CONTROL = 0x08
    LCD_FUNCTION_SET    = 0x20
    LCD_SET_DDRAM_ADDR  = 0x80

    def __init__(self, i2c, addr, num_lines, num_columns):
        self.i2c = i2c
        self.addr = addr
        self.num_lines = num_lines
        self.num_columns = num_columns
        self.backlight = 0x08
        self.init_lcd()
        super().__init__(num_lines, num_columns)

    def init_lcd(self):
        sleep_ms(50)
        self.send(0x03)
        sleep_ms(5)
        self.send(0x03)
        sleep_ms(1)
        self.send(0x03)
        self.send(0x02)
        self.send(self.LCD_FUNCTION_SET | 0x08)
        self.send(self.LCD_DISPLAY_CONTROL | 0x04)
        self.send(self.LCD_CLR)
        sleep_ms(2)
        self.send(self.LCD_ENTRY_MODE | 0x02)

    def send(self, data, mode=0):
        high = mode | (data & 0xF0) | self.backlight
        low = mode | ((data << 4) & 0xF0) | self.backlight
        self.i2c.writeto(self.addr, bytearray([high | 0x04]))
        self.i2c.writeto(self.addr, bytearray([high]))
        self.i2c.writeto(self.addr, bytearray([low | 0x04]))
        self.i2c.writeto(self.addr, bytearray([low]))

    def putchar(self, char):
        self.send(ord(char), mode=0x01)

    def move_to(self, x, y):
        addr = x + 0x40 * y
        self.send(self.LCD_SET_DDRAM_ADDR | addr)



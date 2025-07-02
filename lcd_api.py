# lcd_api.py
class LcdApi:
    def __init__(self, num_lines, num_columns):
        self.num_lines = num_lines
        self.num_columns = num_columns
        self.cursor_x = 0
        self.cursor_y = 0

    def clear(self):
        self.putstr(" " * (self.num_columns * self.num_lines))
        self.move_to(0, 0)

    def move_to(self, x, y):
        self.cursor_x = x
        self.cursor_y = y

    def putstr(self, string):
        for char in string:
            if char == '\n':
                self.cursor_y += 1
                self.cursor_x = 0
            else:
                self.putchar(char)
                self.cursor_x += 1
                if self.cursor_x >= self.num_columns:
                    self.cursor_x = 0
                    self.cursor_y += 1
            if self.cursor_y >= self.num_lines:
                self.cursor_y = 0

    def putchar(self, char):
        raise NotImplementedError



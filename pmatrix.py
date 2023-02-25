import shutil     # import shutil module for accessing terminal size
import time       # import time module for sleep function
import random     # import random module for generating random integers
import struct     # import struct module for working with binary data
import sys        # import sys module for standard I/O operations

class message(str):
    # message class that inherits from str and sets its own speed and position
    def __new__(cls, text, speed):
        self = super(message, cls).__new__(cls, text)
        self.speed = speed
        self.y = -1 * len(text)  # set message position
        self.x = random.randint(0, display().width)
        self.skip = 0
        return self

    def move(self):
        # move the message by increasing y and resetting skip
        if self.speed > self.skip:
            self.skip += 1
        else:
            self.skip = 0
            self.y += 1

class display(list):
    # display class that inherits from list and sets its own width and height
    def __init__(self):
        self.height, self.width = shutil.get_terminal_size()
        self[:] = [' ' for y in range(self.height) for x in range(self.width)]

    def set_vertical(self, x, y, string):
        # set string vertically at x, y position on the display
        string = string[::-1]
        if x < 0:                 # ensure x is within display boundaries
            x = 80 + x
        if x >= self.width:
            x = self.width - 1
        if y < 0:                 # ensure y is within display boundaries
            string = string[abs(y):]
            y = 0
        if y + len(string) > self.height:
            string = string[0:self.height - y]
        if y >= self.height:
            return
        start = y * self.width + x
        length = self.width * (y + len(string))
        step = self.width
        self[start:length:step] = string

    def __str__(self):
        # convert display to a string
        return ''.join(self)

def matrix(iterations, sleep_time=.08):
    # function that generates the matrix rain animation
    messages = []
    d = display()      # create a display object
    for _ in range(iterations):
        messages.append(message('10' * 16, random.randint(1, 5)))   # append a message object to the list
        for text in messages:
            d.set_vertical(text.x, text.y, text)    # set the message on the display
            text.move()                             # move the message
        sys.stdout.write('\033[1m\033[32m%s\033[0m\r' % d)  # print the display
        sys.stdout.flush()
        time.sleep(sleep_time)  # pause the program for sleep_time seconds


if __name__ == '__main__':
    # Loop indefinitely
    while True:
        try:
            # Call the matrix function with 150 iterations
            matrix(150)
        # Catch a KeyboardInterrupt exception, which is raised when the user presses Ctrl+C
        except KeyboardInterrupt:
            # Print a message indicating that the program has stopped
            sys.stdout.write('\n\033[1m\033[32m=== Matrix Stopped ====\033[0m\n')
            # Exit the program
            sys.exit()


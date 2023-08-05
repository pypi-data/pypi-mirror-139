import sys, os, time
from code import terminal


class Chat():
    def __init__(self, name, color):
        self.name = name
        self.color = color

        self.reset = "\033[0m"


    def say(self, text):
        print(self.color+self.name+self.reset, end='')
        for i in text:
            sys.stdout.write(i)
            sys.stdout.flush()
            time.sleep(0.004)
        print()
        input()


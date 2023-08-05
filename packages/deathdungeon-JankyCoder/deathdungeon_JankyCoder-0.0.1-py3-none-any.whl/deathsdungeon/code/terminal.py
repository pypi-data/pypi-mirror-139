import sys, os, time


def clear():
    """Clears the screen"""
    os.system('clear')


def custom(fg, bg=[]):
    """Builds a custom color from an RGB Value"""
    if bg:
        return f"\033[38;2;{fg[0]};{fg[1]};{fg[2]}m\033[48;2;{self.bg[0]};{self.bg[1]};{self.bg[2]}m"
    else:
        return f"\033[38;2;{fg[0]};{fg[1]};{fg[2]}m"


def slow_print(string, t=0.05):
    """Prints a string letter by letter"""
    for letter in string:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(t)
    print()
    


    

reset = "\033[0m"
fgBlack = "\033[30m"
fgBrightBlack = "\033[30;1m"
bgBlack = "\033[40m"
bgBrightBlack = "\033[40;1m"
fgRed = "\033[31m"
fgBrightRed = "\033[31;1m"
bgRed = "\033[41m"
bgBrightRed = "\033[41;1m"
fgGreen = "\033[32m"
fgBrightGreen = "\033[32;1m"
bgGreen = "\033[42m"
bgBrightGreen = "\033[42;1m"
fgYellow = "\033[33m"
fgBrightYellow = "\033[33;1m"
bgYellow = "\033[43m"
bgBrightYellow = "\033[43;1m"
fgBlue = "\033[34m"
fgBrightBlue = "\033[34;1m"
bgBlue = "\033[44m"
bgBrightBlue = "\033[44;1m"
fgMagenta = "\033[35m"
fgBrightMagenta = "\033[35;1m"
bgMagenta = "\033[45m"
bgBrightMagenta = "\033[45;1m"
fgCyan = "\033[36m"
fgBrightCyan = "\033[36;1m"
bgCyan = "\033[46m"
bgBrightCyan = "\033[46;1m"
fgWhite = "\033[37m"
fgBrightWhite = "\033[37;1m"
bgWhite = "\033[47m"
bgBrightWhite = "\033[47;1m"
#Words Per Minute
import curses
from curses import wrapper
import time
import random

def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "Welcome to the Speed Typer!") #row, column
    stdscr.addstr("\nPress any key to begin!")
    stdscr.refresh()
    stdscr.getkey()

def display_text(stdscr, target, current, wpm = 0):
    stdscr.addstr(target)
    stdscr.addstr(1, 0, F"WPM: {wpm}")

    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1)
        if char != correct_char:
            color = curses.color_pair(2)
        stdscr.addstr(0, i, char, color)
    
def load_text():
    with open("random.txt", "r") as f: #context manager
        lines = f.readlines()
        return random.choice(lines).strip()

def wpm_test(stdscr):
    target_text = load_text()
    current_text = [] #list keeps tracks of all keys we have pressed
    wpm = 0
    start_time = time.time() #represents epoch/ current time
    stdscr.nodelay(True)

    while True:
        time_elapsed = max(time.time() - start_time, 1) #new time - start time
        wpm = round((len(current_text) / (time_elapsed / 60))/ 5) # 5 chars = 1 word
        
        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        if "".join(current_text) == target_text: # "" is the delimeter
            stdscr.nodelay(False)
            break

        try:
            key = stdscr.getkey()
        except:
            continue
        
        if ord(key) == 8: #ASCII table
            break

        if key in ("KEY_BACKSPACE", '\b', "\x7f"): #backspace key on diff operating systems
            if len(current_text) > 0:
                current_text.pop() # remove last element from list
        elif len(current_text) < len(target_text):
            current_text.append(key)
    


def main(stdscr): #stdscreen -> output -> terminal
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start_screen(stdscr)
    
    while True:
        wpm_test(stdscr)
        stdscr.addstr(2, 0, "You completed the text! Press any key to continue")
        key = stdscr.getkey()
        
        if ord(key) == 8 :
            break


wrapper(main)

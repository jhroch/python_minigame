# Python minigame (snake)
# Author: Jiří Hroch

import curses
import random
import time

# Settings
height: int = 13
#width: int = 13
width: int = int(height*1.85) # Recommended ratio
timeLimit: int = 30
bonusMultiplier: float = 1

class Player:
    def __init__(self, x, y, points):
        self.x = x
        self.y = y
        self.points = points
    def up(self):
        if(0 <= self.y - 1 < height):
            self.y = self.y-1
    def down(self):
        if(0 <= self.y + 1 < height):
            self.y = self.y+1
    def left(self):
        if(0 <= self.x - 1 < width):
            self.x = self.x-1
    def right(self):
        if(0 <= self.x + 1 < width):
            self.x = self.x+1
    def inc(self):
        self.points = self.points+1

class Korist:
    def __init__(self, x, y):
        self.x = x
        self.y = y

player = Player(0, 0, 0)
korist = Korist(random.randint(0, width-1), random.randint(0, height-1))
startTime = time.time()

def printGame(stdscr, timeLeft) -> None:
    for i in range(height):
        for j in range(width):
            stdscr.addstr("+-")
        stdscr.addstr("+\n")
        for k in range(width):
            if(i == player.y and k == player.x): stdscr.addstr("|*")
            elif(i == korist.y and k == korist.x): stdscr.addstr("|&")
            else: stdscr.addstr("| ")
        stdscr.addstr("|\n")
    for j in range(width):
        stdscr.addstr("+-")
    stdscr.addstr("+\n",)
    stdscr.addstr(f"Points: {player.points}\n")
    stdscr.addstr(f"Time left: {timeLeft}\n")
    
def gameOver(stdscr) -> None:
    while(1):
        stdscr.clear()
        stdscr.addstr(f"GAME OVER!\nYou've had {player.points} points. Congratulation!\nPress q for exit")
        key = stdscr.getch()
        if(key == ord('q')): break
        stdscr.refresh()
        


def main(stdscr):
    curses.curs_set(0) # Skryje kurzor
    stdscr.timeout(1000)
    while(1):
        timeLeft = timeLimit - int(time.time()-startTime) + player.points*bonusMultiplier
        stdscr.clear()
        if(player.x == korist.x and player.y == korist.y):
            player.inc()
            korist.x = random.randint(0, width-1)
            korist.y = random.randint(0, height-1)
        printGame(stdscr, timeLeft)
        stdscr.refresh()
        key = stdscr.getch()
        if(key == ord('q')): break
        if(timeLeft < 1): break
        if(key == curses.KEY_UP): player.up()
        if(key == curses.KEY_DOWN): player.down()
        if(key == curses.KEY_LEFT): player.left()
        if(key == curses.KEY_RIGHT): player.right()
        else: continue
    gameOver(stdscr)

curses.wrapper(main)
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
        self.points = points
        self.body = [(x,y)] # self.body[0] = hlava/start
        self.grow = False
        self.direction = None
        
    def move(self, dx, dy):
        #if(0 <= self.body[0][0] + 1 < width):
            head_x, head_y = self.body[0]
            new_head = (head_x + dx, head_y + dy)
            self.body.insert(0, new_head)  # add new head at the front
            if not self.grow:
                self.body.pop()                # remove last segment (unless growing)
            self.grow = False     
        #else:
            #return 1
    def inc(self):
        self.points = self.points+1
        self.grow = True

class Korist:
    def __init__(self, x, y):
        self.x = x
        self.y = y

player = Player(0, 0, 0)
korist = Korist(random.randint(0, width-1), random.randint(0, height-1))

def printGame(stdscr) -> None:
    for i in range(height):
        for j in range(width):
            stdscr.addstr("+-")
        stdscr.addstr("+\n")
        for k in range(width):
            if(k, i) in player.body[:]: stdscr.addstr("|*")
            elif(i == korist.y and k == korist.x): stdscr.addstr("|&")
            else: stdscr.addstr("| ")
        stdscr.addstr("|\n")
    for j in range(width):
        stdscr.addstr("+-")
    stdscr.addstr("+\n",)
    stdscr.addstr(f"Points: {player.points}\n")
    
def gameOver(stdscr) -> None:
    while(1):
        stdscr.clear()
        stdscr.addstr(f"GAME OVER!\nYou've had {player.points} points. Congratulation!\nPress q for exit\nPress r for restart game")
        key = stdscr.getch()
        if(key == ord('q')): break
        if(key == ord('r')):
            player.body.clear()
            player.body.append((0,0))
            player.points = 0
            main(stdscr)
        stdscr.refresh()
        


def main(stdscr):
    curses.curs_set(0) # Skryje kurzor
    stdscr.timeout(120)
    direction = None
    while(1):
        stdscr.clear()
        if(player.body[0][0] == korist.x and player.body[0][1] == korist.y):
            player.inc()
            korist.x = random.randint(0, width-1)
            korist.y = random.randint(0, height-1)
        printGame(stdscr)
        key = stdscr.getch()
        if(key == ord('q')): break
        if(key == curses.KEY_UP): direction = "up"
        if(key == curses.KEY_DOWN): direction = "down"
        if(key == curses.KEY_LEFT): direction = "left"
        if(key == curses.KEY_RIGHT): direction = "right"
        match direction:
            case "up":
                if player.direction == "down": 
                    direction = "down"
                    continue
                player.move(0, -1)
                player.direction = "up"
            case "down":
                if player.direction == "up": 
                    direction = "up"
                    continue
                player.move(0, 1)
                player.direction = "down"
            case "left":
                if player.direction == "right": 
                    direction = "right"
                    continue
                player.move(-1, 0)
                player.direction = "left"
            case "right":
                if player.direction == "left": 
                    direction = "left"
                    continue
                player.move(1, 0)
                player.direction = "right"
            case _:
                continue

    gameOver(stdscr)

curses.wrapper(main)
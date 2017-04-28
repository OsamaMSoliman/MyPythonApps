from PacMan.Maze import Maze, Direction
from PacMan.Characters import Hero, Enemy

maze = None
hero = None
enemy1 = None
enemy2 = None


def init():
    global maze
    global hero
    global enemy1
    global enemy2
    # create Maze
    maze = Maze(10, 100)
    # create Hero
    hero = Hero(50, 50, 3)
    # create Enemy
    enemy1 = Enemy(0, 0)
    enemy2 = Enemy(99, 99)


def loop():
    global maze
    global hero
    global enemy1
    global enemy2
    # draw Maze
    maze_walls = maze.get_maze_wall_list()
    Xdraw(maze_walls)
    # draw character
    Xdraw(hero.posX, hero.posY)
    # draw enemy
    Xdraw(enemy1.posX, enemy1.posY)
    Xdraw(enemy2.posX, enemy2.posY)
    # move enemy (delayed VERY IMP NOT EVERY FRAME!!!!) not sure what's the best way to approach this (maybe use
    # threading, and maybe it shouldn't be here but in the enemy class itself) draw score
    Xdraw(Hero.SCORE)



def key_event():
    # move character
    global hero
    if Xinput() == "UP":
        hero.move(Direction.NORTH)
    elif Xinput() == "DOWN":
        hero.move(Direction.SOUTH)
    elif Xinput() == "RIGHT":
        hero.move(Direction.EAST)
    elif Xinput() == "LEFT":
        hero.move(Direction.WEST)


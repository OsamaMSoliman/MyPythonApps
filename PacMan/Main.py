from PacMan.Maze import Maze
from PacMan.Characters import Hero, Enemy


def init():
    # create Maze
    maze = Maze(10, 100)
    # create Hero
    hero = Hero(50, 50, 3)
    # create Enemy
    enemy1 = Enemy(0, 0)
    enemy2 = Enemy(99, 99)


def loop():
    # draw Maze
    # draw character
    # draw enemy
    # move enemy (delayed VERY IMP NOT EVERY FRAME!!!!)
    # draw score
    pass


def key_event():
    # move character
    pass

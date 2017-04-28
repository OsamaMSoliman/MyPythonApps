from PacMan.Maze import Maze, Direction, GameOver
from PacMan.Characters import Hero, Enemy

maze = None
hero = None
enemy1 = None
enemy2 = None


def X_init():
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


def X_loop():
    global maze
    global hero
    global enemy1
    global enemy2
    while not GameOver:
        # draw Maze
        maze_walls = maze.get_maze_wall_list()
        X_draw(maze_walls)
        # draw character
        X_draw(hero.posX, hero.posY)
        # draw enemy
        X_draw(enemy1.posX, enemy1.posY)
        X_draw(enemy2.posX, enemy2.posY)
        # move enemy (delayed VERY IMP NOT EVERY FRAME!!!!) not sure what's the best way to approach this (maybe use
        # threading, and maybe it shouldn't be here but in the enemy class itself) draw score
        X_draw(Hero.SCORE)



def X_key_event():
    # move character
    global hero
    if not GameOver:
        if X_input() == "UP":
            hero._move(Direction.NORTH)
        elif X_input() == "DOWN":
            hero._move(Direction.SOUTH)
        elif X_input() == "RIGHT":
            hero._move(Direction.EAST)
        elif X_input() == "LEFT":
            hero._move(Direction.WEST)


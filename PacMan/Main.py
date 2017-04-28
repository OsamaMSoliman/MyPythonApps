from PacMan.Maze import Maze, Direction, GameOver
from PacMan.Characters import Hero, Enemy

maze = None
hero = None
enemy1 = None
enemy2 = None


def X_init():  # <<< Debugging::Abdullah this function tells u how u should initiate the Maze, Hero, Enemies
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


def X_loop():  # <<< Debugging::Abdullah here i'm referring to the loop function that GLUT uses to draw each frame
    global maze
    global hero
    global enemy1
    global enemy2
    if not GameOver:                            # Debugging::Abdullah check if game is over u can stop
                                                # Debugging::Abdullah (not sure how either but that's not a problem as i
                                                # Debugging::Abdullah put the Hero outside the screen if he loses (-1,-1)
        # draw Maze
        maze_walls = maze.get_maze_wall_list()  # Debugging::Abdullah u should draw the maze walls and that's how u get them
        X_draw(maze_walls)                      # Debugging::Abdullah this is a list of lists of tuples [[(x1,y1), (x2,y2)], [], ...]
        # draw character                        # Debugging::Abdullah u can print it to double check
        X_draw(hero.posX, hero.posY)
        # draw enemy
        X_draw(enemy1.posX, enemy1.posY)        # Debugging::Abdullah here is how u should draw the Hero and the Enemies
        X_draw(enemy2.posX, enemy2.posY)
        X_draw(Hero.SCORE)                      # Debugging::Abdullah here i'm not sure how to draw the score,
                                                # Debugging::Abdullah but Hero.SCORE is an int carrying the score


def X_key_event():
    # move character
    global hero
    if not GameOver:                            # Debugging::Abdullah checking if game is not over
        if X_input() == "UP":                   # Debugging::Abdullah i'm not sure how will u determine the state of the input
            hero._move(Direction.NORTH)         # Debugging::Abdullah but that's something u will know from glut docs
        elif X_input() == "DOWN":               # Debugging::Abdullah lastly it's very Important to use the Direction class
            hero._move(Direction.SOUTH)
        elif X_input() == "RIGHT":
            hero._move(Direction.EAST)
        elif X_input() == "LEFT":
            hero._move(Direction.WEST)

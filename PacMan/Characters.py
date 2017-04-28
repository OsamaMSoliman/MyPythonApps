from PacMan.Maze import Maze, Direction, GameOver, random
from _thread import start_new_thread
from time import sleep


class __Character(object):
    def __init__(self, posX=0, posY=0):
        self._startingPosX, self._startingPosY = posX, posY
        self.posX, self.posY = posX, posY

    def _move(self, direction):
        if direction & Direction.NORTH:
            if self.posY + 1 < Maze.SIZE and not Maze.CELLS[self.posX][self.posY + 1].collide_with_wall(direction):
                self.posY += 1
                return True
        if direction & Direction.SOUTH:
            if self.posY - 1 >= 0 and not Maze.CELLS[self.posX][self.posY - 1].collide_with_wall(direction):
                self.posY -= 1
                return True
        if direction & Direction.EAST:
            if self.posX + 1 < Maze.SIZE and not Maze.CELLS[self.posX + 1][self.posY].collide_with_wall(direction):
                self.posX += 1
                return True
        if direction & Direction.WEST:
            if self.posX - 1 > 0 and not Maze.CELLS[self.posX - 1][self.posY].collide_with_wall(direction):
                self.posX -= 1
                return True
        return False


class Hero(__Character):
    LIVE = 1
    SCORE = 0

    def __init__(self, posX=0, posY=0, lives=1):
        super().__init__(posX, posY)
        Hero.LIVE = lives
        Hero.SCORE = 0

    def _move(self, direction):
        is_moved = super(Hero, self)._move(direction)
        if is_moved:
            if Maze.CELLS[self.posX][self.posY].has_enemy:
                # Debugging :: lose live, restart position
                Hero.LIVE -= 1
                self.posX, self.posY = (-1, -1) if Hero.LIVE == 0 else (self._startingPosX, self._startingPosY)
                if Hero.LIVE == 0:
                    GameOver = True
            else:
                Hero.SCORE += Maze.CELLS[self.posX][self.posY].visit()


class Enemy(__Character):
    def __init__(self, posX, posY):
        super().__init__(posX, posY)
        start_new_thread(self.__enemy_moving_loop, ())

    def _move(self, direction):
        # Debugging :: save current position
        temp_x, temp_y = self.posX, self.posY
        is_moved = super(Enemy, self)._move(direction)
        if is_moved:
            # Debugging :: set has_enemy for the new pos with True and the old with False
            Maze.CELLS[temp_x][temp_y].has_enemy = False
            Maze.CELLS[self.posX][self.posY].has_enemy = True
            pass

    def __enemy_moving_loop(self):
        while not GameOver:
            self._move(0b1 << random.randrange(4))
            sleep(1)

from PacMan.Maze import Direction
from PacMan.Maze import Maze


class Character(object):
    def __init__(self, posX=0, posY=0):
        self.startingPosX, self.startingPosY = posX, posY
        self.posX, self.posY = posX, posY

    def move(self, direction):
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


class Hero(Character):
    LIVE = 1
    SCORE = 0

    def __init__(self, posX=0, posY=0, lives=1):
        Character.__init__(self, posX, posY)
        Hero.LIVE = lives
        Hero.SCORE = 0

    def move(self, direction):
        is_moved = super(Hero, self).move(direction)
        if is_moved:
            if Maze.CELLS[self.posX][self.posY].has_enemy:
                # Debugging :: lose live, restart position
                Hero.LIVE -= 1
                self.posX, self.posY = (-1, -1) if Hero.LIVE == 0 else (self.startingPosX, self.startingPosY)
            else:
                score = Maze.CELLS[self.posX][self.posY].visit()
                if score is not None:
                    Hero.SCORE += score


class Enemy(Character):
    def move(self, direction):
        # Debugging :: save current position
        temp_x, temp_y = self.posX, self.posY
        is_moved = super(Enemy, self).move(direction)
        if is_moved:
            # Debugging :: set has_enemy for the new pos with True and the old with False
            Maze.CELLS[temp_x][temp_y].has_enemy = False
            Maze.CELLS[self.posX][self.posY].has_enemy = True
            pass

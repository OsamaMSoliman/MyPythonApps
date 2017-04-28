import random

import math


class Direction(object):
    NORTH = 0b1000
    SOUTH = 0b0100
    EAST = 0b0010
    WEST = 0b0001


class Cell(object):
    SIZE = 10

    def __init__(self, posX, posY, score=1):
        self.wall = self.__random_wall()
        self.posX, self.posY = posX, posY
        self.score = score
        self.visited = False
        self.has_enemy = False  # public var

    @staticmethod
    def __random_wall():
        walls = random.randint(0, 15) & random.randint(0, 15)
        return walls if walls == 15 else 0

    def get_cell_wall_list(self):
        walls = []
        if self.wall & Direction.NORTH:
            walls.append([(self.posX, self.posY + Cell.SIZE), (self.posX + Cell.SIZE, self.posY + Cell.SIZE)])
        if self.wall & Direction.SOUTH:
            walls.append([(self.posX, self.posY), (self.posX + Cell.SIZE, self.posY)])
        if self.wall & Direction.EAST:
            walls.append([(self.posX + Cell.SIZE, self.posY), (self.posX + Cell.SIZE, self.posY + Cell.SIZE)])
        if self.wall & Direction.WEST:
            walls.append([(self.posX, self.posY), (self.posX, self.posY + Cell.SIZE)])
        return walls

    def collide_with_wall(self, direction):
        return True if self.wall & direction else False

    def visit(self):
        if not self.visited:
            self.visited = True
            self.score = 0
        else:
            return self.score


class Maze(object):
    SIZE = None
    CELLS = []

    def __init__(self, cell_size=10, cells_count=100):
        Cell.SIZE = cell_size
        Maze.SIZE = int(math.sqrt(cells_count))  # Maze SIZE = no. of rows or cols
        self.walls = []
        self.__create_maze()

    @staticmethod
    def __create_maze():
        if not Maze.CELLS:
            for i in range(Maze.SIZE):
                for j in range(Maze.SIZE):
                    score = int(math.ceil(random.random() * 10))
                    Maze.CELLS.append(Cell(i, j, score))

    def get_maze_wall_list(self):
        if not self.walls:
            for i in range(Maze.SIZE):
                for j in range(Maze.SIZE):
                    self.walls.extend(Maze.CELLS[i][j].get_cell_wall_list())
        return self.walls

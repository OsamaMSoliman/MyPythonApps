import random
from math import sqrt, ceil


class Direction(object):
    NORTH = 0b1000
    SOUTH = 0b0100
    EAST = 0b0010
    WEST = 0b0001
    opposite = {
        NORTH: SOUTH,
        SOUTH: NORTH,
        EAST: WEST,
        WEST: EAST
    }


class Cell(object):
    SIZE = 10

    def __init__(self, posX, posY, score=1):
        self.__wall = self.__random_wall()
        self.posX, self.posY = posX * Cell.SIZE, posY * Cell.SIZE
        self._score = score
        self.__visited = False
        self.has_enemy = False  # public var

    @staticmethod
    def __random_wall():
        # walls = random.randint(0, 15) & random.randint(0, 15)
        walls = [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST]
        return random.choice(walls)  # walls if walls == 15 else random.randint(0, 15)

    def get_cell_wall_list(self):
        walls = []
        if self.__wall & Direction.NORTH:
            walls.append([(self.posX, self.posY + Cell.SIZE), (self.posX + Cell.SIZE, self.posY + Cell.SIZE)])
        if self.__wall & Direction.SOUTH:
            walls.append([(self.posX, self.posY), (self.posX + Cell.SIZE, self.posY)])
        if self.__wall & Direction.EAST:
            walls.append([(self.posX + Cell.SIZE, self.posY), (self.posX + Cell.SIZE, self.posY + Cell.SIZE)])
        if self.__wall & Direction.WEST:
            walls.append([(self.posX, self.posY), (self.posX, self.posY + Cell.SIZE)])
        return walls

    def collide_with_wall(self, direction):
        print("cell ", self.posX, self.posY, " walls : ", bin(self.__wall))
        return True if self.__wall & direction else False

    def visit(self):
        score = self._score
        if not self.__visited:
            self.__visited = True
            self._score = 0
        return score


class Maze(object):
    Game_Over = False
    SIZE = None
    CELLS = []

    def __init__(self, cell_size=10, cells_count=100):
        Cell.SIZE = cell_size
        Maze.SIZE = round(int(sqrt(cells_count)))  # Maze SIZE = no. of rows or cols
        self.__walls = []
        self.__create_maze()

    @staticmethod
    def __create_maze():
        if not Maze.CELLS:
            for i in range(Maze.SIZE):
                for j in range(Maze.SIZE):
                    score = int(ceil(random.random() * 10))
                    Maze.CELLS.append(Cell(i, j, score))

    def get_maze_wall_list(self):
        if not self.__walls:
            for i in range(Maze.SIZE):
                for j in range(Maze.SIZE):
                    self.__walls.extend(Maze.CELLS[i * Maze.SIZE + j].get_cell_wall_list())
        return self.__walls

    def get_maze_pickups(self):
        # pickups = []
        # for cell in Maze.CELLS:
        #     if cell._score > 0: pickups.append((cell.posX + Cell.SIZE/2, cell.posY + Cell.SIZE/2))
        # return pickups
        return [(cell.posX + Cell.SIZE / 2, cell.posY + Cell.SIZE / 2) for cell in Maze.CELLS if cell._score > 0]

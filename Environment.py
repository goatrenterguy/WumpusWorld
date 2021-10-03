import random


# Class that generates a new levels
class WorldBuilder:
    def __init__(self, size, difficulty):
        self.board = [[' '] * size for i in range(size)]
        self.size = size
        self.difficulty = difficulty
        # Establish probabilities per difficulty
        self.difficulties = {'easy': {'Pwumpus': .05, 'Ppit': .05, 'Pobs': .05},
                             'med': {'Pwumpus': .1, 'Ppit': .1, 'Pobs': .1},
                             'hard': {'Pwumpus': .15, 'Ppit': .15, 'Pobs': .15}}
        self.placeGold()
        self.placeWumpus(self.difficulties[difficulty]['Pwumpus'])
        self.placePit(self.difficulties[difficulty]['Ppit'])
        self.placeObs(self.difficulties[difficulty]['Pobs'])

    # String representation
    def __repr__(self):
        strLevel = "Size: " + str(self.size) + " Difficulty: " + str(self.difficulty) + "\n"
        for lines in self.board:
            strLevel += repr(lines) + "\n"
        return strLevel

    # Randomly place wumpuses on level
    def placeWumpus(self, probability: float):
        for x in range(self.size):
            for y in range(self.size):
                if self.board[y][x] == ' ' and random.random() < probability and (x != 0 or y != 0):
                    self.board[y][x] = 'W'

    # Randomly place pits on level
    def placePit(self, probability):
        for x in range(self.size):
            for y in range(self.size):
                if self.board[y][x] == ' ' and random.random() < probability and (x != 0 and y != 0):
                    self.board[y][x] = 'P'

    # Randomly place obstacles on level
    def placeObs(self, probability):
        for x in range(self.size):
            for y in range(self.size):
                if self.board[y][x] == ' ' and random.random() < probability and (x != 0 and y != 0):
                    self.board[y][x] = 'X'

    def placeGold(self):
        while True:
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            if y != 0 and x != 0:
                self.board[y][x] = "G"
                break


# Class for storing levels
class World:
    def __init__(self, levels):
        self.world = []
        # Establish board sizes
        self.sizes = [5, 10, 15, 20, 25]
        self.difficulties = ['easy', 'med', 'hard']
        self.buildLevels(levels)

    # Override default print
    def __repr__(self):
        strWorld = "Wumpus World:\n"
        for levels in self.world:
            strWorld += repr(levels) + "\n"
        strWorld += "\n+----------------------------------+\n"
        return strWorld

    # Build levels for world
    def buildLevels(self, levels):
        for size in self.sizes:
            for difficulty in self.difficulties:
                for level in range(levels):
                    self.world.append(WorldBuilder(size, difficulty))


class Main:
    World = World(1)
    print(World.world[0])


Main()

import random


# Class that generates a new world
class WorldBuilder:
    def __init__(self, size, difficulty):
        self.board = [[''] * size for i in range(size)]
        self.size = size
        self.difficulty = difficulty
        # Establish probabilities per difficulty
        self.difficulties = {'easy': {'Pwumpus': .05, 'Ppit': .1, 'Pobs': .2},
                             'med': {'Pwumpus': .1, 'Ppit': .2, 'Pobs': .3},
                             'hard': {'Pwumpus': .15, 'Ppit': .3, 'Pobs': .4}}
        self.placeGold()
        self.placeWumpus(self.difficulties[difficulty]['Pwumpus'])
        self.placePit(self.difficulties[difficulty]['Ppit'])
        self.placeObs(self.difficulties[difficulty]['Pobs'])

    # String representation
    def __repr__(self):
        strLevel = "Size: " + str(self.size) + " Difficulty: " + str(self.difficulty) + "\n"
        for cells in self.board:
            strLevel += repr(cells) + "\n"
        return strLevel

    def placeWumpus(self, probability):
        pass

    def placePit(self, probability):
        pass

    def placeObs(self, probability):
        pass

    def placeGold(self):
        while True:
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            self.board[y][x] = "G"
            if y != 0 and x != 0:
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
    print(World)


Main()

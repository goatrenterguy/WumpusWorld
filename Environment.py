import random


# Class that generates a new levels
class WorldBuilder:
    def __init__(self, size, difficulty):
        self.board = [[' '] * size for i in range(size)]
        self.percepts = None
        self.agent = None
        self.size = size
        self.difficulty = difficulty
        # TODO: Tweak values or create more control depending on size
        # Establish probabilities per difficulty
        self.difficulties = {'easy': {'Pwumpus': .05, 'Ppit': .05, 'Pobs': .1},
                             'med': {'Pwumpus': .07, 'Ppit': .07, 'Pobs': .2},
                             'hard': {'Pwumpus': .1, 'Ppit': .11, 'Pobs': .3}}
        self.placeObs(self.difficulties[difficulty]['Pobs'])
        self.placeGold()
        self.placeWumpus(self.difficulties[difficulty]['Pwumpus'])
        self.placePit(self.difficulties[difficulty]['Ppit'])
        self.placeAgent()
        self.buildPercepts()

    # String representation
    def __repr__(self):
        strLevel = "Size: " + str(self.size) + " Difficulty: " + str(self.difficulty) + "\n"
        for lines in self.board:
            strLevel += repr(lines) + "\n"
        return strLevel

    # Build board of percepts based on level
    def buildPercepts(self):
        board = []
        for y in range(len(self.board[0])):
            perceptRow = []
            for x in range(len(self.board[0])):
                percept = ['None', 'None', 'None', 'None', 'None']
                if self.board[y][x] == 'A':
                    self.agent = [x, y]
                neighbors = self.neighbors(x, y)
                if self.board[y][x] == 'X':
                    percept[3] = 'Bump'
                    perceptRow.append(percept)
                else:
                    if 'W' in neighbors:
                        percept[0] = 'Smell'
                    if 'P' in neighbors:
                        percept[1] = 'Breeze'
                    if 'G' in neighbors:
                        percept[2] = 'Glitter'
                    perceptRow.append(percept)
            board.append(perceptRow)
        self.percepts = board

        # Get neighbors of on level level at x,y

    def neighbors(self, x, y):
        neighbors = []
        # Try west of x,y
        try:
            neighbors.append(self.board[y - 1][x])
        except IndexError:
            neighbors.append('None')
        # Try east of x,y
        try:
            neighbors.append(self.board[y][x + 1])
        except IndexError:
            neighbors.append('None')
        # Try south of x,y
        try:
            neighbors.append(self.board[y + 1][x])
        except IndexError:
            neighbors.append('None')
        # Try west of x,y
        try:
            neighbors.append(self.board[y][x - 1])
        except IndexError:
            neighbors.append('None')
        return neighbors

    # Randomly place agent
    def placeAgent(self):
        while True:
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            if self.board[y][x] == ' ' and y != 0 and x != 0:
                self.board[y][x] = "A"
                self.agent = [x, y]
                break

    # Randomly place wumpus on level (only one?)
    def placeWumpus(self, probability: float):
        # for x in range(self.size):
        #     for y in range(self.size):
        #         if self.board[y][x] == ' ' and random.random() < probability and (x != 0 or y != 0):
        #             self.board[y][x] = 'W'
        while True:
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            if self.board[y][x] == ' ' and y != 0 and x != 0:
                self.board[y][x] = "W"
                break

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
                if self.board[y][x] == ' ' and random.random() < probability and (x != 0 and y != 0) or x == 0 or y == 0 or x == self.size - 1 or y == self.size - 1:
                    self.board[y][x] = 'X'

    def placeGold(self):
        while True:
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            if y != 0 and x != 0 and self.board[y][x] == ' ' :
                self.board[y][x] = "G"
                break


# Class for storing levels
class World:
    def __init__(self, levels):
        self.levels = []
        self.percepts = []
        # Establish board sizes
        self.sizes = [7, 12, 17, 22, 27]
        self.difficulties = ['easy', 'med', 'hard']
        self.buildLevels(levels)

    # Override default print
    def __repr__(self):
        strWorld = "Wumpus World:\n"
        for level in self.levels:
            strWorld += repr(level) + "\n"
        strWorld += "\n+----------------------------------+\n"
        return strWorld

    # Build levels for world
    def buildLevels(self, levels):
        for size in self.sizes:
            for difficulty in self.difficulties:
                for level in range(levels):
                    self.levels.append(WorldBuilder(size, difficulty))

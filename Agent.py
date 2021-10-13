from colorama import Fore, Back, Style
from Environment import *
from Objects import *


class Expression:
    def __init__(self):
        self.variables = []
        self.operators = []
        self.functions = []


class Explorer:
    def __init__(self, world: World):
        self.world = world
        self.currentLevel = None
        self.location = None
        self.facing = 'South'
        self.time = 0
        self.points = 0
        self.numGold = 0
        self.numWumpusKilled = 0
        self.numPitsFallenIn = 0
        self.numCellsExplored = 0
        self.numWumpusKilledBy = 0
        self.NumActions = 0
        self.alive = True
        self.hasGold = False
        self.arrows = 0
        self.KB = None
        self.KArchive = []
        self.runner()

    # Runner for explorer
    def runner(self):
        for level in self.world.levels:
            self.currentLevel = level
            self.location = level.agent
            self.KB = KnowledgeBase(level.size)
            self.findGold()
            self.KArchive.append(self.KB)

    # Shot arrow
    def shootArrow(self):
        if self.arrows != 0:
            pass

    # Move the explorer forward
    def moveForward(self):
        self.action += 1
        self.numCellsExplored += 1
        tempLocation = self.location
        if self.direction == 'South':
            self.location[1] += 1
        elif self.direction == 'North':
            self.location[1] -= 1
        elif self.direction == 'East':
            self.location[0] += 1
        elif self.direction == 'West':
            self.location[0] -= 1
        if not self.perceive():
            self.location = tempLocation

    # Register percepts returns true or false if agent can stay in that cell
    def perceive(self):
        if self.currentLevel.board[self.location[1]][self.location[0]] == 'W':
            self.alive = False
            # Can change this value
            self.points -= 10000
            self.numWumpusKilledBy += 1
        elif self.currentLevel.board[self.location[1]][self.location[0]] == 'P':
            self.alive = False
            # Can change this value
            self.points -= 10000
            self.numPitsFallenIn += 1
        elif self.currentLevel.board[self.location[1]][self.location[0]] == 'X':
            # Tell the KB that there is a obstacle at current location
            self.KB.tellPercept(self.currentLevel.percepts[self.location[1][self.location[0]]])
            self.numCellsExplored -= 1
            return False
        elif self.currentLevel.board[self.location[1]][self.location[0]] == 'G':
            self.points += 1000
            self.numGold += 1
            self.hasGold = True
        else:
            # Tell the KB the percepts placeholder fact entered
            self.KB.tell(self.location[0], self.location[1],
                         self.currentLevel.percepts[self.location[1]][self.location[0]])
        return True

    # Turn the explorer
    def turn(self, direction):
        self.NumActions += 1
        self.facing = direction

    # Runner for the agent to find the gold
    def findGold(self):
        self.perceive()
        # Need to visit all known unvisited safe squares not sure the best way to do this aside from checking neighbors
        # and if any of them are safe (We could use a backtracking method to find the closest safe unexplored cell
        #     Record percepts and see if we can make any new inferences in KB
        # If has gold exit
        # If wumpus known and have arrows kill
        # If no safe squares do we kill ourselves or do we risk it? We can experiment with both
        pass


# KnowledgeBase Object
# TODO: Need to add time
class KnowledgeBase:
    def __init__(self, levelSize):
        # self.Clauses = [[Cell] * levelSize for i in range(levelSize)]
        self.clauses = []
        self.levelSize = levelSize

    def __repr__(self):
        s = "Knowledge Base:\n"
        for claus in self.clauses:
            s += "\t" + str(claus) + "\n"
        return s + "+-----------------------------------------------------------------+\n"

    def tell(self, clause):
        self.clauses.append(clause)

    def tellPercept(self, x, y, percepts: list):
        # TODO: Find a way we want to store knowledge in KB. Can we save them as objects and create and object for
        #  cell that contains its attributes i.e smell, explored etc or does it have to be strings / sentences. Can
        #  we have a KB that stores the strings and then an actual object actual object that stores the data and what
        #  they mean? Can we use a dictionary called as the KB and have sub dictionaries like smell that have all the
        #  cells we know have a smell?
        cell = Cell(x, y)
        if "Smell" in percepts:
            self.clauses.append(Smell(cell))
        if "Breeze" in percepts:
            self.clauses.append(Breeze(cell))
        if "Glitter" in percepts:
            self.clauses.append(Glitter(cell))
        if "Bump" in percepts:
            self.clauses.append(Bump(cell))
        if "Scream" in percepts:
            self.clauses.append(Scream(cell))

    # Check if cell is wumpus
    def isWumpus(self, x, y):
        # Check if in Clauses
        # Assume cell is not safe
        # If cell is not safe then there cant be any neighbor that doesnt have a smell
        pass

    # Rule for if the cell is a pit
    def isPit(self, x, y):
        # Check if in Clauses
        # Assume cell is not safe
        # If the cell is not safe then there cant be any neighbors with a breeze
        pass

    # Rule for if the cell is a gold
    def isGold(self, x, y):
        # Check if in Clauses
        # Assume cell is not safe
        # If the cell is not gold then there cant be any neighbors with a glitter
        pass

    def isSafe(self, x, y):
        # Check KB if safe if Safe([x,y]) then return safe if unknown check possibilities i.e check neighbors for
        # smells and see if we can infer if there is a wumpus using proof by contradiction
        scent, breeze, glitter, bump, scream = True

        pass


class Main:
    # world = World(1)
    # print(world.levels[0].percepts)
    # explorer = Explorer(world)
    # print(explorer.KB)
    KB = KnowledgeBase(5)
    cell = Cell(1, 1)
    breeze = Breeze(cell)
    smell = Smell(cell)
    a = Or(breeze, smell)
    KB.tell(a)
    print(KB)


Main()

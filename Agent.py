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
            self.map = [[' '] * level.size for i in range(level.size)]
            self.KB = KnowledgeBase()
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
            self.KB.tellPercept(self.location[0], self.location[1],
                                self.currentLevel.percepts[self.location[1]][self.location[0]])
            self.map[self.location[1]][self.location[0]] = "V"
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
        cell = Cell(x, y)
        if "Smell" in percepts:
            self.clauses.append(Smell(cell))
            self.inferWumpus(cell)
        if "Breeze" in percepts:
            self.clauses.append(Breeze(cell))
            self.inferPits(cell)
        if "Glitter" in percepts:
            self.clauses.append(Glitter(cell))
            self.inferGold(cell)
        if "Bump" in percepts:
            self.clauses.append(Bump(cell))
        if "Scream" in percepts:
            self.clauses.append(Scream(cell))

    # Resolve first order logic
    def BCResolution(self, q):
        if isinstance(q, Brackets):
            return self.BCResolution(q.clause)
        elif isinstance(q, Or):
            lhs = self.BCResolution(q.lhs)
            rhs = self.BCResolution(q.rhs)
            test = lhs or rhs
            return lhs or rhs
        elif isinstance(q, And):
            return self.BCResolution(q.lhs) and self.BCResolution(q.rhs)
        elif isinstance(q, Not) and not isinstance(q.clause, Operator):
            return not self.BCResolution(q.clause)
        elif isinstance(q, Not) and self.findInClauses(q.clause) and self.findInClauses(Visited(q.cell)):
            return False
        elif isinstance(q, Constant) and not self.findInClauses(q) and self.findInClauses(Visited(q.cell)):
            return False
        else:
            return True

    # For some reason the operator "in" did not want to cooperate with out objects so this function checks if the
    # constant is in our clauses
    def findInClauses(self, constant):
        for c in self.clauses:
            if c == constant:
                return True
        return False

    # Infer Wumpus
    def inferNotWumpus(self, cell):
        # Unify the percept (Smell(Cell)) with the
        # rule (not(Smell(Cell)) || Wumpus(Adjacent(Cell)))

        # Get all Smell(Cell) predicates in the knowledge base?
        #
        # for clause in self.clauses:
        #   for sub in clause:
        #       if isInstance(sub, )
        up = Not(Smell(Cell(cell.x, cell.y - 1)))
        down = Not(Smell(Cell(cell.x, cell.y + 1)))
        left = Not(Smell(Cell(cell.x - 1, cell.y)))
        right = Not(Smell(Cell(cell.x - 1, cell.y)))
        clause = Or(Or(up, down), Or(left, right))
        if not self.findInClauses(clause):
            self.clauses.append(clause)

    # Infer Pits
    def inferPits(self, cell):
        up = Pit(Cell(cell.x, cell.y - 1))
        down = Pit(Cell(cell.x, cell.y + 1))
        left = Pit(Cell(cell.x - 1, cell.y))
        right = Pit(Cell(cell.x + 1), cell.y)
        clause = Or(Or(up, down), Or(left, right))
        if not self.findInClauses(clause):
            self.clauses.append(clause)

    # Infer Gold
    def inferGold(self, cell):
        up = Gold(Cell(cell.x, cell.y - 1))
        down = Pit(Cell(cell.x, cell.y + 1))
        left = Pit(Cell(cell.x - 1, cell.y))
        right = Pit(Cell(cell.x + 1), cell.y)
        clause = Or(Or(up, down), Or(left, right))
        if not self.findInClauses(clause):
            self.clauses.append(clause)

    # Infer Gold
    def inferScream(self, cell):
        pass

    # Infer if cell is safe
    def inferSafe(self, cell):
        # Cell is safe if not wumpus or not pit or not obs
        for c in self.clauses:
            pass

    def ask(self, x, y):
        # Check KB if safe if Safe([x,y]) then return safe if unknown check possibilities i.e check neighbors for
        # smells and see if we can infer if there is a wumpus using proof by contradiction
        pass


class Main:
    # world = World(1)
    # print(world.levels[0].percepts)
    # explorer = Explorer(world)
    # print(explorer.KArchive)
    KB = KnowledgeBase(5)
    cell = Cell(1, 1)
    test = Cell(1, 2)
    # KB.tell(Smell(test))
    KB.tell(Visited(test))
    # KB.tell(Wumpus(test))
    # Test for if cell is NOT wumpus
    up = Not(Smell(cell.n()))
    down = Not(Smell(cell.s()))
    left = Not(Smell(cell.w()))
    right = Not(Smell(cell.e()))
    clause = Or(Or(up, down), Or(left, right))

    # Test for if cell IS wumpus
    # up = Smell(cell.n())
    # down = Smell(cell.s())
    # left = Smell(cell.w())
    # right = Smell(cell.e())
    # clause = And(And(up, down), And(left, right))
    print(clause)
    print(KB.clauses)
    # print(c for c in KB.resolve(clause))
    print(KB.BCResolution(clause))


Main()

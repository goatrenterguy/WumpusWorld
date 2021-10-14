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
class KnowledgeBase:
    def __init__(self, levelSize):
        # self.Clauses = [[Cell] * levelSize for i in range(levelSize)]
        self.clauses = []
        # Add rules to the knowledge base. Rules needed:
        # (~sml(cell) | wmp(cell.n()))
        # (~sml(cell) | wmp(cell.e()))
        # (~sml(cell) | wmp(cell.s()))
        # (~sml(cell) | wmp(cell.w()))
        # (~brz(cell) | pit(cell.n()))
        # (~brz(cell) | pit(cell.e()))
        # (~brz(cell) | pit(cell.s()))
        # (~brz(cell) | pit(cell.w()))
        # (~glt(cell) | gld(cell.n()))
        # (~glt(cell) | gld(cell.e()))
        # (~glt(cell) | gld(cell.s()))
        # (~glt(cell) | gld(cell.w()))
        # (~bump(cell) | wall(cell))
        # (~wall(cell) | bump(cell))
        # (~safe(cell) | ~wmp(cell))
        # (~safe(cell) | ~pit(cell))
        # - if visited(cell) then safe(cell)
        # - if number of Scream(Cell) == number of arrows then all wumpus are dead and we can treat them as walls
        self.levelSize = levelSize

    # Custom print statement
    def __repr__(self):
        s = "Knowledge Base:\n"
        for claus in self.clauses:
            s += "\t" + str(claus) + "\n"
        return s + "+-----------------------------------------------------------------+\n"

    # Generic tell that adds the clause to clauses mostly used for testing
    def tell(self, clause):
        self.clauses.append(clause)

    # Add percepts given by agent to KB
    def tellPercept(self, x, y, percepts: list):
        cell = Cell(x, y)
        if "Smell" in percepts and not self.findInClauses(Smell(cell)):
            self.clauses.append(Smell(cell))
        if "Breeze" in percepts and not self.findInClauses(Breeze(cell)):
            self.clauses.append(Breeze(cell))
        if "Glitter" in percepts and not self.findInClauses(Glitter(cell)):
            self.clauses.append(Glitter(cell))
        if "Bump" in percepts and not self.findInClauses(Bump(cell)):
            self.clauses.append(Bump(cell))
        if "Scream" in percepts and not self.findInClauses(Scream(cell)):
            self.clauses.append(Scream(cell))
        if not self.findInClauses(Visited(cell)):
            self.clauses.append(Visited(cell))

    # Resolve first order logic
    def BCResolution(self, q):
        # Check if in brackets and resolve what is in brackets separately
        if isinstance(q, Brackets):
            return self.BCResolution(q.clause)
        # Check if an or statement and resolve left and right hand and or the results
        elif isinstance(q, Or):
            lhs = self.BCResolution(q.lhs)
            rhs = self.BCResolution(q.rhs)
            test = lhs or rhs
            return lhs or rhs
        # Check if an And statement and evaluates the lhs and rhs and "and" the results together
        elif isinstance(q, And):
            return self.BCResolution(q.lhs) and self.BCResolution(q.rhs)
        # Checks if is a Not and the clause is a statement then resolves statement
        elif isinstance(q, Not) and not isinstance(q.clause, Operator):
            return not self.BCResolution(q.clause)
        # Checks if a Not operator and if clause is a constant. checks if it finds it in our existing clauses if it does returns false
        elif isinstance(q, Not) and self.findInClauses(q.clause):
            return False
        # Checks if a constant and looks if its is not in
        elif isinstance(q, Constant) and not self.findInClauses(q) and self.findInClauses(Visited(q.cell)):
            return False
        # Otherwise we return True because we have nothing that contradicts it
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
    def genNotWumpusRule(self, cell):
        # resolve and unify Not(Wumpus(Cell))
        up = Not(Smell(Cell(cell.x, cell.y - 1)))
        down = Not(Smell(Cell(cell.x, cell.y + 1)))
        left = Not(Smell(Cell(cell.x - 1, cell.y)))
        right = Not(Smell(Cell(cell.x + 1, cell.y)))
        clause = Or(Or(up, down), Or(left, right))
        return clause

    # Infer Pits
    def genNotPitRule(self, cell):
        # resolve and unify Not(Pit(Cell))
        up = Not(Pit(Cell(cell.x, cell.y - 1)))
        down = Not(Pit(Cell(cell.x, cell.y + 1)))
        left = Not(Pit(Cell(cell.x - 1, cell.y)))
        right = Not(Pit(Cell(cell.x + 1, cell.y)))
        clause = Or(Or(up, down), Or(left, right))
        return clause

    # Infer Gold
    def genGoldRule(self, cell):
        # resolve and unify Not(Gold(Cell))
        up = Glitter(Cell(cell.x, cell.y - 1))
        down = Glitter(Cell(cell.x, cell.y + 1))
        left = Glitter(Cell(cell.x - 1, cell.y))
        right = Glitter(Cell(cell.x + 1, cell.y))
        clause = And(And(up, down), And(left, right))
        return clause

    # Scream rules
    def inferScream(self, cell):
        pass

    # Infer if cell is safe
    def genSafeRule(self, cell):
        # Cell is safe if not wumpus or not pit
        # Unify into rule
        rule = Or(Not(Wumpus(cell)), Not(Pit(cell)))
        # Resolve Not(Wumpus(cell) and Not(Pit(cell)
        clause = Or(self.genNotWumpusRule(cell), self.genNotPitRule(cell))
        return rule, clause

    # Ask for if the input coordinates are safe
    def askSafe(self, x, y):
        # Check KB if safe if Safe([x,y]) then return safe if unknown check possibilities i.e check neighbors for
        # smells and see if we can infer if there is a wumpus using proof by contradiction
        cell = Cell(x, y)
        for clause in self.clauses:
            if clause == Safe(cell):
                return True
        if self.BCResolution(self.genSafeRule(cell)[1]):
            self.clauses.append(Safe(cell))
            return True
        return False

    def askGold(self, x, y):
        # Is gold if any of the neighbors dont have glitter
        cell = Cell(x, y)
        if self.BCResolution(self.genGoldRule(cell)):
            self.clauses.append(Gold(cell))
            return True
        return False


class Main:
    pass


Main()

from Environment import *


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
        self.KB = KnowledgeBase()

    # Runner for explorer
    def runner(self):
        for level in self.world:
            self.currentLevel = level
            self.location = level.agent
            self.findGold(level)

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
        if self.level[self.location[1]][self.location[0]] == 'W':
            self.alive = False
            # Can change this value
            self.points -= 10000
            self.numWumpusKilledBy += 1
        elif self.level[self.location[1]][self.location[0]] == 'P':
            self.alive = False
            # Can change this value
            self.points -= 10000
            self.numPitsFallenIn += 1
        elif self.level[self.location[1]][self.location[0]] == 'X':
            # Tell the KB that there is a obstacle at current location
            self.KB.tell(["Obs(Cell(x,y))"])
            self.numCellsExplored -= 1
            return False
        elif self.level[self.location[1]][self.location[0]] == 'G':
            self.points += 1000
            self.numGold += 1
            self.hasGold = True
        elif self.level[self.location[1]][self.location[0]] == ' ':
            # Tell the KB the percepts placeholder fact entered
            self.KB.tell("Percepts(Cell(x,y)")
        return True

    # Turn the explorer
    def turn(self, direction):
        self.NumActions += 1
        self.facing = direction

    # Runner for the agent to find the gold
    def findGold(self):
        # Need to visit all known unvisited safe squares not sure the best way to do this aside from checking neighbors
        # and if any of them are safe (We could use a backtracking method to find the closest safe unexplored cell
        #     Record percepts and see if we can make any new inferences in KB
        # If Gold found grab and exit
        # If wumpus known and have arrows kill
        # If no safe squares do we kill ourselves or do we risk it? We can experiment with both
        pass


class KnowledgeBase:
    def __init__(self):
        self.KB = []

    def tell(self, fact):
        # TODO: Find a way we want to store knowledge in KB. Can we save them as objects and create and object for cell
        #  that contains its attributes i.e smell, explored etc or does it have to be strings / sentences. Can we have a
        #  KB that stores the strings and then an actual object actual object that stores the data and what they mean?
        pass

    def FolBcAsk(self, goals, theta=[]):
        if not goals:
            return theta
        query = self.Substitute(theta, goals[0])
        for sentence in self.KB:
            self.StandardizeApart(sentence)

    @staticmethod
    def isCompound(expr):
        if "&" in expr or "|" in expr:
            return True
        return False

    # def getOperators(self, expr):

    @staticmethod
    def isVariable(var):
        if var.isLower():
            return True
        return False

    def Substitute(self, theta, param):
        pass

    def UnifyVar(self, var, x, theta):
        if var in theta:
            return self.Unify(theta[var], x, theta)
        elif x in theta:
            return self.Unify(theta[x], var, theta)
        elif self.OccurCheck(var, x):
            return None
        else:
            theta[var] = x
            return theta

    def Unify(self, x, y, theta=[]):
        # Recursive termination
        if theta is None:
            return None
        # Check if x and y are already identical
        elif x == y:
            return theta
        # Check if x is a variable
        elif self.isVariable(x):
            # If x is a variable then we need to unify x and y
            return self.UnifyVar(x, y, theta)
        # Check if y is a variable
        elif self.isVariable(y):
            # If y is a variable then we need to unify y and x
            return self.UnifyVar(y, x, theta)
        elif self.isCompound(x) and self.isCompound(y):
            return self.Unify(x.args, y.args)
        elif self.isList(x) and self.isList(y):
            return self.Unify(x[1:], y[1:], self.Unify(x[0], y[0], theta))
        else:
            return None

    # Check if var is in x
    def OccurCheck(self, var, x):
        for s in x:
            # If s is a another expression check that expression
            if isinstance(s, list):
                # If var in teh sub expression return True
                if self.OccurCheck(var, s):
                    return True
            # If var == s return true
            elif var == s:
                return True
        # Otherwise return False because var is not in x
        return False

    def isSafe(self, x, y):
        # Check KB if safe
        # if Safe([x,y]) then return safe
        # if unknown check possibilities i.e check neighbors for smells and see if we can infer if there is a wumpus using proof by contradiction
        scent, breeze, glitter, bump, scream = True

        pass




class Main:
    World = World(1)
    print(World)
    print()


Main()

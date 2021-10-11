from Environment import *


class Expression:
    def __init__(self):
        self.variables = []
        self.operators = []
        self.functions = []


class Explorer:
    def __init__(self):
        self.location = (0, 0)
        self.facing = 'South'
        self.time = 0
        self.points = 0
        self.numGold = 0
        self.numWumpusKilled = 0
        self.numPitsFallenIn = 0
        self.numCellsExplored = 0
        self.numWumpusKilledBy = 0
        self.NumActions = 0
        self.age = 0
        self.arrows = 0
        self.KB = KnowledgeBase()

    # Move the explorer forward
    def moveForward(self):
        pass

    # Turn the explorer
    def turn(self, direction):
        pass

    # Runner for the agent to find the gold
    def findGold(self):
        # Need to visit all known unvisited safe squares
        #     Record percepts and see if we can make any new inferences in KB
        # If Gold found grab and exit
        # If wumpus known and have arrows kill
        # If no safe squares do we kill ourselves or do we risk it? We can experiment with both
        pass


class KnowledgeBase:
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
    print(World.percepts[0])
    print()


Main()

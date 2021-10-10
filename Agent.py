from Environment import *


class Explorer:
    def __init__(self):
        self.kb = KnowledgeBase()
        self.location = (0, 0)
        self.facing = 'South'
        self.time = 0


class KnowledgeBase:
    def isCompound(self, expr):
        pass

    def isVariable(self, var):
        pass

    def UnifyVar(self, x, y, theta):
        pass

    def Unify(self, x, y, theta = None):
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




class Main:
    World = World(1)
    print(World.percepts[0])


Main()

class Cell:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self):
        return "Cell(" + str(self.x) + ", " + str(self.y) + ")"


# Object that contains a cell that has a smell
class Smell:
    def __init__(self, cell: Cell):
        self.cell = cell

    def __repr__(self):
        return "Smell(" + repr(self.cell) + ")"


# Object that contains a cell that has a breeze
class Breeze:
    def __init__(self, cell: Cell):
        self.cell = cell

    def __repr__(self):
        return "Breeze(" + repr(self.cell) + ")"


# Object Bump that contains a cell that is an obstacle
class Bump:
    def __init__(self, cell: Cell):
        self.cell = cell

    def __repr__(self):
        return "Bump(" + repr(self.cell) + ")"


# Object Glitter that contains a cell if it has glitter in it
class Glitter:
    def __init__(self, cell: Cell):
        self.cell = cell

    def __repr__(self):
        return "Scream(" + repr(self.cell) + ")"


# Object Scream that contains a cell
class Scream:
    def __init__(self, cell: Cell):
        self.cell = cell

    def __repr__(self):
        return "Scream(" + repr(self.cell) + ")"


# Object that contains a cell that is a known wumpus
class Wumpus:
    def __init__(self, cell: Cell):
        self.cell = cell

    def __repr__(self):
        return "Wumpus(" + repr(self.cell) + ")"


# Object that contains a cell that is a known pit
class Pit:
    def __init__(self, cell: Cell):
        self.cell = cell

    def __repr__(self):
        return "Pit(" + repr(self.cell) + ")"


# Object that contains a cell that is known to be the gold
class Gold:
    def __init__(self, cell: Cell):
        self.cell = cell

    def __repr__(self):
        return "Gold(" + repr(self.cell) + ")"

# Object for negating
class Not:
    def __init__(self, clause):
        self.clause = clause

    def __repr__(self):
        return "!" + self.clause

# Object for or-ing a lhs and rhs
class Or:
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def __repr__(self):
        return str(self.lhs) + " || " + str(self.rhs)

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "Cell(" + str(self.x) + ", " + str(self.y) + ")"

    def __eq__(self, other):
        if isinstance(other, Cell):
            return self.x == other.x and self.y == other.y

    def n(self):
        return Cell(self.x, self.y - 1)

    def e(self):
        return Cell(self.x + 1, self.y)

    def s(self):
        return Cell(self.x, self.y + 1)

    def w(self):
        return Cell(self.x - 1, self.y)


class Constant:
    def __init__(self, cell: Cell):
        self.cell = cell


class Visited(Constant):
    def __init__(self, cell: Cell):
        self.cell = cell

    def __repr__(self):
        return "Visited(" + repr(self.cell) + ")"

    def __eq__(self, other):
        if isinstance(other, Visited):
            return self.cell == other.cell


# Object that contains a cell that has a smell
class Smell(Constant):
    def __init__(self, cell: Cell):
        self.cell = cell

    def __repr__(self):
        return "Smell(" + repr(self.cell) + ")"

    def __eq__(self, other):
        if isinstance(other, Smell):
            return self.cell == other.cell


# Object that contains a cell that has a breeze
class Breeze(Constant):
    def __init__(self, cell: Cell):
        self.cell = cell

    def __repr__(self):
        return "Breeze(" + repr(self.cell) + ")"

    def __eq__(self, other):
        if isinstance(other, Breeze):
            return self.cell == other.cell


# Object Bump that contains a cell that is an obstacle
class Bump(Constant):
    def __init__(self, cell: Cell):
        self.cell = cell

    def __repr__(self):
        return "Bump(" + repr(self.cell) + ")"

    def __eq__(self, other):
        if isinstance(other, Bump):
            return self.cell == other.cell


# Object Glitter that contains a cell if it has glitter in it
class Glitter(Constant):
    def __init__(self, cell: Cell):
        self.cell = cell

    def __repr__(self):
        return "Scream(" + repr(self.cell) + ")"

    def __eq__(self, other):
        if isinstance(other, Glitter):
            return self.cell == other.cell


# Object Scream that contains a cell
class Scream(Constant):
    def __init__(self, cell: Cell):
        self.cell = cell

    def __repr__(self):
        return "Scream(" + repr(self.cell) + ")"

    def __eq__(self, other):
        if isinstance(other, Scream):
            return self.cell == other.cell


# Object that contains a cell that is a known wumpus
class Safe(Constant):
    def __init__(self, cell: Cell):
        self.cell = cell

    def __repr__(self):
        return "Safe(" + repr(self.cell) + ")"

    def __eq__(self, other):
        if isinstance(other, Safe):
            return self.cell == other.cell


# Object that contains a cell that is a known wumpus
class Wumpus(Constant):
    def __init__(self, cell: Cell):
        self.cell = cell

    def __repr__(self):
        return "Wumpus(" + repr(self.cell) + ")"

    def __eq__(self, other):
        if isinstance(other, Wumpus):
            return self.cell == other.cell


# Object that contains a cell that is a known pit
class Pit(Constant):
    def __init__(self, cell: Cell):
        self.cell = cell

    def __repr__(self):
        return "Pit(" + repr(self.cell) + ")"


# Object that contains a cell that is known to be the gold
class Gold(Constant):
    def __init__(self, cell: Cell):
        self.cell = cell

    def __repr__(self):
        return "Gold(" + repr(self.cell) + ")"


class Operator:
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs


# Object for negating
class Not:
    def __init__(self, clause):
        self.clause = clause

    def __repr__(self):
        return "!" + str(self.clause)


# Object for or-ing a lhs and rhs
class Or:
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def __repr__(self):
        return str(self.lhs) + " || " + str(self.rhs)


# Object for and-ing two clauses together
class And:
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def __repr__(self):
        return str(self.lhs) + ' && ' + str(self.lhs)


# Object for adding brackets
class Brackets:
    def __init__(self, clause):
        self.clause = clause

    def __repr__(self):
        return "[" + str(self.clause) + "]"

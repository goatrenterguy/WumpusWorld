from Environment import *
from Objects import *


# FOL reactive explorer
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
        self.numActions = 0
        self.alive = None
        self.hasGold = None
        self.arrows = 0
        self.KB = None
        self.KArchive = []
        self.runner()
        self.map = None

    # Runner for explorer
    def runner(self):
        for level in self.world.levels:
            # Set current level to level
            self.currentLevel = level
            # Set to current location of the agent
            self.location = level.agent
            # Reset variable has Gold to false if on previous level we found gold
            self.hasGold = False
            # Reset alive in case we died on previous level
            self.alive = True
            # Reset the number of action for the level
            self.numActions = 0
            # Initialize the number of arrows for the level
            self.arrows = level.wumpi
            # Initialize a map that stores if we have visited a cell or not
            self.map = [[' '] * level.size for i in range(level.size)]
            # Initialize a knowledge base for the level
            self.KB = KnowledgeBase()
            # Start runner for instructions to find gold
            self.findGold()
            print("Level: \n" + str(level) + "\nPoints: " + str(self.points))
            self.KArchive.append(self.KB)

    # Shoot arrow
    def shootArrow(self):
        if self.arrows != 0:
            startX = self.location[0]
            startY = self.location[1]
            if self.facing == "South":
                while startY != self.currentLevel.size:
                    if str(self.currentLevel.board[startY][startX]) == 'W':
                        self.points += 100
                        self.KB.tell(Scream)
                        return
                    startY += 1

            elif self.facing == "North":
                while startY != 0:
                    if str(self.currentLevel.board[startY][startX]) == 'W':
                        self.points += 100
                        self.KB.tell(Scream)
                        return
                    startY -= 1
            elif self.facing == "East":
                while startX != self.currentLevel.size:
                    if str(self.currentLevel.board[startY][startX]) == 'W':
                        self.points += 100
                        self.KB.tell(Scream)
                        return
                    startX += 1
            elif self.facing == "West":
                while startX != 0:
                    if str(self.currentLevel.board[startY][startX]) == 'W':
                        self.points += 100
                        self.KB.tell(Scream)
                        return
                    startX -= 1
            self.arrows -= 1

    # Move the explorer forward
    def moveForward(self):
        self.NumActions += 1
        self.numCellsExplored += 1
        tempLocation = self.location.copy()
        if self.facing == 'South':
            self.location[1] += 1
        elif self.facing == 'North':
            self.location[1] -= 1
        elif self.facing == 'East':
            self.location[0] += 1
        elif self.facing == 'West':
            self.location[0] -= 1
        if not self.perceive():
            self.location = tempLocation

    # Register percepts returns true or false if agent can stay in that cell
    def perceive(self):
        # Check if we killed ourselves on a Wumpus
        if self.currentLevel.board[self.location[1]][self.location[0]] == 'W':
            self.alive = False
            # Can change this value
            self.points -= 10000
            self.numWumpusKilledBy += 1
        # Check if we fell into a pit and died
        elif self.currentLevel.board[self.location[1]][self.location[0]] == 'P':
            self.alive = False
            # Can change this value
            self.points -= 10000
            self.numPitsFallenIn += 1
        # Check if we ran into a wall
        elif self.currentLevel.board[self.location[1]][self.location[0]] == 'X':
            # Tell the KB that there is a obstacle at current location
            self.KB.tellPercept(self.location[0], self.location[1],
                                self.currentLevel.percepts[self.location[1]][self.location[0]])
            self.numCellsExplored -= 1
            # Return false letting moveForward() know that it hit a wall and should back up
            return False
        # Check if we ran into the gold
        elif self.currentLevel.board[self.location[1]][self.location[0]] == 'G':
            self.points += 1000
            self.numGold += 1
            self.KB.tell(Gold(Cell(self.location[0], self.location[1])))
            self.hasGold = True
        # Otherwise tell the KB or perceptions of the cell
        else:
            # Tell the KB the percepts placeholder fact entered
            self.KB.tellPercept(self.location[0], self.location[1],
                                self.currentLevel.percepts[self.location[1]][self.location[0]])
            if "Smell" in self.currentLevel.percepts[self.location[1]][self.location[0]]:
                self.shootArrow()
            self.map[self.location[1]][self.location[0]] = "V"
        return True

    # Turn the explorer
    def turn(self, direction):
        self.numActions += 1
        self.facing = direction

    # Runner for the agent to find the gold
    def findGold(self):
        # Register the perceptions of the entry cell of the agent
        self.perceive()
        # Continue exploring while we are a live or dont have the gold
        while self.alive and not self.hasGold:
            # Check if move forward is safe
            visitS = self.map[self.location[1] + 1][self.location[0]]
            visitN = self.map[self.location[1] - 1][self.location[0]]
            visitE = self.map[self.location[1]][self.location[0] + 1]
            visitW = self.map[self.location[1]][self.location[0] - 1]
            safeS = self.KB.askSafe(self.location[0], self.location[1] + 1)
            safeN = self.KB.askSafe(self.location[0], self.location[1] - 1)
            safeE = self.KB.askSafe(self.location[0] + 1, self.location[1])
            safeW = self.KB.askSafe(self.location[0] - 1, self.location[1])
            wallS = self.KB.askWall(self.location[0], self.location[1] + 1)
            wallN = self.KB.askWall(self.location[0], self.location[1] - 1)
            wallE = self.KB.askWall(self.location[0] + 1, self.location[1])
            wallW = self.KB.askWall(self.location[0] - 1, self.location[1])

            moved = False

            if safeS and visitS == ' ' and wallS:
                if self.facing == "South":
                    self.moveForward()
                    moved = True
            elif safeN and visitN == ' ' and wallN:
                if self.facing == "North":
                    self.moveForward()
                    moved = True
            elif safeE and visitE == ' ' and wallE:
                if self.facing == "East":
                    self.moveForward()
                    moved = True
            elif safeW and visitW == ' ' and wallW:
                if self.facing == "West":
                    self.moveForward()
                    moved = True

            if safeS:
                if self.facing == "South":
                    self.moveForward()
                    moved = True
            elif safeN:
                if self.facing == "North":
                    self.moveForward()
                    moved = True
            elif safeE:
                if self.facing == "East":
                    self.moveForward()
                    moved = True
            elif safeW:
                if self.facing == "West":
                    self.moveForward()
                    moved = True

            if not moved:
                if safeS:
                    self.turn("South")
                elif safeN:
                    self.turn("North")
                elif safeE:
                    self.turn("East")
                elif safeW:
                    self.turn("West")
            if self.NumActions >= 1000:
                self.alive = False

            '''
            if self.kb.percept_here==bump:
                if (cell to right is unvisited):
                    turn right
                elif (cell to left is unvisited):
                    turn left
                elif (cell to bottom is unvisited):
                    turn around
            else:
                if findUnvisitedCells():
                    if unvisitedCell isSafe():
                        turn/move to unvisitedCell
            else:
                findSafeCell()

            if self.kb.perceptatcell is bump, turn to safe direction in knowledge base
            if cell in front is safe, self.moveForward()
            else if cell to the left is safe, self.turnleft()
            else if cell to right is safe, self.turnright()
            else if no cells safe, backtrack?
            '''

        # Need to visit all known unvisited safe squares not sure the best way to do this aside from checking neighbors
        # and if any of them are safe (We could use a backtracking method to find the closest safe unexplored cell
        #     Record percepts and see if we can make any new inferences in KB
        # If has gold exit
        # If wumpus known and have arrows kill
        # If no safe squares do we kill ourselves or do we risk it? We can experiment with both

class ReactiveExplorer():
    def __init__(self, world: World):
        self.world = world
        self.currentLevel = None
        self.location = None
        self.knowledge = None
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
        self.runner()
        self.map = None

    # Runner for explorer
    def runner(self):
        for level in self.world.levels:
            # Set current level to level
            self.currentLevel = level
            # Set to current location of the agent
            self.location = level.agent
            # Reset variable has Gold to false if on previous level we found gold
            self.hasGold = False
            # Reset alive in case we died on previous level
            self.alive = True
            # Reset the number of action for the level
            self.numActions = 0
            # Initialize the number of arrows for the level
            self.arrows = level.wumpi
            # Initialize a map that stores if we have visited a cell or not
            self.map = [[' '] * level.size for i in range(level.size)]
            # Start runner for instructions to find gold
            self.findGold()
            print("Level: \n" + str(level) + "\nPoints: " + str(self.points))

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
            self.map[self.location[1]][self.location[0]] = "W"
            self.numCellsExplored -= 1
            return False
        elif self.currentLevel.board[self.location[1]][self.location[0]] == 'G':
            self.points += 1000
            self.numGold += 1
            self.hasGold = True
        else:
            self.knowledge = self.currentLevel.percepts[self.location[1]][self.location[0]]
            self.map[self.location[1]][self.location[0]] = "V"
        return True

    # Getter method for the map data for cells adjacent to where the agent currently stands
    def getAdjCellMap(self):
        visitS = self.map[self.location[1] + 1][self.location[0]]
        visitN = self.map[self.location[1] - 1][self.location[0]]
        visitE = self.map[self.location[1]][self.location[0] + 1]
        visitW = self.map[self.location[1]][self.location[0] - 1]
        return visitS, visitN, visitE, visitW

    # Utility method for moving the explorer forward
    def moveForward(self):
        self.NumActions += 1
        self.numCellsExplored += 1
        tempLocation = self.location.copy()
        if self.facing == 'South':
            self.location[1] += 1  # move south
        elif self.facing == 'North':
            self.location[1] -= 1  # move north
        elif self.facing == 'East':
            self.location[0] += 1  # move east
        elif self.facing == 'West':
            self.location[0] -= 1  # move west
        if not self.perceive():  # if the agent cannot stay in the cell (there is a wall)
            self.location = tempLocation  # move it back to the previous cell

    # Utility method for turning the explorer
    # Takes the direction parameter and turns the agent to face that way
    def turn(self, direction):
        self.NumActions += 1
        self.facing = direction

    # Utility method for turning the agent to a random direction other than the direction it currently faces
    def turnRand(self):
        self.NumActions += 1
        if self.facing == 'South':
            self.facing = random.choice(('North', 'East', 'West'))
        elif self.facing == 'North':
            self.facing = random.choice(('South', 'East', 'West'))
        elif self.facing == 'East':
            self.facing = random.choice(('South', 'North', 'West'))
        elif self.facing == 'West':
            self.facing = random.choice(('South', 'North', 'East'))

    # Utility method for turning the agent to any of the four possible directions
    def turnRandOrStay(self):
        self.NumActions += 1  # increment the action count
        lastDirection = self.facing  # store the direction the agent is currently facing
        self.facing = random.choice(('South', 'North', 'East', 'West'))  # face a new direction
        if self.facing == lastDirection:  # if facing the same direction as before
            self.NumActions -= 1  # decrement the action counter because the agent didn't turn

    # Method for shooting an arrow in a straight line in front of the agent
    # Returns true if the arrow hits a Wumpus, and false if it doesn't
    def shootArrow(self):
        self.NumActions += 1  # increment the action counter
        self.arrows -= 1  # decrement the number of arrows
        if self.facing == 'South':
            for i in range(self.currentLevel.size - self.location[1]):  # iterate from to the edge of the board
                if self.currentLevel.board[self.location[1] + i][self.location[0]] == 'W':  # if it hits a Wumpus
                    return True  # return the scream percept
            return False
        if self.facing == 'North':
            for i in range(self.currentLevel.size - self.location[1]):
                if self.currentLevel.board[self.location[1] - i][self.location[0]] == 'W':
                    return True
            return False
        if self.facing == 'East':
            for i in range(self.currentLevel.size - self.location[0]):
                if self.currentLevel.board[self.location[1]][self.location[0] + i] == 'W':
                    return True
            return False
        if self.facing == 'West':
            for i in range(self.currentLevel.size - self.location[0]):
                if self.currentLevel.board[self.location[1]][self.location[0] - i] == 'W':
                    return True
            return False

    # Runner for the agent to find the gold
    def findGold(self):
        while self.alive and not self.hasGold:
            self.perceive()  # gather percepts from the current cell
            s, n, e, w = self.getAdjCellMap()  # gather knowledge about adjacent cells

            # if the agent is next to the gold
            if 'Glitter' in self.knowledge:
                # find unexplored cells to look for gold in
                toExplore = []
                if s == '':
                    toExplore.append('South')
                if n == '':
                    toExplore.append('North')
                if e == '':
                    toExplore.append('East')
                if w == '':
                    toExplore.append('West')

                # turn to face on of the unexplored cells and enter it
                self.facing = random.choice(toExplore)
                self.moveForward()

            # if the adjacent cells are safe enter one of them that is not explored
            if 'Smell' not in self.knowledge and 'Breeze' not in self.knowledge:
                if s == ' ' and self.facing == 'South':  # if the adjacent cell is unexplored and the agent is facing it
                    self.moveForward()  # move forward into the cell
                    continue
                elif n == ' ' and self.facing == 'North':
                    self.moveForward()
                    continue
                elif e == ' ' and self.facing == 'East':
                    self.moveForward()
                    continue
                elif w == ' ' and self.facing == 'West':
                    self.moveForward()
                    continue
                else:  # the agent is not facing an unexplored cell
                    if s == ' ':
                        self.turn("South")  # turn to face the unexplored cell
                        self.moveForward()  # enter the unexplored cell
                    elif n == ' ':
                        self.turn("North")
                        self.moveForward()
                    elif e == ' ':
                        self.turn("East")
                        self.moveForward()
                    elif w == ' ':
                        self.turn("West")
                        self.moveForward()

            # at least one neighboring cell is dangerous so shoot an arrow
            elif self.arrows > 0:
                if not self.shootArrow():  # if there is no scream the cell is safe
                    self.moveForward()  # so enter it
                else:  # if there is a scream
                    self.turnRand()  # turn to face a different direction
                    self.moveForward()  # enter the cell

            # the agent has no more arrows so it moves to a random neighbor
            else:
                self.turnRandOrStay()  # turn to a random direction
                self.moveForward()  # enter the cell


# KnowledgeBase Object
class KnowledgeBase:
    def __init__(self):
        # self.Clauses = [[Cell] * levelSize for i in range(levelSize)]
        # Initialize the list of clauses
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
        # Add non unified rules
        self.clauses.append(And(And(Glitter(Cell("x", "y + 1")), Glitter(Cell("x", "y - 1"))),
                                And(Glitter(Cell("x + 1", "y")), Glitter(Cell("x - 1", "y")))))
        self.clauses.append(Or(Or(Not(Smell(Cell("x", "y + 1"))), Not(Smell(Cell("x", "y - 1")))),
                               Or(Not(Smell(Cell("x + 1", "y"))), Not(Smell(Cell("x - 1", "y"))))))
        self.clauses.append(Or(Or(Not(Breeze(Cell("x", "y + 1"))), Not(Breeze(Cell("x", "y - 1")))),
                               Or(Not(Breeze(Cell("x + 1", "y"))), Not(Breeze(Cell("x - 1", "y"))))))
        self.clauses.append(And(Not(Wumpus(Cell("x", "y"))), Not(Pit(Cell("x", "y")))))

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
        # If there is a smell being passed in and its not already known add it to the knowledge base
        if "Smell" in percepts and not self.findInClauses(Smell(cell)):
            self.clauses.append(Smell(cell))
        # If there is a breeze and its not in the knowledge base add it
        if "Breeze" in percepts and not self.findInClauses(Breeze(cell)):
            self.clauses.append(Breeze(cell))
        # If there is a glitter and its not in the knowledge base add it
        if "Glitter" in percepts and not self.findInClauses(Glitter(cell)):
            self.clauses.append(Glitter(cell))
        # If there is a Bump and its not in the knowledge base add it
        if "Bump" in percepts and not self.findInClauses(Bump(cell)):
            self.clauses.append(Bump(cell))
            # Need to return so that the cell with a wall is not marked as visited throwing off the logic
            return
        # If there is a scream and its not in the knowledge base add it
        if "Scream" in percepts and not self.findInClauses(Scream(cell)):
            self.clauses.append(Scream(cell))
        # Register the cell as visited
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
            return lhs or rhs
        # Check if an And statement and evaluates the lhs and rhs and "and" the results together
        elif isinstance(q, And):
            return self.BCResolution(q.lhs) and self.BCResolution(q.rhs)
        # Checks if is a Not and the clause is a statement then resolves statement
        elif isinstance(q, Not) and not isinstance(q.clause, Operator):
            return not self.BCResolution(q.clause)
        # Checks if a Not operator and if clause is a constant. checks if it finds it in our existing clauses if it does returns false
        elif isinstance(q, Not) and self.findInClauses(q.clause) and self.findInClauses(Visited(q.cell)):
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
        # It is not a Wumpus if there are no smells in the neighboring cells
        up = Not(Smell(Cell(cell.x, cell.y - 1)))
        down = Not(Smell(Cell(cell.x, cell.y + 1)))
        left = Not(Smell(Cell(cell.x - 1, cell.y)))
        right = Not(Smell(Cell(cell.x + 1, cell.y)))
        clause = Or(Or(up, down), Or(left, right))
        return clause

    # Infer Pits
    def genNotPitRule(self, cell):
        # resolve and unify Not(Pit(Cell))
        # It is not a Pit if there are no breezes in the neighboring cells
        up = Not(Breeze(Cell(cell.x, cell.y - 1)))
        down = Not(Breeze(Cell(cell.x, cell.y + 1)))
        left = Not(Breeze(Cell(cell.x - 1, cell.y)))
        right = Not(Breeze(Cell(cell.x + 1, cell.y)))
        clause = Or(Or(up, down), Or(left, right))
        return clause

    # Infer Gold
    def genGoldRule(self, cell):
        # resolve and unify Not(Gold(Cell))
        # It is gold if there are is glitter in the neighboring cells
        up = Glitter(Cell(cell.x, cell.y - 1))
        down = Glitter(Cell(cell.x, cell.y + 1))
        left = Glitter(Cell(cell.x - 1, cell.y))
        right = Glitter(Cell(cell.x + 1, cell.y))
        clause = And(And(up, down), And(left, right))
        return clause

    # Infer if cell is safe
    def genSafeRule(self, cell):
        # Cell is safe if not wumpus or not pit
        # Unify into rule
        rule = Or(Not(Wumpus(cell)), Not(Pit(cell)))
        # Resolve Not(Wumpus(cell) and Not(Pit(cell)
        clause = And(self.genNotWumpusRule(cell), self.genNotPitRule(cell))
        return rule, clause

    # Ask for if the input coordinates are safe
    def askSafe(self, x, y):
        # Check KB if safe if Safe([x,y]) then return safe if unknown check possibilities i.e check neighbors for
        # smells and see if we can infer if there is a wumpus using proof by contradiction
        cell = Cell(x, y)
        for clause in self.clauses:
            if clause == Safe(cell):
                return True
        # If the clause is not in the list of clauses we need to infer it
        if self.BCResolution(self.genSafeRule(cell)[1]):
            self.clauses.append(Safe(cell))
            return True
        return False

    # Ask if cell is gold
    def askGold(self, x, y):
        # Is gold if any of the neighbors dont have glitter
        cell = Cell(x, y)
        for clause in self.clauses:
            if clause == Gold(cell):
                return True
        # If the clause is not in the list of clauses we need to infer it
        if self.BCResolution(self.genGoldRule(cell)):
            self.clauses.append(Gold(cell))
            return True
        return False

    # Ask if a cell is a wall
    def askWall(self, x, y):
        cell = Cell(x, y)
        # Check if the cell is a wall
        if self.findInClauses(Bump(cell)):
            return True
        return False


class Main:
    world = World(1)
    print(world.levels[0])
    ReactExplorer = ReactiveExplorer(world)
    print(ReactExplorer)


Main()
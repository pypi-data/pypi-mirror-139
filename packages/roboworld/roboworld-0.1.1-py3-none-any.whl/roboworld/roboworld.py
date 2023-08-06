from enum import Enum
from sre_parse import State
import numpy as np

from typing import Sequence
import random

from .animator import Animator
from .direction import Direction
from .roboexception import InvalidWorldArgumentsExeception, ObjectMissingException, ObjectInFrontException, CellOccupiedException
from .roboexception import WallInFrontException, SpaceIsFullException, SpaceIsEmptyException
from .cellstate import CellState

class World():
    """
    The world the roboter is exploring.

    The world is the rectangular discrete grid of a cellular automaton.
    A cell can be in one of six CellState: EMPTY (0), OBSTACLE (1, unmoveable), AGENT (2), OBJECT (3, moveable), GOAL (4), AGENT_AT_GOAL (5, AGENT+GOAL).

    Attributes
    ----------
    cells: list
        two dimensional list of CellState, that is, integers between 0 and 5
    marks: list
        tow dimensional list of bool, i.e., of marked cells
    nrows: int
        positve number of rows of the grid
    ncols: int
        positive number of columns of the grid
    agent: Agent
        the agent of the world
    goal: tuple
        (row, col) of the goal to enhance accessing the goal cell
    """

    def __init__(self, nrows, ncols, cells=None, agent_direction=Direction.NORTH, agent_position:list[int]=None, goal_position:list[int]=None) -> None:
        """
        Initializes the world in serveral ways, depending on the arguments.
        
        If cells==None, each cell, except for the agent and goal cell, will be empty.
        If robo_positionn==None, and there is no ROBO state within the cells, the roboter position will be the center of the grid.
        If goal_position==None, and there is no GOAL state within the cells, the goal will be placed randomly such that it is distinct from the robo position.
        """

        if nrows == 0 or ncols == 0 or (cells != None and (len(cells) == 0 or len(cells[0]) == 0)):
            raise InvalidWorldArgumentsExeception()
        self.stack = []
        self.ncols = ncols
        self.nrows = nrows
        self.animation_active = True
        if cells == None:
            self.cells = [[CellState.EMPTY for _ in range(ncols)] for _ in range(nrows)]
        elif nrows != len(cells) or ncols != len(cells[0]):
            raise InvalidWorldArgumentsExeception()
        else:
            self.cells = cells

        # determine the robo position
        if agent_position == None:
            agent_position = self.__find_cell(CellState.AGENT, CellState.AGENT_AT_GOAL)
        if agent_position == None:
            agent_position = [self.nrows // 2, self.ncols // 2]
        self.agent = Agent(agent_position, self, agent_direction=agent_direction)
        self.animator = Animator()

        # determine the goal position
        if goal_position == None:
            goal_position = self.__find_cell(CellState.GOAL)
        if goal_position == None:
            while goal_position == None or (goal_position == agent_position and (ncols > 1 or nrows > 1)):
                goal_position = [np.random.randint(0, nrows), np.random.randint(0, ncols)]
        self.goal = goal_position

        self.cells[agent_position[0]][agent_position[1]] = CellState.AGENT

        if agent_position == self.goal:
            self.cells[self.goal[0]][self.goal[1]] = CellState.AGENT_AT_GOAL
        else:
            self.cells[self.goal[0]][self.goal[1]] = CellState.GOAL
        
        self.marks = [[False for _ in range(ncols)] for _ in range(nrows)]
        self.enable_animation()

    def __repr__(self) -> str:
        """Returns a str-representation of the robo world."""
        representation = ''
        for row in range(self.nrows-1,-1,-1):
            for state in self.cells[row]:
                char = "-"
                if state == CellState.AGENT or state == CellState.AGENT_AT_GOAL:
                    if self.agent.headway == Direction.NORTH:
                        char = 'N'
                    elif self.agent.headway == Direction.SOUTH:
                        char = 'S'
                    elif self.agent.headway == Direction.EAST:
                        char = 'E'
                    else:
                        char = 'W'
                elif state == CellState.OBSTACLE:
                    char = '#'
                elif state == CellState.OBJECT:
                    char = 'O'
                elif state == CellState.GOAL:
                    char = 'G'
                else:
                    char = '-'
                representation += char
            representation += '\n'
        return representation.strip()

    def get_robo(self):
        """Returns the roboter object of this world."""
        return self.agent

    def is_successful(self):
        """Returns true if and only if the roboter found its goal."""
        return self.agent.position[0] == self.goal[0] and self.agent.position[1] == self.goal[1]

    def show(self):
        """Returns a displayabel representation of the world."""
        return self.animator.show(self)

    def get_animation(self, interval=150, save=False, dpi=80):
        """
        Returns a displayable animation of the movement of the roboter.
        Note that this call will clear the animation stack such that the next anmiation starts with the current situation.  

        Parameters
        ----------
        interval: int
            Delay between animation frames in milliseconds.
        save: bool
            If True a gif will be saved at './robo-world-animation.gif'.
        dpi: int
            Controls the dots per inch for the movie frames. Together with the figure's size in inches, this controls the size of the movie.
        """
        return self.animator.get_animation(interval=interval, save=save, dpi=dpi)

    def disable_animation(self):
        """
        Disables the recording of the animation.
        This can be very useful to speed up computation, since recording the animation costs a lot of memory.
        """
        self.animator.disbale()

    def enable_animation(self):
        """Enables the recording of the animation."""
        self.animator.enable()
        self.animator._push(self)

    ## proteced methods

    def _pop(self):
        self.animator._pop()

    def _push(self):
        self.animator._push(self)

    def _move_agent(self, fr, to):
        """
        Moves the agent from a cell fr to another cell to, if this is possible.
        The agent will call this method to update the world.
        If this fails and an exception is risen there is something fundamentally wrong!
        """
        fr_row, fr_col = fr
        to_row, to_col = to

        if not self._is_agent_at(fr_row, fr_col):
            raise RuntimeError(f"There is no robo at {fr}")
        
        if self._is_occupied(to_row, to_col):
            raise RuntimeError(f"The destination {to} of the robo is occupied.")
        
        
        if self._get_state(fr_row, fr_col) == CellState.AGENT_AT_GOAL:
            self._set_state(fr_row, fr_col, CellState.GOAL)
        else:
            self._set_state(fr_row, fr_col, CellState.EMPTY)
        
        if self._get_state(to_row, to_col) == CellState.GOAL:
            self._set_state(to_row, to_col, CellState.AGENT_AT_GOAL)
        else:
            self._set_state(to_row, to_col, CellState.AGENT)

    def _get_state(self, row, col):
        """Returns the state of the cell at (row, col)."""
        return self.cells[row][col]

    def _set_state(self, row, col, state):
        """Sets the state of the cell at (row, col)."""
        self.cells[row][col] = state

    def _is_agent_at(self, row, col):
        """Returns true if and only if the agent/roboter is at (row, col)."""
        return self._get_state(row, col) == CellState.AGENT or self._get_state(row, col) == CellState.AGENT_AT_GOAL

    def _is_object_at(self, row, col):
        """Returns true if and only if a moveable object is at (row, col)."""
        return self._get_state(row, col) == CellState.OBJECT

    def _is_obstacle_at(self, row, col):
        """Returns true if and only if a moveable object is at (row, col)."""
        return self._get_state(row, col) == CellState.OBSTACLE

    def _is_wall_at(self, row, col):
        """Returns true if and only if (row, col) is outside of the world."""
        return row > self.nrows or col > self.ncols

    def _is_occupied(self, row, col):
        """Returns true if and only if (row, col) is occupied by an object, obstacle or the wall (i.e. outside of the world)."""
        return self._is_object_at(row, col) or self._is_obstacle_at(row, col) or self._is_wall_at(row, col)

    def _get_object_at(self, row, col):
        """
        Removes an object at (row, col) and returns it if it is there.
        Otherwise an exception is raised.
        """
        if self._is_object_at(row, col):
            result = self._get_state(row, col)
            self._set_state(row, col, CellState.EMPTY)
            return result
        else:
            raise ObjectMissingException()

    def _set_object_at(self, row, col):
        if self._is_object_at(row, col):
            raise CellOccupiedException()
        else:
            self._set_state(row, col, CellState.OBJECT)

    def _set_mark_at(self, row, col):
        self.marks[row][col] = True

    def _unset_mark_at(self, row, col):
        self.marks[row][col] = False

    def _is_mark_at(self, row, col):
        return self.marks[row][col]
    
    ## private methods

    def __find_cell(self, *states):
        for i, col in enumerate(self.cells):
            for j, cell in enumerate(col):
                for state in states:
                    if cell == state:
                        return (i, j)
        return None

    # static factory methods

    @staticmethod
    def corridor(length:int=10, random_headway:bool=False, nobjects:int=0):

        """
        Returns a corridor (1-D cellular automaton) filled with randomly placed moveable objects.
        The roboter is placed right at the beginning of the corridor.
        There can be at most length-3 objects because there can be no at the cell occupied by the roboter and the goal.
        Furthermore at least one neighboring cell of the roboter has to be empty, otherwise the roboter is stuck (impossible task).

        Parameters
        ----------
        length: int
            Length of the corridor.
        random_headway: bool
            If True the orientation of the roboter is determined randomly, otherwise it is EAST.
        nobjects: int
            Number of objects.
        """

        objects = [CellState.OBJECT for _ in range(min(nobjects, length-3))]
        emptys = [CellState.EMPTY for _ in range(length-3-len(objects))]
        combined = objects + emptys
        random.shuffle(combined)

        cells = [[CellState.AGENT] + [CellState.EMPTY] + combined + [CellState.GOAL]]

        agent_direction = Direction.EAST
        if random_headway:
            agent_direction = random.choice([Direction.NORTH, Direction.SOUTH, Direction.WEST, Direction.EAST])
        return World(nrows=len(cells), ncols=len(cells[0]), cells=cells, agent_direction=agent_direction)

    @ staticmethod
    def maze():
        """Returns a small 6 times 13 simple maze."""
        text = """N#---#---#---
-#-#-#-#-#-#-
-#-#-#-#-#-#-
-#-#-#-#-#-#-
-#-#-#-#-#-#-
---#---#---#G"""

        return World.str_to_world(text)

    @staticmethod
    def complex_maze(nrows:int=10, ncols:int=10, agent_direction:Direction=None):
        """
        Returns a complex, randomly generated nrows times ncols maze.
        It is guaranteed that there is a path from the roboter to its goal.
        
        Parameters
        ----------
        nrows: int
            Number of rows of the maze.
        ncols: int
            Number of columns of the maze.
        nobjects: int
            agent_direction
            The orientation of the roboter (EAST, NORTH, WEST, SOUTH).
            If the parameter is agent_direction==None, the orientation is picked randomly.
            The roboter's position is randomly determined.
        """

        cells = [[CellState.OBSTACLE for _ in range(ncols)] for _ in range(nrows)]

        visited = [[False for _ in range(ncols)] for _ in range(nrows)]

        stack = []
        start = (np.random.randint(0, nrows), np.random.randint(0, ncols))

        def moore(pos):
            return [(pos[0]-1, pos[1]), (pos[0]-1, pos[1]+1), (pos[0], pos[1]+1), (pos[0]+1, pos[1]+1), (pos[0]+1, pos[1]), (pos[0]+1, pos[1]-1), (pos[0], pos[1]-1), (pos[0]-1, pos[1]-1)]

        def critical(pos):
            l1 = [(pos[0]-1, pos[1]), (pos[0]-1, pos[1]+1), (pos[0], pos[1]+1)]
            l2 = [(pos[0], pos[1]+1), (pos[0]+1, pos[1]+1), (pos[0]+1, pos[1])]
            l3 = [(pos[0]+1, pos[1]), (pos[0]+1, pos[1]-1), (pos[0], pos[1]-1)]
            l4 = [(pos[0], pos[1]-1), (pos[0]-1, pos[1]-1), (pos[0]-1, pos[1])]
            return [l1, l2, l3, l4]

        def contains(pos):
            return pos[0] >= 0 and pos[1] >= 0 and pos[0] < nrows and pos[1] < ncols

        def get_neighbours(position):
            return [pos for pos in [
                (position[0] + 1, position[1]),
                (position[0] - 1, position[1]),
                (position[0], position[1] + 1),
                (position[0], position[1] - 1)] if contains(pos)]

        def random_neighbour(position):
            tmp_neighbours = get_neighbours(position)
            neighbours = []
            for neighbour in tmp_neighbours:
                if not visited[neighbour[0]][neighbour[1]]:
                    neighbours.append(neighbour)

            if len(neighbours) > 0:
                return random.choice(neighbours)
            else:
                return None

        def mark(position):
            visited[position[0]][position[1]] = True
            cells[position[0]][position[1]] = CellState.EMPTY
            for nh in moore(position):
                test_positions = critical(nh)
                for test_pos in test_positions:
                    if all(map(lambda e: contains(e) and cells[e[0]][e[1]] == CellState.EMPTY, test_pos)):
                        visited[nh[0]][nh[1]] = True
                        cells[nh[0]][nh[1]] = CellState.OBSTACLE
                        break

        stack.append(start)
        end = start
        max_distance = 0
        while len(stack) > 0:
            next = random_neighbour(stack[-1])
            # dead end
            if next == None:
                stack.pop()
            else:
                mark(next)
                stack.append(next)
                if max_distance < len(stack):
                    max_distance = len(stack)
                    end = next

        if agent_direction == None:
            agent_direction = random.choice([Direction.NORTH, Direction.SOUTH, Direction.WEST, Direction.EAST])

        cells[start[0]][start[1]] = CellState.AGENT
        cells[end[0]][end[1]] = CellState.GOAL

        return World(nrows=len(cells), ncols=len(cells[0]), cells=cells, agent_direction=agent_direction)

    @ staticmethod
    def str_to_world(text: str):
        """
        Retunrs a world by parsing a string that represents the world.
        Single characters have the following semantic:

        # -> (immovable) Obstacle
        G -> Goal
        N -> Roboter (headway==NORTH)
        S -> Roboter (headway==SOUTH)
        W -> Roboter (headway==WEST)
        E -> Roboter (headway==EAST)
        R -> Roboter (random headway)
        O -> Object
        everything else -> Empty
        """

        cells = []
        agent_direction = Direction.EAST
        for row, line in enumerate(text.splitlines()):
            cells.append([])
            for c in line:
                if c in ['N', 'S', 'E', 'W', 'R']:
                    state = CellState.AGENT
                    if c == 'N':
                        agent_direction = Direction.NORTH
                    elif c == 'S':
                        agent_direction = Direction.SOUTH
                    elif c == 'W':
                        agent_direction = Direction.WEST
                    elif c == 'E':
                        agent_direction = Direction.EAST
                    else:
                        agent_direction = random.choice(
                            [Direction.NORTH, Direction.SOUTH, Direction.WEST, Direction.EAST])
                elif c == '#':
                    state = CellState.OBSTACLE
                elif c == 'G':
                    state = CellState.GOAL
                elif c == 'O':
                    state = CellState.OBJECT
                else:
                    state = CellState.EMPTY
                cells[row].append(state)
        return World(nrows=len(cells), ncols=len(cells[0]), cells=cells, agent_direction=agent_direction)

class Agent():
    """
    A representation of the roboter of the robo world.

    A roboter occupies exactly one cell. It can pick up and carray at most one moveable object.
    Objects can only put at empty cells.
    Robo can turn by 90 degree to the left.
    It can only analyse the cell directly in front, therefore, it has an orientation (headway).
    It can mark and unmark cells it occupies but can only spot marks in front.

    Attributes
    ----------
    world: World
        The world of this roboter
    position: list
        The current row and column of the roboter
    headway:
        The current the headway of the roboter (EAST, WEST, NORTH or SOUTH)
    object:
        The current object the roboter is carrying (if any)
    marks: int
        Number of marks the roboter has set and not unset
    print_actions: bool
        If print roboter actions if and only if print_actions==True
    """

    def __init__(self, position: Sequence[int], world: World, agent_direction: Direction=Direction.EAST, print_actions: bool=True) -> None:
        self.world = world
        self.position = [position[0], position[1]]
        self.headway = agent_direction
        self.object = None
        self.marks = 0
        self.print_actions = print_actions

    def __repr__(self) -> str:
        """Returns a str-representation of the agent."""
        return f'robo at {self.position} headway is oriented {self.headway}.'

    def disable_print(self):
        """Deactivates the printing."""
        self.print_actions = False

    def enable_print(self):
        """Activates the printing."""
        self.print_actions = True

    # non-privates
    def is_object_in_front(self) -> bool:
        """Returns True if and only if there is an object in front of robo."""
        return self.__get_state_at(self.headway) == CellState.OBJECT

    def take(self) -> None:
        """
        Takes an object.
        
        Raises
        ------
        SpaceIsFullException
            If robo already carries an object
        WallInFrontException
            If there is a wall in front, i.e., no object
        ObjectMissingException
            If there is no object in front
        """
        if self.object != None:
            raise SpaceIsFullException()
        if self.is_wall_in_front():
            raise WallInFrontException()
        if not self.is_object_in_front():
            raise ObjectMissingException()
        self.object = self.world._get_object_at(*self.__front())
        self.__print(f'takes {self.object}')

    def put(self) -> None:
        """
        Puts the carrying object down in front.
        
        Raises
        ------
        SpaceIsEmptyException
            If robo does not carry an object
        WallInFrontException
            If there is a wall in front, i.e., no object
        ObjectInFrontException
            If there is another object in front
        """

        if not self.is_carrying_object():
            raise SpaceIsEmptyException()
        if self.is_wall_in_front():
            raise WallInFrontException()
        if self.is_object_in_front():
            raise ObjectInFrontException()

        self.world._set_object_at(*self.__front())
        self.__print(f'puts {self.object}')
        self.object = None

    def front_is_clear(self) -> bool:
        """Returns True if and only if thre is no wall in front, i.e., no (immoveable) obstacle and not the boundary of the world."""
        return not self.is_wall_in_front()

    def is_mark_in_front(self) -> bool:
        """Returns True if and only if there is a mark in front."""
        return self.front_is_clear() and self.__is_mark_at(self.headway)

    def is_wall_in_front(self) -> bool:
        """Returns True if and only if there is an (immoveable) obstacle or the boundary of the world in front."""
        return not self.__is_reachable(self.headway)

    def move(self) -> list[int]:
        """
        Moves robo one cell ahead.
        
        Raises
        ------
        WallInFrontException
            If there is an (immoveable) wall in front (obstacle or boundary of the world)
        ObjectInFrontException
            If there is an object (moveable) in front
        """
        before = [self.position[0], self.position[1]]
        if self.is_wall_in_front():
            raise WallInFrontException()
        if self.is_object_in_front():
            raise ObjectInFrontException()
        self.position[0] += self.headway.value[0]
        self.position[1] += self.headway.value[1]
        self.world._move_agent(before, self.position)

        # if self.is_carrying_object():
        #    self.object.set_position(self.position)
        self.world._push()
        self.__print(f'move ({before[1]},{before[0]}) -> ({self.position[1]},{self.position[0]})')
        return self.position

    def set_mark(self) -> None:
        """Marks the current cell, i.e., position."""
        self.world._set_mark_at(*self.position)
        self.__print(f'mark ({self.position[1]},{self.position[0]})')

    def unset_mark(self) -> None:
        """Unmarks the current cell, i.e., position."""
        self.world._unset_mark_at(*self.position)
        self.__print(f'remove mark ({self.position[1]},{self.position[0]})')

    def is_carrying_object(self) -> bool:
        """Returns True if and only if robo is carrying an object."""
        return self.object != None

    def turn_left(self) -> None:
        """Robo turns 90 degrees to the left."""
        before = self.headway
        self.headway = self.headway.next()
        self.__print(f'turn {before} -> {self.headway}')

    def is_facing_north(self) -> bool:
        """Returns True if and only if robo is oriented towords the north."""
        return self.headway == Direction.NORTH

    def toss(self):
        toss = random.randint(0, 1) == 1
        self.__print(f'toss {toss}')
        return toss

    def is_at_goal(self):
        """Returns True if and only if robo is standing at the goal."""
        return self.position[0] == self.world.goal[0] and self.position[1] == self.world.goal[1]

    ## private methods
    def __print(self, fstring: str):
        if self.print_actions:
            print(fstring)

    def __get_state_at(self, direction: Direction) -> CellState:
        y, x = self.position
        if direction == Direction.WEST:
            return self.world._get_state(y, x-1)
        elif direction == Direction.EAST:
            return self.world._get_state(y, x+1)
        elif direction == Direction.NORTH:
            return self.world._get_state(y+1, x)
        else:
            return self.world._get_state(y-1, x)

    def __is_mark_at(self, direction: Direction) -> bool:
        y, x = self.position
        if direction == Direction.WEST:
            return self.world._is_mark_at(y, x-1)
        elif direction == Direction.EAST:
            return self.world._is_mark_at(y, x+1)
        elif direction == Direction.NORTH:
            return self.world._is_mark_at(y+1, x)
        else:
            return self.world._is_mark_at(y-1, x)

    def __is_reachable(self, direction: Direction) -> bool:
        y, x = self.position
        if direction == Direction.WEST:
            return x-1 >= 0 and self.world._get_state(y, x-1) != CellState.OBSTACLE
        elif direction == Direction.EAST:
            return x+1 < self.world.ncols and self.world._get_state(y, x+1) != CellState.OBSTACLE
        elif direction == Direction.NORTH:
            return y+1 < self.world.nrows and self.world._get_state(y+1, x) != CellState.OBSTACLE
        else:
            return y-1 >= 0 and self.world._get_state(y-1, x) != CellState.OBSTACLE

    def __front(self) -> tuple[int, int]:
        return self.position[0] + self.headway.value[0], self.position[1] + self.headway.value[1]

    def __back(self):
        return self.position[0] - self.headway.value[0], self.position[1] - self.headway.value[1]

    # These methods should be implemented by the students in excercises!
    def __turn(self) -> int:
        self.turn_left()
        self.turn_left()
        return 2

    def __turn_right(self) -> int:
        self.turn_left()
        self.turn_left()
        self.turn_left()
        return 3

    def __turn_to_north(self) -> int:
        turns = 0
        while not self.is_facing_north():
            self.turn_left()
            turns += 1
        return turns

    def __turn_to_south(self) -> int:
        turns = self.__turn_to_north()
        turns += self.__turn()
        return turns

    def __turn_to_east(self) -> int:
        turns = self.__turn_to_south()
        self.turn_left()
        return turns + 1

    def __turn_to_west(self) -> int:
        turns = self.__turn_to_north()
        self.turn_left()
        return turns + 1

    def __reverse_turns(self, turns: int):
        for _ in range(4 - (turns % 4)):
            self.turn_left()

    def __is_wall_at(self, direction: Direction) -> bool:
        if direction == Direction.NORTH:
            turns = self.__turn_to_north()
        elif direction == Direction.EAST:
            turns = self.__turn_to_east()
        elif direction == Direction.SOUTH:
            turns = self.__turn_to_south()
        else:
            turns = self.__turn_to_west()
        result = self.is_wall_in_front()
        self.__reverse_turns(turns)
        return result

    def __is_wall_at_west(self) -> bool:
        return self.__is_wall_at(Direction.WEST)

    def __is_wall_at_east(self) -> bool:
        return self.__is_wall_at(Direction.EAST)

    def __is_wall_at_north(self) -> bool:
        return self.__is_wall_at(Direction.NORTH)

    def __is_wall_at_south(self) -> bool:
        return self.__is_wall_at(Direction.SOUTH)

    def __move_west(self):
        self.__turn_to_west()
        return self.move()

    def __move_east(self):
        self.__turn_to_east()
        return self.move()

    def __move_north(self):
        self.__turn_to_north()
        return self.move()

    def __move_south(self):
        self.__turn_to_south()
        return self.move()

    # methods for testing
    def __get_direction(self):
        return self.headway
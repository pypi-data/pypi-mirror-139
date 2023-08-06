from enum import Enum
import numpy as np
import random

from roboworld.animator import Animator

from roboworld.direction import Direction
from .roboexception import InvalidWorldArgumentsExeception, ObjectMissingException, ObjectInFrontException, CellOccupiedException, RoboException
from .cellstate import CellState
from .agent import Agent

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
    animation_active: bool
        todo
    """

    def __init__(self, nrows, ncols, cells=None, agent_direction=Direction.NORTH, agent_position=None, goal_position=None) -> None:
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
            agent_position = (self.nrows // 2, self.ncols // 2)
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

    def get_robo(self):
        return self.agent

    def is_successful(self):
        """Returns true if and only if the roboter found its goal."""
        return self.agent.position[0] == self.goal[0] and self.agent.position[1] == self.goal[1]

    def show(self):
        return self.animator.show(self)

    def get_animation(self, interval=150, save=False, dpi=80):
        return self.animator.get_animation(interval=interval, save=save, dpi=dpi)

    def disable_animation(self):
        self.animator.disbale()

    def enable_animation(self):
        self.animator.disbale()

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
        if not self._is_agent_at(*fr):
            raise RuntimeError(f"There is no robo at {fr}")
        
        if self._is_occupied(*to):
            raise RuntimeError(f"The destination {to} of the robo is occupied.")
        
        fr_row, fr_col = fr
        to_row, to_col = to
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
    def corridor(length=10, random_headway=False, nobjects=0):

        objects = [CellState.OBJECT for _ in range(min(nobjects, length-2))]
        emptys = [CellState.EMPTY for _ in range(length-2-len(objects))]
        combined = objects + emptys
        random.shuffle(combined)

        cells = [[CellState.AGENT] + combined + [CellState.GOAL]]

        agent_direction = Direction.EAST
        if random_headway:
            agent_direction = random.choice(
                [Direction.NORTH, Direction.SOUTH, Direction.WEST, Direction.EAST])
        return World(nrows=len(cells), ncols=len(cells[0]), cells=cells, agent_direction=agent_direction)

    @ staticmethod
    def maze():
        text = """N#---#---#---
-#-#-#-#-#-#-
-#-#-#-#-#-#-
-#-#-#-#-#-#-
-#-#-#-#-#-#-
---#---#---#G"""
        return World.str_to_world(text)

    @staticmethod
    def complex_maze(nrows=10, ncols=10, agent_direction=None):
        cells = [[CellState.OBSTACLE for _ in range(
            ncols)] for _ in range(nrows)]

        visited = [[False for _ in range(
            ncols)] for _ in range(nrows)]

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
            agent_direction = random.choice(
                [Direction.NORTH, Direction.SOUTH, Direction.WEST, Direction.EAST])

        cells[start[0]][start[1]] = CellState.AGENT
        cells[end[0]][end[1]] = CellState.GOAL

        return World(nrows=len(cells), ncols=len(cells[0]), cells=cells, agent_direction=agent_direction)

    @ staticmethod
    def str_to_world(text):
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
                    elif c == 'W':
                        agent_direction = Direction.EAST
                    else:
                        agent_direction = random.choice(
                            [Direction.NORTH, Direction.SOUTH, Direction.WEST, Direction.EAST])
                elif c == '#':
                    state = CellState.OBSTACLE
                elif c == 'G':
                    state = CellState.GOAL
                else:
                    state = CellState.EMPTY
                cells[row].append(state)
        return World(nrows=len(cells), ncols=len(cells[0]), cells=cells, agent_direction=agent_direction)

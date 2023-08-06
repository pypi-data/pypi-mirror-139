import enum

class CellState(enum.IntEnum):
    """
    All possible states of a cell of the cellular automaton.
    
    OBSTACLE is unmoveable while OBJECT is moveable.
    AGENT_AT_GOAL is a combination of AGENT and GOAL.
    """

    EMPTY = 0
    OBSTACLE = 1
    AGENT = 2
    OBJECT = 3
    GOAL = 4
    AGENT_AT_GOAL = 5

import enum

@enum.unique
class Direction(enum.Enum):
    """
    All possible states of a cell of the cellular automaton.
    
    OBSTACLE is unmoveable while OBJECT is moveable.
    AGENT_AT_GOAL is a combination of AGENT and GOAL.
    """

    # ccw ordered (y, x)!!!
    EAST = (0, 1)
    NORTH = (1, 0)
    WEST = (0, -1)
    SOUTH = (-1, 0)

    def next(self):
        """Rotates the current direction by 90 degree in ccw order."""

        if self == Direction.EAST:
            return Direction.NORTH
        if self == Direction.NORTH:
            return Direction.WEST
        if self == Direction.WEST:
            return Direction.SOUTH
        else:
            return Direction.EAST

    def to_float(self):
        """Transforms the direction to a floating point number within [0;1]."""

        if self == Direction.EAST:
            return 0.25
        if self == Direction.NORTH:
            return 0.5
        if self == Direction.WEST:
            return 0.75
        else:
            return 1.0
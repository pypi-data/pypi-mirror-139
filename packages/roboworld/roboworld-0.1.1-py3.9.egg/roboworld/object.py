import typing 

class Object():
    """A moveable obeject of the robo world."""

    def __init__(self, position: typing.Sequence[int], name: str) -> None:
        self.name = name
        self.position = position

    def __str__(self) -> str:
        return self.name

    def set_position(self, position: typing.Sequence[int]):
        self.position = position
from typing import TypedDict, Tuple, Dict, Literal, NamedTuple


class ActionValues(TypedDict):
    UP: float
    DOWN: float
    LEFT: float
    RIGHT: float


Direction = Tuple[int, int]
Danger = Tuple[bool, bool, bool, bool]
Object = Literal['W', 'G', 'R']


class State(NamedTuple):
    danger: Danger
    direction: Direction
    up: Object
    down: Object
    right: Object
    left: Object


QTable = Dict[State, ActionValues]

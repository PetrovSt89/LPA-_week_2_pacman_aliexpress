import dataclasses

@dataclasses.dataclass(frozen=True)
class Const():
    LEFT_X: int = 40
    RIGHT_X: int = 560
    HIGHT_Y: int = 40
    LOW_Y: int = 400
    HEALTH: int = 10
const = Const()
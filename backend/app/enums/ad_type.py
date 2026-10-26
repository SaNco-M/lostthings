from enum import Enum


class LostOrFound(str, Enum):
    LOST = "lost"
    FOUND = "found"

class AdType(str, Enum):
    ITEM = "item"
    ANIMAL = "animal"
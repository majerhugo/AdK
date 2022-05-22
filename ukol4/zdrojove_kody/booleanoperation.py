from enum import *

class BooleanOperation(Enum):
    Union = 0
    Intersection = 1
    Difference_AB = 2
    Difference_BA = 3
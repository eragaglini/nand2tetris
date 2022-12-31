from enum import Enum


class CommandType(Enum):
    C_PUSH = 1
    C_POP = 2
    C_ARITHMETIC = 3
    C_RETURN = 4
    C_FUNCTION = 5
    C_CALL = 6

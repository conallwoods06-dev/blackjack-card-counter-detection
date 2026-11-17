from enum import Enum
from detector.hand import Hand, CARD_VALUES


class Action(Enum):
    HIT = "hit"
    STAND = "stand"
    DOUBLE = "double"

def dealer_value(card: str) -> int:
    if card == "A":
        return 11
    return CARD_VALUES[card]
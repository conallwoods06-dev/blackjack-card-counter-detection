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

def basic_strategy(player_hand: Hand, dealer_card: str) -> Action:
    player_total = player_hand.value()
    dealer_upcard_value = dealer_value(dealer_card)

    # Basic strategy rules for hard totals
    if player_total >= 17:
        return Action.STAND
    elif 13 <= player_total <= 16:
        if dealer_upcard_value >= 7:
            return Action.HIT
        else:
            return Action.STAND
    elif player_total == 12:
        if 4 <= dealer_upcard_value <= 6:
            return Action.STAND
        else:
            return Action.HIT
    elif player_total == 11:
        if dealer_upcard_value < 11:
            return Action.DOUBLE
        else:
            return Action.HIT
    elif player_total == 10:
        if dealer_upcard_value < 10:
            return Action.DOUBLE
        else:
            return Action.HIT
    elif player_total == 9:
        if 3 <= dealer_upcard_value <= 6:
            return Action.DOUBLE
        else:
            return Action.HIT
    else:  # player_total <= 8
        return Action.HIT
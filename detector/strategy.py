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

def _table_action(player_hand: Hand, dealer_card: str) -> Action:
    player_total = player_hand.value()
    dealer_upcard_value = dealer_value(dealer_card)

  # Basic strategy rules for soft totals
    if player_hand.is_soft():
        if player_total >= 19:
            return Action.STAND
        elif player_total == 18:
            if dealer_upcard_value in [2, 7, 8]:
                return Action.STAND
            elif dealer_upcard_value in [3, 4, 5, 6]:
                return Action.DOUBLE
            else:  # dealer_upcard_value in [9, 10, 11]
                return Action.HIT
        elif player_total == 17:
            if dealer_upcard_value in [3, 4, 5, 6]:
                return Action.DOUBLE
            else:
                return Action.HIT
        elif player_total in [15, 16]:
            if dealer_upcard_value in [4, 5, 6]:
                return Action.DOUBLE
            else:
                return Action.HIT
        elif player_total in [13, 14]:
            if dealer_upcard_value in [5, 6]:
                return Action.DOUBLE
            else:
                return Action.HIT
        else:  # player_total <= 12 (soft A-A)
            return Action.HIT
        
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

def basic_strategy(player_hand: Hand, dealer_card: str) -> Action:
    # Call table action and check if answer is allowed
    action = _table_action(player_hand, dealer_card)
    if action == Action.DOUBLE and len(player_hand.cards) > 2:
        if player_hand.is_soft() and player_hand.value() == 18:  # Cannot double after two cards
            return Action.STAND 
        return Action.HIT  
    return action
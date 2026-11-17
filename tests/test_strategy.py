from detector.hand import Hand
from detector.strategy import Action, basic_strategy
import pytest

def make_hand(cards: list[str]) -> Hand:
    hand = Hand()
    for card in cards:
        hand.add(card)
    return hand

@pytest.mark.parametrize("cards, dealer, expected", [
    # cards          dealer  expected
    (["10", "6"],    "10",   Action.HIT),     # hard 16 vs 10
    (["10", "6"],    "6",    Action.STAND),   # hard 16 vs 6
    (["10", "2"],    "3",    Action.HIT),     # hard 12 vs 3  (boundary)
    (["10", "2"],    "4",    Action.STAND),   # hard 12 vs 4  (boundary)
    (["6", "5"],     "A",    Action.HIT),     # 11 vs ace
    (["6", "5"],     "10",   Action.DOUBLE),  # 11 vs 10
    (["6", "4"],     "9",    Action.DOUBLE),  # 10 vs 9  (boundary)
    (["6", "4"],     "10",   Action.HIT),     # 10 vs 10 (boundary)
    (["5", "4"],     "2",    Action.HIT),     # 9 vs 2   (boundary)
    (["5", "4"],     "3",    Action.DOUBLE),  # 9 vs 3   (boundary)
    (["10", "7"],    "A",    Action.STAND),   # hard 17 vs ace
    (["5", "3"],     "6",    Action.HIT),     # 8 vs 6
])
def test_hard_hand_strategy(cards, dealer, expected):
    hand = make_hand(cards)
    assert basic_strategy(hand, dealer) == expected
    
import pytest
from detector.hand import Hand

def make_hand(cards: list[str]) -> Hand:
    hand = Hand()
    for card in cards:
        hand.add(card)
    return hand


def test_ace_six_is_soft_17():
    hand = make_hand(["A", "6"])
    assert hand.is_soft()
    assert hand.value() == 17

def test_ace_six_ten_is_hard_17():
    hand = make_hand(["A", "6", "10"])
    assert not hand.is_soft()
    assert hand.value() == 17

def test_ace_ace_is_soft_12():
    hand = make_hand(["A", "A"])
    assert hand.is_soft()
    assert hand.value() == 12

def test_ace_king_is_blackjack():
    hand = make_hand(["A", "K"])
    assert hand.is_blackjack()
    assert hand.value() == 21

def test_three_card_21_is_not_blackjack():
    hand = make_hand(["7", "7", "7"])
    assert not hand.is_blackjack()
    assert hand.value() == 21

def test_ten_six_nine_is_bust():
    hand = make_hand(["10", "6", "9"])
    assert hand.is_bust()
    assert hand.value() == 25

def test_eight_eight_can_split():
    hand = make_hand(["8", "8"])
    assert hand.can_split()

def test_king_queen_can_split():
    hand = make_hand(["K", "Q"])
    assert hand.can_split()

def test_king_nine_cannot_split():
    hand = make_hand(["K", "9"])
    assert not hand.can_split()

def test_empty_hand_has_value_zero():
    hand = Hand()
    assert hand.value() == 0

def test_four_aces_is_soft_14():
    hand = make_hand(["A", "A", "A", "A"])
    assert hand.is_soft()
    assert hand.value() == 14
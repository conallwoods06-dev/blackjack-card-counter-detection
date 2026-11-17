"""
Tests for Phase 1. Run from the project folder with:   pytest -v

Each test checks ONE fact we know must be true. If you change the code
later and break something, a test goes red and tells you immediately.
"""

import pytest
from detector.shoe import Shoe, CARDS_PER_DECK
from detector.counter import HiLoCounter, KOCounter, OmegaIICounter


def test_shoe_has_right_number_of_cards():
    shoe = Shoe(num_decks=6)
    assert shoe.cards_remaining() == 6 * 52


def test_shoe_has_24_aces_in_six_decks():
    shoe = Shoe(num_decks=6)
    assert shoe.cards.count("A") == 24


def test_same_seed_gives_same_order():
    assert Shoe(seed=42).cards == Shoe(seed=42).cards


def test_needs_shuffle_at_cut_card():
    shoe = Shoe(num_decks=1, penetration=0.75, seed=1)
    dealt = 0
    while not shoe.needs_shuffle():
        shoe.deal()
        dealt += 1
    assert dealt == 39  # 75% of 52


def test_invalid_penetration_rejected():
    with pytest.raises(ValueError):
        Shoe(penetration=1.5)


# The key sanity check: Hi-Lo is a BALANCED system, so after every card
# in the shoe has been seen the running count must be exactly 0.
@pytest.mark.parametrize("seed", range(10))
def test_hilo_full_shoe_sums_to_zero(seed):
    shoe = Shoe(num_decks=6, penetration=1.0, seed=seed)
    counter = HiLoCounter()
    while shoe.cards_remaining() > 0:
        counter.see(shoe.deal())
    assert counter.running_count() == 0


def test_omega_ii_is_balanced_too():
    shoe = Shoe(num_decks=2, penetration=1.0, seed=3)
    c = OmegaIICounter()
    while shoe.cards_remaining() > 0:
        c.see(shoe.deal())
    assert c.running_count() == 0


def test_ko_is_unbalanced():
    # KO adds +1 for every 7: 4 sevens per deck -> ends at +4 per deck.
    shoe = Shoe(num_decks=6, penetration=1.0, seed=3)
    c = KOCounter()
    while shoe.cards_remaining() > 0:
        c.see(shoe.deal())
    assert c.running_count() == 4 * 6


def test_true_count_example():
    c = HiLoCounter()
    for card in ["2", "3", "4", "5", "6", "2"]:  # running count = +6
        c.see(card)
    # 3 decks left -> true count +2
    assert c.true_count(cards_remaining=3 * CARDS_PER_DECK) == pytest.approx(2.0)


def test_unknown_card_raises():
    with pytest.raises(KeyError):
        HiLoCounter().see("Z")

"""
shoe.py - models the "shoe": the box the dealer deals cards from.

A casino shoe usually holds 6 or 8 decks shuffled together. The dealer
does NOT deal every card: a plastic "cut card" is placed part-way
through, and when it comes out the shoe is reshuffled. How far in the
cut card sits is called PENETRATION (e.g. 0.75 = 75% of cards dealt).
Penetration matters a lot to counters: deeper penetration = more
high true counts = more profit.
"""

import random

# Ranks in one suit. We ignore suits entirely, because in blackjack the
# suit never matters. "T" stands for any ten-valued card (10, J, Q, K)
# but we keep J/Q/K separate so the CV module later can report exactly
# what it saw.
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
SUITS_PER_DECK = 4
CARDS_PER_DECK = len(RANKS) * SUITS_PER_DECK  # 52


class Shoe:
    def __init__(self, num_decks: int = 6, penetration: float = 0.75, seed: int | None = None):
        # Validate inputs early ("fail fast"). A bad value here would
        # cause confusing bugs much later, so catch it immediately.
        if num_decks < 1:
            raise ValueError("num_decks must be at least 1")
        if not 0 < penetration <= 1:
            raise ValueError("penetration must be between 0 and 1")

        self.num_decks = num_decks
        self.penetration = penetration

        # Our own random generator. Passing a seed makes the shuffle
        # REPRODUCIBLE: same seed -> same card order every run. This is
        # essential for testing and for repeatable experiments later.
        self._rng = random.Random(seed)

        self.cards: list[str] = []
        self.shuffle()

    def shuffle(self) -> None:
        """Rebuild the full shoe and shuffle it."""
        # One deck = every rank, 4 times. Multiply for num_decks.
        self.cards = RANKS * SUITS_PER_DECK * self.num_decks
        self._rng.shuffle(self.cards)

        # The cut card position: once fewer than this many cards remain,
        # it's time to shuffle.
        total = len(self.cards)
        self._cut_point = int(total * (1 - self.penetration))

    def deal(self) -> str:
        """Remove and return the top card."""
        if not self.cards:
            raise RuntimeError("Shoe is empty - call shuffle() first")
        # pop() takes from the end of the list; since it's shuffled,
        # "the end" is as good as "the top".
        return self.cards.pop()

    def cards_remaining(self) -> int:
        return len(self.cards)

    def decks_remaining(self) -> float:
        return self.cards_remaining() / CARDS_PER_DECK

    def needs_shuffle(self) -> bool:
        """True once the cut card has been reached."""
        return self.cards_remaining() <= self._cut_point

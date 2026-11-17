"""
hand.py - a blackjack hand and its value.
"""

# Aces are listed as 1 here; the Hand class decides when to upgrade to 11.
CARD_VALUES = {
    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
    "10": 10, "J": 10, "Q": 10, "K": 10, "A": 1,
}


class Hand:
    def __init__(self, bet: float = 0.0):
        self.cards: list[str] = []
        self.bet = bet

    def add(self, card: str) -> None:
        self.cards.append(card)

    def _hard_total(self) -> int:
        # Every ace counted as 1.
        return sum(CARD_VALUES[c] for c in self.cards)

    def is_soft(self) -> bool:
        # Soft = we have an ace AND counting one ace as 11 doesn't bust us.
        return "A" in self.cards and self._hard_total() + 10 <= 21

    def value(self) -> int:
        return self._hard_total() + (10 if self.is_soft() else 0)

    def is_blackjack(self) -> bool:
        # Exactly two cards totalling 21 (an ace and a ten-card).
        return len(self.cards) == 2 and self.value() == 21

    def is_bust(self) -> bool:
        return self.value() > 21

    def can_split(self) -> bool:
        # Two cards of equal value, e.g. 8-8 or K-Q.
        return len(self.cards) == 2 and CARD_VALUES[self.cards[0]] == CARD_VALUES[self.cards[1]]

    def __repr__(self) -> str:
        # Controls how a Hand looks when printed - very handy for debugging.
        kind = "soft" if self.is_soft() else "hard"
        return f"Hand({self.cards}, {kind} {self.value()})"
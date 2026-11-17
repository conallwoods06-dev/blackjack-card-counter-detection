"""
counter.py - card counting systems.

We design this so that MANY counting systems can exist side by side.
Later, the detector will ask: "which system (if any) best explains this
player's bets?" So we write a general CountingSystem class and define
each real system as just a table of values.
"""

from detector.shoe import CARDS_PER_DECK

# Each system is just a dictionary: card rank -> count value.
# Hi-Lo: low cards (2-6) leaving the shoe are GOOD for the player
# (more tens and aces remain), so they count +1. High cards count -1.
HI_LO = {
    "2": 1, "3": 1, "4": 1, "5": 1, "6": 1,
    "7": 0, "8": 0, "9": 0,
    "10": -1, "J": -1, "Q": -1, "K": -1, "A": -1,
}

# KO ("Knock-Out"): like Hi-Lo but 7 is also +1. Because there are more
# +1 cards than -1 cards it is "unbalanced": a full shoe does NOT sum to
# zero. Counters using KO don't bother converting to a true count.
KO = {**HI_LO, "7": 1}

# Omega II: a more advanced, multi-level system.
OMEGA_II = {
    "2": 1, "3": 1, "4": 2, "5": 2, "6": 2,
    "7": 1, "8": 0, "9": -1,
    "10": -2, "J": -2, "Q": -2, "K": -2, "A": 0,
}


class CountingSystem:
    def __init__(self, values: dict[str, int], name: str = "custom"):
        self.values = values
        self.name = name
        self._running = 0

    def see(self, card: str) -> None:
        """Update the count with a card that has just become visible."""
        # dict[key] raises KeyError for an unknown card - good: if the
        # CV module ever reports "Z", we want to know loudly.
        self._running += self.values[card]

    def running_count(self) -> int:
        return self._running

    def true_count(self, cards_remaining: int) -> float:
        """Running count divided by decks remaining."""
        decks_left = cards_remaining / CARDS_PER_DECK
        # Guard against dividing by ~0 at the very end of a shoe.
        # Half a deck is a common floor real counters use.
        decks_left = max(decks_left, 0.5)
        return self._running / decks_left

    def reset(self) -> None:
        """Call after every shuffle."""
        self._running = 0


# Convenience constructors so other code can write HiLoCounter().
def HiLoCounter() -> CountingSystem:
    return CountingSystem(HI_LO, "Hi-Lo")

def KOCounter() -> CountingSystem:
    return CountingSystem(KO, "KO")

def OmegaIICounter() -> CountingSystem:
    return CountingSystem(OMEGA_II, "Omega II")

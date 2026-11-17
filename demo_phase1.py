"""
Deal through one shoe and watch the count change.
Run with:   python demo_phase1.py
"""

from detector.shoe import Shoe
from detector.counter import HiLoCounter

shoe = Shoe(num_decks=6, penetration=0.75, seed=7)
counter = HiLoCounter()

highest_tc = 0.0
round_no = 0

while not shoe.needs_shuffle():
    round_no += 1
    # Pretend each round shows ~10 cards (a few players + dealer).
    cards = [shoe.deal() for _ in range(10)]
    for card in cards:
        counter.see(card)

    tc = counter.true_count(shoe.cards_remaining())
    highest_tc = max(highest_tc, tc)

    # A crude text bar so you can SEE the count swing.
    bar = "+" * int(max(tc, 0) * 2) if tc >= 0 else "-" * int(-tc * 2)
    print(f"Round {round_no:2d} | RC {counter.running_count():+3d} | "
          f"decks left {shoe.decks_remaining():4.1f} | TC {tc:+5.1f} {bar}")

print(f"\nShuffle! Highest true count this shoe: {highest_tc:+.1f}")
counter.reset()

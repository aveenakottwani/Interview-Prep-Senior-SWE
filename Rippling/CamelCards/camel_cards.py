"""
Rippling: AI-assisted coding round. Camel Cards.

Card ranks from low to high: 2 3 4 5 6 7 8 9 T J Q K A.
Classes: Card, Rank (stores the rank), Hand (exactly 5 cards), a card sort function that
decides which of two cards ranks higher, and Game, which runs a game between two hands.

Hand types from strongest to weakest:
  Five of a kind:  all 5 cards the same
  Four of a kind:  4 the same + 1 different
  Full house:      3 the same + 2 the same
  Three of a kind: 3 the same + 2 other distinct cards
  Two pair
  One pair
  High card:       all 5 cards distinct

Compare two hands by HandType first. If the types are equal, break the tie by comparing
the cards from left to right; the first higher card wins.

Part 1
  Input:  one line with two hands a b separated by a space, each exactly 5 characters, no '?'.
  Output: 1 if a is stronger, -1 if b is stronger, 0 if tied.
  Example: "33332 2AAAA" -> 1

Part 2: best and worst hand
  Given a hand containing unknown cards '?' (each '?' can independently be replaced with any
  of 2 3 4 5 6 7 8 9 T J Q K A), find the strongest possible hand (best) and the weakest
  possible hand (worst) after replacement, using the rules above.
  Example: "AAAA?" -> AAAAA AAAA2
  Follow-up: optimize from brute force (13^k fills) to building the answer directly.
"""
import sys
from collections import Counter
from enum import Enum, IntEnum
from functools import total_ordering
from typing import List, Tuple

_LABELS = "23456789TJQKA"  # low to high; index + 2 == Rank value


class Rank(Enum):
    """Stores the 13 card ranks, low to high: 2 3 4 5 6 7 8 9 T J Q K A.

    Each member's value is its strength (TWO=2 ... ACE=14), so ranks compare by value.
    """

    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10    # 'T'
    JACK = 11   # 'J'
    QUEEN = 12  # 'Q'
    KING = 13   # 'K'
    ACE = 14    # 'A'

    @classmethod
    def from_char(cls, label: str) -> "Rank":
        """Return the Rank for a single label character such as '7' or 'T'."""
        if len(label) != 1 or label not in _LABELS:
            raise ValueError(f"invalid card label: {label!r}")
        return cls(_LABELS.index(label) + 2)


class HandType(IntEnum):
    """Hand types, weakest to strongest. A higher value means a stronger hand."""

    HIGH_CARD = 1        # all 5 distinct
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4  # 3 the same + 2 other distinct cards
    FULL_HOUSE = 5       # 3 the same + 2 the same
    FOUR_OF_A_KIND = 6   # 4 the same + 1 different
    FIVE_OF_A_KIND = 7   # all 5 the same


# Sorted label counts (largest first) -> HandType.
_COUNTS_TO_TYPE = {
    (5,): HandType.FIVE_OF_A_KIND,
    (4, 1): HandType.FOUR_OF_A_KIND,
    (3, 2): HandType.FULL_HOUSE,
    (3, 1, 1): HandType.THREE_OF_A_KIND,
    (2, 2, 1): HandType.TWO_PAIR,
    (2, 1, 1, 1): HandType.ONE_PAIR,
    (1, 1, 1, 1, 1): HandType.HIGH_CARD,
}


class Card:
    """A single card, identified by its Rank."""

    def __init__(self, label: str) -> None:
        """Build a card from its label character, such as 'A' or '9'."""
        self.rank: Rank = Rank.from_char(label)

    @staticmethod
    def compare(a: "Card", b: "Card") -> int:
        """Card sort function: return a negative number if a ranks below b, 0 if equal, positive if a ranks above b.

        Usable as a sort key via functools.cmp_to_key(Card.compare).
        """
        return a.rank.value - b.rank.value

    def __repr__(self) -> str:
        return _LABELS[self.rank.value - 2]


@total_ordering
class Hand:
    """Exactly 5 cards, kept in the order they were dealt.

    Ordering: compare HandType first; if the types are equal, compare cards left to
    right in dealt order (the Camel Cards rule, not a poker-style sort).
    """

    SIZE = 5

    def __init__(self, labels: str) -> None:
        """Build a hand from a 5-character string such as '32T3K'. Raises ValueError if it isn't 5 cards."""
        if len(labels) != self.SIZE:
            raise ValueError(f"a hand needs exactly {self.SIZE} cards, got {labels!r}")
        self.cards: List[Card] = [Card(c) for c in labels]

    def check_hand(self) -> HandType:
        """Identify which HandType this hand is, from the multiset of its labels."""
        counts = tuple(sorted(Counter(c.rank for c in self.cards).values(), reverse=True))
        return _COUNTS_TO_TYPE[counts]

    def check_rank(self) -> int:
        """Call check_hand() and return the rank (strength, 1-7) of that HandType."""
        return self.check_hand().value

    def _sort_key(self) -> Tuple[int, Tuple[int, ...]]:
        return self.check_rank(), tuple(c.rank.value for c in self.cards)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Hand):
            return NotImplemented
        return self._sort_key() == other._sort_key()

    def __lt__(self, other: "Hand") -> bool:
        if not isinstance(other, Hand):
            return NotImplemented
        return self._sort_key() < other._sort_key()

    def __hash__(self) -> int:
        return hash(self._sort_key())

    def __repr__(self) -> str:
        return "".join(repr(c) for c in self.cards)


class Game:
    """Runs a game between two hands and decides the winner."""

    def __init__(self, hand1: Hand, hand2: Hand) -> None:
        self.hand1 = hand1
        self.hand2 = hand2

    def play(self) -> int:
        """Return 1 if hand1 wins, -1 if hand2 wins, or 0 if the hands are tied.

        Uses Hand's ordering: the stronger HandType wins; if the types are equal, cards
        are compared left to right (2 < 3 < ... < A) and the first higher card wins.
        """
        if self.hand1 > self.hand2:
            return 1
        if self.hand2 > self.hand1:
            return -1
        return 0


def best_and_worst_hands(labels: str) -> Tuple[str, str]:
    """Part 2: each '?' can independently be any of 2 3 4 5 6 7 8 9 T J Q K A.

    Returns (best hand, worst hand) as strings, built directly in O(1) (5 cards, 13 labels):
      - Best: fill every '?' with the most frequent known label. Adding all wildcards to
        the largest group gives the strongest HandType. On a frequency tie the hands first
        differ at the first '?', so the higher rank wins. With no known cards, use 'A'.
      - Worst: fill each '?' left to right with the next smallest label not already in
        the hand. New singles never strengthen the HandType, and the smallest labels go
        first because ties are compared left to right.
    """
    if len(labels) != Hand.SIZE or any(c not in _LABELS and c != "?" for c in labels):
        raise ValueError(f"invalid hand: {labels!r}")

    counts = Counter(c for c in labels if c != "?")
    best_fill = max(counts, key=lambda c: (counts[c], _LABELS.index(c))) if counts else "A"
    best = labels.replace("?", best_fill)

    unused = iter(c for c in _LABELS if c not in counts)  # ascending; 13 labels > 5 slots
    worst = "".join(next(unused) if c == "?" else c for c in labels)
    return best, worst


def main() -> None:
    """Read one line 'a b' (two 5-card hands) from stdin and print 1, -1 or 0."""
    a, b = sys.stdin.readline().split()
    print(Game(Hand(a), Hand(b)).play())


if __name__ == "__main__":
    main()

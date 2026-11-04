import unittest
from itertools import product

from Rippling.CamelCards.camel_cards import _LABELS, Game, Hand, HandType, best_and_worst_hands


class TestHandOrdering(unittest.TestCase):
    def test_given_case_same_type_first_card_breaks_tie(self):
        # Both four of a kind; first card 3 > 2, so the aces in 2AAAA don't matter.
        self.assertEqual(Hand("33332").check_hand(), HandType.FOUR_OF_A_KIND)
        self.assertEqual(Hand("2AAAA").check_hand(), HandType.FOUR_OF_A_KIND)
        self.assertGreater(Hand("33332"), Hand("2AAAA"))
        self.assertLess(Hand("2AAAA"), Hand("33332"))

    def test_stronger_type_wins_regardless_of_cards(self):
        self.assertGreater(Hand("22333"), Hand("AAAKQ"))  # full house > three of a kind

    def test_tie_broken_at_later_card(self):
        self.assertLess(Hand("77788"), Hand("77888"))  # full house, 3rd card 7 < 8

    def test_identical_hands_equal(self):
        self.assertEqual(Hand("KK677"), Hand("KK677"))

    def test_sample_sort_order(self):
        hands = [Hand(s) for s in ["32T3K", "T55J5", "KK677", "KTJJT", "QQQJA"]]
        self.assertEqual([repr(h) for h in sorted(hands)],
                         ["32T3K", "KTJJT", "KK677", "T55J5", "QQQJA"])

    def test_invalid_hands_raise(self):
        for bad in ["1234", "2345X", "AAAAAA"]:
            with self.assertRaises(ValueError):
                Hand(bad)


class TestGamePlay(unittest.TestCase):
    """Spec: 1 if a is stronger, -1 if b is stronger, 0 if tied."""

    def play(self, a: str, b: str) -> int:
        return Game(Hand(a), Hand(b)).play()

    def test_given_case(self):
        self.assertEqual(self.play("33332", "2AAAA"), 1)

    def test_a_stronger_type(self):
        self.assertEqual(self.play("AAAAA", "AA8AA"), 1)

    def test_b_stronger_type(self):
        self.assertEqual(self.play("23456", "A23A4"), -1)

    def test_b_wins_tie_break(self):
        self.assertEqual(self.play("77788", "77888"), -1)

    def test_tie(self):
        self.assertEqual(self.play("KK677", "KK677"), 0)


def _brute_force_best_and_worst(labels: str):
    """Reference answer: try all 13^k fills and keep max/min by Hand's ordering."""
    unknown = [i for i, c in enumerate(labels) if c == "?"]
    best = worst = None
    for fill in product(_LABELS, repeat=len(unknown)):
        chars = list(labels)
        for pos, label in zip(unknown, fill):
            chars[pos] = label
        hand = Hand("".join(chars))
        if best is None or hand > best:
            best = hand
        if worst is None or hand < worst:
            worst = hand
    return repr(best), repr(worst)


class TestBestAndWorst(unittest.TestCase):
    def test_known_cases(self):
        cases = {
            "AAAA?": ("AAAAA", "AAAA2"),  # given example
            "?AAAA": ("AAAAA", "2AAAA"),  # position of ? matters for the tie-break
            "2??45": ("25545", "23645"),  # worst avoids making a pair with 2, 4, 5
            "22??3": ("22223", "22453"),  # best joins the largest group, not "AA"
            "QK??2": ("QKKK2", "QK342"),  # frequency tie -> higher rank (K over Q and 2)
            "A??A2": ("AAAA2", "A34A2"),  # worst skips labels already in the hand
            "?????": ("AAAAA", "23456"),  # no known cards -> A for best
            "KK677": ("KK677", "KK677"),  # no ? -> the hand itself
        }
        for labels, expected in cases.items():
            with self.subTest(labels=labels):
                self.assertEqual(best_and_worst_hands(labels), expected)

    def test_matches_brute_force(self):
        # Every hand over 'AK23?' with up to 3 '?': covers ties, repeats, and ? at every position.
        for t in product("AK23?", repeat=5):
            labels = "".join(t)
            if labels.count("?") > 3:
                continue
            with self.subTest(labels=labels):
                self.assertEqual(best_and_worst_hands(labels),
                                 _brute_force_best_and_worst(labels))

    def test_invalid_input_raises(self):
        for bad in ["AAAA", "AAAAAA", "AAAAX", "??1??"]:
            with self.subTest(labels=bad), self.assertRaises(ValueError):
                best_and_worst_hands(bad)


if __name__ == "__main__":
    unittest.main()

import json
import unittest

from Rippling.Logger.logger import run


class TestRun(unittest.TestCase):
    def test_given_example(self):
        data = {"handlers": [{"type": "filter", "remove": "l"}, {"type": "truncation", "length": 5},
                             {"type": "uppercase"}, {"type": "array"}],
                "messages": ["hello world"]}
        expected = '{"printed":["heo word","hello","HELLO WORLD"],"arrays":[["hello world"]]}'
        self.assertEqual(json.dumps(run(data), separators=(",", ":")), expected)

    def test_remove_is_single_non_overlapping_pass(self):
        data = {"handlers": [{"type": "filter", "remove": "aba"}], "messages": ["ababa"]}
        self.assertEqual(run(data)["printed"], ["ba"])

    def test_empty_results_are_printed(self):
        data = {"handlers": [{"type": "truncation", "length": 0}, {"type": "filter", "remove": "hi"}],
                "messages": ["hi"]}
        self.assertEqual(run(data)["printed"], ["", ""])

    def test_truncate_longer_than_message_keeps_all(self):
        data = {"handlers": [{"type": "truncation", "length": 100}], "messages": ["short"]}
        self.assertEqual(run(data)["printed"], ["short"])

    def test_handlers_get_original_message_in_order(self):
        data = {"handlers": [{"type": "uppercase"}, {"type": "filter", "remove": "a"}], "messages": ["abc", "aa"]}
        self.assertEqual(run(data)["printed"], ["ABC", "bc", "AA", ""])

    def test_store_keeps_duplicates_and_prints_nothing(self):
        data = {"handlers": [{"type": "array"}], "messages": ["a", "a"]}
        self.assertEqual(run(data), {"printed": [], "arrays": [["a", "a"]]})

    def test_search(self):
        data = {"handlers": [{"type": "array"}], "messages": ["ababa", "Hi, Bob"],
                "queries": ["ob", "", "bob", ".*", "i, B"]}
        self.assertEqual(run(data)["search_results"],
                         [["Hi, Bob"], ["ababa", "Hi, Bob"], [], [], ["Hi, Bob"]])

    def test_no_queries_key_means_no_search_results(self):
        data = {"handlers": [{"type": "array"}], "messages": ["x"]}
        self.assertNotIn("search_results", run(data))

    def test_unknown_type_raises(self):
        with self.assertRaises(ValueError):
            run({"handlers": [{"type": "bogus"}], "messages": []})


if __name__ == "__main__":
    unittest.main()

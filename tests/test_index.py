import unittest

from libs.fm_index import FMIndex


class TestFMIndex(unittest.TestCase):
    def test_index_simple(self):
        text = "I am happy buzzing bug"
        index = FMIndex(text)

        self.assertEqual(
            list(index.query("happy")), [(5, 10)]
        )
        self.assertEqual(
            list(index.query("am")), [(2, 4)]
        )
        self.assertEqual(
            list(index.query("cat")), []
        )

    def test_index_multiple(self):
        text = (
            "Once upon a time, in a quiet village, there was a small shop. "
            "This shop was known for its warm atmosphere and friendly owner. "
            "People from the village would gather at the shop, sharing stories and laughter. "
            "The shop became a beloved part of the community, a place where everyone felt welcome."
        )
        index = FMIndex(text)

        self.assertEqual(
            set(index.query("shop")), {(210, 214), (67, 71), (170, 174), (56, 60)}
        )
        self.assertEqual(
            set(index.query("village")), {(142, 149), (29, 36)}
        )
        self.assertEqual(
            set(index.query("welcome")), {(283, 290)}
        )


if __name__ == "__main__":
    unittest.main()

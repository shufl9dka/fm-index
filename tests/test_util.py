import unittest

import util.string as util_string


def stupid_suffix_array(s):
    return sorted(range(len(s)), key=lambda i: s[i:])


def stupid_lexicographic_count_less(s, char):
    return sum(map(lambda c: c < char, s))


class TestUtils(unittest.TestCase):
    def test_suffix_array(self):
        cases = [
            "banana$",
            "mississippi$",
            [80016, 4561, 1 << 21, 4561, 80016, 80016, 4561, 1 << 21, 41],
        ]

        for case in cases:
            self.assertEqual(
                util_string.suffix_array(case), stupid_suffix_array(case)
            )

    def test_bwt(self):
        self.assertEqual(
            util_string.bwt("banana$"),
            "annb$aa"
        )

        self.assertEqual(
            util_string.bwt([80016, 4561, 1 << 21, 4561, 80016, 80016, 4561, 1 << 21, 41]),
            [1 << 21, 1 << 21, 80016, 80016, 80016, 41, 4561, 4561, 4561]
        )

    def test_lexicographic_cnt_less(self):
        cases = [
            "xabacafad",
            "mississippi$",
            [80016, 4561, 1 << 21, 4561, 80016, 80016, 4561, 1 << 21, 41],
        ]

        for case in cases:
            cnt = util_string.lexicographic_cnt_less(case)
            for char in set(list(case)):
                true_cnt = stupid_lexicographic_count_less(case, char)
                self.assertEqual(cnt[char], true_cnt)

    def test_occurance_table(self):
        occ = util_string.OccuranceTable("xabacafad")
        self.assertEqual(occ.count("a", 4), 2)
        self.assertEqual(occ.count("a", 3), 1)
        self.assertEqual(occ.count("f", 4), 0)
        self.assertEqual(occ.count("f", 8), 1)


if __name__ == "__main__":
    unittest.main()

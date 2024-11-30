import bisect

from collections import Counter
from typing import SupportsIndex


def make_ranking(s: SupportsIndex) -> list[int]:
    mapping = {}
    x = sorted(list(s))

    for c in x:
        if c not in mapping:
            mapping[c] = len(mapping) + 1

    return [mapping[c] for c in s]


def suffix_array(s: SupportsIndex) -> list[int]:
    n = len(s)
    rank = make_ranking(s) + [0] * n
    result = list(range(n))
    tmp_rank = [0] * n

    k = 1
    while k < n:
        rank_pairs = [(rank[i], rank[i + k], i) for i in result]
        max_rank_k = max(rp[1] for rp in rank_pairs) + 1

        count = [0] * max_rank_k
        for _, rk, _ in rank_pairs:
            count[rk] += 1

        for i in range(1, max_rank_k):
            count[i] += count[i - 1]

        new_rp = [0] * n
        for rp in reversed(rank_pairs):
            idx = rp[1]
            count[idx] -= 1
            new_rp[count[idx]] = rp

        rank_pairs = new_rp
        max_rank_i = max(rp[0] for rp in rank_pairs) + 1
        count = [0] * max_rank_i

        for rp in rank_pairs:
            count[rp[0]] += 1

        for i in range(1, len(count)):
            count[i] += count[i - 1]

        new_rp = [0] * n
        for rp in reversed(rank_pairs):
            idx = rp[0]
            count[idx] -= 1
            new_rp[count[idx]] = rp
        rank_pairs = new_rp

        result = [rp[2] for rp in rank_pairs]
        tmp_rank[result[0]] = 1

        for i in range(1, n):
            prev_rank = (rank_pairs[i - 1][0], rank_pairs[i - 1][1])
            curr_rank = (rank_pairs[i][0], rank_pairs[i][1])
            tmp_rank[result[i]] = tmp_rank[result[i - 1]] + (prev_rank != curr_rank)
        rank[:n] = tmp_rank
        k <<= 1

    return result


def bwt(s: SupportsIndex, suff: list[int] = None):
    if suff is None:
        suff = suffix_array(s)

    result = [s[i - 1] for i in suff]
    if isinstance(s, str):
        result = ''.join(result)

    return result


def lexicographic_cnt_less(s: SupportsIndex):
    counts = Counter(s)
    result = {}

    total = 0
    for char in sorted(counts):
        result[char] = total
        total += counts[char]

    return result


# could be designed in a more time-efficient way
class OccuranceTable:
    def __init__(self, s: SupportsIndex):
        self.poses = {}
        for i, char in enumerate(s):
            self.poses.setdefault(char, []).append(i)

    def count(self, char, upto: int, *, exclude_upto: bool = True) -> int:
        if char not in self.poses:
            return 0
        return bisect.bisect_right(self.poses[char], upto - int(exclude_upto))

from typing import SupportsIndex

import util.string as util_string


class FMIndex:
    def __init__(self, text: SupportsIndex):
        self._text = text

        self._suff = util_string.suffix_array(text)
        self._bwt = util_string.bwt(text, self._suff)
        self._lx_less_cnt = util_string.lexicographic_cnt_less(self._bwt)
        self._occ = util_string.OccuranceTable(self._bwt)

    def search(self, pattern: SupportsIndex) -> tuple[int, int]:
        start = 0
        end = len(self._bwt) - 1

        for char in reversed(pattern):
            if char not in self._lx_less_cnt:
                return -1, -2

            start = self._lx_less_cnt[char] + self._occ.count(char, start)
            end = self._lx_less_cnt[char] + self._occ.count(char, end + 1) - 1
            if start > end:
                return -1, -2

        return start, end

    def generate_results(self, start: int, end: int, *, n: int, limit: int = -1):
        for i in range(max(start, 0), end + 1):
            if limit == 0:
                break
            limit = max(-1, limit - 1)
            yield (self._suff[i], self._suff[i] + n)

    def query(self, pattern: SupportsIndex):
        start, end = self.search(pattern)
        return self.generate_results(start, end, n=len(pattern))

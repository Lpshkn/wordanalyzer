"""
This module provides the class for splitting a text without spaces. You need just create instance of that class
and call the split function.
"""
from math import log


class TextSplitter:
    def __init__(self, words: list):
        # Build a cost dictionary, assuming Zipf's law
        self.word_cost = dict((word, log((number + 1) * log(len(words)))) for number, word in enumerate(words))
        self.max_len = max(len(x) for x in words)

    def split(self, text):
        # Find the best match for the i first characters, assuming cost has
        # been built for the i-1 first characters.
        # Returns a pair (match_cost, match_length).
        def best_match(index):
            candidates = enumerate(reversed(cost[max(0, index - self.max_len):index]))
            costs = list(((match_cost + self.word_cost.get(text[index - match_length - 1:index].lower(), 9e999),
                           match_length + 1) for match_length, match_cost in candidates))

            return min(costs)

        # Build the cost array.
        cost = [0]
        for i in range(1, len(text) + 1):
            match_cost, match_length = best_match(i)
            cost.append(match_cost)

        # Backtrack to recover the minimal-cost string.
        out = []
        i = len(text)
        while i > 0:
            match_cost, match_length = best_match(i)
            assert match_cost == cost[i]

            out.append(text[i - match_length:i])

            i -= match_length
        return list(reversed(out))

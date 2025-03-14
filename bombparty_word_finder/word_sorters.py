# BombParty Word Finder
# Copyright (C) 2025 BleenEye
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.


import numpy as np
from numpy.typing import NDArray
from .word_use_counts import WORD_COMMONALITIES


USE_COUNTS_FILE = 'word_use_counts.txt'
#with open(USE_COUNTS_FILE) as f:
#    WORD_COMMONALITIES = {line.split(' ')[0]: line.split(' ')[1].strip() for line in f.readlines()}


class BaseSorter(object):
    """#### Base class for all word sorters"""

    id = None

    @classmethod
    def sorter_ids(cls) -> list[tuple[int, str]]:
        ids = []
        for subclass in cls.__subclasses__():
            ids.append((subclass.id, subclass.__name__))
        return ids

    def sort(self, words: NDArray) -> NDArray:
        raise NotImplementedError("BaseSorter is an abstract class, not meant to be instantiated")


class NullSorter(BaseSorter):
    """#### Does not sort words

    Words are returned in the same order as the sorter received them in (alphabetical).
    """

    id = 'n'

    def sort(self, words: NDArray) -> NDArray:
        return words


class RandomSorter(BaseSorter):
    """#### Sorts words randomly

    Words are shuffled without any weighting.
    """

    id = 'r'

    def sort(self, words: NDArray) -> NDArray:
        if words.size <= 1:
            return words
        np.random.shuffle(words)
        return words


class CommonSorter(BaseSorter):
    """#### Sorts words deterministicly by use counts
    
    * Words are ordered by how many times they were used, according to the use counts file.
    * Words with the same use count are sorted in the same order as the sorter received them (alphabetical).
    * Words which do not appear in the use counts file are sorted randomly and after all words that do.
    """

    id = 'c'

    def sort(self, words: NDArray) -> NDArray:
        if words.size <= 1:
            return words
        use_count = np.random.choice(np.arange(start=-1 * words.size, stop=0), size=words.size, replace=False)
        for index, word in enumerate(words):
            try:
                use_count[index] = WORD_COMMONALITIES[word]
            except KeyError:
                continue
        return words[np.argsort(use_count)][::-1]


class RouletteSorter(BaseSorter):
    """#### Sorts words randomly by use counts
    
    * Words are randomly selected with probability based on their use count until all words have been selected.
    * At each selection, the probability of a word being selected is given by:
        * `P = <word_use_count> / <total_use_count_of_all_unselected_words>`
    * Words which do not appear in the use counts file are assigned a use count of 1.
    """

    id = 'u'

    def sort(self, words: NDArray) -> NDArray:
        if words.size <= 1:
            return words
        use_count = np.full(words.size, 1)
        for index, word in enumerate(words):
            try:
                use_count[index] = WORD_COMMONALITIES[word]
            except KeyError:
                continue
        normal_use_count = use_count / np.sum(use_count)
        return words[np.random.choice(words.size, size=len(words,), p=normal_use_count, replace=False)]


def make_sorter(id: str | None = None) -> BaseSorter | None:
    """Return an instance of a subclass of `BaseSorter` which matches the given id.

    Return `None` and print a warning if id does not match any `BaseSorter` subclasses.
    """

    if id == None:
        return None
    sorter = None
    for subclass in BaseSorter.__subclasses__():
        if id == subclass.id:
            sorter = subclass()
            break
    else:
        print(f"WARNING: '{id}' is not a valid word sorter id\nValid ids are:", flush=True)
        for sorter_id, sorter_name in BaseSorter.sorter_ids():
            print(f"    '{sorter_id}' : {sorter_name}", flush=True)
        return None
    print(f"Using {sorter.__class__.__name__}", flush=True)
    return sorter


sorter_ids = set()
for sorter_id, sorter_name in BaseSorter.sorter_ids():
    if sorter_id in sorter_ids:
        raise ValueError(f"id of {sorter_name} conflicts with another sorter's id")
    sorter_ids.add(sorter_id)


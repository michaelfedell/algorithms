"""
On a 4x4 board, find words that can be formed by a sequence of adjacent (top, bottom, left, right, diagonal) letters.
Words must be 3 or more letters.
You may move to any of 8 adjacent letters, however, a word should not have multiple instances of the same cell.
To check if a string is a valid word you may implement a naive dictionary solution for simplicity.
"""
from collections import defaultdict, deque
import typing as t
import time


class Grid:
    def __init__(self, rows: list):
        # Keep dimensions of grid and then flatten letter array
        self.R = len(rows)
        self.C = len(rows[0])
        self.letters = []
        self.dictionary = set()  # will set the available dictionary of words later
        self.graph = defaultdict(list)  # key for each letter index with list of neighbors as value

        for r, row in enumerate(rows):
            for c, letter in enumerate(row):
                i = r * self.R + c  # convert row,column to flat index
                self.letters.append(letter)  # add cell contents to flattened list
                neighbors = [x * self.R + y for x in range(r - 1, r + 2)  # adjacent rows
                             for y in range(c - 1, c + 2)  # adjacent columns
                             if 0 <= x < self.R  # avoid x-boundary
                             and 0 <= y < self.C]  # avoid y-boundary
                self.graph[i] = [c for c in neighbors if c != i]  # omit self from neighbors

    def full_search(self, start: int):
        i = 0
        paths = deque([[start]])
        found_words = set()
        while paths:
            path = paths.popleft()
            new_words, next_paths = self.search(path)
            found_words = found_words.union(new_words)
            paths.extend(next_paths)
            i += 1
            # if i > 999999: return found_words
        return found_words

    def search(self, path: t.List[int]):
        # print(f'starting with {word}')
        # get all possible neighbor indices (unused in current word)
        neighbors = [l for l in self.graph[path[-1]] if l not in path]

        # construct all candidate paths
        candidates = [path + [l] for l in neighbors]

        if len(path) < 2:
            # candidate_words must be 3 characters or longer
            return [], candidates
        else:
            # translate index paths to corresponding letter sequences
            candidate_words = [''.join([self.letters[i] for i in cand_path]) for cand_path in candidates]
        # print(' | '.join(candidate_words))

        return self.dictionary.intersection(candidate_words), candidates

    def set_dict(self, dictionary: set):
        self.dictionary = dictionary


if __name__ == '__main__':
    start_time = time.time()

    # initialize sample grid
    ROWS = [
        ['r', 'a', 'e', 'l'],
        ['m', 'o', 'f', 's'],
        ['t', 'e', 'o', 'k'],
        ['n', 'a', 't', 'i'],
    ]
    N_CELLS = len([l for row in ROWS for l in row])  # max word length
    ROWS = [[l.lower() for l in row] for row in ROWS]  # ensure lowercase for word-matching

    # read in sample dictionary - taken from https://www.mit.edu/~ecprice/wordlist.10000
    with open('../data/english_words.txt') as f:
        word_dictionary = f.read().splitlines()
    word_dictionary = set(word_dictionary)  # ensure no duplicate words passed in dict

    alpha = set(l for row in ROWS for l in row)  # get unique letters in grid
    filtered_dictionary = set()  # keep track of words after filtering for available chars
    for word in word_dictionary:
        if set(word).difference(alpha) or len(word) > N_CELLS:
            continue  # skip words which are not subset of available alphabet or longer than grid
        filtered_dictionary.add(word)

    print('Available Letters:', alpha)
    print(f'Filtered Dictionary has {len(filtered_dictionary)} words')

    grid = Grid(ROWS)
    grid.set_dict(filtered_dictionary)

    # Examine grid construction
    print(grid.graph[0])
    print(grid.graph[3])
    print(grid.graph[5])
    print(grid.search([0, 5]))

    all_words = set()
    # Perform a full search starting from each of the cells in the grid
    for i in range(N_CELLS):
        all_words = all_words.union(grid.full_search(i))
        assert(all_words.issubset(filtered_dictionary))

    print(f'Took {time.time() - start_time} to build dictionary and find {len(all_words)} words in grid')
    all_words = list(all_words)
    print_words = all_words if len(all_words) < 20 else all_words[:20]
    print('\n\n', print_words)

    with open('../data/brute_extracted_words.txt', 'w') as f:
        f.writelines([w + '\n' for w in all_words])

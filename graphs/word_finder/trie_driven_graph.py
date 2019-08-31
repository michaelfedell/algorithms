"""
Prompt:

On a 4x4 board, find words that can be formed by a sequence of adjacent (top, bottom, left, right, diagonal) letters.
Words must be 3 or more letters.
You may move to any of 8 adjacent letters, however, a word should not have multiple instances of the same cell.
To check if a string is a valid word you may implement a naive dictionary solution for simplicity.
"""
from collections import defaultdict, deque
import typing as t
import time


class TrieNode(object):
    """Nodes use a list of pointers which point to other nodes if path continues."""
    def __init__(self, n_alpha: int):
        """
        Create a new empty node for Trie (null pointers for letters in alphabet)

        Args:
            n_alpha: Number of letters in available alphabet

        """
        # will have a key for each potential next letter
        self.children: t.List[t.Union[None, TrieNode]] = [None] * n_alpha
        self.isWord = False  # indicates if the path to this node represents a valid word


class Trie(object):
    """
    Trie is a search tree built for quick lookups of words and prefixes.

    References:
        https://en.wikipedia.org/wiki/Trie

    """
    def __init__(self, alphabet: t.Dict[str, int]):
        """
        Create the Trie with available alphabet.

        Alphabet is passed to limit the size of the Trie. Size in memory is dependent on length of longest
        word in tree (m), and size of alphabet (n); thus O(m*n).

        Searching for words is very fast as an O(1) lookup is made to check for valid child for each
        character in search key; thus total search time is O(m) for word of length m (unless early stop).

        Inserts are equivalent to searches but instead of terminating when no child is available for a
        sought letter, a new node is created for that letter and traversal continues; O(m) insert speed

        Args:
            alphabet: alphabet should map the potential characters in the available alphabet to their
                      respective index for efficient lookup

        """
        self.alphabet = alphabet
        self.n_alpha = len(alphabet)
        self.root = TrieNode(self.n_alpha)

    def insert(self, new_word: str):
        """
        Insert a new word into the Trie. May be subset or superset of existing words or completely new.

        Args:
            new_word: full word to insert in the Trie. Will add between 0 and m nodes for word of length m

        Raises:
            ValueError: if word contains letters which are not part of available alphabet.

        """
        node = self.root  # current node in trie
        for level in range(len(new_word)):  # traverse word one char at a time
            char = self.alphabet.get(new_word[level])  # get index for particular char
            if char is None:
                raise ValueError(f'Character {new_word[level]} is not in available alphabet')
            if not node.children[char]:
                # add a node for this char if not already present at this level
                node.children[char] = TrieNode(self.n_alpha)
            node = node.children[char]  # move to the proper node in trie's next level
        node.isWord = True  # mark that this node terminates a valid word

    def search(self, key: str) -> t.Tuple[bool, bool]:
        """
        Search the Trie to determine if a key is a valid word or the prefix of some valid word.

        Args:
            key: prefix to search for (may be full word or substring)

        Raises:
            ValueError: if word contains letters which are not part of available alphabet.

        Returns:
            key is valid word, key is prefix to other valid words

        """
        if not set(key).issubset(self.alphabet):
            raise ValueError(f'{key} contains characters which are not in available alphabet')
        node = self.root  # current node in trie
        for level in range(len(key)):  # traverse word one char at a time
            char = self.alphabet.get(key[level])  # get index for particular char
            if not node.children[char]:
                return False, False  # branch dies before end of key
            node = node.children[char]  # move to the proper node in trie's next level
        # Interested in whether the searched key is a word itself AND if it has any children
        return node is not None and node.isWord, any(node.children)


class Grid:
    """Stores an arbitrary arrangement of letters in a 4x4 grid in a Graph with edges between adjacent cells."""
    def __init__(self, rows: t.List[t.List[str]], dictionary: Trie):
        """
        Initializes the Grid with dimensions, flattened contents, graph structure and dictionary trie.

        Args:
            rows: letters arranged in columns and rows
            dictionary: word dictionary constructed in a Trie data structure for fast prefix-search

        """
        # Keep dimensions of grid and then flatten letter array
        self.R = len(rows)
        self.C = len(rows[0])
        self.letters = []
        self.dictionary = dictionary
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

    def full_search(self, start: int) -> set:
        """
        Search all possible paths from starting cell, terminating paths which are not valid words or prefixes.

        Args:
            start: index of starting cell in flattened letter array

        Returns:
            set of valid words found when starting from this cell

        """
        paths = deque([[start]])  # initialize deque with starting path
        found_words = set()
        while paths:
            path = paths.popleft()  # take new path to search from top of deque
            # check for valid words and prefixes among this paths immediate neighbors
            new_words, next_paths = self.search(path)
            found_words = found_words.union(new_words)  # collect unique new words
            paths.extend(next_paths)  # add new paths to the back of deque for later searching
        return found_words

    def search(self, path: t.List[int]):
        # get all possible neighbor indices (unused in current word)
        neighbors = [l for l in self.graph[path[-1]] if l not in path]

        # construct all candidate paths
        candidates = [path + [l] for l in neighbors]

        if len(path) < 2:
            # candidate_words must be 3 characters or longer
            return [], candidates

        # translate index paths to corresponding letter sequences
        candidate_words = [''.join([self.letters[i] for i in candidate]) for candidate in candidates]

        # Check all candidate words for validity as words or prefixes
        valid = [self.dictionary.search(cw) for cw in candidate_words]
        valid_words, valid_candidates = list(zip(*valid))

        # Collect valid words and valid prefixes for further searching
        good_words = [w for i, w in enumerate(candidate_words) if valid_words[i]]
        good_candidates = [w for i, w in enumerate(candidates) if valid_candidates[i]]

        return good_words, good_candidates


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
    alpha_dict = {l: i for i, l in enumerate(alpha)}  # convert unique letters to lookup map

    word_trie = Trie(alpha_dict)  # pass alpha_dict to Trie so as to not waste space with unavailable chars
    filtered_dictionary = set()  # keep track of words after filtering for available chars
    for word in word_dictionary:
        if set(word).difference(alpha) or len(word) > N_CELLS:
            continue  # skip words which are not subset of available alphabet or longer than grid
        filtered_dictionary.add(word)
        word_trie.insert(word)

    print('Available Letters:', alpha)
    print(f'Filtered Dictionary has {len(filtered_dictionary)} words')

    grid = Grid(ROWS, word_trie)

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

    with open('../data/extracted_words.txt', 'w') as f:
        f.writelines([w + '\n' for w in all_words])

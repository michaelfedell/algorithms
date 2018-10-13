"""
my_sort is a custom implementation of python's built-in sorted() function.

my_sort operates exactly the same as the base version, accepts an iterable as
input to be sorted, an optional key by which to perform sorting, and a
reversed flag to control direction of sort. Within my_sort, both bubble_sort()
and merge_sort() implementations are available
"""

import time
import logging

# Logger used to debug function internals
LOGGER = logging.getLogger(__name__)
# Limit the messages created by logger according to severity
LOGGER.setLevel(logging.WARN)
ch = logging.StreamHandler()
# Display all log messages created
ch.setLevel(logging.DEBUG)
LOGGER.addHandler(ch)


def bubble_sort(x, *, key=None, reverse=False):
    """
    Sort an iterable object using the bubble sort algorithm.

    Bubble sort operates by comparing adjacent elements in a collection and
    swapping them if needed. While stable, and relatively performant for small
    or mostly-sorted lists, the number of operations required greatly increases
    with list size. This makes bubble sort one of the least efficient sorting
    algorithms.

    For a list of size n, n-1 passes over the list must be performed, making
    a total of (1/2)*n^2 + (1/2)*n comparisons. Number of exchanges will vary
    based on initial arrangement of list.

    Args:
        x (iterable): Iterable collection (list, tuple, str, etc) to be sorted.
        key (function, optional): Defaults to None. Function to be called on
            each element of iterable. Sort will be performed on the return of
            that function. (Should take one parameter and return one value).
        reversed (bool, optional): Defaults to False. Sorts list in descending
            order if True, ascending order otherwise.

    Returns:
        dict: representation of results
            sorted: sorted version of original iterable
            compares: the total number of comparisons made during sort
            swaps: the total number of element swaps made
            time: the time required to perform sort (in nanoseconds)

    Examples:
        print(merge_sort([5,2,4,1,3]))
        >>> {'sorted': [1, 2, 3, 4, 5], 'compares': 10, 'swaps': 7, 'time': 5.3882598876953125e-05}

    """
    num_compares = 0
    num_swaps = 0

    sx = [*x]

    if not key:
        key = lambda x: x

    LOGGER.info('Unsorted list: %s', sx)

    start = time.time()  # record start time to compute runtime

    # len(x) - 1 loops required to fully sort list
    for loop in range(len(sx) - 1, 0, -1):
        LOGGER.debug('loops remaining: %s', loop)
        # the loop number (decreasing) also defines the number
        # of elements to compare during each loop
        for i in range(loop):
            num_compares += 1
            if key(sx[i]) > key(sx[i+1]):  # current element greater than next
                LOGGER.debug('Swapping %s with %s', sx[i], sx[i+1])
                num_swaps += 1
                sx[i], sx[i+1] = sx[i+1], sx[i]  # swap current with next
            LOGGER.debug(sx)
    LOGGER.info('Sorted List: %s', sx)

    if reverse:
        sx = sx[::-1]

    end = time.time()
    return {
        'sorted': sx,
        'compares': num_compares,
        'swaps': num_swaps,
        'time': (end - start)
    }


def merge_sort(x, *, key=None, reverse=False):
    """
    Sort an iterable object using the merge sort algorithm.

    Merge sort is a recursive algorithm that splits an iterable in half and
    then calls itself on each half until only one element remains. It then
    rebuilds the iterable by merging each fragment back together by making
    one-to-one comparisons. Merge sort is much more performant than bubble
    sort, but still not perfectly optimized.

    Args:
        x (iterable): Iterable collection (list, tuple, str, etc) to be sorted.
        key (function, optional): Defaults to None. Function to be called on
            each element of iterable. Sort will be performed on the return of
            that function. (Should take one parameter and return one value).
        reversed (bool, optional): Defaults to False. Sorts list in descending
            order if True, ascending order otherwise.

    Returns:
        dict: representation of results
            sorted: sorted version of original iterable
            compares: the total number of comparisons made during sort
            swaps: the total number of element swaps made
            time: the time required to perform sort (in nanoseconds)

    Examples:
        print(merge_sort([5,2,4,1,3]))
        >>> {'sorted': [1, 2, 3, 4, 5], 'compares': 8, 'merges': 9, 'time': 6.198883056640625e-05}

    """
    start = time.time()

    # raises TypeError if user tries to sort a non-iterable object
    sx = [*x]

    # key allows user to sort the list based on some key function
    if not key:
        key = lambda x: x

    def sort(li, num_compares=0, num_merges=0):
        LOGGER.debug('Splitting %s', li)

        if len(li) > 1:
            mid = len(li) // 2
            left = li[:mid]
            right = li[mid:]
            left, num_compares, num_merges = sort(left, num_compares, num_merges)
            right, num_compares, num_merges = sort(right, num_compares, num_merges)

            i = j = k = 0

            while i < len(left) and j < len(right):
                num_compares += 1
                if key(left[i]) < key(right[j]):
                    li[k] = left[i]
                    i += 1
                else:
                    li[k] = right[j]
                    j += 1
                k += 1

            while i < len(left):
                li[k] = left[i]
                i += 1
                k += 1

            while j < len(right):
                li[k] = right[j]
                j += 1
                k += 1

        num_merges += 1
        LOGGER.debug('Merging %s', li)
        return (li, num_compares, num_merges)

    sx, num_compares, num_merges = sort(sx)

    if reverse:
        sx = sx[::-1]

    end = time.time()
    return {
        'sorted': sx,
        'compares': num_compares,
        'merges': num_merges,
        'time': (end - start)
    }


def time_base(x, *, key=None, reverse=False):
    """
    Wrapper around builtin sorted method to allow easy timing.

    Args:
        x (iterable): Iterable collection (list, tuple, str, etc) to be sorted.
        key (function, optional): Defaults to None. Function to be called on
            each element of iterable. Sort will be performed on the return of
            that function. (Should take one parameter and return one value).
        reversed (bool, optional): Defaults to False. Sorts list in descending
            order if True, ascending order otherwise.

    Returns:
        dict: representation of results
            sorted: sorted version of original iterable
            time: the time required to perform sort (in nanoseconds)

    """
    start = time.time()
    sx = sorted(x, key=key, reverse=reverse)
    end = time.time()

    return {
        'sorted': sx,
        'time': (end - start)
    }


if __name__ == '__main__':
    import random
    import string
    import matplotlib.pyplot as plt

    LETTERS = string.ascii_lowercase

    # Generate random iterables for testing
    int_list = [random.randrange(10) for _ in range(2500)]
    rand_str = ''.join(random.choice(LETTERS) for _ in range(2500))
    list_of_dicts = [{'num': random.randrange(10),
                      'chr': random.choice(LETTERS)} for _ in range(2500)]

    print('Sorting: one list of 2500 integers (reversed), one string of 2500 '
          'characters, and one list of dictionaries where the sort key '
          'function will access a specified element of the dict.')

    # The following tests compare performance of bubble_sort, merge_sort and
    # builtin sorted() methods across various types of random iterables
    bubble_int = bubble_sort(int_list, reverse=True)
    bubble_str = bubble_sort(rand_str)
    bubble_dicts = bubble_sort(list_of_dicts, key=lambda x: x['chr'])

    merge_int = merge_sort(int_list, reverse=True)
    merge_str = merge_sort(rand_str)
    merge_dicts = merge_sort(list_of_dicts, key=lambda x: x['chr'])

    base_int_time = time_base(int_list, reverse=True)['time']
    base_str_time = time_base(rand_str)['time']
    base_dicts_time = time_base(list_of_dicts, key=lambda x: x['chr'])['time']

    # Print results to console in ASCII table
    print('''\
+---------------+---------------+---------------+---------------+--------------+---------------+
|  Sort Method  |  int Time (s) |  str Time (s) | dict Time (s) |  # compares  | # swap/merges |
+===============+===============+===============+===============+==============+===============+
|  Bubble Sort  |{:>15.10}|{:>15.10}|{:>15.10}|{:>14}|{:>15}|
+---------------+---------------+---------------+---------------+--------------+---------------+
|  Merge Sort   |{:>15.10}|{:>15.10}|{:>15.10}|{:>14}|{:>15}|
+---------------+---------------+---------------+---------------+--------------+---------------+
|  Base Sort    |{:>15.8}|{:>15.8}|{:>15.8}|{:>14}|{:>15}|
+---------------+---------------+---------------+---------------+--------------+---------------+\
'''.format(
        bubble_int['time'], bubble_str['time'], bubble_dicts['time'], bubble_int['compares'], bubble_int['swaps'],
        merge_int['time'], merge_str['time'], merge_dicts['time'], merge_int['compares'], merge_int['merges'],
        base_int_time, base_str_time, base_dicts_time, '', ''
    ))

    # Now ready to test sort algorithms against lists of different sizes to
    # measure efficiency gains at scale

    # Generate increasingly large lists of random integers (1 ≤ size ≤ 2048)
    sizes = [2 ** p for p in range(12)]
    list_of_lists = [[random.randrange(1000) for _ in range(n)] for n in sizes]

    bubble_times = [bubble_sort(li)['time'] for li in list_of_lists]
    merge_times = [merge_sort(li)['time'] for li in list_of_lists]
    base_times = [time_base(li)['time'] for li in list_of_lists]

    plt.plot(sizes, bubble_times, label='Bubble Sort')
    plt.plot(sizes, merge_times, label='Merge Sort')
    plt.plot(sizes, base_times, label='Builtin Sorted')
    plt.title('Time to sort increasingly large lists of random integers')
    plt.xlabel('Elements in iterable')
    plt.ylabel('Time to sort (s)')
    plt.legend(loc='upper left')
    plt.show()

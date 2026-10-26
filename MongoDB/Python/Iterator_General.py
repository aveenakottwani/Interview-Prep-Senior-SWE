"""


Implement a UnionIterator class that takes two strictly sorted iterators and produces a new iterator with the following properties:

1. The new iterator contains the union of the elements from both input iterators. If an element appears in both inputs, it appears only once in the new iterator.
2. The elements in the new iterator are also strictly sorted.
3. Avoid using too much memory when the input iterators contain many elements.

Example 1
Iterator 1: 2, 4, 6, 8, 10
Iterator 2: 1, 2, 3, 5, 8, 13
Output: 1, 2, 3, 4, 5, 6, 8, 10, 13

Example 2
Iterator 1: apple, banana, orange, tree
Iterator 2: apple, tree, zoo
Output: apple, banana, orange, tree, zoo

Example 3
Iterator 1: -10, -9, -5, -1, 0, 2, 4
Iterator 2: -9, -5, -3, -2, 0, 1, 2
Output: -10, -9, -5, -3, -2, -1, 0, 1, 2, 4

Example 4
Iterator 1: 1, 2, 3
Iterator 2: (empty)
Output: 1, 2, 3

The input iterators follow this interface:
hasNext() returns true if the iteration has more elements.
next() returns the next element in the iteration (an int or a string).
UnionIterator should take the two iterators in its constructor and implement the same two methods, hasNext() and next().


"""
from typing import Iterator, Any
_DONE = object()          # unique "exhausted" marker

class UnionIterator:
    def __init__(self, iterator1, iterator2):
        self.it1 = iter(iterator1)     # safe: iter() on an iterator returns itself
        self.it2 = iter(iterator2)
        self.h1 = next(self.it1, _DONE)
        self.h2 = next(self.it2, _DONE)

    def hasNext(self) -> bool:
        return self.h1 is not _DONE or self.h2 is not _DONE

    def next(self):
        if not self.hasNext():
            raise StopIteration

        h1, h2 = self.h1, self.h2
        if h2 is _DONE or (h1 is not _DONE and h1 < h2):
            result = h1
            self.h1 = next(self.it1, _DONE)
        elif h1 is _DONE or h2 < h1:
            result = h2
            self.h2 = next(self.it2, _DONE)
        else:                                  # equal: emit once, advance both
            result = h1
            self.h1 = next(self.it1, _DONE)
            self.h2 = next(self.it2, _DONE)
        return result

    # makes it a real Python iterator
    def __iter__(self):
        return self

    def __next__(self):
        return self.next()
Iterator1=iter([ 2, 4, 6, 8, 10])
Iterator2= iter([1, 2, 3, 5, 8, 13])
output=[1, 2, 3, 4, 5, 6, 8, 10, 13]
ui=UnionIterator(Iterator1, Iterator2)
result=[]
result.append(ui.next())
result.append(ui.next())
result.append(ui.next())
result.append(ui.next())
result.append(ui.next())
result.append(ui.next())
result.append(ui.next())
result.append(ui.next())
result.append(ui.next())
print(result==output)
assert result == output


def run(a, b):
    return list(UnionIterator(iter(a), iter(b)))
print("start")
assert run([2,4,6,8,10], [1,2,3,5,8,13]) == [1,2,3,4,5,6,8,10,13]
assert run(["apple","banana","orange","tree"], ["apple","tree","zoo"]) \
       == ["apple","banana","orange","tree","zoo"]
assert run([], [1,2]) == [1,2]            # one empty
assert run([], []) == []                  # both empty
assert run([1,2,3], [1,2,3]) == [1,2,3]   # identical
assert run([1,2], [3,4]) == [1,2,3,4]     # no overlap
assert run([0,1], [0,2]) == [0,1,2]       # zero is a valid value
print("end")



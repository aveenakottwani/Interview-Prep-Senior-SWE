import bisect
import random


class Node:
    __slots__ = ("val", "prev", "next")

    def __init__(self, val: int = 0) -> None:
        self.val = val
        self.prev = self.next = None


class DLL:
    def __init__(self) -> None:
        self.head, self.tail = Node(), Node()
        self.head.next, self.tail.prev = self.tail, self.head

    def add_at_end(self, node: Node) -> None:
        last = self.tail.prev
        last.next, node.prev = node, last
        node.next, self.tail.prev = self.tail, node

    def remove(self, node: Node) -> None:
        node.prev.next, node.next.prev = node.next, node.prev

    def last(self) -> Node:
        return self.tail.prev


class TreeMap:
    def __init__(self) -> None:
        self.keys = []   # sorted list of unique values
        self.map = {}    # value -> list of Node (stack order, topmost last)

    def add(self, val: int, node: Node) -> None:
        if val not in self.map:
            bisect.insort(self.keys, val)
            self.map[val] = []
        self.map[val].append(node)

    def get_max(self):
        return self.keys[-1] if self.keys else None

    def pop_top_node(self, val: int) -> Node:
        """Remove and return the topmost node holding this value."""
        nodes = self.map[val]
        node = nodes.pop()
        if not nodes:
            del self.map[val]
            i = bisect.bisect_left(self.keys, val)
            del self.keys[i]
        return node

    def pop_max_node(self) -> Node:
        return self.pop_top_node(self.keys[-1])


class MaxStack:
    def __init__(self) -> None:
        self.tree = TreeMap()
        self.dll = DLL()
        self.size = 0

    def _check(self) -> None:
        if self.size == 0:
            raise IndexError("stack is empty")

    def push(self, x: int) -> None:
        node = Node(x)
        self.tree.add(x, node)
        self.dll.add_at_end(node)
        self.size += 1

    def pop(self) -> int:
        self._check()
        node = self.dll.last()
        self.tree.pop_top_node(node.val)   # also the last in its value list
        self.dll.remove(node)
        self.size -= 1
        return node.val

    def top(self) -> int:
        self._check()
        return self.dll.last().val

    def peekMax(self) -> int:
        self._check()
        return self.tree.get_max()

    def popMax(self) -> int:
        self._check()
        node = self.tree.pop_max_node()
        self.dll.remove(node)              # O(1) from the middle
        self.size -= 1
        return node.val


# ---------------- Tests ----------------

def test_basic():
    s = MaxStack()
    s.push(5); s.push(1); s.push(5)
    assert s.top() == 5
    assert s.popMax() == 5      # removes the TOP 5
    assert s.top() == 1
    assert s.peekMax() == 5
    assert s.pop() == 1
    assert s.top() == 5

def test_duplicates_order():
    s = MaxStack()
    for x in [3, 7, 3, 7, 2]:
        s.push(x)
    assert s.popMax() == 7      # the later 7
    assert s.popMax() == 7      # the earlier 7
    assert s.peekMax() == 3
    assert s.pop() == 2
    assert s.pop() == 3
    assert s.pop() == 3

def test_single_element():
    s = MaxStack()
    s.push(4)
    assert s.peekMax() == 4 and s.top() == 4
    assert s.popMax() == 4
    assert s.size == 0

def test_pop_then_peek_max():
    s = MaxStack()
    s.push(1); s.push(9)
    assert s.pop() == 9
    assert s.peekMax() == 1

def test_popmax_then_pop():
    s = MaxStack()
    s.push(1); s.push(9); s.push(2)
    assert s.popMax() == 9
    assert s.pop() == 2
    assert s.pop() == 1

def test_negatives_and_zero():
    s = MaxStack()
    for x in [-3, 0, -1]:
        s.push(x)
    assert s.peekMax() == 0
    assert s.popMax() == 0
    assert s.peekMax() == -1

def test_empty_raises():
    s = MaxStack()
    for op in (s.pop, s.top, s.peekMax, s.popMax):
        try:
            op()
            assert False, "expected IndexError"
        except IndexError:
            pass

def test_internal_invariants():
    s = MaxStack()
    for x in [2, 2, 5, 2]:
        s.push(x)
    s.popMax(); s.pop()
    assert s.tree.keys == sorted(s.tree.map)      # keys stay sorted and unique
    assert sum(len(v) for v in s.tree.map.values()) == s.size

class Slow:
    def __init__(self): self.s = []
    def push(self, x): self.s.append(x)
    def pop(self): return self.s.pop()
    def top(self): return self.s[-1]
    def peekMax(self): return max(self.s)
    def popMax(self):
        m = max(self.s)
        for i in range(len(self.s) - 1, -1, -1):
            if self.s[i] == m:
                return self.s.pop(i)

def test_random_vs_brute_force():
    for _ in range(3000):
        a, b, n = MaxStack(), Slow(), 0
        for _ in range(40):
            op = random.choice(["push", "pop", "top", "peekMax", "popMax"]) if n else "push"
            x = random.randint(-3, 5)         # small range forces duplicates
            if op == "push":
                a.push(x); b.push(x); n += 1
            else:
                assert getattr(a, op)() == getattr(b, op)(), op
                if op in ("pop", "popMax"):
                    n -= 1
            assert a.size == n

if __name__ == "__main__":
    test_basic()
    test_duplicates_order()
    test_single_element()
    test_pop_then_peek_max()
    test_popmax_then_pop()
    test_negatives_and_zero()
    test_empty_raises()
    test_internal_invariants()
    test_random_vs_brute_force()
    print("all tests passed")
from collections import OrderedDict


class LRUCache:
    """
    OrderedDict is already a hash map + doubly linked list, so no Node/LinkedList is needed.
    Convention: front (first) = least recently used, end (last) = most recently used.
    """

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache: OrderedDict[int, int] = OrderedDict()  # key -> value

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)  # O(1): mark as most recently used
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)  # existing key: refresh recency
        self.cache[key] = value  # new key is inserted at the end (MRU) automatically

        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)  # O(1): evict LRU from the front


if __name__ == "__main__":
    c = LRUCache(2)
    c.put(4, 4)
    c.put(5, 5)
    print(c.get(4))  # -> 4
    c.put(4, 6)      # updates 4 -> 6
    c.put(7, 7)      # evicts key 5
    print(c.get(5))  # -> -1
    print(c.get(4))  # -> 6
    print(c.get(7))  # -> 7

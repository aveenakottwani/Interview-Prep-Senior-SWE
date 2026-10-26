from sortedcontainers import SortedDict
class Node:
    def __init__(self, val: int) -> None:
        self.val = val
        self.next = None
        self.prev = None

class DLL:
    def __init__(self) -> None:
        self.head = Node(-1)
        self.tail = Node(-1)
        self.head.next=self.tail
        self.tail.prev=self.head

    def add_node_head(self, node: Node) -> Node:
        head_next=self.head.next
        self.head.next=node
        self.node.prev=self.head
        head_next.prev=node
        node.next=head_next

    def add_node_at_end(self, node: Node) -> Node:
        tail_prev=self.tail.prev
        tail_prev.next=node
        node.prev=tail_prev

        node.next=self.tail
        self.tail.prev=node


    def remove_node(self,node:Node):
        node_prev=node.prev
        node_next=node.next

        node_prev.next=node_next
        node_next.prev=node_prev

    def remove_from_end(self):
        tail_prev = self.tail.prev
        remove_node(tail_prev)
        return tail_prev

    def get_last_node(self) -> Node:
        return self.tail.prev



class MaxStack:

    def __init__(self):
        self.sorted_map=SortedDict() # value -> nodes
        self.root=DLL()
        top=None

    def push(self, x: int) -> None:
        node=Node(x)
        if x not in self.sorted_map:
            self.sorted_map[x]=[]
        self.sorted_map[x].append(node)
        self.root.add_node_at_end(node)


    def pop(self) -> int:
        node=self.root.remove_from_end()
        if node.val in self.sorted_map:
            self.sorted_map[node.val].pop()
        return node.val


    def top(self) -> int:
        node=self.root.get_last_node()
        return node.val


    def peekMax(self) -> int:
        key=self.sorted_map.peekitem(-1)
        node_list=self.sorted_map[key]
        return node_list[-1].val

    def popMax(self) -> int:
        key = self.sorted_map.peekitem(-1)
        node_list = self.sorted_map[key]
        removed_node=node_list.pop()
        self.root.remove_node(removed_node)
        return remove_node.val



import java.util.*;

class MaxStack {
    private static class Node {
        int val;
        Node prev, next;
        Node(int val) { this.val = val; }
    }

    private final Node head = new Node(0), tail = new Node(0);
    private final TreeMap<Integer, ArrayList<Node>> map = new TreeMap<>();
    private int size = 0;

    public MaxStack() {
        head.next = tail;
        tail.prev = head;
    }

    private void addAtEnd(Node n) {
        Node last = tail.prev;
        last.next = n;
        n.prev = last;
        n.next = tail;
        tail.prev = n;
    }

    private void unlink(Node n) {
        n.prev.next = n.next;
        n.next.prev = n.prev;
    }

    private void check() {
        if (size == 0) throw new NoSuchElementException("stack is empty");
    }

    // Removes a node from the map's list, the DLL, and the size count.
    private void drop(Node node) {
        ArrayList<Node> list = map.get(node.val);
        list.remove(list.size() - 1);          // topmost duplicate is last
        if (list.isEmpty()) map.remove(node.val);
        unlink(node);
        size--;
    }

    public void push(int x) {
        Node n = new Node(x);
        map.computeIfAbsent(x, k -> new ArrayList<>()).add(n);
        addAtEnd(n);
        size++;
    }

    public int pop() {
        check();
        Node n = tail.prev;
        drop(n);
        return n.val;
    }

    public int top() {
        check();
        return tail.prev.val;
    }

    public int peekMax() {
        check();
        return map.lastKey();
    }

    public int popMax() {
        check();
        ArrayList<Node> list = map.lastEntry().getValue();
        Node n = list.get(list.size() - 1);
        drop(n);
        return n.val;
    }

    public int size() { return size; }
}

public class Main {
    static void eq(int expected, int actual) {
        if (expected != actual)
            throw new AssertionError("expected " + expected + " but got " + actual);
    }

    // Brute force for comparison
    static class Slow {
        ArrayList<Integer> s = new ArrayList<>();
        void push(int x) { s.add(x); }
        int pop() { return s.remove(s.size() - 1); }
        int top() { return s.get(s.size() - 1); }
        int peekMax() { return Collections.max(s); }
        int popMax() {
            int m = Collections.max(s);
            for (int i = s.size() - 1; i >= 0; i--)
                if (s.get(i) == m) return s.remove(i);
            throw new IllegalStateException();
        }
    }

    public static void main(String[] args) {
        // Basic with duplicates
        MaxStack s = new MaxStack();
        s.push(5); s.push(1); s.push(5);
        eq(5, s.top());
        eq(5, s.popMax());        // removes the TOP 5
        eq(1, s.top());
        eq(5, s.peekMax());
        eq(1, s.pop());
        eq(5, s.top());

        // Duplicate order
        s = new MaxStack();
        for (int x : new int[]{3, 7, 3, 7, 2}) s.push(x);
        eq(7, s.popMax());
        eq(7, s.popMax());
        eq(3, s.peekMax());
        eq(2, s.pop());

        // Single element, negatives
        s = new MaxStack();
        s.push(-3); s.push(0); s.push(-1);
        eq(0, s.peekMax());
        eq(0, s.popMax());
        eq(-1, s.peekMax());

        // Empty stack throws
        try { new MaxStack().pop(); throw new AssertionError("no exception"); }
        catch (NoSuchElementException expected) { }

        // Random vs brute force
        Random r = new Random();
        for (int t = 0; t < 3000; t++) {
            MaxStack a = new MaxStack();
            Slow b = new Slow();
            int n = 0;
            for (int i = 0; i < 40; i++) {
                int op = n == 0 ? 0 : r.nextInt(5);
                int x = r.nextInt(9) - 3;       // small range forces duplicates
                switch (op) {
                    case 0: a.push(x); b.push(x); n++; break;
                    case 1: eq(b.pop(), a.pop()); n--; break;
                    case 2: eq(b.top(), a.top()); break;
                    case 3: eq(b.peekMax(), a.peekMax()); break;
                    default: eq(b.popMax(), a.popMax()); n--;
                }
                eq(n, a.size());
            }
        }
        System.out.println("all tests passed");
    }
}
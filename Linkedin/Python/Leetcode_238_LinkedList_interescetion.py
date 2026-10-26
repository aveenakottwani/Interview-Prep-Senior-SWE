"""
Given the heads of two singly linked lists, headA and headB, return the first node at which the two lists intersect. Return None if they do not intersect.

An intersection means that both lists share the same node objects from some node onward; equal values alone do not constitute an intersection. The lists are acyclic.

Requirements:

Do not modify either list.
Use O(m + n) time, where m and n are the list lengths.
Use O(1) extra space.
Example:

A: 4 → 1 → 8 → 4 → 5
B: 5 → 6 → 1 → 8 → 4 → 5
                 ↑
          intersection value: 8

Output: 8
For the following stdin representation:

Line 1: comma-separated values in A's exclusive prefix; an empty line means no exclusive prefix.
Line 2: comma-separated values in B's exclusive prefix; an empty line means no exclusive prefix.
Line 3: comma-separated values in the shared suffix; an empty line means the lists do not intersect.
Print the value of the intersection node, or -1 if there is no intersection. Node values are in [-10^4, 10^4], and the total number of nodes is at most 3 * 10^4.
"""
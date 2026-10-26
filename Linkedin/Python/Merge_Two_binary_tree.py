"""
Merge Two Binary Trees
Given two binary trees, root1 and root2, merge them into a new binary tree and return its root.

Merge rules:

If both trees have a node at the same position, the new node's value is the sum of their values.
If only one tree has a node at a position, keep that node, including its subtree.
If neither tree has a node at a position, that position is absent.
Input Format
The input contains two lines, each representing a binary tree in level-order traversal:

Node values are integers.
A missing node is denoted by null.
Tokens are separated by spaces.
A line containing only null represents an empty tree.
Output Format
Print the merged tree in level-order traversal, with tokens separated by spaces. Trailing null values do not need to be printed. Print null if the result is an empty tree.

Example 1
Input:

1 3 2 5
2 1 3 null 4 null 7
Output:

3 4 5 5 4 null 7
Constraints
Each tree contains between 0 and 10^4 nodes.
Node values are in [-10^4, 10^4].
"""
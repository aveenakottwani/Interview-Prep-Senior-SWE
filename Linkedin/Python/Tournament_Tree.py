"""
Tournament Tree problem:
Given a Tournament Tree (a special binary tree where the value of each non-leaf node equals the smaller value of its two children), find the second smallest value in the entire tree (Second Minimum).

Requirements and further inquiries:
1. The algorithm's time complexity should be better than O(N), aiming for O(log N).
2. Explain and utilize the property of the tournament tree: the second smallest value must be among the nodes that were directly compared with the root node (the global minimum).

First Question (Smoke Test):
Implement a function to determine if a given string represents a valid number:
function isNumber(toTest: string): boolean

Test cases include:
1. '234' -> true
2. '-455' -> true
3. '1e2' -> false
4. '12^2' -> false
5. '23.23' -> true
6. '2.2.4' -> false

https://leetcode.com/discuss/post/125110/linkedin-phone-screen-tournament-tree-pr-aqv9/
"""


"""
Nested List Weight Sum II
The second problem was a disguised (homophone) LeetCode problem. The interviewer did not understand this question at all. I explained the following transformation formula which achieves a one-pass DFS rather than two passes. Despite my thorough explanation, the interviewer could not grasp how it was derived... the skill level was really poor. He told me he didn't know much Python.

The formula:
sum(num * (maxDepth - (the depth of the integer) + 1))
= sum(num) * (maxDepth + 1) - sum(num * depth)

For both problems, I wrote optimal solutions, analyzed corner cases, and dry-run test cases. Yet, one week later, I was rejected. The name was recorded as plq.

"""
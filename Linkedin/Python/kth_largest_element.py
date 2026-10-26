"""
Given an integer array nums and an integer k, return the kth largest element in the array.

The kth largest element is determined by its position in sorted order; it is not the kth distinct element.

Input Format
First line: two integers n k
Second line: n integers representing nums
Output Format
Print one integer: the kth largest element.
Constraints
1 <= n <= 10^5
1 <= k <= n
-10^9 <= nums[i] <= 10^9
Example
Input:

6 2
3 2 1 5 6 4
Output:

5
Explanation: In descending order, the array is [6, 5, 4, 3, 2, 1], so the 2nd largest value is 5.
"""
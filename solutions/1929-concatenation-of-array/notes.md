---
difficulty: Easy
solved: true
review_after:
---

# 1929. Concatenation of Array

[Problem](https://leetcode.com/problems/concatenation-of-array/)

## Notes

Simple problem, basically just adding the entire array to the end of the array(doubling it almost).
Two ways to do it, one is a nested for loop that runs twice, the second one basically adding to the end of our new answer array.
The one I did just sets our answer index, and answer index + length(our second array added on top) in the same loop. Initially set the array to the length of the nums array.

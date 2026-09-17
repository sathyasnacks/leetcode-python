class Solution(object):
    def getConcatenation(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
        
        """
        given an integer array "nums" of length n, and you want to create an array "ans" that is twice the length
        #ans[i+n] == nums[i]

        basically we just want to double the array

        There is multiple ways to do this, we can simple loop through the above "nums" twice in a nested for loop, with the outer loop being "2" and the inner loop being the length of nums.

        such as this: 

        ns = []
        for i in range(2):
            for num in nums:
                ans.append(num)
        return ans

        below is a easier solution
        """


        length = len(nums)
        ans = [0] * (2*(length))

        for i,n in enumerate(nums):
            ans[i] = ans[i+length] = nums[i]
        
        return ans
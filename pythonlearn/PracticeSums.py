# Without using sort method, get the highest number in a list integer.
# iterate the list, capture the first number in a variable
# compare the number with each next number and see which is largest
# capture the largest number in a variable

def find_largest(nums):
    if not nums:
        print("List is Empty")
        return
    largest = nums[0]
    for each_num in nums:
        if largest >= each_num:
            pass
        else:
            largest = each_num
    print(f"{largest} is the largest")


ans=find_largest([])

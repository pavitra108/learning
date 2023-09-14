def convert_temp(c: float):
    k = c + 273.15
    f = c * 1.80 + 32.00
    return [k, f]

ans=convert_temp(112)

print(ans)

# Iterate the list
# Take each number and add to set. If duplicate it wont be added.
# check the count in the set to identify if there is duplicate
# hello
def checkDuplicate(nums):
    myset = set()
    for each_num in nums:
        myset.add(each_num)
    if len(nums) is len(myset):
        print ("No duplicates")
    else:
        print("duplicate exists")

ans=checkDuplicate([1,3,5,9,4])
print(ans)


# Iterate the list
# Take each number and add as a key and check if key already exists

def hasDuplicate(nums):
    my_dict = {}
    for each_num in nums:
        if each_num not in my_dict:
            my_dict[each_num] = ""
        else:
            print('dup exists')
            return True
    return False

ans=hasDuplicate([1,3,5,9,5])
print(ans)



def containsDuplicate(nums):
    index = 0
    for each_num in nums:
        newlist= nums.copy()
        del newlist[index]
        if each_num in newlist:
            return True
        index = index+1
    return False


check=containsDuplicate([5,2,3,1])
print(check)




def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
    """
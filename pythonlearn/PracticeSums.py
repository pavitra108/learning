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


ans=find_largest([4, 7, 2, 8, 4, 5])


#if the letters in caps are available in the list of given 'efficient' letters
def is_efficient(letters):
    eff_letters = set('BCDGIJLMNOPSUVWZ')
    for let in letters:
        if let in eff_letters:
            pass
        else:
            return False
    return True

see = is_efficient("BCDGIJ")
print(see)

#at least one positional argument (someone's given name, and a variadic collection of surnames or modifiers)
# and must handle a variadic collection of keyword-specified arguments with details from a profile.

def create_profile(given_name, *surname, **profile):
    for each in surname:
        print(given_name, each)
    for key, value in profile.items():
        print(key, value, sep=': ')


create_profile("Sebastian", "Thrun", cofounded="Udacity", experience="Stanford Professor")
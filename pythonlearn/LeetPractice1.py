# Merge and sort sum
# remove 0 from list 1
# remove 0 from list 2
# merge values from list 2 to list 1 - duplicates can be there
# sort in increasing order

def merge(nums1, m, nums2, n):
    nums1 = [x for x in nums1 if x != 0]
    nums2 = [y for y in nums2 if y != 0]
    nums1.extend(nums2)
    nums1.sort()
    print(nums1)


a = [1, 2, 4, 0]
b = [3, 7, 0]
ans = merge(a, 4, b, 3)


# Count word sum
# create a dictionary, split words in a string
# iterate each word and check if it there in dic as value
# if word is there, plus one else just 1
# word right before full stop - word and full stop taken as one string(not done
# took the first three index entries from sorted dic

def count_word(para):
    word = para.split()
    word_dic = {}
    for each_word in word:
        if each_word in word_dic:
            val = word_dic[each_word]
            val = val+1
            word_dic[each_word] = val
        else:
            word_dic[each_word] = 1
    return word_dic

def custom_fn(input):
    return input[1]
def call_index(dex):
    return dex
ans = count_word("All Iron Man Movies. Three Iron Man movies. However, Tony Stark played a big part in the MCU and was also one of the key characters in six other movies in the franchise. Iron Man appeared in 9 movies and had one uncredited cameo.")
given_index = call_index(4)
sorted_dic = dict(sorted(ans.items(), key=custom_fn, reverse=True)[:given_index])
ok = print(sorted_dic)


# is a string a palindrome sum
# Take first letter in the word n see if it the same as the last index - length

def check_palindrome(myword):
    l= len(myword) - 1
    for index, each_letter in enumerate(myword):
        next_l = l - index
        gg = myword[next_l]
        if each_letter == gg:
            pass
        else:
            return False

    return True


ans = check_palindrome("level")
print(ans)

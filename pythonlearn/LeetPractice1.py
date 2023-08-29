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

a= 1,2,4,0
b= 3,7,0
ans = merge([a], 4, [b], 3)




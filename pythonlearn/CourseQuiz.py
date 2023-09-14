# return True if all of the letters are efficient
# retuen False if any of the letters are not efficient
# a letter is "efficient" if it is in the collection "BCDGIJLMNOPSUVWZ".

def is_efficient(letters):
    eff_letters = set('BCDGIJLMNOPSUVWZ')
    for let in letters:
        if let in eff_letters:
            pass
        else:
            return False
    return True
see = is_efficient("bcdg")
print(see)


# swaps the keys and values in a dictionary
# a given value might be mapped to by more than one key

def swap_keys_and_values(d):
    set_dict = {key: {value} for key, value in d.items()}
    out_dict = dict()
    for key, value in d.items():
        if value in out_dict:
            hh = out_dict[value]
            hh.add(key)
            out_dict[value] = hh
        else:
            out_dict[value] = {key}
    print(out_dict)

swap_keys_and_values({
    'apple': 5,
    'banana': 2,
    'orange': 8,
    'grape': 2,
    'berry': 2,
    'kiwi': 5
    })


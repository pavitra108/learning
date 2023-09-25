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

# find anagrams exercise

english_words_small = {'open', 'peon', 'nope', 'stone', 'notes', 'onset', 'tones', 'cone', 'pots', 'post', 'stop',
                       'opts', 'tops'}

def load_words_from_filename(filename):
    """Load a set of words from a newline-separated file."""
    with open(filename) as infile:
        return set(line.strip().lower() for line in infile)


def find_anagrams(letters, words):
    english_words_small = {'open', 'peon', 'nope', 'stone', 'notes', 'onset', 'tones', 'cone', 'pots', 'post', 'stop', 'opts', 'tops'}

#sum on decorators
#.catche the output

import functools
import time


catch_dict = {}
def dummy(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        if function.__name__ in catch_dict:
           value_dict = catch_dict[function.__name__]
           n_key = (*args, tuple(kwargs.items()))
           if n_key in value_dict:
               return value_dict[n_key]
           else:
               one_output = function(*args, **kwargs)
               value_dict[n_key] = one_output
               return one_output
        else:
            one_dict ={}
            catch_dict[function.__name__] = one_dict
            output = function(*args, **kwargs)
            one_dict[(*args, tuple(kwargs.items()))] = output
            return output
    return wrapper

@dummy
def addmy(x, y):
    time.sleep(5)
    return x+y

@dummy
def sub(x,y):
    time.sleep(5)
    return x-y

print(addmy(1,3))
print(addmy(1,5))
print(sub(1,3))
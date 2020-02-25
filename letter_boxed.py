import sys, numpy as np, string, itertools, os

# This is a large set of words for use with NYT Letter Boxed.  I will update
# this list as I find words that are not allowed
abspath = os.path.abspath(__file__)
dictionary = os.path.split(abspath)[0]+'/data/dictionary.txt'
max_num_words = 3 # My laptop gets memory issues with large N (>3)

word_list = np.loadtxt(dictionary, dtype=str)
word_list = [word.lower() for word in word_list] # Make lower case

alphabet = string.ascii_lowercase

# If given a list of N strings, is there an ordering such that the last letter
# of each string is the first letter of the subsequent string
def check_string_ordering(word_list):

    orderings = itertools.permutations(word_list)
    for ordering in orderings:
        for i,word in enumerate(ordering):
            if i==len(ordering)-1:
                return(ordering)
            elif word[-1]==ordering[i+1][0]:
                continue
            else:
                break

    return(None)

# Parsing input.  Give input as abcdef
try:
    inp=str(sys.argv[1])
    if len(set(inp))!=12:
        error = 'ERROR: input the full twelve letter board as argument!\n'
        error += 'Usage: python letter_boxed.py abcdefghijkl'
        print(error)
        sys.exit()
    if any([char not in alphabet for char in inp]):
        error = 'ERROR: at least one of '+inp+' is not a letter!\n'
        error += 'Usage: python letter_boxed.py abcdefghijkl'
        print(error)
        sys.exit()
except:
    error = 'ERROR: input the full twelve letter board as argument!\n'
    error += 'Usage: python letter_boxed.py abcdefghijkl'
    print(error)
    sys.exit()

sides=[inp[0:3],inp[3:6],inp[6:9],inp[9:12]]
print('Input board is {0}'.format(sides))
sides=[l.lower() for l in sides]
all_letters = ''.join(sides)
alphabet = string.ascii_lowercase
not_letters = ''.join([a for a in alphabet if a not in all_letters])

# First step is to cut down the word_list to only words whose letters are all
# contained in all_letters and whose consecutive letters are not on the same
# "side"
keep = []
for k,word in enumerate(word_list):
    idx1 = -1
    idx2 = -1
    good = True
    for i,letter in enumerate(word):
        if letter not in all_letters:
            good = False
            break
        if i > 0:
            if idx1 == -1:
                idx1 = int(all_letters.index(word[i-1])/3)
            idx2 = int(all_letters.index(word[i])/3)

            if idx1 == idx2:
                good = False
                break

            idx1 = int(idx2)

    if good:
        keep.append(k)

word_list = list(np.array(word_list)[keep])

# Now we (hopefully) have a managable list of words.
print('Number of good words is {0}'.format(len(word_list)))

# Next step is to iterate through solutions with N words, starting with N=1.
# These solutions must meet two criteria: one is that all 12 letters are
# in the set of N words, the second is that the list of N words must have an
# ordering such that the last letter of the ith word is the first letter of the
# i+1th word.
for N in np.arange(1, max_num_words+1):

    # First make a list containing all N word combinations from cut word_list
    possible_solutions = itertools.combinations(word_list, N)

    # Iterate through all solutions and check if they match both criteria.  If
    # we find a solution that matches both then break
    for solution in possible_solutions:
        good = None
        if len(set(''.join(solution)))<12:
            continue
        if N > 1:
            good = check_string_ordering(solution)
            if good:
                break

    if not good:
        print('No good solution for N={0}'.format(N))
    else:
        break

if good:
    print('Good solution for N={0} is {1}'.format(N, good))

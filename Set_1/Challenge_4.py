# Detect single-character XOR
# One of the 60-character strings in this file (../InputFiles/1_4.txt) has been encrypted by single-character XOR.
# Find it.

from Utils.crypto import score_string, single_byte_bruteforce
from operator import itemgetter

file = "../InputFiles/1_4.txt"

with open(file) as f:
    strings = f.readlines()

strings = [x.strip("\n") for x in strings]

result_list = []
linenumber = 1
for s in strings:
    for i in range(0, 255):
        s_output = single_byte_bruteforce(s, chr(i))
        score = score_string(s_output)
        result_list.append((s_output, score, s, linenumber))
    linenumber += 1

result_list.sort(key=itemgetter(1), reverse=True)

winner = result_list[:1]

print winner

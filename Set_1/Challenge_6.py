# There's a file here. It's been base64'd after being encrypted with repeating-key XOR.
# Decrypt it.
import itertools
from Utils.crypto import hamming_distance, slicer, chunker, single_byte_bruteforce, score_string, repeating_key_xor
import base64
from operator import itemgetter

file = "../InputFiles/1_6.txt"

print hamming_distance(bytearray("this is a test"), bytearray("wokka wokka!!!"))

with open(file) as f:
    input_file = f.read()

raw_string = bytearray(base64.b64decode(input_file))
# print raw_string

hams = []

for i in range(2, 41):
    segments = slicer(raw_string, i, 50)
    combine = itertools.combinations(segments, 2)
    hamscore = 0
    for s1, s2 in combine:
        hamscore += hamming_distance(s1, s2) / i
    hamscore /= 6
    hams.append((hamscore, i))

hams.sort(key=itemgetter(0))

# Probable keylength
keylength = hams[0][1]


chunks = chunker(raw_string, keylength)
transposed_blocks = zip(*chunks)
i = 0
key = ""
for block in transposed_blocks:
    scores = []
    for x in range(0, 255):
        scores.append((score_string(single_byte_bruteforce(bytearray(block), chr(x))), chr(x)))
    scores.sort(key=itemgetter(0), reverse=True)
    print "Probable key for block {0} is {1}".format(i, scores[0][1])
    i += 1
    key += scores[0][1]
print "Full key is {0}".format(key) + "\n"

print "Decoded message: \n" + repeating_key_xor(raw_string, key)

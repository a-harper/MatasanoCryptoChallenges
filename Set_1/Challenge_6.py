# There's a file here. It's been base64'd after being encrypted with repeating-key XOR.
# Decrypt it.
import itertools
from Utils.crypto import hamming_distance, slicer
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
    segments = slicer(raw_string, i, 4)
    combine = itertools.combinations(segments, 2)
    hamscore = 0
    for s1, s2 in combine:
        hamscore += hamming_distance(s1, s2) / i
    hamscore /= 6
    hams.append((hamscore, i))

hams.sort(key=itemgetter(1), reverse=True)
print hams[:15]

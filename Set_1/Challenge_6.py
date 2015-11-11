# There's a file here. It's been base64'd after being encrypted with repeating-key XOR.
# Decrypt it.

from Utils.crypto import hamming_distance
import base64
from operator import itemgetter

file = "../InputFiles/1_6.txt"

print hamming_distance(bytearray("this is a test"), bytearray("wokka wokka!!!"))

with open(file) as f:
    input_file = f.read()

raw_string = bytearray(base64.b64decode(input_file))
# print raw_string

hams = []

for i in range(2, 40):
    b_array1 = raw_string[0:i-1]
    b_array2 = raw_string[i-1:(i*2) - 1]
    hams.append(((hamming_distance(b_array1, b_array2)) / i, i))

hams.sort(key=itemgetter(1), reverse=True)
print hams[0]

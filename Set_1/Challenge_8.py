#
# Detect AES in ECB mode
#
# In this file are a bunch of hex-encoded ciphertexts.
#
# One of them has been encrypted with ECB.
#
# Detect it.
#
# Remember that the problem with ECB is that it is stateless and deterministic; the same 16 byte plaintext block will
# always produce the same 16 byte ciphertext.

import Utils.crypto as crypto

file = "../InputFiles/1_8.txt"

with open(file) as f:
    text = f.readlines()

text = [x.strip("\n") for x in text]

l_num = 0

for line in text:
    decoded = bytearray.fromhex(line)
    blocks = crypto.slicer(decoded, 16, (len(decoded) / 16))
    score = crypto.score_ecb(blocks)
    if score > 0:
        print "Match on line {0} with score {1}".format(l_num, score)
        print line
    l_num += 1

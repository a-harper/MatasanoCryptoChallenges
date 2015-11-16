# Byte-at-a-time ECB decryption (Simple)
#
# Copy your oracle function to a new function that encrypts buffers under ECB mode using a consistent but unknown key
# (for instance, assign a single random key, once, to a global variable).
#
# Now take that same function and have it append to the plaintext, BEFORE ENCRYPTING, the following string:

# Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg
# aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq
# dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg
# YnkK

#  Base64 decode the string before appending it. Do not base64 decode the string by hand; make your code do it.
# The point is that you don't know its contents.
#
# What you have now is a function that produces:
#
# AES-128-ECB(your-string || unknown-string, random-key)

#  It turns out: you can decrypt "unknown-string" with repeated calls to the oracle function!
#
# Here's roughly how:
#
#     Feed identical bytes of your-string to the function 1 at a time --- start with 1 byte ("A"), then "AA",
#     then "AAA" and so on. Discover the block size of the cipher. You know it, but do this step anyway.
#     Detect that the function is using ECB. You already know, but do this step anyways.
#     Knowing the block size, craft an input block that is exactly 1 byte short (for instance,
#     if the block size is 8 bytes, make "AAAAAAA"). Think about what the oracle function is going to put in that last
#     byte position.
#     Make a dictionary of every possible last byte by feeding different strings to the oracle; for instance,
#     "AAAAAAAA", "AAAAAAAB", "AAAAAAAC", remembering the first block of each invocation.
#     Match the output of the one-byte-short input to one of the entries in your dictionary. You've now discovered the
#     first byte of unknown-string.
#     Repeat for the next byte.

from Utils import crypto as crypto
import base64

key = None

appender = 'Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzd' \
               'GFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK'


def find_block_size():
    global key
    if key is None:
        key = crypto.generate_bytes(16)
    # One block
    len1 = len(crypto.encryption_oracle2(b'', key))
    len2 = 0
    i = 0
    while len2 <= len1:
        len2 = len(crypto.encryption_oracle2(bytearray([0] * i), key))
        i += 1
    len3 = len2 - len1
    return len3


block_size = find_block_size()
print block_size

# Check for ECB
if crypto.score_ecb(crypto.encryption_oracle2(bytearray([0] * 47), key)) >= 1:
    print "ECB"

discovered = ""
for n in range(1, 17):
    discovered += crypto.brute_ecb_character(crypto.encryption_oracle2, key, n, discovered)
print discovered


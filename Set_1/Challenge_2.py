# Fixed XOR
# Write a function that takes two equal-length buffers and produces their XOR combination.
# If your function works properly, then when you feed it the string:
# 1c0111001f010100061a024b53535009181c
# ... after hex decoding, and when XOR'd against:
# 686974207468652062756c6c277320657965
# ... should produce:
# 746865206b696420646f6e277420706c6179

from Utils.crypto import fixed_xor
import binascii

input_string = "1c0111001f010100061a024b53535009181c"

b1 = bytearray.fromhex(input_string)

xor_against = "686974207468652062756c6c277320657965"

b2 = bytearray.fromhex(xor_against)

print b1
print b2

output = fixed_xor(b1, b2)
print output

print binascii.hexlify(bytearray(output))

# There's a file here. It's been base64'd after being encrypted with repeating-key XOR.
# Decrypt it.

from Utils.crypto import hamming_distance

print hamming_distance("this is a test", "wokka wokka!!!")
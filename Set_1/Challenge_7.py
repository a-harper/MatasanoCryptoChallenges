# AES in ECB mode
#
# The Base64-encoded content in this file has been encrypted via AES-128 in ECB mode under the key
#
# "YELLOW SUBMARINE".
#
# (case-sensitive, without the quotes; exactly 16 characters; I like "YELLOW SUBMARINE" because it's exactly 16 bytes long, and now you do too).
#
# Decrypt it. You know the key, after all.
#

from Crypto.Cipher import AES
import base64

key = b'YELLOW SUBMARINE'
file = "../InputFiles/1_7.txt"
with open(file) as f:
    text = base64.b64decode(f.read())

cipher = AES.new(key, AES.MODE_ECB)
plaintext = cipher.decrypt(text)

print plaintext

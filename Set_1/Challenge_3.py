# Single-byte XOR cipher
# The hex encoded string:
# 1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736
# ... has been XOR'd against a single character. Find the key, decrypt the message.
from Utils.crypto import score_string, single_byte_bruteforce
from operator import itemgetter

input_string = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
result_list = []

for i in range(0, 255):
    result = single_byte_bruteforce(bytearray.fromhex(input_string), chr(i))
    if len(result) > 0:
        score = score_string(result)
        result_list.append((result, score))

result_list.sort(key=itemgetter(1), reverse=True)

best_result = result_list[:1]
print best_result

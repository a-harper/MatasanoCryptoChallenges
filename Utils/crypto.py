def fixed_xor(first_bytestring, second_bytestring):
    return ''.join(chr(x ^ y) for x, y in zip(first_bytestring, second_bytestring))


def repeating_key_xor(string, key):
    key_padded = (key * ((len(string)/len(key))+1))[:len(string)]
    string_bytes = bytearray(string)
    key_bytes = bytearray(key_padded)

    return fixed_xor(string_bytes, key_bytes)


def single_byte_bruteforce(string, char):
    string_bytes = bytearray.fromhex(string)
    char_byte = bytearray(char)
    output_bytes = b''
    for x in string_bytes:
        output_bytes += chr(x ^ char_byte[0])
    return output_bytes


def score_string(string):
    score = 0
    for c in string:
        ascii_value = ord(c)
        if ascii_value == 32:
            score += 20
        elif ascii_value in (101, 97, 105, 111, 118):
            score += 20
        elif ascii_value < 31:
            score -= 50
        elif ascii_value < 64:
            score += 1
        elif ascii_value < 127:
            score += 5
        elif ascii_value < 255:
            score -= 5
    return score


def hamming_distance(string1, string2):
    bytes1 = bytearray(string1)
    bytes2 = bytearray(string2)
    diffs = 0
    for ch1, ch2 in zip(bytes1, bytes2):
        if ch1 != ch2:
            diffs += 1
    return diffs

def fixed_xor(first_bytestring, second_bytestring):
    return ''.join(chr(x ^ y) for x, y in zip(first_bytestring, second_bytestring))


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

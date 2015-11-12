from itertools import izip


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


def hamming_distance(bytearray1, bytearray2):
    return sum(bin(i ^ j).count("1") for i, j in zip(bytearray1, bytearray2))


def slicer(string, slicesize, n):
    return [string[x:x+slicesize] for x in xrange(0, n*slicesize, slicesize)]


def chunker(s, n):
    """ Yield successive chunks from l.
    :param s: input
    :param n: chunk size
    :return: chunk
    """
    for i in xrange(0, len(s), n):
        ret = s[i:i+n]
        if len(ret) < 29:
            ret += '\x00' * (29 - len(ret))
        yield ret

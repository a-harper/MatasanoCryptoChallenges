import itertools
from Crypto.Cipher import AES
import random
import base64


def fixed_xor(first_bytestring, second_bytestring):
    return ''.join(chr(x ^ y) for x, y in zip(first_bytestring, second_bytestring))


def repeating_key_xor(b_array, key):
    key_padded = (key * ((len(b_array)/len(key))+1))[:len(b_array)]
    key_bytes = bytearray(key_padded)

    return fixed_xor(b_array, key_bytes)


def single_byte_bruteforce(b_array, char):
    char_byte = bytearray(char)
    output_bytes = b''
    for x in b_array:
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


def chunker(s, n, pad=True):
    """ Yield successive chunks from l.
    :param s: input
    :param n: chunk size
    :param pad: pad last string to length
    :return: chunk
    """
    for i in xrange(0, len(s), n):
        ret = s[i:i+n]
        if len(ret) < n and pad:
            ret += '\x00' * (n - len(ret))
        yield ret


def score_ecb(b_arraylist):
    pairs = itertools.combinations(b_arraylist, 2)
    return sum([(1 if (p[0] == p[1]) else 0) for p in pairs])


def pad_block(block, desired_length, padchars='\x04', plain=False):
    b_array = bytearray(block)
    b_array += padchars * (desired_length - (len(block) if plain else len(b_array)))
    return b_array


def encrypt_cbc(text, iv, key):
    blocks = chunker(text, 16)
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = b''
    previous = iv
    for block in blocks:
        cipherblock = cipher.encrypt(fixed_xor(bytearray(previous), bytearray(block)))
        ciphertext += cipherblock
        previous = cipherblock
    return ciphertext


def decrypt_cbc(text, iv, key):
    blocks = chunker(text, 16)
    cipher = AES.new(key, AES.MODE_ECB)
    plaintext = b''
    previous = iv
    for block in blocks:
        plainblock = fixed_xor(bytearray(cipher.decrypt(buffer(block))), previous)
        plaintext += plainblock
        previous = block
    return plaintext


def to_bytes(n, length, endianness='big'):
    h = '%x' % n
    s = ('0'*(len(h) % 2) + h).zfill(length*2).decode('hex')
    return s if endianness == 'big' else s[::-1]


def generate_bytes(n):
    return to_bytes(random.getrandbits(8*n), n)


def encryption_oracle(text):
    prepend = generate_bytes(random.randrange(5, 11))
    append = generate_bytes(random.randrange(5, 11))
    plaintext = prepend + text + append
    if len(plaintext) % 16 != 0:
        plaintext = str(pad_block(plaintext, len(plaintext) + (16 - (len(plaintext) % 16)), plain=True))
    key = generate_bytes(16)
    iv = generate_bytes(16)
    cipher = AES.new(key, AES.MODE_ECB)
    if random.randrange(2):
        print 'Encrypting with CBC'
        return bytearray(encrypt_cbc(plaintext, iv, key))
    else:
        print 'Encrypting with EBC'
        return bytearray(cipher.encrypt(str(plaintext)))
    # return bytearray(encrypt_cbc(plaintext, iv, key) if random.randrange(2) else cipher.encrypt(plaintext))


def detection_oracle(funct):
    s = bytearray([0] * 47)
    t = funct(s)
    if score_ecb(chunker(t, 16)) > 0:
        return 'ECB Score: ' + str(score_ecb(chunker(t, 16)))
    return 'CBC'


def encryption_oracle2(text, key):
    appender = 'Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzd' \
               'GFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK'
    to_append = base64.b64decode(appender)
    s = text + to_append
    plaintext = pad_block(s, len(s) + (16 - (len(s) % 16)))
    cipher = AES.new(key, AES.MODE_ECB)
    return bytearray(cipher.encrypt(str(plaintext)))


def brute_ecb_character(funct, key, n, discovered=""):
    if n <= 16:
        one_byte_short = 'A' * (16 - n)
        output = funct(one_byte_short, key)[0:16]
        for i in range(0, 256):
            check = funct(one_byte_short + discovered + chr(i), key)[0:16]
            if check == output:
                print "Char in {0} position = {1}".format(n, chr(i))
                return chr(i)
    else:
        "Fuck it."



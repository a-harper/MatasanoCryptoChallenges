def fixed_xor(first_bytestring, second_bytestring):

    output = b''

    for x, y in zip(first_bytestring, second_bytestring):
        output += bytes([x ^ y])

    return output

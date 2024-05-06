dna_mp = ['A', 'C', 'G', 'T']
def byte_to_bin(data):
    return ''.join(format(byte, '08b') for byte in data)

def bin_to_DNA(data):
    return "".join(dna_mp[int(data[i: i + 2], 2)] for i in range(0, len(data), 2))

def byte_to_DNA(data):
    data = byte_to_bin(data)
    return bin_to_DNA(data)

def xor(data1, data2):
    return bytes([a ^ b for a, b in zip(data1, data2)])

def char_to_int(c):
    if c == 'A':
        return 0
    elif c == 'C':
        return 1
    elif c == 'G':
        return 2
    elif c == 'T':
        return 3
    raise ValueError('invalid character {}'.format(c))

def DNA_to_byte(data):
    if len(data) % 4 == 1:
        return None
    result = b''
    for i in range(0, len(data), 4):
        tmp = char_to_int(data[i]) * 64 + char_to_int(data[i + 1]) * 16 + char_to_int(data[i + 2]) * 4 + char_to_int(data[i + 3])
        result += tmp.to_bytes(1, byteorder='big')
    return result


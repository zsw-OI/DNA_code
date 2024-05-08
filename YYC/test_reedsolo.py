from reedsolo import RSCodec, ReedSolomonError
from bitarray import bitarray
from bitarray.util import ba2int

# Create a Reed-Solomon codec instance, 10 is the number of ECC (Error Correction Code) symbols
rs = RSCodec(2)

dna2binary = {"A": bitarray('00'), "T": bitarray('01'), "C": bitarray('10'), "G": bitarray('11')}
binary2dna = {ba2int(value): key for key, value in dna2binary.items()}

def bitarray_to_dna(bit_arr):
    """ Convert bitarray to DNA sequence """
    # Ensure the bitarray length is a multiple of 2
    if len(bit_arr) % 2 != 0:
        raise ValueError("Bitarray length must be a multiple of 2.")

    dna_sequence = ''
    for i in range(0, len(bit_arr), 2):
        # Extract two bits at a time
        two_bits = bit_arr[i:i+2]
        # Convert bitarray slice to integer
        dna_base = binary2dna[ba2int(two_bits)]
        # Append the corresponding DNA base to the result string
        dna_sequence += dna_base

    return dna_sequence

# Original message
message = "ATCG"

res = bitarray()
for base in message:
    res.extend(dna2binary[base])

print(res)
# Encode the message
encoded = bytearray(rs.encode(res))

# Print the original encoded message
print("Encoded message:", encoded)
print(encoded[0])

encoded_bit = bitarray()
encoded_bit.frombytes(encoded)
print(len(encoded_bit))
print(bitarray_to_dna(encoded_bit))
# Introduce an error in the encoded message
# Here, we change one byte in the encoded message
corrupted = (encoded)

# Try to decode the corrupted message
try:
    decoded = rs.decode(corrupted)
    print("Decoded message:", decoded)
except ReedSolomonError:
    print("Decoding failed: The message is too corrupted")

# The output should show the original message if error correction is successful


import sys
import argparse

from Encoder import Encoder
from FileReader import FileReader
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="input file", required=True)
parser.add_argument("-o", "--output", help="output file", default="./fountain.data")
parser.add_argument("-l", "--length", help="dna segment length", required=True, type=int)
parser.add_argument("-a", "--alpha", help="redundancy threshold", default=0.5, type=float)
parser.add_argument("-d", "--delta", help="Robust Soliton distribution delta", default=0.001, type=float)
parser.add_argument("-c", "--variance", help="Robust Soliton variance", default=0.025, type=float)
parser.add_argument("-s","--seed", help="random seed", default=113, type=int)
args = parser.parse_args()



if args.length % 4 != 0:
    raise ValueError("length is not a multiple of 4")

reader = FileReader(args.input, int(args.length / 4))
data = reader.read()

print("Encoded bytes length " + str(len(data)))

encoder = Encoder(data, args.alpha, args.variance, args.delta, args.seed)
dna_list = encoder.encode()
output_file = args.output
print(dna_list[0])
print(len(dna_list[0]))
with open(output_file, "w") as f:
    for dna in dna_list:
        f.write(dna + '\n')

exit(0)


import argparse
from Decoder import Decoder

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="input file", default="./noised_fountain.data")
parser.add_argument("-l", "--length", help="original length", required=True, type=int)
parser.add_argument("-o", "--output", help="output file", default="./decoded.data")
parser.add_argument("-d", "--delta", help="Robust Soliton ditribution delta", default=0.001, type=float)
parser.add_argument("-c", "--variance", help="Robust Solition variance", default=0.025, type=float)
parser.add_argument("-s","--seed", help="random seed", default=113, type=int)
args = parser.parse_args()

dna_list = []
with open(args.input, "r") as f:
    st = f.readline()
    while st:

        dna_list.append(st.strip())
        st = f.readline()
decoder = Decoder(args.length, dna_list, args.variance, args.delta, args.seed)
result = decoder.decode()
output_file = args.output

with open(output_file, "wb") as f:
    for data in result:
        f.write(data)
exit(0)
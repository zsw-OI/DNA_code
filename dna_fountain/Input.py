import sys
import argparse

from Encoder import Encoder
from FileReader import FileReader
def main(input, syn_error, seq_error, copies, output = "./fountain.data", length = 128, alpha = 0.03, delta = 0.001, variance = 0.025, seed = 113):
    tl = length + 34
    valid_rate = (1 - syn_error)**tl * (1-(1-(1-seq_error)**tl)**copies)
    if length % 4 != 0:
        raise ValueError("length is not a multiple of 4")
    reader = FileReader(input, int(length / 4))
    data = reader.read()

    print("Encoded bytes size " + str(len(data)))

    encoder = Encoder(data, valid_rate, alpha, variance, delta, seed)
    dna_list = encoder.encode()
    density = 2.0 * len(data) / len(dna_list) * length / tl
    print("Encoding density: " + str(density))

    output_file = output
    print("Encoded " + str(len(dna_list)) + " DNA segments")
    with open(output_file, "w") as f:
        for dna in dna_list:
            f.write(dna + '\n')
    return len(data), density

if __name__ == '__main__' :
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="input file", required=True)
    parser.add_argument("-o", "--output", help="output file", default="./fountain.data")
    parser.add_argument("-l", "--length", help="dna segment length", default=128, type=int)
    parser.add_argument("-a", "--alpha", help="redundancy threshold", default=0.03, type=float)
    parser.add_argument("-d", "--delta", help="Robust Soliton distribution delta", default=0.001, type=float)
    parser.add_argument("-c", "--variance", help="Robust Soliton variance", default=0.025, type=float)
    parser.add_argument("-sd","--seed", help="random seed", default=113, type=int)
    parser.add_argument("-se", "--syn_error", help="synthesize error", type=float, required=True)
    parser.add_argument("-qe", "--seq_error", help="sequence error", type=float, required=True)
    parser.add_argument("-cp", "--copies", help="number of copies", type=int, required=True)
    args = parser.parse_args()

    

    l,_ = main(input = args.input, output = args.output, length = args.length, alpha = args.alpha, delta = args.delta, variance = args.variance, seed = args.seed, syn_error = args.syn_error, seq_error = args.seq_error, copies = args.copies)
    # print(l, _)
    exit(l)

    # tl = args.length + 34
    # valid_rate = (1 - args.syn_error)**tl * (1-(1-(1-args.seq_error)**tl)**args.copies)

    # if args.length % 4 != 0:
    #     raise ValueError("length is not a multiple of 4")

    # reader = FileReader(args.input, int(args.length / 4))
    # data = reader.read()

    # print("Encoded bytes size " + str(len(data)))

    # encoder = Encoder(data, valid_rate, args.alpha, args.variance, args.delta, args.seed)
    # dna_list = encoder.encode()

    # print("Encoding density: " + str(2.0 * len(data) / len(dna_list) * args.length / tl))

    # output_file = args.output
    # print("Encoded " + str(len(dna_list)) + " DNA segments")
    # with open(output_file, "w") as f:
    #     for dna in dna_list:
    #         f.write(dna + '\n')
    # exit(0)


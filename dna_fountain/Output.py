import argparse
from Decoder import Decoder
def main(length, input = "./noised_fountain.data", output = "./decoded.data", delta = 0.001, variance = 0.025, seed = 113):
    dna_list = []
    with open(input, "r") as f:
        st = f.readline()
        while st:
            dna_list.append(st.strip())
            st = f.readline()
    decoder = Decoder(length, dna_list, variance, delta, seed)
    result, recovery = decoder.decode()
    if result is None:
        return recovery
    output_file = output
    with open(output_file, "wb") as f:
        for data in result:
            f.write(data)
    return recovery

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="input file", default="./noised_fountain.data")
    parser.add_argument("-l", "--length", help="original length", required=True, type=int)
    parser.add_argument("-o", "--output", help="output file", default="./decoded.data")
    parser.add_argument("-d", "--delta", help="Robust Soliton ditribution delta", default=0.001, type=float)
    parser.add_argument("-c", "--variance", help="Robust Solition variance", default=0.025, type=float)
    parser.add_argument("-s","--seed", help="random seed", default=113, type=int)
    args = parser.parse_args()
    main(length = args.length, input = args.input, output = args.output, delta = args.delta, variance = args.variance, seed = args.seed)
    exit(0)
    # dna_list = []
    # with open(args.input, "r") as f:
    #     st = f.readline()
    #     while st:

    #         dna_list.append(st.strip())
    #         st = f.readline()
    # decoder = Decoder(args.length, dna_list, args.variance, args.delta, args.seed)
    # result = decoder.decode()
    # if result is None:
    #     exit(1)
    # output_file = args.output

    # with open(output_file, "wb") as f:
    #     for data in result:
    #         f.write(data)
    # exit(0)
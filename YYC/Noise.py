import argparse
import random
from tqdm import tqdm
class Noise(object):
    def __init__(self, syn_error, seq_error, copies):
        self.syn_error = syn_error
        self.seq_error = seq_error
        self.copies = copies

    def insert_dna(self, dna_sequence, p):
        result = ""
        for base in dna_sequence:
            result += base
            if random.random() < p:
                result += random.choice("ATGC")
        return result

    def delete_dna(self, dna_sequence, p):
        result = ""
        for base in dna_sequence:
            if random.random() >= p:
                result += base
        return result

    def replace_dna(self, dna_sequence, p):
        result = ""
        for base in dna_sequence:
            if random.random() < p:
                result += random.choice("ATGC")
            else:
                result += base
        return result
    def add_noises_single(self, dna, error_rate):
        p = error_rate / 3
        dna = self.replace_dna(dna, p)
        dna = self.insert_dna(dna, p)
        dna = self.delete_dna(dna, p)
        return dna

    def add_noises(self, dna_list):
        tmp = []
        result = []
        for dna in dna_list:
            tmp.append(self.add_noises_single(dna, self.syn_error))
        cnt = 0
        for dna in tqdm(tmp):
            for _ in range(self.copies):
                result.append(self.add_noises_single(dna, self.seq_error))
        random.shuffle(result)
        return result

def main(input = "./output/120.dna", output = "./output/120_err.dna", syn_error = 0.001, seq_error = 0.01, copies = 444):
    noiser = Noise(syn_error, seq_error, copies)
    dna_list = []
    with open(input, "r") as f:
        st = f.readline()
        while st:
            dna_list.append(st.strip())
            st = f.readline()

    dna_list = noiser.add_noises(dna_list)
    with open(output, "w") as f:
        for dna in dna_list:
            f.write(dna + '\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="input file", default="./output/120.dna")
    parser.add_argument("-o", "--output", help="output file", default="./output/120_err.dna")
    parser.add_argument("-se", "--syn_error", help="synthesize error", default=0.001, type=float)
    parser.add_argument("-qe", "--seq_error", help="sequence error", default=0.01, type=float)
    parser.add_argument("-cp","--copies", help="number of copies", default=444, type=int)
    args = parser.parse_args()
    main(input = args.input, output = args.output, syn_error = args.syn_error, seq_error = args.seq_error, copies = args.copies)
    # noiser = Noise(args.syn_error, args.seq_error, args.copies)

    # dna_list = []
    # with open(args.input, "r") as f:
    #     st = f.readline()
    #     while st:
    #         dna_list.append(st.strip())
    #         st = f.readline()

    # dna_list = noiser.add_noises(dna_list)
    # with open(args.output, "w") as f:
    #     for dna in dna_list:
    #         f.write(dna + '\n')
    exit(0)

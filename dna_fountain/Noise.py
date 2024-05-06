import argparse
import random

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
        for dna in tmp:
            for _ in range(self.copies):
                result.append(self.add_noises_single(dna, self.seq_error))
        random.shuffle(result)
        return result

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="input file", default="./fountain.data")
parser.add_argument("-o", "--output", help="output file", default="./noised_fountain.data")
parser.add_argument("-se", "--syn_error", help="synthesize error", default=0.001, type=float)
parser.add_argument("-qe", "--seq_error", help="sequence error", default=0.01, type=float)
parser.add_argument("-c","--copies", help="number of copies", default=100, type=int)
args = parser.parse_args()

noiser = Noise(args.syn_error, args.seq_error, args.copies)

dna_list = []
with open(args.input, "r") as f:
    st = f.readline()
    while st:
        dna_list.append(st.strip())
        st = f.readline()

dna_list = noiser.add_noises(dna_list)
with open(args.output, "w") as f:
    for dna in dna_list:
        f.write(dna + '\n')
exit(0)

from Random import Random
from Soliton_distribution import Soliton_distribution
from reedsolo import RSCodec
import math
import random
import Function
from tqdm import tqdm

class Encoder(object):
    def __init__(self, chunks, valid_rate, alpha, sd_c, sd_delta, seed = 114514):
        self.random_gen = Random(seed)
        self.K = len(chunks)
        self.chunks = chunks
        self.sd_gen = Soliton_distribution(self.K, sd_c, sd_delta)
        self.limit = self.K * self.sd_gen.Z / valid_rate * (1 + alpha)
        # self.limit = int(math.ceil(self.limit))
        self.limit = int(math.ceil((1 + alpha) * self.limit))
        self.codec = RSCodec(2)
    def extract_chunks(self, d, seed):
        random.seed(seed)
        return random.sample(self.chunks, d)
    def parse_dna(self, chunk, seed):
        chunk = seed.to_bytes(4, byteorder='big') + chunk
        return Function.byte_to_DNA(self.codec.encode(chunk))

    def encode(self):
        DNA_list = []
        # print("Encoding " + str(self.limit) + " chunks")
        for i in tqdm(range(0, self.limit)):
            seed = self.random_gen.next()
            d = self.sd_gen.calculate(seed)
            chunks = self.extract_chunks(d, seed)
            result = chunks[0]
            for i in range(1, len(chunks)):
                result = Function.xor(result, chunks[i])
            DNA_list.append(self.parse_dna(result, seed))
        return DNA_list




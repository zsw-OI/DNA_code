import copy

from Soliton_distribution import Soliton_distribution
from Random import Random
from reedsolo import RSCodec
from collections import Counter
import Function
import random
class Decoder(object):
    def __init__(self, K, dna_list, sd_c, sd_delta, seed = 114514):
        self.random_gen = Random(seed)
        self.sd_gen = Soliton_distribution(K, sd_c, sd_delta)
        self.dna_list = dna_list
        self.codec = RSCodec(2)
        self.result = [None for _ in range(K)]
        self.K = K
        self.out_edge = [[] for _ in range(K)] # from index to message
        self.in_edge = [] # from message to index
        self.val = []
        self.ct = 0
    def get_data(self, dna):
        if len(dna) % 4 != 0:
            return -1, None
        data = Function.DNA_to_byte(dna)
        corrected_data = None

        try:
            corrected_data = self.codec.decode(data)[0]
        except:
            return -1, None
        encoded_data = self.codec.encode(corrected_data)
        if encoded_data != data:
            return -1, None
        seed = int.from_bytes(encoded_data[0 : 4], "big")
        return seed, corrected_data[4 :]
    def extract_id(self, seed, d):
        random.seed(seed)
        return random.sample([i for i in range(0, self.K)], d)
    def update(self, u):
        ee = copy.deepcopy(self.out_edge[u])
        for v in ee:
            if not v in self.out_edge[u]:
                continue
            self.val[v] = Function.xor(self.val[v], self.result[u])
            self.in_edge[v].remove(u)
            self.out_edge[u].remove(v)
            if len(self.in_edge[v]) == 1:
                u1 = self.in_edge[v][0]
                self.result[u1] = self.val[v]
                self.in_edge[v] = []
                self.out_edge[u1].remove(v)
                self.update(u1)
    def insert(self, data, edges):
        remained_edges = []
        for e in edges:
            if self.result[e] is not None:
                data = Function.xor(data, self.result[e])
            else:
                remained_edges.append(e)
        if len(remained_edges) == 0:
            return
        elif len(remained_edges) == 1:
            self.result[remained_edges[0]] = data
            self.update(remained_edges[0])
            self.ct += 1
            return
        else:
            self.val.append(data)
            id = len(self.val) - 1
            in_e = []
            for e in remained_edges:
                in_e.append(e)
                self.out_edge[e].append(id)
            self.in_edge.append(in_e)
            return

    def decode(self):
        counter = Counter(self.dna_list)
        sorted_counter = sorted(counter.items(), key=lambda x: x[1], reverse=True)
        dna_list = [t[0] for t in sorted_counter]
        vis = dict()
        cnt = 0
        cnt1 = 0
        for dna in dna_list:
            cnt += 1

            if cnt % 100 == 0:
                print("Read chunk " + str(cnt) + ", used chunk" + str(cnt1))
            
            seed, data = self.get_data(dna)
            if seed == -1 or seed in vis:
                continue
            vis[seed] = True
            d = self.sd_gen.calculate(seed)
            edges = self.extract_id(seed, d)
            cnt1 += 1
            self.insert(data, edges)
        cnt = 0
        for i in range(self.K):
            if self.result[i] == None:
                cnt += 1
        
        if cnt > 0:
            print(str(cnt) + " chunks were not decoded!")
            raise Exception("Decoding failed!")
        return self.result

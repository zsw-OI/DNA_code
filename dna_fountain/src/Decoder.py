import copy

from Soliton_distribution import Soliton_distribution
from Random import Random
from reedsolo import RSCodec
from collections import Counter, deque
import Function
import random
from Trie import Trie
from tqdm import tqdm
class Decoder(object):
    def __init__(self, K, dna_list, sd_c, sd_delta, seed = 114514):
        self.random_gen = Random(seed)
        self.sd_gen = Soliton_distribution(K, sd_c, sd_delta)
        self.dna_list = list(set(dna_list))
        self.dna_list_pro = []
        self.codec = RSCodec(2)
        self.result = [None for _ in range(K)]
        self.K = K
        self.out_edge = [[] for _ in range(K)] # from index to message
        self.in_edge = [] # from message to index
        self.val = []
        self.solved = 0
        self.prefix_trie = Trie()
        self.suffix_trie = Trie()
        for dna in self.dna_list:
            self.prefix_trie.insert(dna)
            self.suffix_trie.insert(dna[::-1])
        self.copies_num = len(dna_list) // K

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
    def update_BFS(self, u):
        que = deque([u])
        while que:
            u = que.popleft()
            ee = copy.deepcopy(self.out_edge[u])
            for v in ee:
                if not v in self.out_edge[u]:
                    continue
                self.val[v] = Function.xor(self.val[v], self.result[u])
                self.in_edge[v].remove(u)
                self.out_edge[u].remove(v)
                if len(self.in_edge[v]) == 1:
                    u1 = self.in_edge[v][0]
                    self.in_edge[v] = []
                    self.out_edge[u1].remove(v)
                    
                    if self.result[u1] != None:
                        continue
                    self.solved += 1
                    self.result[u1] = self.val[v]
                    que.append(u1)
        

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
            if self.result[remained_edges[0]] != None:
                return
            self.result[remained_edges[0]] = data
            self.update_BFS(remained_edges[0])
            self.solved += 1
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

    def count_edit_distance_one(self, dna):
        n = len(dna)
        half_length = n // 2

        prefix = dna[:half_length]
        suffix = dna[-half_length:]

        # 统计相同前缀 >= len(dna)/2 或 相同后缀 >= len(dna)/2 的 dna 数量
        count_prefix = self.prefix_trie.search_with_prefix(prefix)
        count_suffix = self.suffix_trie.search_with_prefix(suffix[::-1])

        return count_prefix + count_suffix

    def decode(self):
        
        vis = dict()
        cnt = 0
        cnt1 = 0
        bases = ['A', 'T', 'C', 'G']

        for dna in tqdm(self.dna_list):
            if not dna:
                continue
            if len(dna) % 4 == 0:
                self.dna_list_pro.append(dna)
                for pos in range(len(dna)):
                    for new_base in bases:
                        if new_base == dna[pos]:
                            continue
                        new_dna = dna[:pos] + new_base + dna[pos+1:]
                        if self.count_edit_distance_one(new_dna) >= 0.9 * self.copies_num:
                            self.dna_list_pro.append(new_dna)

            elif len(dna) % 4 == 1:
                for pos in range(len(dna)):
                    new_dna = dna[:pos] + dna[pos+1:]
                    if self.count_edit_distance_one(new_dna) >= 0.9 * self.copies_num:
                        self.dna_list_pro.append(new_dna)

            elif len(dna) % 4 == 3:
                for pos in range(len(dna)):
                    for new_base in bases:
                        new_dna = dna[:pos] + new_base + dna[pos:]
                        if self.count_edit_distance_one(new_dna) >= 0.9 * self.copies_num:
                            self.dna_list_pro.append(new_dna)
                for new_base in bases:
                    new_dna = dna + new_base
                    if self.count_edit_distance_one(new_dna) >= 0.9 * self.copies_num:
                        self.dna_list_pro.append(new_dna)

        self.dna_list_pro = list(set(self.dna_list_pro))
        for dna in tqdm(self.dna_list_pro):
            cnt += 1

            # if cnt % 1000 == 0:
            #     print("Read chunk " + str(cnt) + ", used chunk " + str(cnt1), ", solved / total " + str(self.solved) + "/" + str(self.K))
            
            seed, data = self.get_data(dna)
            if seed == -1 or seed in vis:
                continue
            vis[seed] = True
            d = self.sd_gen.calculate(seed)
            edges = self.extract_id(seed, d)
            cnt1 += 1
            self.insert(data, edges)
            if self.solved == self.K:
                break
        ccnt = 0
        for i in range(self.K):
            if self.result[i] == None:
                ccnt += 1
        if ccnt > 0:
            print("Decoding failed!")
            print(str(ccnt) + " chunks were not decoded!")
            return None, 1.0 - ccnt / self.K
        print("Read chunk " + str(cnt) + ", used chunk " + str(cnt1), ", solved / total " + str(self.solved) + "/" + str(self.K))
        return self.result, 1.0

class FileReader(object):
    def __init__(self, file, chunk_size):
        self.file = file
        self.chunk_size = chunk_size

    def read(self):
        data = ""
        with open(self.file, 'rb') as f:
            data = f.read()
        L = len(data)

        if L % self.chunk_size != 0:
            data = data + b'\x00' * (self.chunk_size - L % self.chunk_size)
        # L = (L + self.chunk_size - 1) // self.chunk_size
        chunk_list = [data[i : i + self.chunk_size] for i in range(0, L, self.chunk_size)]

        return chunk_list
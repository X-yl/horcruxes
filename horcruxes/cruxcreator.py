from cruxio import HorcruxFileWriter
from Crypto.Cipher import AES

class HorcruxCreateManager():

    def __init__(self, source, n, k, blocksize, outdir):
        import os
        import secrets
        import shamir
        from math import ceil
        self.blocksize = blocksize or os.stat(source).st_size//10
        self.numblocks = ceil(os.stat(source).st_size/self.blocksize)
        self.source = open(source, 'rb')
        self.n = n
        self.k = k
        self.secret = secrets.randbelow(shamir.MAX_PRIME)
        self.shares = shamir.generate_shares(self.secret, n, k)
        self.files = []
        self.aes = AES.new(self.secret.to_bytes(16, byteorder='big'), mode=AES.MODE_CTR)
        self.nonce = self.aes.nonce
        for i in range(n):
           self.files.append(HorcruxFileWriter(os.path.join(outdir, f"{source}_{i+1}_of_{n}.hcx")))

    def write_headers(self):
        file: HorcruxFile = None
        srchash = self.hash_source()
        for i,file in enumerate(self.files):
            file.write_headers(srchash, self.nonce, self.n, self.k, i, self.blocksize, self.numblocks, self.shares[i])
        

    def hash_source(self):
        """Obtains a murmurhash3 hash of source file"""
        import mmh3
        val = 0
        while chunk:=self.source.read(1024):
            val = mmh3.hash128(chunk, val)
        
        self.source.seek(0)
        return val

    def write_block(self, bno):
        fileno = bno * (self.n-self.k+1) % self.n
        block = self.source.read(self.blocksize)

        encrypted = self.aes.encrypt(block)
        for _ in range(self.n-self.k+1):
            self.files[fileno].write_block(encrypted)
            fileno += 1
            fileno %= self.n

    def write(self):
        from tqdm import tqdm
        for i in tqdm(range(self.numblocks), desc="Encrypting"):
            self.write_block(i)

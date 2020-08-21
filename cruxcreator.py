from cruxwriter import HorcruxFile
from Crypto.Cipher import AES

class HorcruxCreateManager():

    def __init__(self, source, n, k, blocksize,secret, shares, outdir):
        self.srcfilename = source
        self.source = open(source, 'rb')
        self.n = n
        self.k = k
        self.blocksize = blocksize
        self.shares = shares
        self.secret = secret
        self.files = []
        self.aes = AES.new(secret.to_bytes(16, byteorder='big'), mode=AES.MODE_CTR)
        self.nonce = self.aes.nonce
        for i in range(n):
           self.files.append(HorcruxFile(outdir + f"{source}_horcrux_{i+1}_of_{n}", 'wb'))

    def write_headers(self):
        file: HorcruxFile = None
        srchash = self.hash_source()
        for i,file in enumerate(self.files):
            file.write_headers(srchash, self.nonce, self.n, self.k, i, self.blocksize, self.shares[i])
        

    def hash_source(self):
        """Obtains a murmurhash3 hash of source file"""
        import mmh3
        val = 0
        while chunk:=self.source.read(1024):
            val = mmh3.hash128(chunk, val)
        
        self.source.seek(0)
        return val

    def write_block(self, bno):
        fileno = bno * (self.n-self.k+1) % len(self.files)
        block = self.source.read(self.blocksize)

        encrypted = self.aes.encrypt(block)

        for _ in range(self.n-self.k+1):
            self.files[fileno].write_block(encrypted)
            fileno += 1
            fileno %= len(self.files)

    def write(self):
        import os
        from math import ceil
        srcblocks = ceil(os.stat(self.srcfilename).st_size/self.blocksize)

        for i in range(srcblocks):
            self.write_block(i)

import shamir
shares = shamir.generate_shares(1337, 5, 3)
x = HorcruxCreateManager("horcrux.txt", 5, 3, 651, 1337, shares, "./output/")
x.write_headers()
x.write()
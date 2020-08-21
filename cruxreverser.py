from cruxio import HorcruxFileReader
from Crypto.Cipher import AES

class HorcruxReverseManager():
    def __init__(self, filenames, dest):
        self.files = []
        self.dest = open(dest, 'wb')
        for file in filenames:
            self.files.append(HorcruxFileReader(file))

        if len(set(file.hashval for file in self.files)) > 1:
            raise ValueError("Horcruxes do not belong to same source file.")
        
        if len(set(file.nonce for file in self.files)) > 1:
            raise ValueError("Horcruxes do not have same nonce.")

        if self.files[0].k < len(files):
            raise ValueError(f"Not enough horcruxes. Required {files[0].k}")

        self.nonce = self.files[0].nonce
        self.n=self.files[0].n
        self.k=self.files[0].k
        self.filenos = [file.pos for file in self.files]
        self.numblocks = self.files[0].numblocks
        self.blocksize = self.files[0].blocksize
        self.secret = self.get_secret()
        self.aes = AES.new(self.secret.to_bytes(16, 'big'), AES.MODE_CTR, nonce=self.nonce)

    def get_secret(self):
        import shamir
        shares = [file.share for file in self.files]

        return shamir.find_secret(shares)

    def decrypt(self):
        from tqdm import tqdm

        for bno in tqdm(range(self.numblocks), "Decrypting"):
            self.decrypt_block(bno)


    def decrypt_block(self, bno):
        fileno = bno*(self.n-self.k+1) % self.n
        offset = bno*(self.n-self.k+1)
        
        for _ in range(self.n-self.k+1):
            if fileno in self.filenos: break
            fileno += 1
            offset += 1
            fileno %= self.n
        else:
            raise AssertionError("Something's gone horribly wrong. A reqired block was not found in any file.")

        offset = offset//self.n
        
        block = self.files[self.filenos.index(fileno)].read_block_at(offset)
        decrypted = self.aes.decrypt(block)
        self.dest.write(decrypted)


if __name__ == "__main__":
    import os
    files = [ 'output/' + x for x in  os.listdir('./output/')[:5]] 
    dest = 'uncrux.mkv'

    hrm = HorcruxReverseManager(files, dest)
    hrm.decrypt()


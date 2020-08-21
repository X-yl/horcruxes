class HorcruxFile():
    """Wraps a horcrux file

        |-------------------------headers------------------------|--blocks--|
     => |HXL1|hash128|nonce|n|k|pos|blocksize|share[0]|share[1]|&| .|.|.|.  |

        hash128, n,k,pos,share[0],share[1] are all 128 bit unsigned integers (big endian).
        
        pos = file pos
    """


    def __init__(self, filename, mode):
        self.file = open(filename, mode)
    
    def write_headers(self, sourcehash: int, nonce: bytes, n: int, k: int, pos: int, blocksize: int, share: tuple):
        """ Writes headers to file """

        self.file.write(b"HXL1")
        self.file.write(sourcehash.to_bytes(128//8, 'big'))
        self.file.write(nonce)

        for x in [n, k, pos, blocksize, share[0], share[1]]:
            self.file.write(x.to_bytes(128//8, byteorder='big'))

        self.file.write(b'&')

    def write_block(self, block: bytes):
        self.file.write(block)

    def close(self):
        self.file.close()

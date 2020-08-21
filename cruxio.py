class HorcruxFileWriter():
    """Wraps a horcrux file for writing.

        |------------------------------headers-----------------------------|--blocks--|
     => |HXL1|hash128|nonce|n|k|pos|blocksize|numblocks|share[0]|share[1]|&| .|.|.|.  |

        n,k,pos,blocksize,numblocks,share[0] are all 32 bit unsigned integers (big endian).
        hash128 and share[1] are 128 bit unsigned integers (big endian).
    """


    def __init__(self, filename):
        self.file = open(filename, 'wb')
    
    def write_headers(self, sourcehash: int, 
                            nonce: bytes, 
                            n: int, 
                            k: int, 
                            pos: int, 
                            blocksize: int, 
                            numblocks:int, 
                            share: tuple):

        """ Writes headers to file """

        self.file.write(b"HXL1")
        self.file.write(sourcehash.to_bytes(128//8, 'big'))
        self.file.write(nonce)

        for x in [n, k, pos, blocksize, numblocks, share[0]]:
            self.file.write(x.to_bytes(32//8, byteorder='big'))

        self.file.write(share[1].to_bytes(128//8, 'big'))

        self.file.write(b'&')

    def write_block(self, block: bytes):
        self.file.write(block)

    def close(self):
        self.file.close()


class HorcruxFileReader():
    """Wraps a horcrux file for reading.

        |------------------------------headers-----------------------------|--blocks--|
     => |HXL1|hash128|nonce|n|k|pos|blocksize|numblocks|share[0]|share[1]|&| .|.|.|.  |

        n,k,pos,blocksize,numblocks,share[0] are all 32 bit unsigned integers (big endian).
        hash128 and share[1] are 128 bit unsigned integers (big endian).
    """

    def __init__(self, filename):
        self.file = open(filename, 'rb')
        name = self.file.read(4)
        if name != b"HXL1": raise ValueError(f"File {filename} is not a horcrux")
        self.hashval = int.from_bytes(self.file.read(16), byteorder="big")

        def read_int():
            return int.from_bytes(self.file.read(4), byteorder="big")

        self.nonce = self.file.read(8)
        self.n =         read_int()
        self.k =         read_int()
        self.pos =       read_int()
        self.blocksize = read_int()
        self.numblocks = read_int()
        self.share =    (read_int(), int.from_bytes(self.file.read(128//8), "big"))
        if self.file.read(1) != b"&": 
            raise ValueError("Header not terminated. File may be corrupted")

        self.headerend = self.file.tell()
    
    def read_block_at(self, offset):
        self.file.seek(self.headerend + offset * self.blocksize, 0)
        return self.file.read(self.blocksize)
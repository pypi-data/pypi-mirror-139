# we will be using sha256 to hash the blocks
from hashlib import sha256


# a simple implementation of blockchain
class BlockChain:
    def __init__(self):
        # blocks stored sequentially
        self.blocks = []

    def create_block(self, id:int, nonce:int, prev_hash:str, transactions:list):
        if len(self.blocks) == 0:
            # create genisis Block
            self.new_block = Block(0, 0, 0, transactions)
        else:
            # create block with previous hash in it
            self.new_block = Block(len(self.blocks), 0, self.blocks[-1].block_hash, transactions)
        return self.new_block

    def add_block(self, block):
        self.blocks.append(block)


# block template
class Block:
    def __init__(self, id:int, nonce:int, prev_hash:str, transactions:list):
        # initialize all the fields of block
        self.id = id
        self.nonce = nonce
        self.transactions = transactions
        self.prev_hash = prev_hash
        self.block_hash = self.get_hash()
    
    # function to get hash of current block
    def get_hash(self):
        header_bin = (str(self.prev_hash)+str(self.id)+str(self.transactions)+str(self.nonce)).encode("utf-8")
        inner_hash = sha256(header_bin).hexdigest().encode()
        outer_hash = sha256(inner_hash).hexdigest()
        return outer_hash
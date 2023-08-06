from hashlib import sha256

# implement miner class
class Miner:
    def __init__(self):
        # all supported algorithms
        self.supported_algos = ["PoW"]
        # current algo in use
        self.use_algo = "PoW"
        # dict with associated functions
        self.generate_proof = {
            "PoW":self.PoW
        }
    
    # mine the block
    def mine(self, block) -> None:
        self.block = block
        self.hashis = block.block_hash
        
        pow = self.generate_proof[self.use_algo]()
        
        # update blocks hash
        block.block_hash = pow
        
        print("[Mined] Block id: %d , Block Hash: %s" % (self.block.id, self.block.block_hash))
    
    # select the algorithm for proof
    def select_algo(self, algo:str):
        self.use_algo = algo
    
    # proof of work algorithm
    def PoW(self):
        
        # make first 2 digits zeros in the hash
        # by changing the nonce
        while self.hashis[:2] != "00":
            # change the nonce
            self.block.nonce+=1
            # re hash the block
            self.hashis = self.block.get_hash()
        
        return self.hashis
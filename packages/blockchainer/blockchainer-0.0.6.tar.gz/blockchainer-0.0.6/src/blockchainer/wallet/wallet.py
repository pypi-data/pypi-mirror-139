'''
Generate private-public key pair
'''

from fastecdsa import curve, ecdsa, keys



class Wallet:
    
    def __init__(self, file_path=None):
        # if a file path is given
        if file_path:
            keys.import_key(filepath=file_path, curve=curve.secp256k1)
        else:
            self.priv_key = keys.gen_private_key(curve=curve.secp256k1)
            self.pub_key = keys.get_public_key(self.priv_key, curve=curve.secp256k1)
            
            # compress the pub_key
            
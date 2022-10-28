from BlockchainUtils import BlockchainUtils


class Lot():
    """Stores and manages lots"""

    def __init__(self, publicKey, iteration, lastBlockHash):
        self.publicKey = str(publicKey)
        self.iteration = iteration
        self.lastBlockHash = str(lastBlockHash)

    def lotHash(self):
        """Creates the lot hash is based on the public key and last block hash"""
        hashData = self.publicKey + self.lastBlockHash
        for _ in range(self.iteration):  # Different iteration will hash a different number of times and so create a different final hash
            hashData = BlockchainUtils.hash(hashData).hexdigest()
        return hashData

from BlockchainUtils import BlockchainUtils
from Lot import Lot


class ProofOfStake():
    """Consensus algorithm - keeps track of amount of stake of each account (to decide who is the next forger)"""

    def __init__(self):
        self.stakers = {}  # Mapping of account to stake
        self.setGenesisNodeStake()  # Initial staker

    def setGenesisNodeStake(self):
        """Adds initial staker to dictionary"""
        genesisPublicKey = open('keys/genesisPublicKey.pem', 'r').read()
        self.stakers[genesisPublicKey] = 1  # Their stake is 1

    def update(self, publicKeyString, stake):
        """Updates stake of an account"""
        if publicKeyString in self.stakers.keys():  # If public key in dictionary, update
            self.stakers[publicKeyString] += stake
        else:  # Else, add to dictionary
            self.stakers[publicKeyString] = stake

    def get(self, publicKeyString):
        """Returns stake of an account"""
        if publicKeyString in self.stakers.keys():
            return self.stakers[publicKeyString]
        else:
            return None

    def validatorLots(self, seed):
        """Creates list of all lots"""
        lots = []
        for validator in self.stakers.keys():
            for stake in range(self.get(validator)):  # More stake will mean more lots for that account
                lots.append(Lot(validator, stake+1, seed))
        return lots

    def winnerLot(self, lots, seed):
        """Finds which lot won"""
        winnerLot = None
        leastOffset = None
        referenceHashIntValue = int(BlockchainUtils.hash(seed).hexdigest(), 16)  # The lot whose hash is closest to this value is the winner lot (will always be 16 bytes)
        for lot in lots:
            lotIntValue = int(lot.lotHash(), 16)
            offset = abs(lotIntValue - referenceHashIntValue)
            if leastOffset is None or offset < leastOffset:
                leastOffset = offset
                winnerLot = lot
        return winnerLot  # Returns winnerLot

    def forger(self, lastBlockHash):
        """Finds who will be the forger and returns their public key"""
        lots = self.validatorLots(lastBlockHash)
        winnerLot = self.winnerLot(lots, lastBlockHash)
        return winnerLot.publicKey


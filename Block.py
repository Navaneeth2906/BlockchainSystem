import time
import copy


class Block():
    """For creating and managing blocks - a container that holds data (including transactions)"""

    def __init__(self, transactions, lastHash, forger, blockCount):
        self.blockCount = blockCount
        self.transactions = transactions
        self.lastHash = lastHash
        self.timestamp = time.time()
        self.forger = forger  # Public Key of forger
        self.signature = ''  # Signature of forger

    @staticmethod
    def genesis():
        """Creates first block (as a starting point)"""
        genesisBlock = Block([], 'genesisHash', 'genesis', 0)  # There are no transactions
        genesisBlock.timestamp = 0  # This means the timestamp of the genesis block is constant
        return genesisBlock

    def toJson(self):
        """Will help display block in readable dictionary form"""
        data = {}
        data['blockCount'] = self.blockCount
        data['lastHash'] = self.lastHash
        data['signature'] = self.signature
        data['forger'] = self.forger
        data['timestamp'] = self.timestamp
        jsonTransactions = []
        for transaction in self.transactions:
            jsonTransactions.append(transaction.toJson())
        data['transactions'] = jsonTransactions
        return data

    def payload(self):
        """Generates same dictionary as toJson method but without signature"""
        jsonRepresentation = copy.deepcopy(self.toJson())
        jsonRepresentation['signature'] = ''
        return jsonRepresentation

    def sign(self, signature):
        """Adds signature to block"""
        self.signature = signature
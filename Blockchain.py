from Block import Block
from BlockchainUtils import BlockchainUtils
from AccountModel import AccountModel
from ProofOfStake import ProofOfStake


class Blockchain():
    """For creating and managing a linked list of blocks"""

    def __init__(self):
        self.blocks = [Block.genesis()]
        self.accountModel = AccountModel()  # Blockchain is aware of all of the accounts
        self.pos = ProofOfStake()

    def addBlock(self, block):
        """Adds a block to the blockchain and executes the transactions in the block"""
        self.executeTransactions(block.transactions)
        self.blocks.append(block)

    def toJson(self):
        """Will help display blockchain in readable dictionary form"""
        data = {}
        jsonBlocks = []
        for block in self.blocks:
            jsonBlocks.append(block.toJson())
        data['blocks'] = jsonBlocks
        return data

    def blockCountValid(self, block):
        """Checks if the blockCount is one greater than the previous block's blockCount"""
        if self.blocks[-1].blockCount == block.blockCount - 1:  # Note - indexing with -1 gets latest block
            return True
        else:
            return False

    def lastBlockHashValid(self, block):
        """Checks if the last hash is the hash of the previous block's hash"""
        latestBlockchainBlockHash = BlockchainUtils.hash(
            self.blocks[-1].payload()).hexdigest()
        if latestBlockchainBlockHash == block.lastHash:
            return True
        else:
            return False

    def getCoveredTransactionSet(self, transactions):
        """Gets all of the covered transactions"""
        coveredTransactions = []
        for transaction in transactions:
            if self.transactionCovered(transaction):
                coveredTransactions.append(transaction)
            else:
                print('transaction is not covered by sender')
        return coveredTransactions

    def transactionCovered(self, transaction):
        """Checks if a user has enough funds to perform a transaction"""
        if transaction.type == 'EXCHANGE':  # If a transaction is an exchange transaction it is always covered
            return True
        senderBalance = self.accountModel.getBalance(
            transaction.senderPublicKey)
        if senderBalance >= transaction.amount:
            return True
        else:
            return False

    def executeTransactions(self, transactions):
        """Will execute each transaction in a list of transactions"""
        for transaction in transactions:
            self.executeTransaction(transaction)

    def executeTransaction(self, transaction):
        """Will execute a transaction"""
        if transaction.type == 'STAKE':
            sender = transaction.senderPublicKey
            receiver = transaction.receiverPublicKey
            if sender == receiver:  # For the transaction to actually be of type stake, the sender and receiver public keys must be the same
                amount = transaction.amount
                self.pos.update(sender, amount)  # The stake is added
                self.accountModel.updateBalance(sender, -amount)  # The amount staked is deducted from balance
        else:
            sender = transaction.senderPublicKey
            receiver = transaction.receiverPublicKey
            amount = transaction.amount
            self.accountModel.updateBalance(sender, -amount)  # Subtract from sender
            self.accountModel.updateBalance(receiver, amount)  # Add to receiver

    def nextForger(self):
        """Returns the next forger"""
        lastBlockHash = BlockchainUtils.hash(
            self.blocks[-1].payload()).hexdigest()  # Gets last block hash
        nextForger = self.pos.forger(lastBlockHash)
        return nextForger

    def createBlock(self, transactionsFromPool, forgerWallet):
        """Creates a new block"""
        coveredTransactions = self.getCoveredTransactionSet(
            transactionsFromPool)  # See which transactions are covered
        self.executeTransactions(coveredTransactions)  # Executes covered transactions
        newBlock = forgerWallet.createBlock(
            coveredTransactions, BlockchainUtils.hash(self.blocks[-1].payload()).hexdigest(), len(self.blocks))  # Creates new block and adds signature (uses method in wallet)
        self.blocks.append(newBlock)  # Adds new block to blockchain
        return newBlock  # Block is returned so that it can be broadcast

    def transactionExists(self, transaction):
        """Checks if transaction is already in blockchain"""
        for block in self.blocks:  # Iterate through all blocks
            for blockTransaction in block.transactions:  # Iterate in block
                if transaction.equals(blockTransaction):
                    return True  # The transaction already exists in the blockchain
        return False

    def forgerValid(self, block):
        """Checks if forger is actually valid"""
        forgerPublicKey = self.pos.forger(block.lastHash)
        proposedBlockForger = block.forger
        if forgerPublicKey == proposedBlockForger:
            return True
        else:
            return False

    def transactionsValid(self, transactions):
        """Checks if transactions are actually valid"""
        coveredTransactions = self.getCoveredTransactionSet(transactions)
        if len(coveredTransactions) == len(transactions):
            return True
        return False
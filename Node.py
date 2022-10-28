from TransactionPool import TransactionPool
from Wallet import Wallet
from Blockchain import Blockchain
from SocketCommunication import SocketCommunication
from NodeAPI import NodeAPI
from Message import Message
from BlockchainUtils import BlockchainUtils
import copy


class Node():
    """The managing entity that runs the blockchain system in the network of nodes"""

    def __init__(self, ip, port, key=None):
        self.p2p = None
        self.ip = ip
        self.port = port
        self.blockchain = Blockchain()
        self.transactionPool = TransactionPool()
        self.wallet = Wallet()
        if key is not None:
            self.wallet.fromKey(key)  # Gets key pair from file

    def startP2P(self):
        """Starts socket communication"""
        self.p2p = SocketCommunication(self.ip, self.port)
        self.p2p.startSocketCommunication(self)

    def startAPI(self, apiPort):
        """Starts Node API"""
        self.api = NodeAPI()
        self.api.injectNode(self)
        self.api.start(apiPort)

    def handleTransaction(self, transaction):
        """Checks if transaction is valid and does not already exist - if valid it broadcasts it"""
        data = transaction.payload()
        signature = transaction.signature
        signerPublicKey = transaction.senderPublicKey
        signatureValid = Wallet.signatureValid(
            data, signature, signerPublicKey)  # Check if signature is valid
        transactionExists = self.transactionPool.transactionExists(transaction)  # Checks if transaction already exists in the pool
        transactionInBlock = self.blockchain.transactionExists(transaction)
        if not transactionExists and not transactionInBlock and signatureValid:  # If the signature is valid and the transaction is new, it is added to the pool
            self.transactionPool.addTransaction(transaction)
            message = Message(self.p2p.socketConnector,'TRANSACTION', transaction)
            encodedMessage = BlockchainUtils.encode(message)
            self.p2p.broadcast(encodedMessage)  # Broadcasts transaction as message
            forgingRequired = self.transactionPool.forgingRequired()  # Checks if forging is required
            if forgingRequired:
                self.forge()

    def handleBlock(self, block):
        """Broadcasts new block to all participants"""
        forger = block.forger
        blockHash = block.payload()
        signature = block.signature
        # Checks if block is valid for security purposes
        blockCountValid = self.blockchain.blockCountValid(block)
        lastBlockHashValid = self.blockchain.lastBlockHashValid(block)
        forgerValid = self.blockchain.forgerValid(block)
        transactionsValid = self.blockchain.transactionsValid(
            block.transactions)
        signatureValid = Wallet.signatureValid(blockHash, signature, forger)
        if not blockCountValid:
            self.requestChain()
        if lastBlockHashValid and forgerValid and transactionsValid and signatureValid:
            self.blockchain.addBlock(block)
            self.transactionPool.removeFromPool(block.transactions)
            message = Message(self.p2p.socketConnector, 'BLOCK', block)
            self.p2p.broadcast(BlockchainUtils.encode(message))

    def handleBlockchainRequest(self, requestingNode):
        """Sends blockchain to requesting node as a message"""
        message = Message(self.p2p.socketConnector,
                          'BLOCKCHAIN', self.blockchain)
        self.p2p.send(requestingNode, BlockchainUtils.encode(message))

    def handleBlockchain(self, blockchain):
        """Updates our blockchain"""
        localBlockchainCopy = copy.deepcopy(self.blockchain)  # Copy of own blockchain
        localBlockCount = len(localBlockchainCopy.blocks)  # Number of blocks in our blockchain
        receivedChainBlockCount = len(blockchain.blocks)  # Number of blocks in received blockchain
        if localBlockCount < receivedChainBlockCount:
            for blockNumber, block in enumerate(blockchain.blocks):  # Iterating through received blockchain
                if blockNumber >= localBlockCount:  # Until a new block is found
                    localBlockchainCopy.addBlock(block)
                    self.transactionPool.removeFromPool(block.transactions)
            self.blockchain = localBlockchainCopy

    def forge(self):
        """Checks if you are the forger and triggers block creation if necessary"""
        forger = self.blockchain.nextForger()
        if forger == self.wallet.publicKeyString():
            print('i am the forger')
            block = self.blockchain.createBlock(
                self.transactionPool.transactions, self.wallet)
            self.transactionPool.removeFromPool(
                self.transactionPool.transactions)  # Clears transaction pool by removing all transactions added to block
            message = Message(self.p2p.socketConnector, 'BLOCK', block)
            self.p2p.broadcast(BlockchainUtils.encode(message))  # The new block is broadcast
        else:
            print('i am not the forger')

    def requestChain(self):
        """Generating a message that requests the blockchain"""
        message = Message(self.p2p.socketConnector, 'BLOCKCHAINREQUEST', None)
        self.p2p.broadcast(BlockchainUtils.encode(message))



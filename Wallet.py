
from Cryptodome.PublicKey import RSA
from Transaction import Transaction
from Block import Block
from BlockchainUtils import BlockchainUtils
from Cryptodome.Signature import PKCS1_v1_5  # Used to generate and validate signatures


class Wallet():
    """For creating and managing key pairs"""

    def __init__(self):
        """To generate a key pair"""
        self.keyPair = RSA.generate(2048)  # Creates new RSA key pair (the argument is a model)

    def fromKey(self, file):
        """Creating key pair of first staker"""
        key = ''
        with open(file, 'r') as keyfile:
            key = RSA.importKey(keyfile.read())
        self.keyPair = key

    def sign(self, data):
        """To create a signature"""
        dataHash = BlockchainUtils.hash(data)  # Gets hash from data
        signatureSchemeObject = PKCS1_v1_5.new(self.keyPair)  # Creates object that will sign and validate signatures from key pair
        signature = signatureSchemeObject.sign(dataHash)  # Creates signature, in binary, which is the hash of the data encrypted with your private key
        return signature.hex()

    @staticmethod
    def signatureValid(data, signature, publicKeyString):
        """To check if a signature is valid"""
        signature = bytes.fromhex(signature)  # Gets signature in bytes
        dataHash = BlockchainUtils.hash(data)  # Gets hash from data
        publicKey = RSA.importKey(publicKeyString)  # Gets public key from string representation
        signatureSchemeObject = PKCS1_v1_5.new(publicKey)  # Provides public key to validate
        signatureValid = signatureSchemeObject.verify(dataHash, signature)  # Checks if signature is valid (gives Bool)
        return signatureValid

    def publicKeyString(self):  # Creates string representation of public key
        """Creates string representation of public key"""
        publicKeyString = self.keyPair.publickey().exportKey(
            'PEM').decode('utf-8')
        return publicKeyString

    def createTransaction(self, receiver, amount, type):
        """Creates a transaction"""
        transaction = Transaction(
            self.publicKeyString(), receiver, amount, type)  # Creates transaction
        signature = self.sign(transaction.payload())  # Creates signature
        transaction.sign(signature)  # Adds signature to transaction
        return transaction

    def createBlock(self, transactions, lastHash, blockCount):
        """Creates a block"""
        block = Block(transactions, lastHash,
                      self.publicKeyString(), blockCount)  # Creates block
        signature = self.sign(block.payload())  # Creates signature
        block.sign(signature)  # Adds your signature (signature of forger) to block
        return block
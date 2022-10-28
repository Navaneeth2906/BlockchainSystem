import uuid  # Library that generates a globally unique random ID
import time
import copy


class Transaction():
    """For creating and managing transactions"""

    def __init__(self, senderPublicKey, receiverPublicKey, amount, type):
        self.senderPublicKey = senderPublicKey
        self.receiverPublicKey = receiverPublicKey
        self.amount = amount
        self.type = type
        self.id = (uuid.uuid1()).hex  # Creates and assigns transaction ID in hexadecimal
        self.timestamp = time.time()  # States when a transaction was generated
        self.signature = ''

    def toJson(self):
        """Creates dictionary based on state of object"""
        return self.__dict__

    def sign(self, signature):
        """Sets the signature"""
        self.signature = signature

    def payload(self):
        """Generates same dictionary as toJson method but without signature"""
        jsonRepresentation = copy.deepcopy(self.toJson())  # Gets copy of toJson representation (without altering)
        jsonRepresentation['signature'] = ''  # Removes signature
        return jsonRepresentation

    def equals(self, transaction):
        """Checks if a transaction is equal to another"""
        if self.id == transaction.id:  # If IDs are same they are equal
            return True
        else:
            return False

from Cryptodome.Hash import SHA256
import json
import jsonpickle


class BlockchainUtils():
    """Contains various static methods for the Blockchain system"""

    @staticmethod  # Static method means 'self' is not needed - they are methods bound to a class rather than an object
    def hash(data):
        """Creates a hash of data using  the SHA-256 hash algorithm"""
        dataString = json.dumps(data)  # Takes data and makes it into string form
        dataBytes = dataString.encode('utf-8')  # Converts string to binary representation
        dataHash = SHA256.new(dataBytes)  # Hashes data
        return dataHash

    @staticmethod
    def encode(objectToEncode):
        """Encodes message object into a format that is allowed to be sent across the network"""
        return jsonpickle.encode(objectToEncode, unpicklable=True)

    @staticmethod
    def decode(encodedObject):
        """Recreates object"""
        return jsonpickle.decode(encodedObject)
class AccountModel():
    """For holding information about and managing all the accounts in the network"""

    def __init__(self):
        self.accounts = []  # List of public keys of all the participants in the network
        self.balances = {}  # Mapping between public key and token

    def addAccount(self, publicKeyString):
        """Adds account and sets balance to zero"""
        if not publicKeyString in self.accounts:
            self.accounts.append(publicKeyString)
            self.balances[publicKeyString] = 0

    def getBalance(self, publicKeyString):
        """Returns balance in account"""
        if publicKeyString not in self.accounts:  # If an account does not exist, it is added
            self.addAccount(publicKeyString)
        return self.balances[publicKeyString]

    def updateBalance(self, publicKeyString, amount):
        """Updates balance in account"""
        if publicKeyString not in self.accounts:  # If an account does not exist, it is added
            self.addAccount(publicKeyString)
        self.balances[publicKeyString] += amount
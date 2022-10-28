

class TransactionPool():
    """For creating and managing a list of transactions"""

    def __init__(self):
        self.transactions = []  # A list of transactions

    def addTransaction(self, transaction):
        """Adds transaction to list"""
        self.transactions.append(transaction)

    def transactionExists(self, transaction):
        """Checks if a transaction exists in the list"""
        for poolTransaction in self.transactions:
            if poolTransaction.equals(transaction):  # Uses equals method from Transactions
                return True
        return False

    def removeFromPool(self, transactions):
        """Removes transactions from the pool, i.e., if they have been added to a block"""
        newPoolTransactions = []
        for poolTransaction in self.transactions:
            insert = True
            for transaction in transactions:
                if poolTransaction.equals(transaction):
                    insert = False
            if insert == True:
                newPoolTransactions.append(poolTransaction)
        self.transactions = newPoolTransactions

    def forgingRequired(self):
        """Decides if it is time to create a new block"""
        if len(self.transactions) >= 3:  # If the number of transactions in the pool have surpassed a certain number (one)
            return True
        else:
            return False
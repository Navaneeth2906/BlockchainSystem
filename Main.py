from Transaction import Transaction
from Wallet import Wallet
from TransactionPool import TransactionPool
from Block import Block
from Blockchain import Blockchain
import pprint
from BlockchainUtils import BlockchainUtils
from AccountModel import AccountModel
from Node import Node
import sys

if __name__ == '__main__':
    ip = sys.argv[1]
    port = int(sys.argv[2])
    apiPort = int(sys.argv[3])
    keyFile = None
    if len(sys.argv) > 4:
        keyFile = sys.argv[4]

    node = Node(ip, port, keyFile)
    node.startP2P()
    node.startAPI(apiPort)

'''RUN EACH OF THE FOLLOWING FOUR COMMANDS IN A SEPARATE TERMINAL WINDOW'''
# python3 Main.py localhost 10001 5000 keys/genesisPrivateKey.pem
# python3 Main.py localhost 10003 5003 keys/stakerPrivateKey.pem
# python3 Main.py localhost 10002 5001
'''Look at Interaction.py code'''
# python3 Interaction.py
'''To see the blockchain of each node, click on the link generated and look at the NodeAPI file to see all possible routes'''

'''As you can see, when you instantiate a node, you can also specify a public key if they are to be a possible forger'''



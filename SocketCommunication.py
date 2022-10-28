from p2pnetwork.node import Node
from PeerDiscoveryHandler import PeerDiscoveryHandler
from SocketConnector import SocketConnector
from BlockchainUtils import BlockchainUtils
import json

class SocketCommunication(Node):
    """To allow P2P communication with other nodes"""

    def __init__(self, ip, port):
        super(SocketCommunication, self).__init__(ip, port, None)
        self.peers = []  # List of connected nodes
        self.peerDiscoveryHandler = PeerDiscoveryHandler(self)  # Creates peer discovery handler
        self.socketConnector = SocketConnector(ip, port)

    def connectToFirstNode(self):
        """Creates connection with very first node"""
        if self.socketConnector.port != 10001:  # Checks that you are not the very first node
            self.connect_with_node('localhost', 10001)

    def startSocketCommunication(self, node):
        """Uses provided IP and port (which form a socket) to open communication with other nodes"""
        self.node = node
        self.start()
        self.peerDiscoveryHandler.start()
        self.connectToFirstNode()

    def inbound_node_connected(self, connected_node):
        """Performs 'handshake' when node connects to you"""
        self.peerDiscoveryHandler.handshake(connected_node)

    def outbound_node_connected(self, connected_node):
        """Performs 'handshake' when you connect to a node"""
        self.peerDiscoveryHandler.handshake(connected_node)

    def node_message(self, connected_node, message):
        """To send a message to a connected node"""
        message = BlockchainUtils.decode(json.dumps(message))  # Decodes message back to object
        if message.messageType == 'DISCOVERY':
            self.peerDiscoveryHandler.handleMessage(message)
        elif message.messageType == 'TRANSACTION':
            transaction = message.data
            self.node.handleTransaction(transaction)
        elif message.messageType == 'BLOCK':
            block = message.data
            self.node.handleBlock(block)
        elif message.messageType == 'BLOCKCHAINREQUEST':
            self.node.handleBlockchainRequest(connected_node)
        elif message.messageType == 'BLOCKCHAIN':
            blockchain = message.data
            self.node.handleBlockchain(blockchain)

    def send(self, receiver, message):
        """Sends message to specific node"""
        self.send_to_node(receiver, message)

    def broadcast(self, message):
        """Broadcasts message to all connected nodes"""
        self.send_to_nodes(message)
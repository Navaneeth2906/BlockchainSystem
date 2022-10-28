import threading
import time
from Message import Message
from BlockchainUtils import BlockchainUtils

class PeerDiscoveryHandler():
    """Broadcasts known connections and checks if new connections, with new nodes, are available"""

    def __init__(self, node):
        self.socketCommunication = node

    def start(self):
        """Starts the status and discovery method in their own thread"""
        statusThread = threading.Thread(target=self.status, args=())
        statusThread.start()
        discoveryThread = threading.Thread(target=self.discovery, args=())
        discoveryThread.start()

    def status(self):
        """Broadcasting all the nodes you are connected to"""
        while True:
            print('Current Connections:')
            for peer in self.socketCommunication.peers:
                print(str(peer.ip) + ':' + str(peer.port))  # Displays socket of peer (which is the port number added to the IP address)
            time.sleep(5)

    def discovery(self):
        """Checking for new nodes by broadcasting a handshake message"""
        while True:
            handshakeMessage = self.handshakeMessage()
            self.socketCommunication.broadcast(handshakeMessage)
            time.sleep(10)

    def handshake(self, connected_node):
        """Performs a handshake with a connected node"""
        handshakeMessage = self.handshakeMessage()
        self.socketCommunication.send(connected_node, handshakeMessage)

    def handshakeMessage(self):
        """Creates handshake message that contains data of a node's known nodes"""
        ownConnector = self.socketCommunication.socketConnector  # Own connector
        ownPeers = self.socketCommunication.peers  # Own peers
        data = ownPeers
        messageType = 'DISCOVERY'
        message = Message(ownConnector, messageType, data)
        encodedMessage = BlockchainUtils.encode(message)
        return encodedMessage

    def handleMessage(self, message):
        """If not in already, add message sender to peers list and then connect with new peers in the message sender's peer list"""
        peersSocketConnector = message.senderConnector  # Socket connector of sender
        peersPeerList = message.data  # Peer list of sender
        newPeer = True
        for peer in self.socketCommunication.peers:
            if peer.equals(peersSocketConnector):
                newPeer = False
        if newPeer:  # If the sender does not exist in your peers list, add them
            self.socketCommunication.peers.append(peersSocketConnector)

        for peersPeer in peersPeerList:
            peerKnown = False
            for peer in self.socketCommunication.peers:
                if peer.equals(peersPeer):
                    peerKnown = True
            if not peerKnown and not peersPeer.equals(self.socketCommunication.socketConnector):  # If a node is not in your peers list (and is not you), connect with it
                self.socketCommunication.connect_with_node(
                    peersPeer.ip, peersPeer.port)


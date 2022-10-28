class SocketConnector():
    """For saving the IP and port of a connection"""

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def equals(self, connector):
        """To see if a connector is same as another"""
        if connector.ip == self.ip and connector.port == self.port:
            return True
        else:
            return False
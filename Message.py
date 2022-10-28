

class Message():
    """For creating messages"""

    def __init__(self, senderConnector, messageType, data):
        self.senderConnector = senderConnector  # Where to send message
        self.messageType = messageType
        self.data = data

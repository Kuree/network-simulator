class Device:
    def __init__(self, id):
        self.id = id

    def on_receive(self, packet):
        pass

    def send(self, payload):
        pass

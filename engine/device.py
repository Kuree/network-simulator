class Device:
    ''' the base class for simulation node
    '''
    def __init__(self, id):
        self.id = id
        self.__is_active = True

    def _on_receive(self, packet):
        ''' this will be called any time a transmission is made to the medium
        '''
        if self.__is_active:
            self.on_receive(packet)
    
    def is_active(self):
        return self.__is_active

    def sleep(self):
        self.__is_active = False

    def wake_up(self):
        self.__is_active = True

    def on_receive(self, packet):
        pass

    def _send(self, payload, time=1):
        pass

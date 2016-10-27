class Device:
    ''' the base class for simulation node
    '''
    def __init__(self, id):
        self.id = id
        self._medium = []
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

    def _send(self, payload, time=1, medium_index = 0):
        if len(self._medium) == 0:
            raise Exception("Device has no medium attached")
        self._medium[medium_index][1](payload, time)

    def is_medium_busy(self, medium_index = 0):
        if len(self._medium) == 0:
            return False # if there is no medium attach to the device
        return self._medium[medium_index][0].is_busy()

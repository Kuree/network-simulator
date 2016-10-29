import random

class Device:
    ''' the base class for simulation node
    '''
    def __init__(self, id, seed = 1, jitter_range = 0.1):
        self.id = id
        self.random = random.Random(seed)
        self._medium = []
        self.__is_active = True
        self.jitter_range = jitter_range

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

    def jitter(self):
        ''' return the random jitter for the device
        '''
        jitter = (self.random.random() - 0.5) * self.jitter_range
        return jitter

    def send(self, payload, duration=1, size = 1, medium_index = 0):
        if len(self._medium) == 0:
            raise Exception("Device has no medium attached")
        self._medium[medium_index][1](payload, duration, size)

    def is_medium_busy(self, medium_index = 0):
        if len(self._medium) == 0:
            return False # if there is no medium attach to the device
        return self._medium[medium_index][0].is_busy()

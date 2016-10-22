import simpy
import blinker

# this defines the transmission medium

class TransmissionPacket:
    def __init__(self, id, payload):
        #self.env = env
        self.payload = payload
        self.id = id

class TransmissionMedium:
    def __init__(self, env, medium_name = "signal"):
        self.env = env
        self.__signal = blinker.signal(medium_name)

        # is_busy is useful for CSMA based protocol
        self.__is_busy = False
        
        self.__active_time = 0

    def __on_traffic(self, packet):
        print(packet.time)

    def add_device(self, device):
        ''' this method adds a device to the transmission medium
        '''
        self.__subscribe(device._on_receive)
        def _transmit(payload, time):
            self.__transmit(device, payload, time)
        device._send = _transmit

    def __subscribe(self, callback):
        self.__signal.connect(callback)

    def __transmit(self, device, payload, time):
        ''' called when device wants to transmit data
        '''
        self.__signal.send(TransmissionPacket(device.id, payload))
        self.__active_time = time

        # note that only one can actually transmite
        # hence need a way to indicate intereference
        self.__is_busy = True
    
    def is_busy(self):
        return self.__is_busy

    def run(self):
        while True:
            if self.__is_busy:
                # might need mutx to protect it
                yield self.env.timeout(self.__active_time)
                self.__active_time = 0
                self.__is_busy = False
            else:
                yield self.env.timeout(0.001)


import simpy
import blinker


# this defines the transmission medium

class TransmissionPacket:
    def __init__(self, env, id, content):
        self.env = env
        self.content = content
        self.id = id

    def _log(self, logger):
        logger.log(self.env.time, id)


class TransmissionMedium:
    def __init__(self, env, medium_name = "signal"):
        self.env = env
        self.__signal = blinker.signal(medium_name)

    def subscribe(self, callback):
        self.__signal.connect(callback)

    def transmit(self, packet):
        self.__signal.send(packet)


if __name__ == "__main__":
    def r(obj):
        print(obj)

    env = simpy.Environment()
    t = TransmissionMedium(env)

    t.subscribe(r)

    t.transmit("hello")

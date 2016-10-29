import bootstrap

import simpy
from engine import BaseStation, Device, TransmissionMedium
 
def test(env):
    MESSAGE1 = "TEST1"
    MESSAGE2 = "TEST2"
    def process(packet):
        # only receives test1 becaus we let test2 collides with other packets
        assert packet.payload == MESSAGE1
    bs = BaseStation(env = env, id =1)
    bs.process = process # simply way to override the method
    d1 = Device(2)
    d2 = Device(3)
    t = TransmissionMedium(env)

    t.add_device(bs)
    t.add_device(d1)
    t.add_device(d2)
    d1.send(MESSAGE1, 1)
    yield env.timeout(1.1)
    # both message should be dropped
    d2.send(MESSAGE2, 2)
    yield env.timeout(1.1)
    d1.send(MESSAGE2)
    assert t.is_busy() == True


if __name__ == "__main__":
    env = simpy.Environment()
    env.process(test(env))

    env.run(until = 20)

import bootstrap

import simpy
from engine import Device, TransmissionMedium
 
def test(env):
    MESSAGE1 = "TEST1"
    MESSAGE2 = "TEST2"
    def process(packet):
        # only receives test1 becaus we let test2 collides with other packets
        assert packet.payload == MESSAGE1
    bs = Device(env = env, id =1, rates=[20])
    bs.process = process # simply way to override the method
    d1 = Device(2, env, rates=[20])
    d2 = Device(3, env, rates=[20])
    t = TransmissionMedium(env)

    t.add_device(bs)
    t.add_device(d1)
    t.add_device(d2)
    d1.send(MESSAGE1, 1 * d1.MTU)
    yield env.timeout(1.1)
    # both message should be dropped
    d2.send(MESSAGE2, 2 * d2.MTU)
    yield env.timeout(1.1)
    d1.send(MESSAGE2, 1 * d1.MTU)
    assert t.is_busy() == True


if __name__ == "__main__":
    env = simpy.Environment()
    env.process(test(env))

    env.run(until = 20)

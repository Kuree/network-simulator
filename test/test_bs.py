import bootstrap

import simpy
from engine import BaseStation, Device, TransmissionMedium
 
def test(env):

    bs = BaseStation(env = env, id =1)
    d1 = Device(2)
    d2 = Device(3)
    t = TransmissionMedium(env)

    t.add_device(bs)
    t.add_device(d1)
    t.add_device(d2)
    yield env.timeout(1)

if __name__ == "__main__":
    env = simpy.Environment()
    env.process(test(env))

    env.run(until = 20)

from pyns.engine import TransmissionMedium
import simpy
from pyns.engine import Device
import logging

def test_medium():
    env = simpy.Environment()
    env.process(simpy_medium(env))
    env.run(until=10)
   

def simpy_medium(env):
    def listen(packet):
        assert packet.payload == TEST_MESSAGE1
    TEST_MESSAGE1 = "TEST1"
    TEST_MESSAGE2 = "TEST2"
    
    t = TransmissionMedium(env)
    d1 = Device(1, env, [20])
    d2 = Device(2, env, [20])
    d1.on_receive += listen
    t.add_device(d1)
    t.add_device(d2)
    # this one should be successful
    d1.send(TEST_MESSAGE1, d1.MTU)
    yield env.timeout(1.1)
    assert t.is_busy(d1) == False
    d1.sleep()
    # this should be sucessful as well
    d1.send(TEST_MESSAGE2, 2 * d1.MTU)
    yield env.timeout(1.1)
    assert t.is_busy(d1) == True
    yield env.timeout(1.1)
    assert t.is_busy(d1) == False
    # collision
    d1.send(TEST_MESSAGE1, 2 * d1.MTU)
    yield env.timeout(1)
    d2.wake_up()
    # collision
    d2.send(TEST_MESSAGE1, 2 * d2.MTU)
    yield env.timeout(1.1)
    assert t.is_busy(d2) == True
    yield env.timeout(1.1)
    assert t.is_busy(d2) == False

if __name__ == "__main__":
    test_medium()

import bootstrap

from engine import TransmissionMedium
import simpy
from engine import Device
import logging

if __name__ == "__main__":
    TEST_MESSAGE1 = "TEST1"
    TEST_MESSAGE2 = "TEST2"
    def listen(packet):
        assert packet.payload == TEST_MESSAGE1

    env = simpy.Environment()

    def test():
        logger = logging.getLogger("signal")
        logger.setLevel(logging.DEBUG)
        #ch = logging.StreamHandler()
        #ch.setLevel(logging.ERROR)
        #logger.addHandler(ch)
        #logger.debug("test")
        t = TransmissionMedium(env)
        d1 = Device(1)
        d2 = Device(2)
        d1.on_receive = listen
        t.add_device(d1)
        t.add_device(d2)
        # this one should be successful
        d1._send(TEST_MESSAGE1, 1)
        yield env.timeout(1)
        assert env.now == 1
        assert t.is_busy() == False
        d1.sleep()
        # this should be sucessful as well
        d1._send(TEST_MESSAGE2, 2)
        yield env.timeout(1)
        assert env.now == 2
        assert t.is_busy() == True
        yield env.timeout(1)
        assert env.now == 3
        assert t.is_busy() == False
        # collision
        d1._send(TEST_MESSAGE1, 2)
        yield env.timeout(1)
        d2.wake_up()
        # collision
        d2._send(TEST_MESSAGE1, 2)
        yield env.timeout(1)
        assert env.now == 5
        assert t.is_busy() == True
        yield env.timeout(1)
        assert t.is_busy() == False
    env.process(test())
    env.run(until=10)


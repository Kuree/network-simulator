from pyns.phy import PHYLayer, BPSK
from pyns.engine import Device, TransmissionMedium
import math
import simpy

def test_FSPL():
    layer = PHYLayer(0)
    p1 = (0, 0)
    p2 = (0.1, 0.1)
    frequency = 10 * 10**6
    loss = layer.get_path_loss(p1, p2, frequency)
    assert abs(loss - 76) < 0.5 # test it against standard RF packege

def test_BPSK():
    bpsk = BPSK(0)
    ber = bpsk.compute_ber(12, True)
    assert abs(math.log(ber, 10) + 8) < 0.05


def test_path_loss():
    rates = [20]
    env = simpy.Environment()
    d1 = Device(env = env, id =0, rates=[20], lat=0.1, lng=0.1)
    d2 = Device(env = env, id =1, rates=[20], lat=0.1, lng=0.1)
    layer = PHYLayer(120)
    t = TransmissionMedium(env, layer=layer)

    t.add_device(d1)
    t.add_device(d2)

    def on_receive1(packet):
        assert packet.id == 0
    
    def on_receive2(packet):
        assert False # should not receive

    
    d2.on_receive += on_receive1

    def sim_test():
        d1.send("test", size = 10)
        yield env.timeout(1)

        d2.on_receive -= on_receive1
        d2.on_receive += on_receive2

        # test no receive
        t.layer.threshold = 10
        d1.send("test", size = 10)

        yield env.timeout(1)

    env.process(sim_test())

    env.run(until=10)

def test_ebn0():
    layer = PHYLayer(42) # 42 is the meaning of life
    point1 = (0, 0)
    point2 = (0.1, 0.1)
    ebno = layer.get_ebn0(point1, point2, noise)
    pass


if __name__ == "__main__":
    test_FSPL()
    test_BPSK()
    test_path_loss()

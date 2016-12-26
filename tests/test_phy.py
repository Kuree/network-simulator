from pyns.phy import PHYLayer, BPSK, QPSK
from pyns.engine import Device, TransmissionMedium
from pyns.phy import utility, get_planit_path_loss
import math
import simpy

def test_FSPL():
    layer = PHYLayer(0, 10000, 1)
    p1 = (0, 0)
    p2 = (0.1, 0.1)
    frequency = 10 * 10**6 # 10 MHz
    loss = layer.get_path_loss(p1, p2, frequency)
    assert abs(loss - 76) < 0.5 # test it against standard RF packege

def test_BPSK():
    bpsk = BPSK(0)
    ber = bpsk.compute_ber(12, True)
    assert abs(math.log(ber, 10) + 8) < 0.05

def test_path_loss():
    rates = [20]
    env = simpy.Environment()
    d1 = Device(env = env, id =0, rates=[20], lat=0, lng=0)
    d2 = Device(env = env, id =1, rates=[20], lat=0.1, lng=0.1)
    layer = PHYLayer(120, 10000, 1) # 10 KHz bandwidth. won't be used in the simulation
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


def test_noise_power():
    # based on example 3.1.4 page 88
    noise_figure = 6
    bandwidth = 20* (10**6)
    noise_power = utility.get_noise_power(noise_figure, bandwidth)
    assert abs(noise_power - 10**(-125 / 10)) < 0.01

def test_get_prx_min():
    # page 135 example 3.7.1 (b)
    ebn0 = 10 ** ( 10.2/10)
    Rb = 30 * (10**6)
    B = 20 * (10**6)
    noise_figure = 6
    Pn = utility.get_noise_power(noise_figure, B)
    prx_min = utility.get_prx_min(ebn0, Rb, B, Pn)
    prx_min = 10 * math.log(prx_min * 1000, 10)
    assert abs(prx_min + 83) < 0.05

def test_ebn0():
    # reversed the problem using well-selected points
    # page 135 example 3.7.1 (c)
    layer = PHYLayer(42, 20* (10**6), 1) # 20 Mhz bandwidth
    point1 = (0, 0)
    point2 = (0.00069,0.00068) # ensure the distance is around 110 meters
    rate = 30 * (10**6) # 30 Mbit/s
    frequency = 5 * (10 ** 9) # 5 Ghz
    noise_figure = 6 # 6 db
    gain = 2 # dbi
    ptx = 0.1 # 100 mw
    ebn0 = layer.get_ebn0(ptx, point1, point2, rate, frequency, noise_figure, gain, gain)
    assert abs(ebn0 - 10.47) < 0.1


def test_planit():
    url = "https://www.eg.bucknell.edu/planit/api/"
    api_key = "eyJhbGciOiJIUzI1NiJ9.IjU4M2M3Y2EyNDdlZmE2MzgwMmI1NzNjOCI._fMAFEPDDGiAv9z6uhAKZVeBQx8TyCH1WzkzZzuXQew"

    get_path_loss = get_planit_path_loss(url, api_key)


    a=(-76.881249, 40.954899)
    b=(-76.897619, 40.955291)

    assert get_path_loss(a, b, 900*10**6) == 136.1580257011434


if __name__ == "__main__":
    test_FSPL()
    test_BPSK()
    test_path_loss()
    test_ebn0()
    test_get_prx_min()
    test_noise_power()
    test_planit()

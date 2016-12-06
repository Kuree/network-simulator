from pyns.phy import PHYLayer, BPSK
import math


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


if __name__ == "__main__":
    test_FSPL()
    test_BPSK()

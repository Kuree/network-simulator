from pyns.phy import PHYLayer
import scipy.special
import math


class BPSK(PHYLayer):
    def __init__(self, threshold, bandwidth = 12500):
        super().__init__(threshold, bandwidth, 1)

    def compute_ber(self, ebn0, is_log=False):
        # use in db
        if is_log: ebn0 = 10 ** (ebn0 / 10)
        return 0.5 * scipy.special.erfc(math.sqrt(ebn0))

class QPSK(PHYLayer):
    def __init__(self, threshold, bandwidth = 12500):
        super().__init__(threshold, bandwidth, 2)

    def compute_ber(self, ebn0, is_log=False):
        # use in db
        if is_log: ebn0 = 10 ** (ebn0 / 10)
        return 2 * scipy.special.erfc(math.sqrt(2 * ebn0)) + \
                scipy.special.erfc(math.sqrt(4 * ebn0))



from pyns.phy import PHYLayer
import scipy.special
import math


class BPSK(PHYLayer):
    def __init__(self, threshold):
        super().__init__(threshold)

    def compute_ber(self, ebn0, is_log=False):
        # use in db
        if is_log: ebn0 = 10 ** (ebn0 / 10)
        return 0.5 * scipy.special.erfc(math.sqrt(ebn0))



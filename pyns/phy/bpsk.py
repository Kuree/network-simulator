from pyns.phy import PHYLayer
import scipy.special

class BPSK(PHYLayer):
    def __init__(self, threshold):
        super().__init__(threshold)

    def compute_ber(self, ebn0, is_log=False):
        # use in db
        if not is_log: ebn0 = 10 ** (ebn0 / 20)
        return 0.5 * scipy.special.erfc(ebn0)


b = BPSK(10)
print(b.compute_per(7, 20))

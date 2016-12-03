import math


def get_dbw(watts):
    return 10 * math.log(watts)

def get_prx(p_tx, gtx, grx, loss):
    '''
    get received signal power
    page 134
    ptx: transmitted power, dbm
    gtx: gain of the transmit antenna, dbi
    grx: gain of the receive antenna, dbi
    loss: path loss, db
    '''
    return ptx + gtx + grx - loss


def get_prx_min(ebn0, Rb, B, Pn):
    '''
    get minimum required received signal power
    page 133
    ebn0: required ebn0
    Rb: bit rate bits/second
    B: bandwidth
    Pn: noise power
    NOTE: this is not in db
    '''
    return ebn0 * Rb / B * Pn


def get_noise_power(noise_figure, T=293):
    ''' 
    get noise power based on noise figure
    page 133
    noise_figure: receiver noise figure, db
    T: temperature, K
    B: Nyquist bandwidth, hz
    return Pn
    '''
    k = 1.38064852 # this is boltzmann's constant
    return k * T * 10**(noise_figure / 10) * B




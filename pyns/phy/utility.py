import math


def get_db(value):
    return 10 * math.log(value)

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

def get_ebn0(self, Rb, B, Pn, prx):
    return prx / Pn * B / Rb


def get_prx_min(ebn0, Rb, B, Pn):
    '''
    get minimum required received signal power
    page 133
    ebn0: required ebn0
    Rb: bit rate bits/second
    B: bandwidth
    Pn: noise power
    return prx

    NOTE 
    ----
    This is not in db
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


def get_distance(origin, destination):
    '''returns Haversine distance between two points in km
    '''
    # this is from https://gist.github.com/rochacbruno/2883505
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371 # km

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d

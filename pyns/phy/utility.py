import math


def get_db(value):
    return 10 * math.log(value, 10)

def get_prx(ptx, gtx, grx, loss):
    '''
    get received signal power
    page 134
    ptx: transmitted power, db
    gtx: gain of the transmit antenna, dbi
    grx: gain of the receive antenna, dbi
    loss: path loss, db
    '''
    return ptx - 30 + gtx + grx - loss # minus 30 to convert dbm to db

def get_ebn0(Rb, B, Pn, prx, use_log = False):
    print("Rb", Rb, "B", B, "Pn", Pn, "prx", prx)
    if use_log:
        return prx - get_db(Pn) + get_db(B) - get_db(Rb)
    else:
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


def get_noise_power(noise_figure, B, T=293):
    ''' 
    get noise power based on noise figure
    page 133
    noise_figure: receiver noise figure, db
    T: temperature, K
    B: Nyquist bandwidth, hz
    return Pn
    '''
    k = 1.38064852 * (10** -23) # this is boltzmann's constant
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

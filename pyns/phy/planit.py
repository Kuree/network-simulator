import requests
import json

GLOBAL_CACHE = {}

def get_planit_path_loss(entry_point, api_key):
    global GLOBAL_CACHE
    args = {"key": api_key}
    service="pathloss"
    itwom = "itwomparams"
    if entry_point[-1] == "/":
        url = entry_point + service
        url_itwom = entry_point + itwom
    else:
        url = "{0}/{1}".format(entry_point, service)
        url_itwom = "{0}/{1}".format(entry_point, itwom)
    # get itwom parameters
    r = requests.post(url_itwom, json=args)
    itwomparam = r.json()["result"]
    def get_path_loss(point1, point2, frequency):
        if frequency in GLOBAL_CACHE and (point1, point2) in GLOBAL_CACHE[frequency]:
            return GLOBAL_CACHE[frequency][(point1, point2)]
        freq = frequency / 10**6 # switch to MHz
        itwomparam["freq_mhz"] = freq
        args["src"] = point1
        args["dst"] = point2
        args["itowmparam"] = itwomparam
        r = requests.post(url, json=args)
        result = r.json()[0]
        if frequency not in GLOBAL_CACHE:
            GLOBAL_CACHE[frequency] = {}
        GLOBAL_CACHE[frequency][(point1, point2)] = result
        return result
    return get_path_loss


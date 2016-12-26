import requests
import json


def get_planit_path_loss(entry_point, api_key):
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
        frequency /= 10**6 # switch to MHz
        itwomparam["freq_mhz"] = frequency
        args["src"] = point1
        args["dst"] = point2
        args["itowmparam"] = itwomparam
        r = requests.post(url, json=args)
        result = r.json()
        return result[0]
    return get_path_loss


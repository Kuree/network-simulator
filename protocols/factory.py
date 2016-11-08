from . import TDMANode, TDMABaseStation
from . import CSMANode, CSMABaseStation
from . import LPDQNode, LPDQBaseStation

import json

class ProtocolType:
    TDMA = 1
    CSMA = 2
    LPDQ = 3

def create_basestation(protocol_type, id, env, config = "config.json"):
    with open(config) as f:
        config_data = json.load(f)
    args = config_data[protocol_type]
    args["id"] = id
    args["env"] = env
    if protocol_type == ProtocolType.TDMA:
        return TDMABaseStation(*args)
    else if protocol_type == ProtocolType.CSMA:
        return CSMABaseStation(*args)
    else if protocol_type == ProtocolType.LPDQ:
        return LPDQBaseStation(*args)
    return None

def create_node(protocol_type, id, env, config = "config.json"):
    with open(config) as f:
        config_data = json.load(f)
    args = config_data[protocol_type]
    args["id"] = id
    args["env"] = env
    if protocol_type == ProtocolType.TDMA:
        return TDMANode(*args)
    else if protocol_type == ProtocolType.CSMA:
        return CSMANode(*args)
    else if protocol_type == ProtocolType.LPDQ:
        return LPDQNode(*args)
    return None




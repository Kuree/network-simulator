from . import TDMANode, TDMABaseStation
from . import CSMANode, CSMABaseStation
from . import LPDQNode, LPDQBaseStation

import json
import inspect

class ProtocolType:
    TDMA = 1
    CSMA = 2
    LPDQ = 3

def create_basestation(protocol_type, id, env, config, special_arg = None):
    with open(config) as f:
        args = json.load(f)
    args["id"] = id
    args["env"] = env
    if protocol_type == ProtocolType.TDMA:
        args = __process_args(TDMABaseStation.__init__, args, special_arg)
        return TDMABaseStation(**args)
    elif protocol_type == ProtocolType.CSMA:
        args = __process_args(CSMABaseStation.__init__, args, special_arg)
        return CSMABaseStation(**args)
    elif protocol_type == ProtocolType.LPDQ:
        args = __process_args(LPDQBaseStation.__init__, args, special_arg)
        return LPDQBaseStation(**args)
    return None

def create_node(protocol_type, id, env, config, special_arg = None):
    with open(config) as f:
        args = json.load(f)
    args["id"] = id
    args["env"] = env
    if protocol_type == ProtocolType.TDMA:
        args = __process_args(TDMANode.__init__, args, special_arg)
        return TDMANode(**args)
    elif protocol_type == ProtocolType.CSMA:
        args = __process_args(CSMANode.__init__, args, special_arg)
        return CSMANode(**args)
    elif protocol_type == ProtocolType.LPDQ:
        args = __process_args(LPDQNode.__init__, args, special_arg)
        return LPDQNode(**args)
    return None

def __process_args(func, args, special_arg):
    # remove unused args
    func_args = inspect.getargspec(func).args
    key_list = args.keys()
    # load the special arg
    for key in special_arg:
        args[key] = special_arg[key]
    
    args = {k:v for k, v in args.items() if k in func_args}
    return args


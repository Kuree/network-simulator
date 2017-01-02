from . import TDMANode, TDMABaseStation
from . import CSMANode, CSMABaseStation
from . import LPDQNode, LPDQBaseStation
from . import DQNNode, DQNBaseStation
from . import ALOHANode, ALOHABaseStation
import json
import inspect

class ProtocolType:
    TDMA = 0
    CSMA = 1
    LPDQ = 2
    DQN  = 3
    ALOHA = 4

SPECIAL_ATTRIBUTES = ["lat", "lng", "path_loss"]

def create_basestation(protocol_type, id, env, config, special_arg = None):
    args = __load_config(config)
    args["id"] = id
    args["env"] = env
    bs = None
    if protocol_type == ProtocolType.TDMA:
        args = __process_args(TDMABaseStation.__init__, args, special_arg)
        bs = TDMABaseStation(**args)
    elif protocol_type == ProtocolType.CSMA:
        args = __process_args(CSMABaseStation.__init__, args, special_arg)
        bs = CSMABaseStation(**args)
    elif protocol_type == ProtocolType.LPDQ:
        args = __process_args(LPDQBaseStation.__init__, args, special_arg)
        bs = LPDQBaseStation(**args)
    elif protocol_type == ProtocolType.DQN:
        args = __process_args(DQNBaseStation.__init__, args, special_arg)
        bs = DQNBaseStation(**args)
    elif protocol_type == ProtocolType.ALOHA:
         args = __process_args(ALOHABaseStation.__init__, args, special_arg)
         bs = ALOHABaseStation(**args)
    
    for name in SPECIAL_ATTRIBUTES:
        __set_attributes(bs, config, name)

    return bs

def create_node(protocol_type, id, env, config, special_arg = None):
    args = __load_config(config)
    args["id"] = id
    args["env"] = env
    node = None
    if protocol_type == ProtocolType.TDMA:
        args = __process_args(TDMANode.__init__, args, special_arg)
        node = TDMANode(**args)
    elif protocol_type == ProtocolType.CSMA:
        args = __process_args(CSMANode.__init__, args, special_arg)
        node = CSMANode(**args)
    elif protocol_type == ProtocolType.LPDQ:
        args = __process_args(LPDQNode.__init__, args, special_arg)
        node = LPDQNode(**args)
    elif protocol_type == ProtocolType.DQN:
        args = __process_args(DQNNode.__init__, args, special_arg)
        node = DQNNode(**args)
    elif protocol_type == ProtocolType.ALOHA:
        args = __process_args(ALOHANode.__init__, args, special_arg)
        node = ALOHANode(**args)

    for name in SPECIAL_ATTRIBUTES:
        __set_attributes(node, config, name)

    return node

def __load_config(config):
    if type(config) == str:
        with open(config) as f:
            return json.load(f)
    elif type(config) == dict:
        return config
    else:
        return {} 

def __set_attributes(device, config, name):
    if device is not None and name in config:
        setattr(device, name, config[name])


def __process_args(func, args, special_arg):
    # remove unused args
    func_args = inspect.getargspec(func).args
    key_list = args.keys()
    # load the special arg
    if special_arg is not None:
        for key in special_arg:
            args[key] = special_arg[key]
    
    args = {k:v for k, v in args.items() if k in func_args}
    return args


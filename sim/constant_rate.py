from bootstrap import *

from engine import TransmissionMedium
from protocols import create_basestation, create_node, ProtocolType
import simpy

env = simpy.Environment()


for i in range(10):
    special_arg = {"total": 10, "scheduled_time": i, 
            "seed": i, "p": 0.05, "m":3, "slot_t": 0.1, 
            "feedback_t": 0.1, "rate": [1]}
    n = create_node(ProtocolType.LPDQ, i, env, "default.json", special_arg)

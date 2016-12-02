from bootstrap import *

from engine import TransmissionMedium
from protocols import LPDQNode, LPDQBaseStation
import simpy
from random_mock import RandomMock

def test(env, nodes, bs):
    MTU = nodes[0].MTU
    def on_receive1(packet):
        payload = packet.payload
        if type(payload) == str:
            # first node should not have any problem
            assert abs(env.now - 1.8) < 0.1
    bs.on_receive += on_receive1
    nodes[0].random = RandomMock([0])
    nodes[0].send("test", MTU)
    yield env.timeout(3)

    # simulation time is 3 now
    # this will create a contention
    nodes[1].random = RandomMock([0])
    nodes[2].random = RandomMock([0])
    nodes[1].send("", MTU)
    nodes[2].send("", MTU)
    def on_receive2(payload):
        if type(payload) == str:
            assert False # should not have data transmitted
    bs.on_receive -= on_receive1
    bs.on_receive += on_receive2
    yield env.timeout(2)
    nodes[0].random = RandomMock([1])
    nodes[0].send("", MTU)
    nodes[3].random = RandomMock([1])
    nodes[3].send("", MTU)
    yield env.timeout(2)
    assert bs.crq == 1
    # create dtq
    nodes[1].random = RandomMock([2])
    def on_receive3(payload):
        if type(payload) == str:
            assert payload.id == 3
            print(env.now)
            assert abs(env.now - 7.8) < 0.1
    bs.on_receive -= on_receive2
    bs.on_receive += on_receive3
    yield env.timeout(2)
    
    #bs.on_receive = on_receive2
    yield env.timeout(5) 


def main():
    env = simpy.Environment()
    rates = [30]
    slot_t = 0.1
    feedback_t = 0.1

    random_list = range(10)

    t = TransmissionMedium(env)
    bs = LPDQBaseStation(0, env, 0, 3, rates=rates, jitter_range = 0.0001, feedback_t = feedback_t, slot_t = slot_t)
    t.add_device(bs)
    nodes = []
    TOTAL = 10
    for i in range(1, TOTAL + 1):
        node = LPDQNode(i, env, feedback_t = feedback_t, slot_t = slot_t, m=3, rates = rates, guard = 0.01, seed = i, jitter_range = 0.001)
        t.add_device(node)
        nodes.append(node)
    env.process(test(env, nodes, bs))
    
    env.run(until=10)

if __name__ == "__main__":
    main()

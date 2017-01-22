from pyns.engine import TransmissionMedium
from pyns.protocols import LORANode, LORABaseStation, LORAACK
import simpy

def simpy_LORA(env, nodes, bs):
    # first node to send message
    def on_receive_1(packet):
        if type(packet.payload) == LORAACK:
            assert abs(env.now - 6 - 2/30) < 0.1

    nodes[0].on_receive += on_receive_1
    MTU = nodes[0].MTU
    nodes[0].send("", MTU)

    yield env.timeout(4)

def test_LORA():
    env = simpy.Environment()
    rates = [30]
    t = TransmissionMedium(env)
    bs = LORABaseStation(0, env, rates)
    t.add_device(bs)
    nodes = []
    TOTAL = 3
    for i in range(1, TOTAL + 1):
        node = LORANode(i, env, rates, guard = 0.01, seed = i, jitter_range = 0.001)
        t.add_device(node)
        nodes.append(node)
    env.process(simpy_LORA(env, nodes, bs))

    env.run(until=40)

if __name__ == "__main__":
    test_LORA()

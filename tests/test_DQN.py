from pyns.engine import TransmissionMedium
from pyns.protocols import DQNNode, DQNBaseStation
import simpy
from pyns.utility.random_mock import RandomMock

def simpy_DQN(env, nodes, bs):
    # use an example close to the paper with modicication
    # http://ieeexplore.ieee.org/xpls/icp.jsp?arnumber=7457611
    # setting up the random seeds
    nodes[0].random = RandomMock([0, 0])
    nodes[1].random = RandomMock([0, 1])
    nodes[2].random = RandomMock([0, 2])
    nodes[3].random = RandomMock([0, 3])
    nodes[4].random = RandomMock([1])
    nodes[5].random = RandomMock([3])
    nodes[6].random = RandomMock([2, 0, 0])
    nodes[7].random = RandomMock([2, 0, 1])
    for i in range(8):
        nodes[i].send("", nodes[i].MTU / 16 * 10) # send 10 data slots

    def on_receive(packet):
        payload = packet.payload
        id = packet.id 
        #if type(payload) == str:
        #    if id == 5:
        #        assert abs(env.now - 26.8) < 0.1
        #    elif id == 6:
        #        assert abs(env.now - 36.8) < 0.1
        #    elif id == 1:
        #        assert abs(env.now - 46.8) < 0.1
        #    elif id == 2:
        #        assert abs(env.now - 56.8) < 0.1
        #    elif id == 3:
        #        assert abs(env.now - 76.8) < 0.1
        #    elif id == 4:
        #        assert abs(env.now - 86.8) < 0.1
        #    elif id == 7:
        #        assert abs(env.now - 96.8) < 0.1
        #    elif id == 8:
        #        assert abs(env.now - 106.8) < 0.1

    bs.on_receive += on_receive

    yield env.timeout(10)

def test_DQN():
    env = simpy.Environment()
    rates = [30]
    slot_t = 0.5
    feedback_t = 0.5
    N = 16
    random_list = range(10)
    bs_seed = 0
    m = 4

    t = TransmissionMedium(env)
    bs = DQNBaseStation(0, env, N, bs_seed, m, rates=rates, jitter_range = 0.0001, feedback_t = feedback_t, slot_t = slot_t)
    t.add_device(bs)
    nodes = []
    TOTAL = 10
    for i in range(1, TOTAL + 1):
        node = DQNNode(i, env, N = N, feedback_t = feedback_t, slot_t = slot_t, m=m, rates = rates, guard = 0.01, seed = i, jitter_range = 0.001)
        t.add_device(node)
        nodes.append(node)
    env.process(simpy_DQN(env, nodes, bs))
    
    env.run(until=60)

if __name__ == "__main__":
    test_DQN()

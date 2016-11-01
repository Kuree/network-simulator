import bootstrap

from engine import Device, BaseStation

class DQObject:
    REQUEST = 0
    FEEDBACK = 1
    def __init__(self, obj_type):
        self.type = obj_type


class DQRequest(DQObject):
    def __init__(self, slot):
        super().__init__(DQObject.REQUEST)
        self.slot = slot

class DQFeedback(DQObject):
    def __init__(self, slots, dtq, crq):
        self.slots = slots
        self.dtq = dtq
        self.crq = crq


class LPDQNode(Device):
    IDLE = 0
    IN_TRANSMISSION = 1
    DTQ  = 2
    CRQ  = 3

    def __init__(self, id, env, seed, jitter_range, rate, average_packet_size, m, packet_rate):
        super().__init(id, env, seed=seed, jitter_range=jitter_range)
        self.rate = rate
        self.average_packet_size = average_packet_size
        self.m = m
        self.packet_rate = packet_rate
        self.sleep_time = self.random.randint(0, 20)   # TODO: change this to parameter
        
        self..chosen_slot = 0
        
        self.state = LPDQNode.IDLE

        self.env.process(self.run())

    def on_receive(self, packet):
        if self.state == LPDQNode.IN_TRANSMISSION:
            payload = packet.payload
            if type(payload) != DQFeedback:
                return # not valid packet
            if payload.slots[self.chosen_slot]: # it's a successful request
                queue_position = 0
                for i in range(self.chosen_slot):
                    if payload.slots[i]:
                        queue_position += 1
                self.sleep_time = payload.dtq + queue_position
                self.state = LPDQNode.DTQ
            else:
                # enter crq
                queue_position = 0
                for i in range(self.chosen_slot):
                    if not payload.slots[i]:
                        queue_posiiton += 1
                self.sleep_time = payload.crq + queue_position
                self.state = LPDQNode.CRQ


    def run(self):
        while True:
            yield self.env.timeout(self.sleep_time)
            if self.state == LPDQNode.IDLE:
                # decide whether to transmit the packet
                if self.random.random() < self.rate: # needs to transmit
                    self.state = LPDQNode.IN_TRANSMISSION


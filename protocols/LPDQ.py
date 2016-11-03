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
    # finite state machine
    IDLE = 0
    IN_TRANSMISSION = 1
    DTQ  = 2
    CRQ  = 3

    def __init__(self, id, env, seed, jitter_range, rate, m, packet_rate, slot_t, feedback_t):
        super().__init(id, env, seed=seed, jitter_range=jitter_range)
        self.rate = rate
        #self.average_packet_size = average_packet_size
        self.m = m
        self.packet_rate = packet_rate
        self.rate = rate
        # this controls the time for overhead
        self.slot_t = selt_t
        self.feedback_t = feedback_t

        # smooth out the start up process
        self.sleep_time = self.random.randint(0, 20)   # TODO: change this to parameter
        
        self..chosen_slot = 0
        
        self.state = LPDQNode.IDLE

        self.env.process(self.run())

    def on_receive(self, packet):
        if self.state == LPDQNode.IN_TRANSMISSION:
            payload = packet.payload
            if type(payload) != DQFeedback:
                return # not valid packet
            if payload.slots[self.chosen_slot] == 1: # it's a successful request
                queue_position = 0
                for i in range(self.chosen_slot):
                    if payload.slots[i] == 1:
                        queue_position += 1 # compute the dtq
                self.sleep_time = payload.dtq + queue_position
                self.state = LPDQNode.DTQ
            else:
                # enter crq
                queue_position = 0
                for i in range(self.chosen_slot):
                    if payload.slots[i] > 1:
                        queue_posiiton += 1 # compute the crq position
                self.sleep_time = payload.crq + queue_position
                self.state = LPDQNode.CRQ


    def run(self):
        while True:
            yield self.env.timeout(self.sleep_time)
            if self.state == LPDQNode.IDLE:
                # decide whether to transmit the packet
                if self.random.random() < self.rate: # needs to transmit
                    self.state = LPDQNode.IN_TRANSMISSION
                    self.sleep_time = 0
            elif self.state == LPDQ.IN_TRANSMISSION:
                self.chosen_slot = self.rancom.randrange(self.m)
                # compute the offset for slot
                # sleep_time
                sleep_time = self.slot_t / self.m * self.chosen_slot
                yield self.env.timeout(sleep_time)
                self.send(DQRequest(self.chosen_slot))
            elif self.state == LPDQ.DTQ:
                # skip the slot time
                yield self.env.timeout(self.slot_t)
                # send dummpy payload
                duration = 1 - self.slot_t - self.feedback_t
                # send data in data slot
                self.send(1, duration = duration, rate=self.rate)
                self.state = LPDQ.IDLE
            elif self.state == LPDQ.CRQ:
                # try to transmit again
                self.sleep_time = 0
                self.state = LPDQ.IN_TRANSMISSION


class LPDQServer(device):
    def __init__(self, id, env, seed, m, rate, jitter_range, feedback_t, slot_t):
        super().__init__(id, env, seed = seed, jitter_range = jitter_range)
        self.m = m
        self.rate = rate
        self.feedback_t
        self.slot_t = slot_t
        
        self.receive_window = 0.1 # 0.1 buffer


        self.__init_slots()

        self.env.process(self.run())


    def on_receive(self, packet):
        payload = packet.payload
        if type(payload) == DQRequest:
            # only interested in slot request
            timestamp = packet.timestamp
            slot_raw = timestamp % 1 - self.receive_window # calibrate with the receive window
            slot = slot_raw / self.slot_t * self.m 
            if slot < self.m: # if it's larger or equal to, we don't need to take care of as it will cause packet drop
                slot = int(slot)
                self.slots[slot] += 1
        


    def __init_slots(self):
        self.slots = [0 for i in range(self.m)]


    def run(self):
        # dump to feedback slot
        yield self.env.timeout(1 - self.slot_t)
        while True:
            self.send(DQFeedback(self.slots, self.dtq, self.crq))
            self.__init_slots()
            self.env.timeout(1)
        




import bootstrap

from engine import Device

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


class DQNNode(Device):
    # finite state machine
    IDLE = 0
    IN_TRANSMISSION = 1
    DTQ  = 2
    CRQ  = 3
    WAIT = 4

    def __init__(self, id, env, seed, jitter_range, rates, m, N, slot_t, feedback_t, guard):
        MTU = self._compute_mtu(1 - slot_t - feedback_t - guard * (m + 1), rates[0])
        super().__init__(id, env, rates, seed=seed, jitter_range=jitter_range, guard=guard, MTU = MTU)
        #self.average_packet_size = average_packet_size
        self.m = m
        # this controls the time for overhead
        self.slot_t = slot_t
        self.feedback_t = feedback_t

        self.N = N

        # smooth out the start up process
        self.sleep_time = 0
        
        self.chosen_slot = 0
        
        self.state = DQNNode.IDLE

    def on_receive(self, packet):
        if self.state == DQNNode.WAIT:
            payload = packet.payload
            if type(payload) != DQFeedback:
                return # not valid packet
            if payload.slots[self.chosen_slot] == 1: # it's a successful request
                #print("received slots", payload.slots)
                queue_position = 0
                for i in range(self.chosen_slot):
                    if payload.slots[i] == 1:
                        queue_position += 1 # compute the dtq
                self.sleep_time = payload.dtq + queue_position
                self.state = DQNNode.DTQ
            else:
                # enter crq
                queue_position = 0
                for i in range(self.chosen_slot):
                    if payload.slots[i] > 1:
                        queue_posiiton += 1 # compute the crq position
                self.sleep_time = payload.crq + queue_position
                self.state = DQNNode.CRQ


    def _schedule_send(self, payload, duration, size, medium_index, is_overhead, antenna):
        with antenna.request() as req:
            yield req
            sent = False
            self.state = DQNNode.IN_TRANSMISSION
            self.sleep_time = 1 - (self.env.now % 1)
            while not sent:
                yield self.env.timeout(self.sleep_time)
                if self.state == DQNNode.IN_TRANSMISSION:
                    self.chosen_slot = self.random.randrange(self.m)
                    # compute the offset for slot
                    # sleep_time
                    sleep_time = self.slot_t / self.m * self.chosen_slot
                    yield self.env.timeout(sleep_time)
                    slot_duration = self.slot_t / self.m - self.guard
                    slot_size = slot_duration * self.rates[0]
                    self._send(DQRequest(self.chosen_slot), slot_duration, slot_size, 0, is_overhead = True)
                    #print("id:", self.id, "slot", self.chosen_slot) 

                    # this will put it to sleep till contention result is out
                    # TODO: fix this ugly approach
                    self.state = DQNNode.WAIT
                    yield self.env.timeout(1 - (self.env.now % 1))
                    
                elif self.state == DQNNode.DTQ:
                    # skip the slot time
                    yield self.env.timeout(self.slot_t)
                    # send dummpy payload
                    # send data in data slot
                    # TODO: fix the rate here
                    self._send(payload, duration = duration, size=size, medium_index = 0, is_overhead = False)
                    self.state = DQNNode.IDLE
                    sent = True
                elif self.state == DQNNode.CRQ:
                    # try to transmit again
                    self.sleep_time = 1 - (self.env.now % 1)
                    self.state = DQNNode.IN_TRANSMISSION


class DQNBaseStation(Device):
    def __init__(self, id, env, seed, m, rates, N, jitter_range, feedback_t, slot_t):
        super().__init__(id, env, rates, seed = seed, jitter_range = jitter_range)
        self.m = m
        self.feedback_t = feedback_t
        self.slot_t = slot_t
        
        self.window_size = 0.01 # 0.1 buffer
        self.dtq = 0
        self.crq = 0

        self.N = N

        self.__init_slots()

        self.env.process(self.run())


    def on_receive(self, packet):
        payload = packet.payload
        if type(payload) == DQRequest:
            # only interested in slot request
            slot_raw = self.env.now % 1 # TODO: calibrate with the receive window
            if slot_raw < 0:
                slot_raw = 0
            slot = int(slot_raw / self.slot_t * self.m)
            #print("time", self.env.now, "slot", slot, "slot raw", slot_raw)
            if slot < self.m: # if it's larger or equal to, we don't need to take care of as it will cause packet drop
                self.slots[slot] += 1
        


    def __init_slots(self):
        self.slots = [0 for i in range(self.m)]


    def run(self):
        # dump to feedback slot
        yield self.env.timeout(1 - self.slot_t)
        while True:
            # print("sending slots", self.slots)
            duration =  self.feedback_t - self.window_size
            size = self.rates[0] * duration
            self._send(DQFeedback(self.slots, self.dtq, self.crq), duration, size, medium_index = 0, is_overhead = True)

            # increment the counter accordingly
            for i in range(len(self.slots)):
                if self.slots[i] > 1:
                    self.crq += 1
                elif self.slots[i] == 1:
                    self.dtq += 1

            self.__init_slots()
            yield self.env.timeout(1)
            # decrease the counter
            self.dtq = self.dtq - 1 if self.dtq > 0 else 0
            self.crq = self.crq - 1 if self.crq > 0 else 0
        



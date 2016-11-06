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


class LPDQNode(Device):
    # finite state machine
    IDLE = 0
    IN_TRANSMISSION = 1
    DTQ  = 2
    CRQ  = 3
    WAIT = 4

    def __init__(self, id, env, seed, jitter_range, rate, m, packet_rate, slot_t, feedback_t):
        super().__init__(id, env, seed=seed, jitter_range=jitter_range)
        self.rate = rate
        #self.average_packet_size = average_packet_size
        self.m = m
        self.packet_rate = packet_rate
        self.rate = rate
        # this controls the time for overhead
        self.slot_t = slot_t
        self.feedback_t = feedback_t

        self.window_size = 0.001
        self.PRECESION = 0.001

        # smooth out the start up process
        self.sleep_time = self.random.randint(0, 20)   # TODO: change this to parameter
        
        self.chosen_slot = 0
        
        self.state = LPDQNode.IDLE

        self.env.process(self.run())

    def on_receive(self, packet):
        if self.state == LPDQNode.WAIT:
            payload = packet.payload
            if type(payload) != DQFeedback:
                return # not valid packet
            if payload.slots[self.chosen_slot] == 1: # it's a successful request
                # print("received slots", payload.slots)
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

    def send(self, payload, size, medium_index = 0):
        # need to implement this part
        pass


    def _schedule_send(self, timestamp, payload, duration, size, medium_index, is_overhead):
        while self.state != LPDQNode.IDLE:
            yield self.env.timeout(self.PRECISION) # need to wait till the current transmission is finished
        sent = False
        while not sent:
            if self.state == LPDQNode.IDLE:
                # decide whether to transmit the packet
                if self.random.random() < self.packet_rate: # needs to transmit
                    self.state = LPDQNode.IN_TRANSMISSION
                    self.sleep_time = 1 - (self.env.now % 1)
            elif self.state == LPDQNode.IN_TRANSMISSION:
                self.chosen_slot = self.random.randrange(self.m)
                # compute the offset for slot
                # sleep_time
                sleep_time = self.slot_t / self.m * self.chosen_slot
                print("slot", self.chosen_slot, "sleep time", sleep_time)
                yield self.env.timeout(sleep_time)
                self.send(DQRequest(self.chosen_slot), duration = self.slot_t / self.m - self.window_size, is_overhead = True)
                

                # this will put it to sleep till contention result is out
                # TODO: fix this ugly approach
                self.state = LPDQNode.WAIT
                yield self.env.timeout(1 - (self.env.now % 1))
                
            elif self.state == LPDQNode.DTQ:
                # skip the slot time
                yield self.env.timeout(self.slot_t)
                # send dummpy payload
                duration = 1 - self.slot_t - self.feedback_t - self.window_size
                # send data in data slot
                # TODO: fix the rate here
                size = duration * self.rate[0]
                self.send(1, duration = duration, size=size)
                self.state = LPDQNode.IDLE
            elif self.state == LPDQNode.CRQ:
                # try to transmit again
                self.sleep_time = 0
                self.state = LPDQNode.IN_TRANSMISSION


class LPDQBaseStation(Device):
    def __init__(self, id, env, seed, m, rate, jitter_range, feedback_t, slot_t):
        super().__init__(id, env, seed = seed, jitter_range = jitter_range)
        self.m = m
        self.rate = rate
        self.feedback_t = feedback_t
        self.slot_t = slot_t
        
        self.window_size = 0.01 # 0.1 buffer
        self.dtq = 0
        self.crq = 0

        self.__init_slots()

        self.env.process(self.run())


    def on_receive(self, packet):
        payload = packet.payload
        if type(payload) == DQRequest:
            # only interested in slot request
            slot_raw = self.env.now % 1 # TODO: calibrate with the receive window
            if slot_raw < 0:
                slot_raw = 0
            slot = slot_raw / self.slot_t * self.m 
            print("time", self.env.now, "slot", slot, "slot raw", slot_raw)
            if slot < self.m: # if it's larger or equal to, we don't need to take care of as it will cause packet drop
                slot = int(slot)
                self.slots[slot] += 1
        


    def __init_slots(self):
        self.slots = [0 for i in range(self.m)]


    def run(self):
        # dump to feedback slot
        yield self.env.timeout(1 - self.slot_t)
        while True:
            print("sending slots", self.slots)
            self.send(DQFeedback(self.slots, self.dtq, self.crq), duration = self.feedback_t - self.window_size, is_overhead = True)

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
        




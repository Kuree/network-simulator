# this script analyze the trace files from the medium

import argparse
import json
import numpy
import os


class Analyzer:
    def __init__(self, filename, rate):
        if not os.path.isfile(filename):
            raise Exception("Log file does not exist")
        with open(filename) as f:
            raw_data = f.readlines()
            self.packet_data = [l.split() for l in raw_data]
        self.rate = rate


    def process_raw(self, packet_data):
        busy_time = 0
        for packet_index in range(len(packet_data)):
            packet = packet_data[packet_index]
            timestamp, node_id, size, duration, is_overhead = packet
            
            timestamp = float(timestamp)
            packet[0] = timestamp

            node_id = int(node_id)
            packet[1] = node_id

            size = float(size)
            packet[2] = size

            duration = float(duration)
            packet[3] = duration

            is_overhead = bool(int(is_overhead))
            packet[4] = is_overhead

            if timestamp < busy_time:
                # this is a collision
                packet.append(True) # this packet should be dropped
                # we also nned to back trace the previous one
                if packet_index > 0:
                    pre_packet = packet_data[packet_index - 1]
                    pre_packet[-1] = True
            else:
                # we are good for this one so far...
                packet.append(False)
            busy_time = max(timestamp + duration, busy_time) # compute the next busy_time
        return busy_time

    def compute_stats(self):
        total_time = self.process_raw(self.packet_data)
        throughput = sum([packet[2] for packet in self.packet_data if not packet[-1] and not packet[-2]]) / total_time

        return total_time, throughput

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Trace analyzer for network simulation output")
    parser.add_argument("-f", action="store", dest="filename", type=str, required=True, help="file name for the log file")
    parser.add_argument("-r", action="store", dest="rate", type=float, default=30, help="rate used to compute utility")
#parser.add_argument("-format", action="store", dest="format", type=str, default="format.json", help="format file for the trace")
    args = parser.parse_args()

    filename = args.filename
    rate = args.rate
    an = Analyzer(filename, rate)
    print(*an.compute_stats())

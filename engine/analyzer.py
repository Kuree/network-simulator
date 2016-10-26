# this script analyze the trace files from the medium

import argparse
import json
import numpy
 

def process_raw(packet_data):
    busy_time = 0
    for packet_index in range(len(packet_data)):
        packet = packet_data[packet_index]
        timestamp, node_id, size, duration, is_overhead = packet
        timestamp = float(timestamp)
        node_id = int(node_id)
        size = int(size)
        duration = float(duration)
        is_overhead = bool(is_overhead)
        if timestamp < busy_time:
            # this is a collision
            busy_time = max(timestamp + duration, busy_time) # compute the next busy_time
            packet.append(False) # this packet should be dropped
            # we also nned to back trace the previous one
            if packet_index > 0:
                pre_packet = packet_data[packet_index - 1]
                pre_packet[-1] = False
        else:
            # we are good for this one so far...
            packet.append(False)
            busy_time = timestamp + duration
    return busy_time

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Trace analyzer for network simulation output")
    parser.add_argument("-f", action="store", dest="filename", type=str, required=True, help="file name for the log file")
#parser.add_argument("-format", action="store", dest="format", type=str, default="format.json", help="format file for the trace")
    args = parser.parse_args()

    filename = args.filename
    with open(filename) as f:
        raw_data = f.readlines()
        packet_data = [l.split() for l in raw_data]

    total_time = process_raw(packet_data)
    print(total_time)

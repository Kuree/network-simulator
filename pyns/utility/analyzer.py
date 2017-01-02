# this script analyze the trace files from the medium

import argparse
import json
import numpy
import os
import collections

class Analyzer:
    def __init__(self, filename, rate, format_file=""):
        if not os.path.isfile(filename):
            raise Exception("Log file does not exist")
        if format_file == "": # use the default trace files
            dir_path = os.path.dirname(os.path.realpath(__file__))
            dir_path = os.path.dirname(dir_path)
            format_file = os.path.join(dir_path, "engine", "format.json")
        if not os.path.isfile(format_file):
            raise Exception("Trace format file does not exit")

        with open(filename) as f:
            raw_data = f.readlines()
            self.packet_data = [l.split() for l in raw_data]
        self.rate = rate
        
        with open(format_file) as f:
            self.format = json.load(f)

    def process_packet(self, packet):
        kwargs = {}
        for entry in self.format:
            name = entry["name"]
            index = entry["index"]
            if index >= len(packet):
                raise Exception("Log file was generated using different trace format")
            value = packet[index]
            data_type = entry["type"]
            value = self.process_type(value, data_type)
            kwargs[name] = value
        Packet = collections.namedtuple('Packet', ' '.join(kwargs.keys()))
        return Packet(**kwargs)


    def process_type(self, data, data_type):
        if data_type == "string" or data_type == str:
            return str(data)
        elif data_type == "int" or data_type == int:
            return int(data)
        elif data_type == "bool" or data_type == bool:
            return bool(data)
        elif data_type == "float" or data_type == float:
            return float(data)
        else:
            return data

    def process_raw(self, packet_data):
        busy_time = 0
        for packet_index in range(len(packet_data)):
            raw_packet = packet_data[packet_index]
            packet = self.process_packet(raw_packet)
            packet_data[packet_index] = packet # replace the old packet
            if packet.timestamp < busy_time:
                # this is a collision
                packet_data[packet_index] = packet._replace(valid = False) # this packet should be dropped
                # we also nned to back trace the previous one
                if packet_index > 0:
                    pre_packet = packet_data[packet_index - 1]
                    pre_packet = pre_packet._replace(valid = False)
                    packet_data[packet_index - 1] = pre_packet
            
            busy_time = max(packet.timestamp + packet.duration, busy_time) # compute the next busy_time
        return busy_time

    def compute_stats(self):
        '''
            return total_time, average throughput, channel utility
        '''
        total_time = self.process_raw(self.packet_data)
        if total_time == 0:
            return 0, 0, 0
        throughput = sum([packet.size for packet in self.packet_data if packet.valid and not packet.is_overhead]) / total_time

        return total_time, throughput, throughput / self.rate

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Trace analyzer for network simulation output")
    parser.add_argument("-f", action="store", dest="filename", type=str, required=True, help="file name for the log file")
    parser.add_argument("-r", action="store", dest="rate", type=float, default=30, help="rate used to compute utility")
    parser.add_argument("-format", action="store", dest="format", type=str, default="", help="format file for the trace")
    args = parser.parse_args()

    an = Analyzer(args.filename, args.rate, args.format)
    stats = an.compute_stats()
    print("Simulation time: {1}\nThroughput: {2}\nUtility: {3} (using channel transmission rate {0} bytes/s".format(args.rate, *stats))

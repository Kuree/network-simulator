# this script analyze the trace files from the medium

import argparse

parser = argparse.ArgumentParser(description="Trace analyzer for network simulation output")
parser.add_argument('-f', action="store", dest="filename", type=str, required=True, help="file name for the log file")
args = parser.parse_args()

filename = args.filename

print(filename)

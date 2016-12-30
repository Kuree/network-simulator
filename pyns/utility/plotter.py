import argparse
import os
from pyns.utility.analyzer import Analyzer
import json
#import numpy

# this plotter tries to plot the line graph


def parse_name(path, config):
    '''
        first it will split path in entries by '-'
        config foramt:
            "name": a list of [index1, index2, bool]. if not bool, result[index2] = entries[index1] else use the legend[entries[index1]]
            "rate": the max transmission rate of the channel
            "legend": used to indicate which one is which. notice that str is used in entry key
        results: 
        [legend entry, x]
    '''
    path = os.path.basename(path)
    config_name = config["name"]
    entries = path.split("-")
    result = ["", ""]
    for index1, index2, use_name in config_name:
        if use_name:
            value = config["legend"][entries[index1]]
        else:
            value = float(entries[index1])
        result[index2] = value
    return result


def plot(data, xscale):
    ''' plot the data points'''
    import matplotlib.pyplot as plt # import here to avoid package dependency detect
    
    fig, ax = plt.subplots()
    for legend in data:
        data_pairs = data[legend]
        data_pairs.sort(key=lambda x: x[0])
        
        x = [entry[0] * xscale for entry in data_pairs]
        y = [entry[1] for entry in data_pairs]

        ax.plot(x, y, label=legend)
    legend = ax.legend(loc="upper left")

    return ax, plt


def main():
    parser = argparse.ArgumentParser(description="Generic plotter for ns")
    parser.add_argument("-d", action="store", dest="dir_path", required=True, help="the folder to the logs")
    parser.add_argument("-f", action="store", dest="config", required=True, help="the config file to plot the logs")
    args = parser.parse_args()

    dir_path = args.dir_path
    config_file = args.config
    # check all the parameters
    if not os.path.isdir(dir_path):
        print("log folder does not exist")
        exit()
    if not os.path.isfile(config_file):
        print("config file does not exist")
    
    with open(config_file) as f:
        config = json.load(f)

    data_files = [path for path in os.listdir(dir_path) if path[0] != "."]

    data = {}
    for path in data_files:
        path = os.path.join(dir_path, path)
        legend, x_label = parse_name(path, config)
        # call the analyzer to analyze the trace files
        ana = Analyzer(path, config["rate"])
        result = ana.compute_stats()
        # add the data points
        if legend in data:
            data[legend].append((x_label, result[-1]))
        else:
            data[legend] = [(x_label, result[-1])]
    if "xscale" in config:
        xscale = config["xscale"]
    else:
        xscale = 1
    ax, plt = plot(data, xscale)
    ax.set_xlabel(config["xlabel"])
    ax.set_ylabel(config["ylabel"])

    plt.show()


if __name__ == "__main__":
    main()

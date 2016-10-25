import logging
import json
import os

class TraceFormatter(logging.Formatter):
    TRACE_FORMAT = "format.json"
    def __init__(self, env):
        self.env = env
        filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), TraceFormatter.TRACE_FORMAT)
        with open(filename) as f:
            self.values = json.load(f)
            self.values.sort(key=lambda k:k["index"])
        super(TraceFormatter, self).__init__()

    def format(self, record):
        packet = record.msg
        values = []
        for entry in self.values:
            name = entry["name"]
            value = getattr(packet, name)
            value_type = entry["type"]
            if value_type == "int":
                value = int(value)
            elif value_type == "float":
                value = float(value)
            values.append(str(value))
        return " ".join(values)

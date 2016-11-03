if __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import simpy
import logging
import random
import argparse
from engine import TransmissionMedium
from engine import SimArg

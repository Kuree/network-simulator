from bootstrap import *

from protocols import LPDQNode, LPDQBaseStation

def main(args):
    pass


if __name__ == "__main__":
    parser = SimArg(description="CSMA protocol simulator")
    parser.add_argument("-m", action="store", dest="m", default=3, type=int, help="number of mini-slots")
    parser.add_argument("-slot_t", action="store", dest="slot_t", default=0.1, type=float, help="duration of mini-stlos frame (total)")
    parser.add_argument("-feedback_t", action="store", dest="feedback_t", default=0.1, type=float, help="duration of feedback frame (total)")

    args = parser.parse_args()

    main(args)
 


from . import utility
import math

class PHYLayer:
    def __init__(self, threshold):
        self.threshold = threshold

    def compute_ber(self, ebn0, is_log=False):
        return 0

    def compute_per(self, ebn0, size, is_log=False):
        '''
        size is in byte
        '''
        ber = self.compute_ber(ebn0, is_log)
        return 1 - (1 - ber)**(size * 8)

    def __parse_points(self, point1, point2):
        if hasattr(point1, 'lat'):
            lat1 = point1.lat
        else:
            lat1 = point1[0]
        if hasattr(point1, "lng"):
            lng1 = point1.lng
        else:
            lng1 = point1[1]

        if hasattr(point2, 'lat'):
            lat2 = point1.lat
        else:
            lat2 = point2[0]
        if hasattr(point2, "lng"):
            lng2 = point2.lng
        else:
            lng2 = point2[1]    
        return (lat1, lng1), (lat2, lng2)

    def get_distance(self, point1, point2):
        point1, point2 = self.__parse_points(point1, point2)
        distance = utility.get_distance(point1, point2)
        distance = distance * 1000 # meters
        return distance

    def get_path_loss(self, point1, point2, frequency):
        '''frequency is in hz
        returns db
        '''
        # this is free space path loss
        # you need to override this method to get better estimation
        distance = self.get_distance(point1, point2)
        return 20 * math.log(distance, 10) + 20 * math.log(frequency, 10) + 20 * math.log(4 * math.pi/ 299792458, 10)


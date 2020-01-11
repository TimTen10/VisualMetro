import os
import json
from metro.station import Station

class Metroline:

    def __init__(self, linename, color, stationsfolder):
        self.name = linename
        self.color = color
        self.stationsfolder = stationsfolder
        self.line = self._init_line(stationsfolder)
        self.zone = self._init_zone()

    def _init_line(self, folder):
        unsorted_line, line = [], []
        for root, dirs, files in os.walk(folder):
            for file in files:
                if file.endswith('.json'):
                    with open(folder + f'/{file}', 'r') as jsonfile:
                        station_dict = json.load(jsonfile)
                        unsorted_line.append(Station(station_dict))

        # TODO: check for endless loops -> throw errors if no match was found
        prev = None
        while len(unsorted_line) != len(line):
            for station in unsorted_line:
                if station.prev == prev:
                    prev = station.name
                    line.append(station)
                    break
        return line

    def _init_zone(self):
        # first coordinate up and down, second one left and right
        #topbottom = sorted(self.line, key = lambda x: x.location[0], reverse=True)
        bottomtop = sorted([x.location[0] for x in self.line])
        leftright = sorted([x.location[1] for x in self.line])
        return [bottomtop[0], bottomtop[-1], leftright[0], leftright[-1]]

def _test():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    tt_path = dir_path + f'/../timetableparser/parsedtimetables'
    asakusa = Metroline('Asakusa', 'red', tt_path)
    print(asakusa.zone)

if __name__ == '__main__':
    _test()

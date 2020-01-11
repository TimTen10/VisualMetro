class Station:

    def __init__(self, station_info):
        # TODO: Add a station ID e.g. A13 or use name as such
        self.name = station_info['name']
        self.prev = station_info['prev']
        self.next = station_info['next']
        self.departures = station_info['departures']
        self.location = station_info['location']

    def get_times(self, hour):
        # for now does not handle the input of false values like negatives
        return [time for time in self.departures if time.startswith(str(hour) + ':')]

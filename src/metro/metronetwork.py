class Metronetwork:

    def __init__(self, name, metrolines):
        self.name = name
        self.lines = metrolines
        self.zone = self._init_zone()

    def _init_zone(self):
        return [
            min([line.zone[0] for line in self.lines]),
            max([line.zone[1] for line in self.lines]),
            min([line.zone[2] for line in self.lines]),
            max([line.zone[3] for line in self.lines]),
        ]

def main():
    pass

if __name__ == '__main__':
    main()

class Race:

    def __init__(self):
        self._freeway = None
        self._devices = {}
        self._laps = None

    @property
    def freeway(self):
        return self._freeway

    @freeway.setter
    def freeway(self, fway):
        self._freeway = fway
        return self

    @property
    def laps(self):
        return self._laps

    @laps.setter
    def laps(self, laps):
        self._laps = laps
        return self

    @property
    def devices(self):
        return self._devices

    def add_device(self, dev):
        self._devices[dev.name] = dev
        return self

    def get_device_by_name(self, name):
        return self._devices[name]

    def setup(self):
        for name, dev in self._devices.items():
            dev.new_location(self.get_freeway())

class Race:

    def __init__(self):
        self._freeway = None
        self._devices = {}
        self._laps = None

    def set_freeway(self, fway):
        self._freeway = fway
        return self

    def get_freeway(self):
        return self._freeway

    def set_laps(self, laps):
        self._laps = laps
        return self

    def get_laps(self):
        return self._laps

    def get_devices(self):
        return self._devices

    def add_device(self, dev):
        self._devices[dev.name] = dev
        return self

    def get_device_by_name(self, name):
        return self._devices[name]

    def setup(self):
        for name, dev in self._devices.items():
            dev.new_location(self.get_freeway())

class EHanlder:

    def __init__(self):
        self._race = None
        self._running = False
        self._freeze = False
        self._delay  = 10
        self._worker_cbs = []
        self._rtime = None
        self._endame = []

    def tick(self):
        self._rtime += 1

    def set_delay(self, delay):
        self._delay = delay
        return self

    def add_worker_cb(self, cb):
        self._worker_cbs.append(cb)
        return self

    def get_race(self):
        return self._race

    def set_race(self, r):
        self._race = r
        return self

    def call_worker_cbs(self, dev):
        for cb in self._worker_cbs:
            if cb not None:
                cb(dev)

    def worker(self, dev):
        dev.running = True
        while self._running:
            if not dev.running:
                return
            if not self._freeze:
                dev.freeway_traverse()
            self.call_worker_cbs(dev)
            # time.Sleep(self.delay * Milliseconds)

    def _default_worker(self, dev):
        if dev.location.get_laps() == self.get_race().get_laps():
            dev.running = False
            self.endgame.append(dev)
            if len(self.endgame) == len(self.get_race().get_devices()):
                self.stop()

    def setup(self):
        self._running = True
        for k, dev in self._race.get_devices().items():
            # go self.worker(dev)
            pass
        self.add_worker_cb(self._default_worker)
        while self._running:
            # time.Sleep(self._delay) * Milliseconds
            self.tick()

    def stop(self):
        self._running = False

    def set_freeze(self, freeze):
        self._freeze = freeze
        return self

    def is_running(self):
        return self._running

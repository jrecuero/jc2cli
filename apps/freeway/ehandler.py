import threading
import time


class EHandler:

    def __init__(self):
        self._race = None
        self._running = False
        self._freeze = False
        self._delay  = 10
        self._worker_cbs = []
        self._rtime = 0
        self._endgame = []

    def tick(self):
        self._rtime += 1

    @property
    def delay(self):
        return self._delay

    @delay.setter
    def delay(self, delay):
        self._delay = delay
        return self

    def add_worker_cb(self, cb):
        self._worker_cbs.append(cb)
        return self

    @property
    def race(self):
        return self._race

    @race.setter
    def race(self, r):
        self._race = r
        return self

    def call_worker_cbs(self, dev):
        for cb in self._worker_cbs:
            if cb is not None:
                cb(dev)

    def setup(self):
        for dev in self.race.devices.values():
            dev.new_location(self.race.freeway)

    def worker(self, dev):
        dev.running = True
        while self._running:
            if not dev.running:
                return
            if not self._freeze:
                dev.freeway_traverse()
                # print('travesing {} {}'.format(dev.name, dev.get_location_index()))
            self.call_worker_cbs(dev)
            time.sleep(self._delay / 1000)

    def _default_worker_thread(self, dev):
        if dev.location.laps == self.race.laps:
            dev.running = False
            self._endgame.append(dev)
            if len(self._endgame) == 1:
                print("[{}] winner {}: {}".format(len(self._endgame), dev.name, self._rtime))
            else:
                print("[{}] device {}: {}".format(len(self._endgame), dev.name, self._rtime))
            if len(self._endgame) == len(self.race.devices):
                self.stop()

    def _ticker_thread(self):
        while self._running:
            time.sleep(self._delay / 1000)
            self.tick()

    def start(self):
        threads = []
        self._running = True
        self.add_worker_cb(self._default_worker_thread)
        t = threading.Thread(target=self._ticker_thread)
        threads.append(t)
        t.start()
        for k, dev in self.race.devices.items():
            t = threading.Thread(target=self.worker, args=(dev, ))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()

    def stop(self):
        self._running = False

    def set_freeze(self, freeze):
        self._freeze = freeze
        return self

    def is_running(self):
        return self._running

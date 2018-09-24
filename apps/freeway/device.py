import random
from location import Location


class Device:

    def __init__(self, name, dclass, dsubclass, power):
        self._name = name
        self._dclass = dclass
        self._dsubclass = dsubclass
        self._powrr = power
        self._location = None
        self._driver = None
        self._running = False
        self._dry = False

    @property
    def name(self):
        return self._name

    @property
    def dclass(self):
        return self._dclass

    @property
    def dsubclass(self):
        return self._dsubclass

    @property
    def power(self):
        return self._power

    @property
    def location(self):
        return self._location

    @property
    def driver(self):
        return self._driver

    @driver.setter
    def driver(self, value):
        self._driver = value

    @property
    def running(self):
        return self._running

    @running.setter
    def running(self, value):
        self._running = value

    def get_location(self):
        return self.location.get_location()

    def get_location_index(self):
        return self.location.get_location_index()

    def new_location(self, fway):
        self._location = Location(fway)
        return self.get_location()

    def _dice_it(self, todice):
        if not self._dry:
            dice = random.random()
            return int(todice * dice)
        return todice

    def traversing(self):
        sect, _ = self.get_location()
        spec = sect.spec()
        return self._diceit(sect.traversion() * self.driver.traversing(spec) * self.power)

    def entering(self, speed):
        sect, _ = self.get_location()
        spec = sect.spec()
        return self._diceit(sect.entering(speed) * self.driver.entering(spec, speed) * speed)

    def exiting(self, speed):
        sect, _ = self.get_location()
        spec = sect.spec()
        return self._diceit(sect.exiting(speed) * self.driver.exiting(spec, speed) * speed)

    def freeway_traverse(self):
        sect, dev_pos = self.get_location()
        dev_speed = self.traversing()
        position = dev_pos * dev_speed
        while position >= sect.length:
            next_speed = position - sect.length
            exit_speed = self.exiting(next_speed)
            sect, _ = self.location.next_section()
            position = self.entering(exit_speed)
        self.location.pos = position

    def __str__(self):
        isect, pos = self.get_location_index()
        return 'name:{0} class|sub: {1}|{2} power: {3} loc: {4}-{5} driver: {6}'.format(self.name,
                                                                                        self.dclass, self.dsubclass,
                                                                                        self.power,
                                                                                        isect, pos,
                                                                                        self.driver.name)

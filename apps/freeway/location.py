class Location:

    def __init__(self, freeway):
        self._freeway = freeway
        self._isect = 0
        self._pos = 0
        self._laps = 0

    @property
    def freeway(self):
        return self._freeway

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, position):
        self._pos = position

    @property
    def section(self):
        return self._freeway.get_section(self.position)

    @property
    def laps(self):
        return self._laps

    def get_location(self):
        return self.section, self.pos

    def get_location_index(self):
        return self._isect, self.pos

    def next_section(self):
        self._isect, islap = self.freeway.next_section_index(self.isect)
        if islap:
            self._laps += 1
        self.pos = 0
        return self.get_location()

    def lap_as_int(self):
        total = self.pos
        for i in range(self.isect):
            total += self.freeway.get_section(i).length
        return total

    def as_int(self):
        return (self.laps * self.freeway.lap_len()) + self.lap_as_int()

    def __str__(self):
        return "laps: {0} sec: {1} pos: {2}".format(self.laps, self._isext, self.pos)

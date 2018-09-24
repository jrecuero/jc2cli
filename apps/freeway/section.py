class Spec:
    Nada = 0
    Straight = 1
    Turn = 2

    def string(self, value):
        names = ['None', 'Straight', 'Turn']
        return names[value]


class Section:

    def __init__(self, length, width, spec=Spec.Straight, traversing=None, entering=None, exiting=None):
        self._length = length
        self._width = width
        self._spec = spec
        self._traversing = traversing
        self._entering = entering
        self._exiting = exiting

    @property
    def length(self):
        return self._length

    @property
    def width(self):
        return self._width

    @property
    def spec(self):
        return self._spec

    def traversing(self):
        if self._traversing:
            return self._traversing(self._spec)
        return 1

    def entering(self, speed):
        if self._entering:
            return self._entering(self._spec, speed)
        return 1

    def exiting(self, speed):
        if self._exiting:
            return self._exiting(self._spec, speed)
        return 1

    def __str__(self):
        return "len/width: {0}/{1} spec: {2}".format(self.length, self.width, Spec.string(self.spec))


class QSection:

    def __init__(self, section):
        self._section = section
        self._devices = []

    @property
    def section(self):
        return self._section

from section import QSection


class Freeway:

    def __init__(self):
        self._qsections = []

    def get_section(self, isect):
        return self._qsections[isect].section

    def add_section(self, sect):
        self._qsections.append(QSection(sect))

    @property
    def length(self):
        return len(self._qsections)

    def lap_len(self):
        total = 0
        for i in range(self.length):
            total += self.get_section(i).length
        return total

    def next_section_index(self, isect):
        isect += 1
        if self.length <= isect:
            return 0, True
        return isect, False

    def __str__(self):
        output = 'len: {0}\n'.format(self.length)
        for i, qs in enumerate(self.._qsections):
            output += '\t{0}: {1}\n'.format(i, str(qs.get_section(i)))
        return output

import ehandler
import race
import freeway
import section
import device
from cursor import Cursor


if __name__ == '__main__':
    Cursor.print(Cursor.clear_entire_screen())
    Cursor.print(Cursor.move_upper_left(0))
    _ehdlr = ehandler.EHandler()
    _race = race.Race()
    _freeway = freeway.Freeway()
    _freeway.add_section(section.Section(100, 1, section.Spec.Straight))
    _freeway.add_section(section.Section(50, 1, section.Spec.Turn))
    _freeway.add_section(section.Section(100, 1, section.Spec.Straight))
    _freeway.add_section(section.Section(50, 1, section.Spec.Turn))
    _race.freeway = _freeway
    _devices = [device.Device('dev-80', 'dev-class', 'dev-sub', 80),
                device.Device('dev-50', 'dev-class', 'dev-sub', 50),
                device.Device('dev-90', 'dev-class', 'dev-sub', 90),
                device.Device('dev-60', 'dev-class', 'dev-sub', 60),
                device.Device('dev-70', 'dev-class', 'dev-sub', 70), ]
    # _devices = [device.Device('dev-80', 'dev-class', 'dev-sub', 80), ]
    for dev in _devices:
        _race.add_device(dev)
    _race.laps = 5
    _ehdlr.race = _race
    _ehdlr.setup()
    _ehdlr.delay = 100
    _ehdlr.start()

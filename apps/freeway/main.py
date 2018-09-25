import ehandler
import race
import freeway
import section
import device


if __name__ == '__main__':
    _ehdlr = ehandler.EHandler()
    _race = race.Race()
    _freeway = freeway.Freeway()
    _freeway.add_section(section.Section(100, 1, section.Spec.Straight))
    _freeway.add_section(section.Section(50, 1, section.Spec.Turn))
    _freeway.add_section(section.Section(100, 1, section.Spec.Straight))
    _freeway.add_section(section.Section(50, 1, section.Spec.Turn))
    _race.set_freeway(_freeway)
    _devices = [device.Device('dev-80', 'dev-class', 'dev-sub', 80),
                device.Device('dev-50', 'dev-class', 'dev-sub', 50),
                device.Device('dev-90', 'dev-class', 'dev-sub', 90),
                device.Device('dev-60', 'dev-class', 'dev-sub', 60),
                device.Device('dev-70', 'dev-class', 'dev-sub', 70), ]
    # _devices = [device.Device('dev-80', 'dev-class', 'dev-sub', 80), ]
    for dev in _devices:
        _race.add_device(dev)
    _race.set_laps(5)
    _ehdlr.set_race(_race)
    _ehdlr.setup()
    _ehdlr.set_delay(100)
    _ehdlr.start()

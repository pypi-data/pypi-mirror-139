from AyAdb import AyAdb


class Touch:
    __device: AyAdb = None

    def __init__(self, device=None):
        self.__device = device

    def tap(self, x, y):
        return self.__device.shell(f'input tap {x} {y}', True)

    def swipe(self, x1, y1, x2, y2, duration=None):
        if duration is None:
            return self.__device.shell(f'input swipe {x1} {y1} {x2} {y2}', True)
        else:
            return self.__device.shell(f'input swipe {x1} {y1} {x2} {y2} {duration}', True)

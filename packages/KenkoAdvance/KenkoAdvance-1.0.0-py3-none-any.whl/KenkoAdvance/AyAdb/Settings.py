from AyAdb import AyAdb


class Settings:
    __device: AyAdb = None

    def __init__(self, device=None):
        self.__device = device

    def show_touches(self, value=None):
        if value is None:
            return self.__device.shell('settings get system show_touches').strip() == '1'
        return self.__device.shell(f'settings put system show_touches {("1" if value else "0")}')

    def pointer_location(self, value=None):
        if value is None:
            return self.__device.shell('settings get system pointer_location').strip() == '1'
        return self.__device.shell(f'settings put system pointer_location {("1" if value else "0")}')


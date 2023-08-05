from AyAdb import AyAdb
import re


class Info:
    __device: AyAdb = None

    def __init__(self, device=None):
        self.__device = device

    # Application Binary Interface
    # like: arm64-v8a
    def cpu_abi(self):
        return self.__device.shell('getprop ro.product.cpu.abi').strip()

    # like: 7.1.2
    def version_release(self):
        return self.__device.shell('getprop ro.build.version.release').strip()

    # like: 25
    def version_sdk(self):
        return int(self.__device.shell('getprop ro.build.version.sdk').strip())

    # like: (720, 1280)
    def screen_resolution(self):
        size_str = self.__device.shell('wm size').strip()
        re_result = re.search(r'Override size: (\d+)x(\d+)', size_str)
        if re_result:
            return int(re_result.group(1)), int(re_result.group(2))
        else:
            re_result = re.search(r'Physical size: (\d+)x(\d+)', size_str)
            if re_result:
                return int(re_result.group(1)), int(re_result.group(2))
            else:
                return 0, 0

    # like: 320
    def screen_density(self):
        dpi_str = self.__device.shell('wm density').strip()
        dpi_str = dpi_str.split('Physical density: ')[1]
        dpi_str = dpi_str.split(' ')[0]
        return int(dpi_str)

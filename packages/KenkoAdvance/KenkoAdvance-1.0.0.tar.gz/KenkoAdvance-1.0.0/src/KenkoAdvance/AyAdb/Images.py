import os
from random import random

from AyAdb import AyAdb


class Images:
    __device: AyAdb = None

    def __init__(self, device=None):
        self.__device = device

    def capture_screen(self, raw=False, use_file_system=False) -> bytes:
        # return PNG bytes if not raw
        command = 'screencap'
        if not raw:
            command += ' -p'
        if not use_file_system:
            return self.__device.shell(command, exec_out=True, decode=False, timeout=60)
        else:
            rand_name = str(int(random() * 100))
            command += '  /data/local/tmp/screenshot' + rand_name
            self.__device.shell(command, exec_out=True)
            self.__device.pull('/data/local/tmp/screenshot' + rand_name, 'screenshot' + rand_name)
            self.__device.files.del_file('/data/local/tmp/screenshot' + rand_name)
            with open('screenshot' + rand_name, 'rb') as f:
                file_content = f.read()
            os.remove('screenshot' + rand_name)
            return file_content

        # HOW TO USE RAW MODE
        # https://stackoverflow.com/questions/22034959/what-format-does-adb-screencap-sdcard-screenshot-raw-produce-without-p-f
        # https://stackoverflow.com/questions/7142169/pils-image-frombuffer-expected-data-length-when-using-ctypes-array
        # screenshot = device.images.capture_screen(raw=False)[12:]
        # screen_width, screen_height = device.info.screen_resolution()
        # # from ctypes import c_ubyte, cast, POINTER
        # # tmp = cast(screenshot, POINTER(c_ubyte*4*screen_width*screen_height)).contents
        # imm = Image.frombuffer('RGBA', (screen_width, screen_height), screenshot, 'raw', 'RGBX', 0, 1)
        # imm.show()

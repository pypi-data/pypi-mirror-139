"""
    一系列adb操作，目前仅支持远程连接
"""
import os
from adb_shell.auth.keygen import keygen as generate_key
from adb_shell.adb_device import AdbDeviceTcp
from adb_shell.auth.sign_pythonrsa import PythonRSASigner
from .adb_command import *
# from .Settings import *
# from .Info import *
# from .Touch import *
# from .App import *
from importlib import import_module


def load_adbkey(adbkey_path, auto_create: bool = True):
    _dir = os.path.dirname(adbkey_path)
    if not os.path.exists(_dir):
        if not auto_create:
            raise FileNotFoundError(adbkey_path)
        os.makedirs(_dir)
    try:
        with open(adbkey_path, 'r') as f:
            key = f.read()
        with open(adbkey_path + '.pub', 'r') as f:
            pub = f.read()
        return [PythonRSASigner(pub, key)]
    except FileNotFoundError:
        if not auto_create:
            raise
        generate_key(adbkey_path)
        return load_adbkey(adbkey_path, auto_create=False)


class AyAdb:
    __connected = False
    __device: AdbDeviceTcp = None
    __adbkey = None

    def __init__(self, host: str, port: int, adbkey_path: str = './adbkey'):
        self.__adbkey = load_adbkey(adbkey_path)
        self.__device = AdbDeviceTcp(host, port, default_transport_timeout_s=9.)
        self.settings = import_module('.Settings', package='AyAdb').Settings(self)
        self.info = import_module('.Info', package='AyAdb').Info(self)
        self.touch = import_module('.Touch', package='AyAdb').Touch(self)
        self.app = import_module('.App', package='AyAdb').App(self)
        self.files = import_module('.Files', package='AyAdb').Files(self)
        self.images = import_module('.Images', package='AyAdb').Images(self)

    def __del__(self):
        if self.__connected:
            self.disconnect()

    def connect(self):
        if self.__connected:
            return True
        try:
            self.__connected = self.__device.connect(rsa_keys=self.__adbkey, auth_timeout_s=0.1)
        except Exception:
            raise Exception('连接失败')
        return self.__connected

    def disconnect(self):
        self.__connected = self.__device.close()

    def shell(self, cmd: str, exec_out: bool = False, decode: bool = True, timeout: float = None):
        if self.__connected:
            if exec_out:
                if timeout:
                    return self.__device.exec_out(cmd, decode=decode, transport_timeout_s=timeout, read_timeout_s=timeout)
                return self.__device.exec_out(cmd, decode=decode, transport_timeout_s=timeout)
            if timeout:
                return self.__device.shell(cmd, decode=decode, transport_timeout_s=timeout, read_timeout_s=timeout)
            return self.__device.shell(cmd, decode=decode, transport_timeout_s=timeout)
        return None

    def reboot(self, fastboot: bool = False):
        return self.__device.reboot(fastboot)

    def pull(self, src: str, dst: str):
        return self.__device.pull(src, dst)

    def push(self, src: str, dst: str):
        return self.__device.push(src, dst)

    def stat(self, path: str):
        return self.__device.stat(path)

    def list(self, path: str):
        return self.__device.list(path)

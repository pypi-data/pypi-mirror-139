from AyAdb import AyAdb


class Files:
    __device: AyAdb = None

    def __init__(self, device=None):
        self.__device = device

    def create_directory(self, directory):
        self.__device.shell('mkdir -p ' + directory)

    def is_exists(self, file):
        return self.__device.shell('[ -e ' + file + ' ] && echo 1 || echo 0').strip() == '1'

    def is_directory(self, directory):
        return self.__device.shell('[ -d ' + directory + ' ] && echo 1 || echo 0').strip() == '1'

    def is_file(self, file):
        return self.__device.shell('[ -f ' + file + ' ] && echo 1 || echo 0').strip() == '1'

    def del_file(self, file):
        self.__device.shell('rm -rf ' + file)

    def del_directory(self, directory):
        self.del_file(directory)

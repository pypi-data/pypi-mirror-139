from AyAdb import AyAdb


class App:
    __device: AyAdb = None

    def __init__(self, device=None):
        self.__device = device

    def get_main_activity(self, package_name):
        return self.__device.shell(f"cmd package resolve-activity -c android.intent.category.LAUNCHER {package_name} | sed -n '/name=/s/^.*name=//p'")

    def launch(self, package_name, activity=None, use_monkey=False):
        if use_monkey:
            return self.__device.shell(f'monkey -p {package_name} -c android.intent.category.LAUNCHER --pct-syskeys 0 1')
        return self.__device.shell(f'am start -n {package_name}/{activity if activity else self.get_main_activity(package_name)}')

    def stop(self, package_name):
        return self.__device.shell(f'am force-stop {package_name}')

    def install_apk(self, apk_path, replace=False, downgrade=False):
        filename = apk_path.split('/')[-1]
        self.__device.push(apk_path, '/data/local/tmp/' + filename)
        command = 'pm install '
        if replace:
            command += '-r '
        if downgrade:
            command += '-d '
        command += '/data/local/tmp/' + filename
        result = self.__device.shell(command)
        self.__device.shell('rm /data/local/tmp/' + filename)
        return result

    def uninstall_apk(self, package_name, keep_data=False):
        command = 'pm uninstall '
        if keep_data:
            command += '-k '
        command += package_name
        return self.__device.shell(command)

    def current_activity(self):
        tmp_str = self.__device.shell('dumpsys window | grep mCurrentFocus').strip()
        tmp_str = tmp_str.split(' ')[-1]
        tmp_str = tmp_str.split('/')
        return '/'.join(tmp_str[:-1]), tmp_str[-1][:-1]

    def get_installed_packages(self):
        tmp_list = []
        for line in self.__device.shell('pm list packages').split('\n'):
            try:
                tmp_list.append(line.split(':')[1].replace('\r', ''))
            except IndexError:
                pass
        return tmp_list


from anadroid.utils.Utils import execute_shell_command


class WorkUnit(object):
    def __init__(self, bin_cmd):
        self.command = bin_cmd
        self.cmd_args = {}
        self.has_timeout = False

    def execute(self, pkg_name, *args, **kwargs):
        self.command = self.command + pkg_name
        print("executing command " + self.command)
        res = execute_shell_command(self.command)
        res.validate(Exception("Error executing command " + self.command))

    def build_command(self,  pkg_name, *args, **kwargs):
        self.command = self.command % pkg_name if "%" in self.command else self.command + " " + pkg_name
        if 'timeout' in kwargs:
            self.add_timeout(kwargs.get('timeout'))
        return self.command

    def add_timeout(self, timeout_val):
        if not self.has_timeout:
            self.command = f"timeout {timeout_val} {self.command}"
            self.has_timeout = True

    def config(self, id=None, *args, **kwargs):
        #adb shell monkey -s $monkey_seed -p $package -v --pct-syskeys 0 --ignore-security-exceptions --throttle $delay_bt_events $monkey_nr_events) &> $localDir/monkey$monkey_seed.log)"
        cmd = self.command + " "
        cmd += "" if id is None else id
        for k, v in kwargs.items():
            cmd += f' {k} {v}'
        self.command = cmd

    def export_results(self, target_dir=None):
        pass

    def append_prefix(self, prefix):
        self.command = prefix + " " + self.command
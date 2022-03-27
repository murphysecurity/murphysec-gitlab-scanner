# coding: utf-8
import subprocess
import platform


class MurphyScan:
    def __init__(self, token):
        self.token = token

    def scan(self, path):
        sysstr = platform.system()
        if sysstr == "Windows":
            cmd = f'./client/murphysec-cli-win.exe scan ./projects/{path} --json --token {self.token }'
            print("Call Windows tasks")
        elif sysstr == "Linux":
            cmd = f'./client/murphysec-linux-amd64 scan ./projects/{path} --json --token {self.token}'
            print("Call Linux tasks")
        elif sysstr == "Darwin":
            cmd = f'./client/murphysec-darwin-amd64 scan ./projects/{path} --json --token {self.token}'
            print("Call mac tasks")
        else:
            print('can not surport system {}'.format(sysstr))
            cmd = ''
        return self.__runcmd(cmd)

    def __runcmd(self, cmd):
        ret = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8",
                             timeout=3600)
        if ret.returncode == 0:
            return ret.stdout
        else:
            print(ret)
            raise RuntimeError(f"scan {cmd} error")
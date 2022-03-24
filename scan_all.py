# coding: utf-8
import json
import gitlab
import subprocess
import platform
from datetime import datetime
import os
import stat
import shutil
import optparse


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


class MyGitlab:
    def __init__(self, addr, token):
        self.token = token
        self.addr = addr
        self.gl = gitlab.Gitlab(self.addr, private_token=self.token)

    def __runcmd(self, command):
        ret = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8",
                             timeout=3600)
        if ret.returncode == 0:
            return ret.stdout
        else:
            raise RuntimeError(f"runcmd {command} error")

    def get_repo_list(self):
        pro_list = self.gl.projects.list()
        clone_list = []
        for pro in pro_list:
            clone_list.append(pro.http_url_to_repo)
        return clone_list

    def clone(self, git_url):
        path = datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')
        clone_url = f"{git_url.split('://')[0]}://oauth2:{self.token}@{git_url.split('://')[1]}"
        res = self.__runcmd(f"git clone {clone_url} projects/{path}")
        if res == None:
            raise RuntimeError(f"clone {git_url} error")
        return path

    def del_code(self, path):
        path = os.getcwd() + '/projects/' + path
        print(path)
        if os.path.exists(path):
            for fileList in os.walk(path):
                for name in fileList[2]:
                    os.chmod(os.path.join(fileList[0], name), stat.S_IWRITE)
                    os.remove(os.path.join(fileList[0], name))
            shutil.rmtree(path)


def run(git_addr, git_token, mf_token):
    my_gl = MyGitlab(addr=git_addr, token=git_token)
    mf = MurphyScan(token=mf_token)
    repos = my_gl.get_repo_list()
    for repo_url in repos:
        path = my_gl.clone(repo_url)
        scan_res = mf.scan(path)
        my_gl.del_code(path)
        print(json.loads(scan_res))
        # 添加自己的逻辑


if __name__ == '__main__':
    usage = "python %prog -A/--address <unning address> -T/--Token <unning gitlab_token> -t/--token <unning mf_token>"
    parser = optparse.OptionParser(usage)
    parser.add_option('-A', '--address', dest='address', type='string', help='running gitlab address', default='')
    parser.add_option('-T', '--gitlab_token', dest='gitlab_token', type='string', help='running gitlab token', default='')
    parser.add_option('-t', '--mf_token', dest='mf_token', type='string', help='running murphy token', default='')
    options, args = parser.parse_args()
    run(options.address, options.gitlab_token, options.mf_token)

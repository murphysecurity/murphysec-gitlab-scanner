# coding: utf-8
import gitlab
import subprocess
from datetime import datetime
import os
import stat
import shutil


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

    def clone_branch(self, git_url, branch):
        path = datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')
        clone_url = f"{git_url.split('://')[0]}://oauth2:{self.token}@{git_url.split('://')[1]}"
        res = self.__runcmd(f"git clone -b {branch} {clone_url} projects/{path}")
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
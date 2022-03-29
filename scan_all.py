# coding: utf-8
import json
import optparse
from libs.git import MyGitlab
from libs.murphy import MurphyScan



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

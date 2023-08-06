import paramiko


class SSHClient:
    def __init__(self, host, user, password):
        self.sshClient = paramiko.SSHClient()
        self.sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 允许连接不在know_hosts文件中的主机
        self.sshClient.connect(host, 22, user, password, look_for_keys=False)

    def execmd(self, cmdStr):
        """
        :param cmdStr: 需要输入的命令
        """
        stdin, stdout, stderr = self.sshClient.exec_command(cmdStr)
        return stdout

    def close(self):
        self.sshClient.close()

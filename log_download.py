from config_log_download import *
import paramiko, getpass, gzip, os
from os import remove


try:
    remove(prm_log_name)
except FileNotFoundError:
    pass
try:
    remove(prm_log_name + '.gz')
except FileNotFoundError:
    pass

password = getpass.getpass(prompt='pwd:')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=remote_host, username=remote_usr, password=password)
stdin, stdout, stderr = ssh.exec_command('uptime')

print(stdout.readline())

stdin, stdout, stderr = ssh.exec_command('rm -f ' + remote_work_dir + r'/*')
stdin, stdout, stderr = ssh.exec_command('cp ' + remote_log_dir + r' ' + remote_work_dir)
stdin, stdout, stderr = ssh.exec_command('gzip ' + remote_work_dir + r'/' + prm_log_name)
stdin, stdout, stderr = ssh.exec_command('ls -lF ' + remote_work_dir)

for line in stdout.read().splitlines():
    print(line)

ftp = ssh.open_sftp()
ftp.get(remote_work_dir + r'/' + prm_log_name + r'.gz', prm_log_name + r'.gz')

ftp.close()
ssh.close()

with gzip.open(prm_log_name + '.gz', 'rb') as inF:
    with open(prm_log_name, 'wb') as outF:
        for inline in inF:
            outF.write(inline)

inF.close()
outF.close()

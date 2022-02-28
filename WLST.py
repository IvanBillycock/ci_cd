import subprocess
import paramiko
from urlparse import urlparse

adminUser="*******"
adminPassword="******"
adminUrl="t3://eb-exp-demo-ufos.otr.ru:7001"
applicationName='sufd-server'
targetServers="test_ms_dir"
#targetServers="WC_Portlet"
WLST="/oracle/oem13c/wlserver/common/bin/wlst.sh"

ssh_key_path = "/home/oracle/.ssh/id_rsa"
ssh_login = 'oracle'

### wlst commands
wlst_cd = "cd('/AppDeployments/sufd-server')\n"
wlst_print = "print cmo.getAbsoluteSourcePath()\n"
wlst_connect = 'connect("{}", "{}", "{}")\n'.format(adminUser, adminPassword, adminUrl)


def get_mserver_dir():
    wlst_session.stdin.write(wlst_cd)
    wlst_session.stdin.flush()
    wlst_session.stdin.write(wlst_print)
    stdout_wlst_string = wlst_session.communicate()[0]
### do not use this piece below. it was fixed in python 3
    stdout_wlst_list = stdout_wlst_string.split('\n')
    for row in stdout_wlst_list:
        if 'servers/' in row:
            half_path = row.find('servers/')
            path = (row[:(half_path+8)]) + targetServers
    return path


def delete_mserver_folder():
    try:
        print('Deleting a Managed Server folder')
        ssh_parsed_url = urlparse(adminUrl)
        ssh_host = ssh_parsed_url.hostname.split(':')[0]
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        k = paramiko.RSAKey.from_private_key_file(ssh_key_path)

        client.connect(ssh_host, username=ssh_login, pkey = k)
        stdin, stdout, stderr = client.exec_command('rm -rf ' + mserver_dir)
        client.close()
        print('Deleting done and looks good')
    except IndexError as delete_mserver_folder_error:
        print('Deleting failed. Probably a problem in ssh connection')
        print(delete_mserver_folder_error)


try:
    print("WLST session Staring")
    wlst_session = subprocess.Popen(WLST, shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    wlst_session.stdin.write(wlst_connect)
    mserver_dir = get_mserver_dir()
    print(mserver_dir)
    delete_mserver_folder()
    wlst_session.stdin.close()
    print("WLST Closed")
except IndexError as e:
    print("it didn't work out...")
    print(e)
    wlst_session.stdin.close()




### jython version with run .sh
def get_mserver_dir():
    serverConfig()
    cd("/AppDeployments/" + applicationName)
    absolute_path = cmo.getAbsoluteSourcePath()
    domainRuntime()
    half_path = absolute_path.find('servers/')
    mserver_dir = (absolute_path[:(half_path+8)]) + targetServers
    return mserver_dir

# Deploy script init
try:
    mserver_dir = get_mserver_dir()
    os.system(r'./rm_mserver_dir.sh' +' '+ section +' '+ mserver_dir)
except:
    print "Unexpected error: ", sys.exc_info()[0]
    dumpStack()
    raise

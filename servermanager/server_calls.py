import paramiko

def get_system_info(client):
    """ Get system basic info about OS , architecture 
    It is already parsed for html exhibition"""
    stdin,stdout,stderr = client.exec_command('uname -srnm')

    return stdout.read()

def get_disk_info(client):
    """ Execute df command on remote server """
    #connect to remote server
    stdin,stdout,stderr = client.exec_command('df -h')

    return parse_disk_info(stdout.read())

def parse_disk_info(disk_info):
    """ Parse the info from 'df' command """
    # info format Filesystem,Size,Used,Avail,Use%,Mounted on
    info = []
    _info = disk_info.split('\n')
    for entry in _info[1:-1]:
        _entry = entry.split()
        assert _entry != []
        if  '/' in _entry[0]:
            info.append(entry)
    return info

def get_processes_info(client):
    """ Get processes information on remote server """
    stdin,stdout,stderr = client.exec_command('ps')
    info = stdout.read().split('\n')
    return info

def get_services_info(client):
    """ Get processes information on remote server """
#    stdin,stdout,stderr = client.exec_command('ps ax')
#    return stdout.read()
    return 'Not implemented yet'

def get_mem_info(client):
    """ Get RAM usage information on remote server """
    stdin,stdout,stderr = client.exec_command('vmstat')
    info = stdout.read().split('\n')
    return parse_mem_info(info)

def parse_mem_info(mem_info):
    """ Format vmstat info """
    _info = []
    #parse header
    _info.append(mem_info[0].split(' ')) 
    #parse sub-header
    _info.append(mem_info[1].split()) 
    #parse content
    _info.append(mem_info[2].split()) 
    #make return dictionaries
    mem = {'swapped':_info[2][2],'free':_info[2][3],'cached':_info[2][5]}
    cpu = {'used':_info[2][12],'sys':_info[2][13],'idle':_info[2][14]}
    return mem,cpu

def estabilish_connection(server_info):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    #missing host key policy
    client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy()) 
    client.connect(**server_info)
    return client

def get_all_info(client):
    info = {}
    info['disk'] = get_disk_info(client)
    info['system'] = get_system_info(client)
    info['processes'] = get_processes_info(client)
    info['mem'],info['cpu'] = get_mem_info(client)
#   info['services'] = get_disk_info(client)
    return info

# Tests
def get_server():
    #testing
    key_filename='~/.ssh/id_rsa'
    # basic info: hostname, port, username, password (or key_filename?)
    # testing server info
    server_info = {'hostname':'localhost','username':'dsl','password':'dsl','port':5022}
    return server_info 

def test_info_functions():
    # receive the server connection info
    server_info = get_server()
    # connect to the remote server
    client = estabilish_connection(server_info)
    #execute the functions
    return get_all_info(client)

if __name__ == '__main__':
    print test_info_functions()

    



import netmiko
from netmiko import ConnectHandler
import configparser

config = configparser.ConfigParser()
config.read("/scripts/config.ini")

iosv_l2 = {
    'device_type': config['networkswitch.credentials']['device_type'],
    'ip': config['networkswitch.credentials']['ipaddress'],
    'username': config['networkswitch.credentials']['username'],
    'password': config['networkswitch.credentials']['password'],
    'secret': config['networkswitch.credentials']['adminpassword'],
}

net_connect =ConnectHandler(**iosv_l2)
net_connect.enable()
getAllPortStatus=net_connect.send_command('show ip int brief')

print(getAllPortStatus)
portsStatus = []
counter=0

for line in getAllPortStatus.splitlines():
    line = line.split()
    counter += 1
    
    useful=[]
    for value in line:
        useful.append(value)

    portsStatus.append(useful)
print(portsStatus)



#config_commands = [ 'int loop 0', 'ip addre 1.1.1.1 255.255.255.0', 'no sh']
#output = net_connect.send_config_set(config_commands)
#print (output)
#output =net_connect.send_command('show ip int brief')
#print (output)

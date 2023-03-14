from netmiko import ConnectHandler
import configparser
import logging
import sqlite3

#Config
config = configparser.ConfigParser()
config.read("/scripts/config.ini")

#Logging
logging.basicConfig(filename=config['projectinfo']['logPath']+"latest.log", level=logging.DEBUG)
logger = logging.getLogger("netmiko")

device = {
    'device_type': config['networkswitch.credentials']['device_type'],
    'ip': config['networkswitch.credentials']['ipaddress'],
    'username': config['networkswitch.credentials']['username'],
    'password': config['networkswitch.credentials']['password'],
    'secret': config['networkswitch.credentials']['adminpassword'],
}

#Establish connection
connection =ConnectHandler(**device)
connection.enable()

#
# Data processing
#
conn = sqlite3.connect(config['projectinfo']['databasePath']+config['projectinfo']['databaseFileName'])
cur = conn.cursor()

def disableSinglePort(port):
    port = str(port)

    # TODO CHECK HOW LONG THE PORT IS OFFLINE BEFORE SHUTING DOWN

    print("Disabled port: "+port)
    config_commands = [
        "interface range fa0/" + port, 
        'shutdown'
    ]
    response = connection.send_config_set(config_commands)

def enableSinglePort(port):
    port = str(port)
    print("Enabled port: "+port)
    config_commands = [
        "interface range fa0/" + port, 
        'no shutdown'
    ]
    response = connection.send_config_set(config_commands)


def enableAllPorts():
    print("Waiting for port activation")
    
    cur = conn.cursor()
    cur.execute(""" SELECT portname FROM network_switch """)

    f = cur.fetchall()
    for interface in f:        
        config_commands = [
            "interface " + interface[0], 
            "no shutdown"
        ]
        connection.send_config_set(config_commands)
    print("Enabled all ports")

def disableAllUnsedPorts():
    print("Waiting for port deactivation")
    
    cur = conn.cursor()
    cur.execute(""" SELECT portname, status FROM network_switch """)

    f = cur.fetchall()
    for interface in f:
        if (interface[1] != 1):
            config_commands = [
                "interface " + interface[0], 
                "shutdown"
            ]
            connection.send_config_set(config_commands)
    print("Disabled all unused ports")
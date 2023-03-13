import netmiko
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

disableSinglePort(1)
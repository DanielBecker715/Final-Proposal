import os, configparser
from .switchstatus import *
from .switchconnection import SwitchConnection
import logging


#Config
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '..', 'config.ini'))

#Logging
logging.basicConfig(filename=config['projectinfo']['logPath']+"latest.log", level=logging.DEBUG)
logger = logging.getLogger("netmiko")

#
# Data processing
#    
def enableSinglePort(port):
    # When its a distionary its already mapped
    if (type(port) != dict):
        port = database.mapToDatabaseFields(port)
    if (port["status"] != 1):
        print("Enabled port: "+port["portname"])
        database.updatePortStatus((port["ipaddress"], port["ok"], port["method"], 0, 0, datetime.datetime.now(), port["portname"]))
        config_commands = [
            "interface " + port["portname"], 
            "no shutdown"
        ]
        SwitchConnection.getConnection().send_config_set(config_commands)

def disableSinglePort(port):
    if (type(port) != dict):
        port = database.mapToDatabaseFields(port)
    if (port["status"] == 0):
        print("Disabled port: "+port["portname"])
        database.updatePortStatus((port["ipaddress"], port["ok"], port["method"], 2, 2, datetime.datetime.now(), port["portname"]))
        config_commands = [
            "interface " + port["portname"], 
            "shutdown"
        ]
        SwitchConnection.getConnection().send_config_set(config_commands)

def enableAllPorts():
    savePortStatusToDatabase(getPortStatusFromSwitch())
    ports = database.getPortStatusFromDatabase()

    print("Waiting for port activation")
    for port in ports:
        enableSinglePort(port)
    #for port in database.getPortStatusByDatabase():
        #rint(port) # DEBUG

def disableAllUnsedPorts():
    savePortStatusToDatabase(getPortStatusFromSwitch())
    
    ports = database.getPortStatusFromDatabase()

    print("Waiting for port deactivation")
    for port in ports:
        dat = datetime.datetime.strptime(port["latest_port_change"], '%Y-%m-%d %H:%M:%S.%f')
        minutes_diff = (datetime.datetime.now() - dat).total_seconds() / 60.0
        if (minutes_diff >= int(config["sheduler.general"]["shedulerBlocksPortsInMinutes"])):
            if (port["status"] == 0):
                disableSinglePort(port)
    # DEBUG
    #for port in database.getPortStatusByDatabase():
        #print(port)
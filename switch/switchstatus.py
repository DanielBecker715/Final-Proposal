import os, configparser, datetime
from netmiko import ConnectHandler
import database.dbcontroller as database
import configparser
from rich import *
from .switchconnection import SwitchConnection

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '..', 'config.ini'))

#
# Data processing
#
def getPortStatusFromSwitch():
    connection = SwitchConnection.getConnection()

    getAllPortStatus = connection.send_command('show ip int brief')

    portsStatus = []
    for line in getAllPortStatus.splitlines():
        array = line.split()

        #Convert values into database readable values
        useful=[]
        for value in array:
            if (value == "down"):
                useful.append(0)
            elif (value == "administratively"):
                useful.append(2)
            elif (value == "up"):
                useful.append(1)
            elif (value == "YES"):
                useful.append(1)
            elif (value == "NO"):
                useful.append(0)
            else:
                useful.append(value)
        dct = {}
        dct["portname"] = useful[0]
        dct["ipaddress"] = useful[1]
        dct["ok"] = useful[2]
        dct["method"] = useful[3]
        dct["status"] = useful[4]
        dct["protocol"] = useful[5]
        dct["latest_port_change"] = datetime.datetime.now()
        portsStatus.append(dct)
    portsStatus = portsStatus[2:]
    #Removes the headlines
    return portsStatus

def savePortStatusToDatabase(portStatusList):
    # If ports in DB exists then update / else insert
    oldData = getPortStatusFromSwitch()

    counter = 0
    for port in portStatusList:
        if (port["status"] != oldData[counter]["status"]):
            database.updatePortStatus((port["ipaddress"], port["ok"], port["method"], port["status"], port["protocol"], datetime.datetime.now(), port["portname"]))
            print("Wrote port: "+port["portname"]+"to "+port["status"])
        counter += 1
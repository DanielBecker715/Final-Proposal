#!/usr/bin/env python3
import sys, os, sqlite3
import configparser
import glob
import switch.switchstatus as switchstatus
import database.dbcontroller as databse
import card.cardcontroller as cardcontroller
import card.card_scheduler as scheduler
from switch.switchconnection import SwitchConnection
import multiprocessing as mp
import queue

#Config
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))
sys.path.append(config['projectinfo']['projectPath'])

allImportantPaths = [
    config['projectinfo']['logPath'],
    config['projectinfo']['databasePath']
]

# Check all paths for existing and create them if not
for path in allImportantPaths:
    if (not os.path.exists(path)):
        os.makedirs(path)

# Remove old logs
files = glob.glob(config['projectinfo']['logPath']+"*")
for file in files:
    os.remove(file)

# Ensures that the most important tables are populated
if (databse.countNetworkSwitchTable == 0):
    conn = sqlite3.connect(config['projectinfo']['databasePath']+config['projectinfo']['databaseFileName'])
    interfaces = switchstatus.getPortStatusListBySwitch()
    for interface in interfaces:
        databse.insertPortStatus(conn, (interface["ipaddress"], interface["ok"], interface["method"], interface["status"], interface["protocol"], interface["portname"]))
    conn.close()

# TODO: When a port is connected and then removed it doesnt gets disabled

# protect the entry point
if __name__ == '__main__':
    singleton = SwitchConnection.getInstance()
    connection = singleton.connect(
        device_type=config['networkswitch.credentials']['device_type'],
        ip=config['networkswitch.credentials']['ipaddress'],
        username=config['networkswitch.credentials']['username'],
        password=config['networkswitch.credentials']['password'],
        secret=config['networkswitch.credentials']['adminpassword']
    )
    
    scheduler.runScheduler()
    #cardcontroller.listenForCard()
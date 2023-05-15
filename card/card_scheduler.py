import os, configparser
import schedule, time
import switch.switchcontroller as switch
import database.dbcontroller as database

from netmiko import ConnectHandler

#Config
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '..', 'config.ini'))

device = {
    'device_type': config['networkswitch.credentials']['device_type'],
    'ip': config['networkswitch.credentials']['ipaddress'],
    'username': config['networkswitch.credentials']['username'],
    'password': config['networkswitch.credentials']['password'],
    'secret': config['networkswitch.credentials']['adminpassword'],
}

connection = ConnectHandler(**device)
connection.enable()

def job():
    print("Job started")
    switch.disableAllUnsedPorts()
    print("Job done")

schedule.every(int(config['sheduler.general']['shedulerJobInSeconds'])).seconds.do(job)

def runScheduler():
    while 1:
        schedule.run_pending()
        time.sleep(1)
import netmiko
from netmiko import ConnectHandler
import configparser
import sqlite3

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

portsStatus = []
for line in getAllPortStatus.splitlines():
    line = line.split()

    useful=[]
    for value in line:
        if (value == "down"):
            useful.append(0)
        elif (value == "administratively"):
            useful.append(0)
        elif (value == "up"):
            useful.append(1)
        else:
            useful.append(value)

    portsStatus.append(useful)
#Removes the headlines
portsStatus = portsStatus[2:]

#
# Data processing
#
conn = sqlite3.connect(config['projectinfo']['databasePath']+config['projectinfo']['databaseFileName'])
cur = conn.cursor()

def countTable():
    cur.execute("select count(*) from network_switch")
    return cur.fetchall()[0][0]

# Save response to databse
def update_task(conn, task):
    sql = ''' UPDATE network_switch
              SET ipaddress = ?,
                  ok = ?,
                  method = ?,
                  status = ?,
                  protocol = ?
              WHERE portname = ?'''
    cur.execute(sql, task)
    conn.commit()
    
# Save response to databse
def insert_task(conn, task):
    sql = ''' INSERT INTO network_switch (portname,ipaddress,ok,method,status,protocol)
        VALUES(?,?,?,?,?,?) '''
    cur.execute(sql, task)
    conn.commit()

# If ports in DB exists then update / else insert 
if (countTable() != 0):
    for array in portsStatus:
        update_task(conn, (array[1], array[2], array[3], array[4], array[5], array[0]))
        print((array[0], array[1], array[2], array[3], array[4], array[5]))
else:
    for array in portsStatus:
        insert_task(conn, (array[0], array[1], array[2], array[3], array[4], array[5]))
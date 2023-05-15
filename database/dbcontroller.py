import os, configparser, sqlite3

#Config
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '..', 'config.ini'))

def mapToDatabaseFields(port):
    dct = {}
    dct["portname"] = port[0]
    dct["ipaddress"] = port[1]
    dct["ok"] = port[2]
    dct["method"] = port[3]
    dct["status"] = port[4]
    dct["protocol"] = port[5]
    dct["latest_port_change"] = port[6]
    return dct

def mapListToDatabaseFields(ports):
    tmp = []
    for port in ports:
        dct = {}
        dct["portname"] = port[0]
        dct["ipaddress"] = port[1]
        dct["ok"] = port[2]
        dct["method"] = port[3]
        dct["status"] = port[4]
        dct["protocol"] = port[5]
        dct["latest_port_change"] = port[6]
        tmp.append(dct)
    return tmp

def countNetworkSwitchTable(conn):
    cur = conn.cursor()
    cur.execute("select count(*) from network_switch")
    result = cur.fetchall()[0][0]
    cur.close()
    return result

def getPortStatusFromDatabase():
    conn = sqlite3.connect(config['projectinfo']['databasePath']+config['projectinfo']['databaseFileName'])
    cur = conn.cursor()
    cur.execute("select portname, ipaddress, ok, method, status, protocol, latest_port_change from network_switch")
    ports = cur.fetchall()
    cur.close()
    tmp = mapListToDatabaseFields(ports)
    return tmp

def updatePortStatus(task):
    conn = sqlite3.connect(config['projectinfo']['databasePath']+config['projectinfo']['databaseFileName'])
    cur = conn.cursor()
    cur.execute('''UPDATE network_switch
                    SET ipaddress = ?,
                        ok = ?,
                        method = ?,
                        status = ?,
                        protocol = ?,
                        latest_port_change = ?
                    WHERE portname = ?''', task)
    conn.commit()
    conn.close()
    
def insertPortStatus(conn, task):
    sql = ''' INSERT INTO network_switch (portname,ipaddress,ok,method,status,protocol)
        VALUES(?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()
    cur.close()
import os, configparser
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

class SwitchConnection:
    __instance = None
    __connection = None

    @staticmethod
    def getInstance():
        if SwitchConnection.__instance == None:
            SwitchConnection()
        return SwitchConnection.__instance
    
    @staticmethod
    def getConnection():
        return SwitchConnection.__connection

    def __init__(self):
        """ Virtually private constructor. """
        if SwitchConnection.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            SwitchConnection.__instance = self

    def connect(self, **kwargs):
        if self.__connection == None:
            self.__connection = ConnectHandler(**kwargs)
        return self.__connection

#!/usr/bin/env python3
import configparser
import os
import glob

#Config
config = configparser.ConfigParser()
config.read("/scripts/config.ini")

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
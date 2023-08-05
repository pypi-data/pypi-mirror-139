#!/usr/bin/env python3

"""
This module backs up all Powershell scripts in Intune.

Parameters
----------
path : str
    The path to save the backup to
output : str
    The format the backup will be saved as
token : str
    The token to use for authenticating the request
"""

import json
import os
import base64
import yaml

from .clean_filename import clean_filename
from .graph_request import makeapirequest
from .get_add_assignments import get_assignments

## Set MS Graph endpoint
endpoint = "https://graph.microsoft.com/beta/deviceManagement/deviceManagementScripts/"

## Get all Powershell scripts and save them in specified path


def savebackup(path, output, token):
    configpath = path+"/"+"Scripts/Powershell/"
    data = makeapirequest(endpoint, token)

    for script in data['value']:
        script_data = makeapirequest(endpoint + script['id'], token)
        remove_keys = {'id', 'createdDateTime',
                       'version', 'lastModifiedDateTime'}
        for k in remove_keys:
            script_data.pop(k, None)

        print("Backing up Powershell script: " + script_data['displayName'])
        if os.path.exists(configpath) == False:
            os.makedirs(configpath)

        ## Get assignments of Device Configuration
        get_assignments(endpoint, script_data, script['id'], token)

        ## Get filename without illegal characters
        fname = clean_filename(script_data['displayName'])
        ## Save Powershell script as JSON or YAML depending on configured value in "-o"
        if output != "json":
            with open(configpath+fname+".yaml", 'w') as yamlFile:
                yaml.dump(script_data, yamlFile, sort_keys=False,
                          default_flow_style=False)
        else:
            with open(configpath+fname+".json", 'w') as jsonFile:
                json.dump(script_data, jsonFile, indent=10)

        ## Save Powershell script data to the script data folder
        if os.path.exists(configpath + "Script Data/") == False:
            os.makedirs(configpath + "Script Data/")
        decoded = base64.b64decode(
            script_data['scriptContent']).decode('utf-8')
        f = open(configpath+"Script Data/"+script_data['fileName'], 'w')
        f.write(decoded)
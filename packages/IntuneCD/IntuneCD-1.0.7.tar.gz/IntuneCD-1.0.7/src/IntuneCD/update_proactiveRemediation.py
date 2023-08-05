#!/usr/bin/env python3

"""
This module updates all Powershell scripts in Intune if the configuration in Intune differs from the JSON/YAML file.

Parameters
----------
path : str
    The path to where the backup is saved
token : str
    The token to use for authenticating the request
"""

import json
import os
import base64
import yaml
import re

from .graph_request import makeapirequest, makeapirequestPatch, makeapirequestPost
from .get_add_assignments import add_assignment

from deepdiff import DeepDiff

## Set MS Graph endpoint
endpoint = "https://graph.microsoft.com/beta/deviceManagement/deviceHealthScripts"


def update(path, token, assignment=False):

    ## Set Powershell script path
    configpath = f'{path}/Proactive Remediations'
    ## If Powershell script path exists, continue
    if os.path.exists(configpath) == True:
        for filename in os.listdir(configpath):
            file = os.path.join(configpath, filename)
            # If path is Directory, skip
            if os.path.isdir(file):
                continue
            # If file is .DS_Store, skip
            if filename == ".DS_Store":
                continue

            ## Check which format the file is saved as then open file, load data and set query parameter
            with open(file) as f:
                    if filename.endswith(".yaml"):
                        data = json.dumps(yaml.safe_load(f))
                        repo_data = json.loads(data)
                        q_param = {
                            "$filter": f"displayName eq '{repo_data['displayName']}'"}
                    elif filename.endswith(".json"):
                        f = open(file)
                        repo_data = json.load(f)
                        q_param = {"$filter": f"displayName eq '{repo_data['displayName']}'"}

                    ## Create object to pass in to assignment function
                    assign_obj = {}
                    if "assignments" in repo_data:
                        assign_obj['assignments'] = repo_data['assignments']
                    repo_data.pop('assignments', None)

                    ## Get Powershell script with query parameter
                    mem_proactiveRemediation = makeapirequest(endpoint, token,q_param)

                    ## If Powershell script exists, continue
                    if mem_proactiveRemediation['value']:
                        print("-" * 90)
                        q_param = None
                        ## Get Powershell script details
                        mem_data = makeapirequest(endpoint + "/" + mem_proactiveRemediation['value'][0]['id'], token,q_param)
                        pid = mem_data['id']
                        ## Remove keys before using DeepDiff
                        remove_keys = {'id', 'createdDateTime','version','lastModifiedDateTime','isGlobalScript','highestAvailableVersion'}
                        for k in remove_keys:
                            mem_data.pop(k, None)

                        ## Check if assignment needs updating and apply chanages
                        if assignment == True:
                            add_assignment(endpoint, assign_obj,pid,token,proactive_remediation=True)

                        ## Check if script data is saved and read the file
                        detection_script_name = f"{configpath}/Script Data/{repo_data['displayName']}_DetectionScript.ps1"
                        remediation_script_name = f"{configpath}/Script Data/{repo_data['displayName']}_RemediationScript.ps1"
                        if os.path.exists(detection_script_name) and os.path.exists(remediation_script_name):
                            with open(detection_script_name, 'r') as df:
                                repo_detection_config = df.read()
                            with open(remediation_script_name, 'r') as rf:
                                repo_remediation_config = rf.read()

                            mem_detection_config = base64.b64decode(
                                mem_data['detectionScriptContent']).decode('utf-8')
                            mem_remediation_config = base64.b64decode(
                                mem_data['remediationScriptContent']).decode('utf-8')

                            ddiff = DeepDiff(mem_detection_config, repo_detection_config, ignore_order=True).get('values_changed', {})
                            rdiff = DeepDiff(mem_remediation_config, repo_remediation_config, ignore_order=True).get('values_changed', {})
                            cdiff = DeepDiff(mem_data, repo_data, ignore_order=True, exclude_paths=["root['detectionScriptContent']",
                                                                                                    "root['remediationScriptContent']"]).get('values_changed', {})

                            ## If any changed values are found, push them to Intune
                            if cdiff or ddiff or rdiff:
                                print("Updating Proactive Remediation: " + \
                                      repo_data['displayName'] + ", values changed:")
                                if cdiff:
                                    for key, value in cdiff.items():
                                        setting = re.search("\[(.*)\]", key).group(1)
                                        new_val = value['new_value']
                                        old_val = value['old_value']
                                        print(f"Setting: {setting}, New Value: {new_val}, Old Value: {old_val}")
                                if ddiff:
                                    print(
                                        "Detection script changed, check commit history for change details")
                                if rdiff:
                                    print(
                                        "Remediation script changed, check commit history for change details")
                                detection_bytes = repo_detection_config.encode(
                                    'utf-8')
                                remediation_bytes = repo_remediation_config.encode(
                                    'utf-8')
                                repo_data['detectionScriptContent'] = base64.b64encode(
                                    detection_bytes).decode('utf-8')
                                repo_data['remediationScriptContent'] = base64.b64encode(
                                    remediation_bytes).decode('utf-8')
                                request_data = json.dumps(repo_data)
                                makeapirequestPatch(endpoint + "/" + pid, token,q_param,request_data)
                            else:
                                print(
                                    'No difference found for Proactive Remediation: ' + repo_data['displayName'])

                    ## If Powershell script does not exist, create it and assign
                    else:
                        print("-" * 90)
                        print("Proactive Remediation not found, creating: " + \
                              repo_data['displayName'])
                        request_json = json.dumps(repo_data)
                        post_request = makeapirequestPost(endpoint, token,q_param=None,jdata=request_json,status_code=201)
                        add_assignment(endpoint, assign_obj,post_request['id'],token,proactive_remediation=True)
                        print("Proactive Remediation created with id: " + post_request['id'])
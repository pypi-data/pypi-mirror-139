#!/usr/bin/env python3

"""
This module updates all Windows Enrollment Profiles in Intune if the configuration in Intune differs from the JSON/YAML file.

Parameters
----------
path : str
    The path to where the backup is saved
token : str
    The token to use for authenticating the request
"""

import json
import os
import yaml
import re

from .graph_request import makeapirequest, makeapirequestPatch, makeapirequestPost
from .get_add_assignments import add_assignment
from deepdiff import DeepDiff

## Set MS Graph endpoint
endpoint = "https://graph.microsoft.com/beta/deviceManagement/windowsAutopilotDeploymentProfiles"


def update(path, token, assignment=False):

    ## Set Windows Enrollment Profile path
    configpath = path+"/"+"Enrollment Profiles/Windows"
    ## If Windows Enrollment Profile path exists, continue
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
                        q_param = {"$filter": "displayName eq " +
                            "'" + repo_data['displayName'] + "'"}
                    elif filename.endswith(".json"):
                        f = open(file)
                        repo_data = json.load(f)
                        q_param = {"$filter": "displayName eq " + "'" + repo_data['displayName'] + "'"}

                    ## Create object to pass in to assignment function
                    assign_obj = {}
                    if "assignments" in repo_data:
                        assign_obj['assignments'] = repo_data['assignments']
                    repo_data.pop('assignments', None)

                    ## Get Windows Enrollment Profile with query parameter
                    mem_data = makeapirequest(endpoint, token,q_param)

                    ## If Windows Enrollment Profile exists, continue
                    if mem_data['value']:
                        print("-" * 90)
                        pid = mem_data['value'][0]['id']
                        ## Remove keys before using DeepDiff
                        remove_keys = {'id', 'createdDateTime','version','lastModifiedDateTime'}
                        for k in remove_keys:
                            mem_data['value'][0].pop(k, None)

                        ## Check if assignment needs updating and apply chanages
                        if assignment == True:
                            add_assignment(endpoint, assign_obj,pid,token,status_code=201,extra_url=None,wap=True)

                        diff = DeepDiff(mem_data['value'][0], repo_data, ignore_order=True).get('values_changed', {})

                        ## If any changed values are found, push them to Intune
                        if diff:
                            print("Updating Windows Enrollment profile: " + \
                                  repo_data['displayName'] + ", values changed:")
                            for key, value in diff.items():
                                setting = re.search("\[(.*)\]", key).group(1)
                                new_val = value['new_value']
                                old_val = value['old_value']
                                print(
                                    f"Setting: {setting}, New Value: {new_val}, Old Value: {old_val}")
                            if repo_data['managementServiceAppId']:
                                pass
                            else:
                                repo_data['managementServiceAppId'] = ""
                            request_data = json.dumps(repo_data)
                            makeapirequestPatch(endpoint + "/" + pid, token,q_param,request_data)
                        else:
                            print(
                                'No difference found for Windows Enrollment profile: ' + repo_data['displayName'])

                    ## If Autopilot profile does not exist, create it and assign
                    else:
                        print("-" * 90)
                        print(
                            "Autopilot profile not found, creating profile: " + repo_data['displayName'])
                        request_json = json.dumps(repo_data)
                        post_request = makeapirequestPost(endpoint, token,q_param=None,jdata=request_json,status_code=201)
                        add_assignment(endpoint, assign_obj,post_request['id'],token,status_code=201,extra_url=None,wap=True)
                        print("Autopilot profile created with id: " + post_request['id'])
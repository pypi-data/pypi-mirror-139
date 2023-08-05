import json
import os
from configparser import ConfigParser

import requests
import yaml


class MorphConfig(object):
    def __init__(self):
        # Process config file
        contentPackSelection = os.environ.get("CONTENTPACK")
        path_to_contentPack = os.path.join("contentpacks", contentPackSelection)
        configur = ConfigParser()
        configur.read(path_to_contentPack + "/configs.ini")
        # contentPack = contentPackSelection
        # Set Variables
        self.baseURL = configur.get("DEFAULT", "BASE_URL")
        self.ADMIN_USERNAME = configur.get("DEFAULT", "ADMIN_USERNAME")
        self.ADMIN_PASSWORD = configur.get("DEFAULT", "ADMIN_PASSWORD")
        #self.ROOT_USERNAME = configur.get("DEFAULT", "ROOT_USERNAME")
        #self.ROOT_PASSWORD = configur.get("DEFAULT", "ROOT_PASSWORD")

        def bearer():
            #  logger = morph_log.get_logger('getg')
            url = (
                self.baseURL
                + "/oauth/token?grant_type=password&scope=write&client_id=morph-api"
            )
            payload = {"username": self.ADMIN_USERNAME, "password": self.ADMIN_PASSWORD}
            result = requests.request("POST", url, verify=False, data=payload)
            jsonDump = json.loads(result.text)
            # logger.debug(jsonDump["access_token"])
            return jsonDump["access_token"]

        self.bearer = bearer()

    def verify(self):
        return False

    def header_appJson(self):
        return {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.bearer,
        }
    def initHeader(self):
        return {"Content-Type": "application/json"}
    def imageWhiteLabel(self):
        return {"Authorization": "Bearer " + self.bearer}

    def authBearer_noContent(self):
        return {"Authorization": "Bearer " + self.bearer}

    def createGroups(self):
        # group.createGroups()
        return self.baseURL + "/api/groups"

    def searchGroupsName(self):
        # group.getGroups()
        return self.baseURL + "/api/groups?name="

    def createRole(self):
        # role.genericRoleCreate
        return self.baseURL + "/api/roles"

    def searchRolePhrase(self):
        # role.genericRoleCreate_getRoleID_helper
        return self.baseURL + "/api/roles?phrase="

    def updateRolePermission(self):
        # role.genericRoleCreate_updateRole_feature_helper
        # used in conjunction with create role
        return "/update-permission"

    def updateGroupRolePerm(self):
        # role.groupAccess
        return "/update-group"

    def createInputs(self):
        # input.inputcreate
        return self.baseURL + "/api/library/option-types"

    def searchInputsName(self):
        # input.inputcreate
        return self.baseURL + "/api/library/option-types?name="

    def whitelabel(self):
        return self.baseURL + "/api/whitelabel-settings"

    def whitelabelimage(self):
        return self.baseURL + "/api/whitelabel-settings/images"

    def fileTemplate(self):
        return self.baseURL + "/api/library/container-templates"

    def tasks(self):
        return self.baseURL + "/api/tasks"

    def templateLookup(self):
        return self.baseURL + "/api/library/container-templates?name="

    def addWiki(self):
        return self.baseURL + "/api/wiki/pages"

    def searchWiki(self):
        return self.baseURL + "/api/wiki/pages?name="

    def createUser(self):
        return self.baseURL + "/api/users"

    def initSetup(self):
        return self.baseURL + "/api/setup/init"

    # def searchGroupsName(self):
    #    return self.baseURL+'/api/groups?name='

    # createGroup = self.baseURL+'/api/groups'
    # searchGroupName = baseURL+'/api/groups?name='


class Logger:
    def mainLogger():
        pass


class CreateGroupVars:
    def __init__(self, file):
        self.filename = file

    def __call__(self):
        with open(self.filename) as f:
            try:
                file = self.filename
                file = yaml.safe_load(f)
            except Exception as e:
                print("Exception: ", e)
        for k, v in file["groups"].items():
            name = file["groups"][k]["name"]
            description = file["groups"][k]["description"]
            location = file["groups"][k]["location"]
            code = file["groups"][k]["code"]
            return name, description, location, code
        # for loop here to name variables
        print("test")

    def payload(self):
        # create payload.
        print("test")

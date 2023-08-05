import glob
import json

import requests

# import urllib3
import yaml

from . import morph_log
from .classes import MorphConfig

# from tqdm import tqdm


#def getBearerToken(baseURL, sysPasswd):
#    url = baseURL + "/oauth/token?grant_type=password&scope=write&client_id=morph-api"
#    payload = {"username": ROOT_USERNAME, "password": sysPasswd}
#    result = requests.request("POST", url, verify=False, data=payload)
#    print(result.text)
#    jsonDump = json.loads(result.text)
#    return jsonDump["access_token"]


# def setup(baseURL, sysPasswd):
#    try:
#        executeSetup(baseURL, sysPasswd)
#    except Exception as e:
#        logger.error("Exception occurred", exc_info=True)
#        logger.error(
#            "There was an issue with the initial setup. Please check that you have the proper variables in the .env"
#        )
#        logger.debug("applianceName: " + APPLIANCE_NAME)
#        logger.debug("applianceURL: " + baseURL)
#        logger.debug("accountName: " + MASTER_TENANT)
#        logger.debug("username: " + ROOT_USERNAME)
#        logger.debug("email: " + ROOT_EMAIL)
#        logger.debug("firstname: " + ROOT_NAME)


# def executeSetup(baseURL, sysPasswd):
#    logger.info("Initial Setup Starting")
#    print("Executing Initial Setup")
#    url = baseURL+"/api/setup/init"
#    logger.debug("URL Endpoint: "+url)
#    payload = json.dumps({
#        "applianceName": APPLIANCE_NAME,
#        "applianceUrl": baseURL,
#        "accountName": MASTER_TENANT,
#        "username": ROOT_USERNAME,
#        "password": sysPasswd,
#        "email": ROOT_EMAIL,
#        "firstName": ROOT_NAME
#    })
#    headers = {'Content-Type': 'application/json'}
#    response = requests.request("POST", url, verify=False, headers=headers, data=payload)
#    logger.info("Completed Initial Setup: "+response.text)



def initSetup(yaml_file):
    logger = morph_log.get_logger("initSetup")
    morphApi = MorphConfig()
    header = morphApi.initHeader()
    url = morphApi.initSetup()
    verifySSL = morphApi.verify()
    files = glob.glob(yaml_file)
    for file in files:
        yaml_file = file
        logger.info('Current file: '+yaml_file)
    with open(yaml_file) as file:
        try:
            result=yaml.safe_load(file)
        except yaml.YAMLError as exc:
            logger.error(exc)
            logger.error('Unable to load file')
        #content = yaml.safe_load_all(file)
    applianceName = result['applianceName']
    applianceUrl = result['applianceUrl']
    accountName = result['accountName']
    username = result['username']
    password = result['password']
    email = result['email']
    firstname = result['firstName']
    payload = json.dumps({
        "applianceName": applianceName,
        "applianceUrl": applianceUrl,
        "accountName": accountName,
        "username": username,
        "password": password,
        "email": email,
        "firstName": firstname
    })
    response = requests.request(
        "POST", url, verify=verifySSL, headers=header, data=payload
    )
    logger.warning(response.text)

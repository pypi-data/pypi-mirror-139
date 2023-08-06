import json
import yaml
import requests
import os
import glob
from . import morph_log
import urllib
from .classes import MorphConfig

def getInputs(inputChecker):
    logger = morph_log.get_logger('getinput')
    logger.debug('###########    DEBUG    #############')
    logger.debug('Name: '+inputChecker)
   #logger.debug('bearerToken: '+bearerToken)
   # logger.debug('baseURL: '+baseURL)
    logger.debug('###########    DEBUG    #############')
    try:
        return getInput_helper(inputChecker, logger)
    except Exception as e:
        logger.warning(
            inputChecker +
            ' Found Null Value for Input Lookup.  Setting Variable to "none" and passing exception'
        )
        return 'none'

def getInput_helper(inputChecker, logger):
    morphApi= MorphConfig()
    url_searchInputsName = morphApi.searchInputsName()
    url = url_searchInputsName+inputChecker
    header = morphApi.header_appJson()
    verifySSL = morphApi.verify()
    #headers = {'Content-Type': 'application/json','Authorization': 'Bearer ' +bearerToken}
    result = requests.request("GET", url, verify=verifySSL, headers=header)
    print(result.text)
    jsonData = result.json()
    inputID = jsonData['inputs'][0]['id']
    logger.debug('###########    DEBUG    #############')
    logger.debug('url: '+url)
    logger.debug('groupID: '+ str(inputID))
   # logger.debug('baseURL: '+baseURL)
    logger.debug('###########    DEBUG    #############')
    return inputID


def inputCreate(yaml_file):
    logger = morph_log.get_logger('crinput')
    morphApi= MorphConfig()
    url_createInputs = morphApi.createInputs()
    url_searchInputsName = morphApi.searchInputsName()
    header = morphApi.header_appJson()
    verifySSL = morphApi.verify()
    #headers = {'Content-Type': 'application/json','Authorization': 'Bearer ' +bearerToken}
    files = glob.glob(yaml_file)
    #url = baseURL+'/api/library/option-types'
    for file in files: 
        yaml_file = file
        logger.info('Current file: '+yaml_file)
        with open(yaml_file) as f:
            try: 
                result=yaml.safe_load(f)
            except yaml.YAMLError as exc:
                logger.error(exc)
                logger.error('Was unable to load the yaml file.')
        for k, v in result['inputs'].items():
            name = result['inputs'][k]['name']
            description = result['inputs'][k]['description']
            type = result['inputs'][k]['type']
            fieldName = result['inputs'][k]['fieldName']
            fieldLabel = result['inputs'][k]['fieldLabel']
            payload = json.dumps({
                    "optionType": {
                      "name": name,
                      "type": type,
                      "description": description,
                      "fieldName": fieldName,
                      "fieldLabel": fieldLabel
                    }
            })
            inputChecker = urllib.parse.quote(name)
            checkinputs = url_searchInputsName+inputChecker
            checkInputsrequest = requests.request("GET", checkinputs, verify=verifySSL, headers=header)
            checkInputsrequest = json.loads(checkInputsrequest.text)
            if len(checkInputsrequest['optionTypes']) == 0:
                logger.info('Input not found: '+name)
                logger.info('Input will be created.')
                requests.request('POST', url_createInputs, verify=verifySSL, headers=header, data=payload)
            elif name == checkInputsrequest['optionTypes'][0]['name']:
                logger.info('Input already exists: '+name+'. Skipping...')
import json

import requests
import urllib3
import yaml

from . import morph_log
from .classes import MorphConfig

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def userRole_array_helper():
    print("Eventual check if user is real or not. ")


def createUser(yaml_file):
    logger = morph_log.get_logger("createUser")
    morphApi = MorphConfig()
    header = morphApi.header_appJson()
    url = morphApi.createUser()
    verifySSL = morphApi.verify()
    with open(yaml_file) as file:
        # logger.info('Yaml File', yaml_file)
        content = yaml.safe_load_all(file)
        # logger.info('content', content)
        next(content)  # skip first document
        for doc in content:
            # print('one doc')
            payload = json.dumps(doc, indent=2)
            # print(json.dumps(doc, indent=2))
            response = requests.request(
                "POST", url, verify=verifySSL, headers=header, data=payload
            )
            logger.info(response.text)

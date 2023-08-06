import glob
from configparser import ConfigParser

import yaml

from . import file_handler, initapp, morph_log


def contentPack_initSetup(contentPackSelection):
    # Process config file
    configur = ConfigParser()
    configur.read(contentPackSelection + "/configs.ini")
    # Logging
    logger = morph_log.get_logger("cp_impl")
    files_inContentPack = glob.glob(contentPackSelection + "/*")
    for file in files_inContentPack:
        if file.endswith(".yaml") and file == contentPackSelection + "/initial.yaml":
            yaml_file = file
            logger.info("Current contentPack file processing: " + yaml_file)
            # with open(yaml_file, 'r') as stream:
            document = open(yaml_file, "r")
            generator = yaml.safe_load_all(document)
            dictoinary = generator.__next__()
            # print(dictoinary)
            morpheusComponent = dictoinary["morpheusComponent"]
            logger.info("Morpheus Component Detected: " + morpheusComponent)
            logger.info("Verifying Yaml: " + yaml_file)
            file_handler.verify_yaml_structure_helper(morpheusComponent, yaml_file)
            if morpheusComponent in ["init", "initial", "setup"]:
                logger.info("Initial Setup")
                initapp.initSetup(yaml_file)
                logger.info("Initital Setup Complete")

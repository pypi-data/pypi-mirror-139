import fnmatch
import glob
import time
from configparser import ConfigParser
import os
import yaml

from . import (
    cypher,
    file_handler,
    file_ImportScript,
    group,
    input,
    morph_log,
    role,
    tasks,
    users,
    whitelabel,
    wiki,
    getBearerToken
)


def contentPack_implementation(contentPackSelection):
    """
    # Contentpack Implementation

    ## Summary
    This function executes when the contentPackSelection finds the morpheusComponent as implementation.

    ### Inputs
    - contentPackSelection

    associated functions: user_select_contentPack
    """
    # Process config file
    configur = ConfigParser()
    configur.read(contentPackSelection + "/configs.ini")
    # contentPack = contentPackSelection
    # Set Variables
    baseURL = configur.get("DEFAULT", "BASE_URL")
    ADMIN_USERNAME = configur.get("DEFAULT", "ADMIN_USERNAME")
    ADMIN_PASSWORD = configur.get("DEFAULT", "ADMIN_PASSWORD")

    bearerToken = getBearerToken.bearerToken(baseURL, ADMIN_USERNAME, ADMIN_PASSWORD)
    os.environ["bearerToken"] = bearerToken
    # Logging
    logger = morph_log.get_logger("cp_impl")
    # Process content pack yaml files.
    files_inContentPack = sorted(glob.glob(contentPackSelection + "/*"))
    for file in files_inContentPack:
        if file.endswith(".yaml") and file != contentPackSelection + "/version.yaml" and file != contentPackSelection + "/initial.yaml":
            yaml_file = file
            logger.info("Current contentPack file processing: " + yaml_file)
            #with open(yaml_file, 'r') as stream:
            document = open(yaml_file, 'r')
            generator = yaml.safe_load_all(document)
            dictoinary = generator.__next__()
            #print(dictoinary)
            morpheusComponent = dictoinary["morpheusComponent"]
            logger.info("Morpheus Component Detected: " + morpheusComponent)
            logger.info("Verifying Yaml: " + yaml_file)
            file_handler.verify_yaml_structure_helper(morpheusComponent, yaml_file)
            if morpheusComponent in ["groups", "group"]:
                logger.info("Adding Groups")
                group.createGroups(yaml_file)
                logger.info("Completed: Groups")
            # if morpheusComponent == 'license':
            #    print('Adding License')
            #    license.add_license(baseURL, bearerToken, yaml_file)
            #    print('Completed: License')
            elif morpheusComponent in ["roles", "role"]:
                logger.info("Adding Roles")
                role.genericRoleCreate(yaml_file)
                logger.info("Completed: Roles")
            elif morpheusComponent in ["users", "user"]:
                logger.info("Adding Users")
                users.createUser(yaml_file)
                logger.info("Completed: Users")
            elif morpheusComponent in ["cyphers", "cypher"]:
                logger.info("Adding Cyphers")
                cypher.cypherCreate(baseURL, yaml_file)
                logger.info("Completed: Cyphers")
            elif morpheusComponent in ["inputs", "input"]:
                logger.info("Adding Input")
                input.inputCreate(yaml_file)
                logger.info("Completed: Inputs")
            elif morpheusComponent in ["whitelabel", "whitelabels"]:
                logger.info("Updating Whitelabel")
                whitelabel.updateWhiteLabel(yaml_file)
                logger.info("Completed: Update Whitelabel")
            elif morpheusComponent in ["templates", "template"]:
                logger.info("Adding Templates")
                file_ImportScript.create_Template_fromCP(
                    yaml_file, contentPackSelection
                )
                logger.info("Completed: Templates")
            elif morpheusComponent in [
                "shellScript",
                "shellScripts",
                "shellscript",
                "shellscripts",
            ]:
                logger.info("Adding Shell Tasks")
                tasks.shellScript(yaml_file, contentPackSelection)
                logger.info("Completed: Shell Tasks")
        # elif morpheusComponent in ['libraryTemplateTask']:
        #     logger.info('Adding Library Template Task')
        #     tasks.libraryTemplate(yaml_file)
        #     logger.info('Completed template')

    if file.endswith(".png"):
        if fnmatch.fnmatch(file, "*header_logo*"):
            logoHeader = file_handler.imageResizer(file)
            whitelabel.updateLogoHeader(logoHeader)
        if fnmatch.fnmatch(file, "*footer_logo*"):
            logoFooter = file_handler.imageResizer(file)
            whitelabel.updateLogoFooter(logoFooter)
        if fnmatch.fnmatch(file, "*login_logo*"):
            logoLogin = file_handler.imageResizer(file)
            whitelabel.updateLogoLogin(logoLogin)
    if file.endswith(".md"):
        logger.info("Adding Wiki Entries")
        wiki.addWikiEntry(file)
        logger.info("Completed: Wiki Entries")

#def contentPack_initSetup(contentPackSelection):
#     # Process config file
#    configur = ConfigParser()
#    configur.read(contentPackSelection + "/configs.ini")
#    # Logging
#    logger = morph_log.get_logger("cp_impl")
#    files_inContentPack = glob.glob(contentPackSelection + "/*")
#    for file in files_inContentPack:
#        if file.endswith(".yaml") and file == contentPackSelection + "/initial.yaml":
#            yaml_file = file
#            logger.info("Current contentPack file processing: " + yaml_file)
#            #with open(yaml_file, 'r') as stream:
#            document = open(yaml_file, 'r')
#            generator = yaml.safe_load_all(document)
#            dictoinary = generator.__next__()
#            #print(dictoinary)
#            morpheusComponent = dictoinary["morpheusComponent"]
#            logger.info("Morpheus Component Detected: " + morpheusComponent)
#            logger.info("Verifying Yaml: " + yaml_file)
#            file_handler.verify_yaml_structure_helper(morpheusComponent, yaml_file)
#            if morpheusComponent in ["init", "initial", "setup"]:
#                logger.info("Initial Setup")
#                initapp.initSetup(yaml_file)
#                logger.info("Initital Setup Complete")



def contentPack_file_processor(contentPackSelection):
    """
    # Content Pack file processor

    ## Summary
    This module - takes the contentpack selection and cycles through the version.yaml file to understand what type of contentpack it will be.

    Depending on the type: implementation, catalogItems, init, pov are currently supported - it will then process all the files and call the appropriate modules.

    ### Inputs
    - contentPackSelection

    associated functions: contentPack_implementation
    """
    # Logging
    logger = morph_log.get_logger("cp_fpro")

    print("Starting File Processor")
    time.sleep(1)
    print("I am a processor.... checking files")
    time.sleep(5)
    with open(contentPackSelection + "/version.yaml") as f:
        loaded_version_yaml = yaml.safe_load(f)
        logger.info("Loaded Version.yaml")
        type_of_contentPack = loaded_version_yaml["type"]
    if type_of_contentPack == "implementation":
        logger.info("Processing ContentPack Type Implementation")
        contentPack_implementation(contentPackSelection)
        logger.info("Completed: ContentPack")
    if type_of_contentPack == "setup":
        logger.info("Processing ContentPack Type Setup")
        contentPack_initSetup(contentPackSelection)
        logger.info("Completed Initial Setup")
        #contentPack_implementation(contentPackSelection)

        

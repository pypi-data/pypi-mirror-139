Morpheus Implementation Module

Purpose
The purpose of this script is to help remove friction as it relates to implementation, proof of value, and environment consitencey during configuration. 

ContentPacks 

Contentpacks are a collection of yamls files with pre-defined configurations in them.  They provide a portable method to quickly implement the Morpheus platform in multiple environments.  

What does a contentpack consist of?
It consists of some of the following itmes:

configs.ini - contains things like an admin username and password, baseURL (appliance URL)
groups.yaml (any name will do) - contains all the groups that would be created.
license.yaml (any name will do) - contains the license file for an environment. 
role.yaml (any name will do) - contains the roles that would be created.  This file also contains the features and groups that the role would need access to. 
version.yaml (this name is required) - contains the base information about the contentpack.


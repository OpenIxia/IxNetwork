*** Settings ***
Library  BuiltIn
Library  String
Library  Collections
Library  configIxNetwork.py

# Prerequisites:
#    - Add module path to PYTHONPATH
#
# Enter CLI:
#    python --variable paramFile:bgpParams.py --variable connectToApiServer:windows <script.robot>

*** Test Cases ***
Config IxNework

	Log To Console  Buidling configuration using: ${paramfile}
	Config  paramModuleName=${paramfile}  connectToApiServer=${connectToApiServer}
 
 

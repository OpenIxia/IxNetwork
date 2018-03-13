*** Variables ***
${apiServerIp}  192.168.70.3

*** Settings ***
Library  BuiltIn
Library  String
Library  Collections
${mainObj}=  Library  /home/hgee/Dropbox/MyIxiaWork/OpenIxiaGit/IxNetwork/RestApi/Python/Modules/IxNetRestApi.py  apiServerIp=${apiServerIp}  serverIpPort=11009  serverOs=windows
Library  /home/hgee/Dropbox/MyIxiaWork/OpenIxiaGit/IxNetwork/RestApi/Python/Modules/IxNetRestApiFileMgmt.py  ${mainObj}


# Enter CLI:
#    python --variable paramFile:bgpParams.py --variable connectToApiServer:windows <script.robot>

***Test cases***
Connect to API server

	Log To Console  Load JSON config file
	JsonReadConfig  bgpSimplified.json  
	#Set Suite Variable  ${mainObj}




#*** Test Cases ***
#Load Config File
#
#	Log To Console  Loading config file: ${configfile}
#	Config  paramModuleName=${paramfile}  connectToApiServer=${connectToApiServer}
	
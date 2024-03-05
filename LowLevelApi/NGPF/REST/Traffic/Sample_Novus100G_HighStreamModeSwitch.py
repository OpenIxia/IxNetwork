###############################################################################


################################################################################
#                                                                              #
#    Copyright 1997 - 2020 by IXIA  Keysight                                   #
#    All Rights Reserved.                                                      #
#                                                                              #
################################################################################


################################################################################
#                                                                              #
#                                LEGAL  NOTICE:                                #
#                                ==============                                #
# The following code and documentation (hereinafter "the script") is an        #
# example script for demonstration purposes only.                              #
# The script is not a standard commercial product offered by Ixia and have     #
# been developed and is being provided for use only as indicated herein. The   #
# script [and all modifications, enhancements and updates thereto (whether     #
# made by Ixia and/or by the user and/or by a third party)] shall at all times #
# remain the property of Ixia.                                                 #
#                                                                              #
# Ixia does not warrant (i) that the functions contained in the script will    #
# meet the user's requirements or (ii) that the script will be without         #
# omissions or error-free.                                                     #
# THE SCRIPT IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, AND IXIA        #
# DISCLAIMS ALL WARRANTIES, EXPRESS, IMPLIED, STATUTORY OR OTHERWISE,          #
# INCLUDING BUT NOT LIMITED TO ANY WARRANTY OF MERCHANTABILITY AND FITNESS FOR #
# A PARTICULAR PURPOSE OR OF NON-INFRINGEMENT.                                 #
# THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE SCRIPT  IS WITH THE #
# USER.                                                                        #
# IN NO EVENT SHALL IXIA BE LIABLE FOR ANY DAMAGES RESULTING FROM OR ARISING   #
# OUT OF THE USE OF, OR THE INABILITY TO USE THE SCRIPT OR ANY PART THEREOF,   #
# INCLUDING BUT NOT LIMITED TO ANY LOST PROFITS, LOST BUSINESS, LOST OR        #
# DAMAGED DATA OR SOFTWARE OR ANY INDIRECT, INCIDENTAL, PUNITIVE OR            #
# CONSEQUENTIAL DAMAGES, EVEN IF IXIA HAS BEEN ADVISED OF THE POSSIBILITY OF   #
# SUCH DAMAGES IN ADVANCE.                                                     #
# Ixia will not be required to provide any software maintenance or support     #
# services of any kind (e.g., any error corrections) in connection with the    #
# script or any part thereof. The user acknowledges that although Ixia may     #
# from time to time and in its sole discretion provide maintenance or support  #
# services for the script, any such services are subject to the warranty and   #
# damages limitations set forth herein and will not obligate Ixia to provide   #
# any additional maintenance or support services.                              #
#                                                                              #
################################################################################

################################################################################
#                                                                              #
# Description:                                                                 #
#    This sample assign one Novus 100G normal port to virtural port,           # 
#    Then it switches the mode to high stream mode of same speed               #
#                                                                              #
################################################################################

if 'py' not in dir():                       # define stuff if we don't run from harness
    class TestFailedError(Exception): pass
    class Py: pass
    py = Py()
    py.ixTclServer  =  "10.36.77.54"
    py.ixRestPort    =  '11010'
# END HARNESS VARS ************************************************************

import requests
import json

node =  'http://'+  py.ixTclServer+':'+ str(py.ixRestPort)

# Adding a Virtual Port to IxNetwork API Server
headers = {
    'Content-type': 'application/json'
}
body = {
	'name':'Port-1'
}
response = requests.request('POST', node+'/api/v1/sessions/1/ixnetwork/vport', headers=headers, json=body, verify=False)

# Assigning a Real Novus 100G normal mode port
body = {
	'arg1': [
		'10.36.77.102;12;1' # Chassis;Card;Resource Group
	],
	'arg2': [
		'/api/v1/sessions/1/ixnetwork/vport/1'
	],
	'arg3': True
}
response = requests.request('POST', node+'/api/v1/sessions/1/ixnetwork/operations/assignports', headers=headers, json=body, verify=False)

# Avaliable speed mode for Novus100G Fanout Card

speedModes =["novusHundredGigNonFanOut",
"novusFourByTwentyFiveGigNonFanOut",
"novusTwoByFiftyGigNonFanOut",
"novusOneByFortyGigNonFanOut",
"novusFourByTenGigNonFanOut",
"novusHundredGigNonFanOutHighStream",
"novusFourByTwentyFiveGigNonFanOutHighStream",
"novusTwoByFiftyGigNonFanOutHighStream",
"novusOneByFortyGigNonFanOutHighStream",
"novusFourByTenGigNonFanOutHighStream"]


# Changing the mode of the same port to 100G high stream Mode

body = {
	'arg1': [
		'10.36.77.102;12;1'# Chassis;Card;Resource Group
	],
	'arg2': [
		speedModes[5]
	],
	'arg3': True
}

  
response = requests.request('POST', node+'/api/v1/sessions/1/ixnetwork/operations/switchmodelocations', headers=headers, json=body, verify=False)
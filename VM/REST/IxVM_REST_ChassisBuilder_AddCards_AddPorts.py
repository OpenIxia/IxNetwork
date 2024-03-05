#!/usr/bin/python

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
#    - Connects to a chassis                                                   #
#    - Removes all elements from the topology                                  #
#    - Adds a couple of cards                                                  #
#    - Adds a couple of ports to the cards                                     #
#                                                                              #
################################################################################

# HARNESS VARS ****************************************************************
# NOTE: Change these variables according to your setup.
if 'py' not in dir():                       # define stuff if we don't run from harness
    class TestFailedError(Exception): pass
    class Py: pass
    py = Py()
    py.ports           = [('10.10.10.10', '1', '1'), ('10.10.10.10', '2', '1')]
    py.ixTclServer  =  "11.11.11.11"
    py.ixRestPort   =  "12345"
    py.IP_list = ["1.1.1.1", "1.1.1.2"]
# END HARNESS VARS ************************************************************

import sys
import zipfile
# Needed for REST API
import time
import requests
import json

# Import REST Library library
from FW_RestApiUtils import *
from VM_RestApiUtils import RestCB
from utils import sm

#######################################################
## Script steps start
#######################################################

print ("Sleep 15 sec to finish initialization for IxNet")
time.sleep(15)

ixnetUrl = "http://" + py.ixTclServer + ":" + py.ixRestPort + "/api/v1/"
urlHeadersJson = {'content-type': 'application/json'}

port_tuple = py.ports[0]
chassis = port_tuple[0]
print ("Chassis IP is:", chassis)

# Get the desired session based on Process ID
print ("All Sessions connected:")
allSessions = getIxNetSessions(ixnetUrl)
allSessionsList = allSessions

for sess in allSessionsList:
    print ("id: " + str(sess['id']) + "\t PID: " + str(sess['mwSdmProcessId']) + "\t State:" + str(sess['state']))
    sessionId = sess['id']

sessionUrl = getIxNetSessionUrl(ixnetUrl, sessionId)

print ("")
print ("#######################################################")
print ("")

ixNetExec(sessionUrl,"newConfig")

print ("")
print (" * Connecting to chassis... " + str(chassis))
print ("")

arg1 = {"arg1": chassis}
a = ixNetExec(sessionUrl, "connectToChassis", arg1)

vChassisUrl = sessionUrl + "/availableHardware/virtualChassis"

print ("")
print (" * IP_list :" + str(py.IP_list))
print ("")

print ("")
RestCB.clear_topology(sessionUrl)

print ("")
card1 = RestCB.addIxvmCard(sessionUrl , py.IP_list[0] , 1 , "300")

print ("")
port1 = RestCB.addIxvmPort(card1, "eth1")
print ("")
port2 = RestCB.addIxvmPort(card1, "eth2", 10)
print ("")
port3 = RestCB.addIxvmPort(card1, "eth5", "" , True, 3000)
print ("")
port4 = RestCB.addIxvmPort(card1, "eth4", "8" , True, 5000)
print ("")

print ("")
card2 = RestCB.addIxvmCard(sessionUrl , py.IP_list[1] , 4 , "400")
print ("")

port1 = RestCB.addIxvmPort(card2, "eth1")
print ("")
port2 = RestCB.addIxvmPort(card2, "eth2", 5)
print ("")
port3 = RestCB.addIxvmPort(card2, "eth3", "" , True, 2000)
print ("")
port4 = RestCB.addIxvmPort(card2, "eth7", "7" , True, 4000)
print ("")


topo_result = RestCB.getChassisTopology(sessionUrl)

expected_topology = [
['Port',
  [('Card ID', '=', '1', None),
   ('Card IP', '=', py.IP_list[0], None),
   ('KeepAlive', '=', '300', None),
   ('Port ID', '=', '1', None),
   ('Interface Name', '=', 'eth1', None),
   ('Promisc', '=', '0', None),
   ('MTU', '=', '1500', None),
   ('Speed', '=', '1000', None)]],
['Port',
  [('Card ID', '=', '1', None),
   ('Card IP', '=', py.IP_list[0], None),
   ('KeepAlive', '=', '300', None),
   ('Port ID', '=', '2', None),
   ('Interface Name', '=', 'eth5', None),
   ('Promisc', '=', '1', None),
   ('MTU', '=', '3000', None),
   ('Speed', '=', '1000', None)]],
['Port',
  [('Card ID', '=', '1', None),
   ('Card IP', '=', py.IP_list[0], None),
   ('KeepAlive', '=', '300', None),
   ('Port ID', '=', '8', None),
   ('Interface Name', '=', 'eth4', None),
   ('Promisc', '=', '1', None),
   ('MTU', '=', '5000', None),
   ('Speed', '=', '1000', None)]],
   ['Port',
[('Card ID', '=', '1', None),
   ('Card IP', '=', py.IP_list[0], None),
   ('KeepAlive', '=', '300', None),
   ('Port ID', '=', '10', None),
   ('Interface Name', '=', 'eth2', None),
   ('Promisc', '=', '0', None),
   ('MTU', '=', '1500', None),
   ('Speed', '=', '1000', None)]],

['Port',
  [('Card ID', '=', '4', None),
   ('Card IP', '=', py.IP_list[1], None),
   ('KeepAlive', '=', '400', None),
   ('Port ID', '=', '1', None),
   ('Interface Name', '=', 'eth1', None),
   ('Promisc', '=', '0', None),
   ('MTU', '=', '1500', None),
   ('Speed', '=', '1000', None)]],
['Port',
  [('Card ID', '=', '4', None),
   ('Card IP', '=', py.IP_list[1], None),
   ('KeepAlive', '=', '400', None),
   ('Port ID', '=', '2', None),
   ('Interface Name', '=', 'eth3', None),
   ('Promisc', '=', '1', None),
   ('MTU', '=', '2000', None),
   ('Speed', '=', '1000', None)]],
   ['Port',
[('Card ID', '=', '4', None),
   ('Card IP', '=', py.IP_list[1], None),
   ('KeepAlive', '=', '400', None),
   ('Port ID', '=', '5', None),
   ('Interface Name', '=', 'eth2', None),
   ('Promisc', '=', '0', None),
   ('MTU', '=', '1500', None),
   ('Speed', '=', '1000', None)]],
['Port',
  [('Card ID', '=', '4', None),
   ('Card IP', '=', py.IP_list[1], None),
   ('KeepAlive', '=', '400', None),
   ('Port ID', '=', '7', None),
   ('Interface Name', '=', 'eth7', None),
   ('Promisc', '=', '1', None),
   ('MTU', '=', '4000', None),
   ('Speed', '=', '1000', None)]]
]

if sm.checkStats(topo_result, expected_topology,True):
    raise TestFailedError("Topologies do not match")

print ("")
print (" - Clean UP")
print ("")

print ("#######################################################")
print ("# Test PASS ")
print ("#######################################################")

print ("DONE")

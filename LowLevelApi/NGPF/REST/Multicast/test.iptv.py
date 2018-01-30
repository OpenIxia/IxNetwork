#!/usr/local/bin/python2.7
################################################################################
# Version 1.0    $Revision: 1 $
# $Author: Indranil Acharya $
#
#    All Rights Reserved.
#
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
#    This sample script														   #
#    - Loads config				                                               #
#    - Starts IGMP Router                                                      #
#    - Starts IGMP Host                                                        #
#    - Confirms all sessions are up                                            #
#    - Starts traffic                                                          #
#    - Confirm expected Traffic Item statistics                                #
#                                                                              #
################################################################################

# HARNESS VARS ****************************************************************
if 'py' not in dir():                       # define stuff if we don't run from harness
    class TestFailedError(Exception): pass
    class Py: pass
    py = Py()
    py.ports        = [('10.200.113.7', '8', '7'), ('10.200.113.7', '8', '8')]
    py.ixTclServer  =  "10.200.225.53"
    py.ixRestPort    =  '11020'
    py.ixTclPort     =  8020
# END HARNESS VARS ************************************************************
#------------------------------------------------------------------------------
import sys
import zipfile
import time
import json
################################################################################
# Import REST Library library
################################################################################
#from FW_RestApiUtils import *
import restAPI as rest

#######################################################
## Script steps start
#######################################################

print "Sleep 5 sec to finish initialization for IxNet"
time.sleep(5)

#######################################################
## Preparing IxNet URL
#######################################################

ixnetUrl = "http://"+py.ixTclServer+":"+str(py.ixRestPort)+"/api/v1/"
urlHeadersJson = {'content-type': 'application/json'}
urlHeadersData = {'content-type': 'application/octet-stream'}

sessionUrl=ixnetUrl+'sessions/1/ixnetwork/' #Assuming the session number is 1,change accordingly
print "#######################################################"
print ""

#######################################################
# Cleaning up IxNetwork
#######################################################

print "Doing new Config   "
rest.ixNetExec(sessionUrl, "newConfig")

#######################################################
# Loading IxNetwork Configuration
#######################################################
configName='config.iptv.ixncfg'
print "Loading the configuration file ...",configName
rest.ixNetLoadConfig(sessionUrl, configName)
time.sleep(5)
#######################################################
# Assigning Physical Ports
#######################################################
rest.ixNetAssignPorts(sessionUrl, py.ports)
time.sleep(10)

#######################################################
# Starts IGMP Router 
#######################################################

print "Starting IGMP Router first"
igmp_router_url=sessionUrl+'topology'
data = {"arg1":["/api/v1/sessions/1/ixnetwork/topology/2"]}
rest.ixNetExec(igmp_router_url,"start",data) 
time.sleep(10)

#######################################################
# Starts IGMP Host
#######################################################
print "Starting IGMP Host Second"
igmp_host_url=sessionUrl+'topology/deviceGroup/ethernet/ipv4/igmpHost'
data = {"arg1":["/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1/igmpHost/1"]}
rest.ixNetExec(igmp_host_url,"start",data) 
time.sleep(30)

#######################################################
# Retrive Stats And Verify
#######################################################
data = rest.ixNetGetStats(sessionUrl, "Protocols Summary",["Protocol Type","Sessions Up","Sessions Total","Sessions Down"])
print "Checking for all the sessions to be up"
if rest.verifyStatsForUP(sessionUrl):
    print "PASS-All Sessions are UP!!"
	
################################################################################
# Generate, apply and start traffic
################################################################################
print "Starting the Traffic"
rest.generateApplyStartTraffic(sessionUrl,refreshBeforeApply=True)
time.sleep(15)

#######################################################
# Retrive Stats And Verify
#######################################################
data = rest.ixNetGetStats(sessionUrl, "Traffic Item Statistics",["Traffic Item","Tx Frames","Rx Frames","Frames Delta","Loss %"])
if data["Tx Frames"]<"1":raise TestFailedError ("FAIL:Stats are not Correct,expected Tx Frames to be > 0")
print "PASS- Test case Passed !!"
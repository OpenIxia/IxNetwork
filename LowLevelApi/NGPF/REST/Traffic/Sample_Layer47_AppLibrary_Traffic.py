
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
# script [and all modifications enhancements and updates thereto (whether      #
# made by Ixia and/or by the user and/or by a third party)] shall at all times #
# remain the property of Ixia.                                                 #
#                                                                              #
# Ixia does not warrant (i) that the functions contained in the script will    #
# meet the users requirements or (ii) that the script will be without          #
# omissions or errorfree.                                                      #
# THE SCRIPT IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND AND IXIA         #
# DISCLAIMS ALL WARRANTIES EXPRESS IMPLIED STATUTORY OR OTHERWISE              #
# INCLUDING BUT NOT LIMITED TO ANY WARRANTY OF MERCHANTABILITY AND FITNESS FOR #
# A PARTICULAR PURPOSE OR OF NONINFRINGEMENT.                                  #
# THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE SCRIPT  IS WITH THE #
# USER.                                                                        #
# IN NO EVENT SHALL IXIA BE LIABLE FOR ANY DAMAGES RESULTING FROM OR ARISING   #
# OUT OF THE USE OF OR THE INABILITY TO USE THE SCRIPT OR ANY PART THEREOF     #
# INCLUDING BUT NOT LIMITED TO ANY LOST PROFITS LOST BUSINESS LOST OR          #
# DAMAGED DATA OR SOFTWARE OR ANY INDIRECT INCIDENTAL PUNITIVE OR              #
# CONSEQUENTIAL DAMAGES EVEN IF IXIA HAS BEEN ADVISED OF THE POSSIBILITY OF    #
# SUCH DAMAGES IN ADVANCE.                                                     #
# Ixia will not be required to provide any software maintenance or support     #
# services of any kind (e.g. any error corrections) in connection with the     #
# script or any part thereof. The user acknowledges that although Ixia may     #
# from time to time and in its sole discretion provide maintenance or support  #
# services for the script any such services are subject to the warranty and    #
# damages limitations  forth herein and will not obligate Ixia to provide      #
# any additional maintenance or support services.                              #
#                                                                              #
################################################################################

#################################################################################
#                                                                              	#
# Description:                                                                 	#
#	The script below represents an end to end workflow for AppLibrary Traffic. 	#
#	Steps:																	   	#			
#	1. Chassis connection and TCL server connection							   	#	
#	2. Scenario configuration at layer 2-3									   	#	
#	3. Creation of Applibrary traffic										   	#	
#	4. Per connection parameters configuration 								   	#	
#	5. Traffic apply and start 												   	#
#	6. Statistics operations: drill down in a loop							   	#	
#	7. Test criteria evaluation													#
#	8. Stop traffic															   	#
#													  	 						#		
#################################################################################

if 'py' not in dir():                       # define stuff if we don't run from harness
    class TestFailedError(Exception): pass
    class Py: pass
    py = Py()
    py.ports        = [('10.200.113.7', '8', '7'), ('10.200.113.7', '8', '8')]
    py.ixTclServer  =  "10.200.225.53"
    py.ixRestPort    =  '11020'
    py.ixTclPort     =  8020
# END HARNESS VARS ************************************************************

################################################################################
# Import the IxNet library
################################################################################
import sys,time,copy,pprint,os,ast
from restAPIV import *

################################################################################
# Connect to IxNet client
################################################################################

ixNet = IxNet(py.ixTclServer, int(py.ixTclPort)+3000)
ixNet.connect()
root = ixNet.getRoot()

################################################################################
# Cleaning up IxNetwork
################################################################################

print "Cleaning up IxNetwork..."
ixNet.execute('newConfig')
#------------------------------------
# Adding 2 ports
#------------------------------------

print "Adding offline ports to the configuration"
vport1 = ixNet.add(root, 'vport')
ixNet.commit()
vport1ID = ixNet.remapIds (vport1)[0]

vport2 = ixNet.add(root, 'vport')
ixNet.commit()
vport2ID = ixNet.remapIds(vport2)[0]
ixNet.commit()

#------------------------------------
# Mapping ports to real ports
#------------------------------------
################################################################################
# Assign ports 
################################################################################
vports = ixNet.getList(ixNet.getRoot(), 'vport')
print "Assigning ports to " + str(vports) + " ..."
assignPorts=ixNet.execute('assignPorts',py.ports,[],vports,True )

#------------------------------------
# Adding 1st topology, Device Group, Ethernet, IPv4
#------------------------------------

print "Building first topology and building its stack"
addedTopology_1 = ixNet.add (root, 'topology')
ixNet.commit()
addedTopology_1ID = ixNet.remapIds(addedTopology_1)[0]

addedDG = ixNet.add(addedTopology_1ID, 'deviceGroup')
ixNet.commit()
addedDGID = ixNet.remapIds(addedDG)[0]

addedEthernet = ixNet.add (addedDGID, 'ethernet')
ixNet.commit()
addedEthernetID = ixNet.remapIds(addedEthernet)[0]

addedIPv4 = ixNet.add(addedEthernetID, 'ipv4')
ixNet.commit()
addedIPv4ID = ixNet.remapIds(addedIPv4)[0]

#------------------------------------
# Configure 1st topology
#------------------------------------
print "************1",addedIPv4
addressMV = ixNet.getAttribute(addedIPv4[0], '-address')
ixNet.setMultiAttribute(addressMV + '/counter','-step','0.0.0.1','-start','201.1.0.1','-direction' ,'increment',)
ixNet.commit()

prefixMV = ixNet.getAttribute(addedIPv4[0], '-prefix')
ixNet.setMultiAttribute(prefixMV + '/singleValue', '-value','16')
ixNet.commit()

gatewayMV =ixNet.getAttribute(addedIPv4[0],'-gatewayIp')
ixNet.setMultiAttribute(gatewayMV + '/counter','-step','0.0.0.1','-start','201.1.1.1','-direction' ,'increment',)
ixNet.commit()

#------------------------------------
# Adding 2st topology, Device Group, Ethernet, IPv4
#------------------------------------

print "Building first topology and building its stack"
addedTopology_2 = ixNet.add (root, 'topology')
ixNet.commit()
addedTopology_2ID = ixNet.remapIds(addedTopology_2)[0]

addedDG = ixNet.add(addedTopology_2ID, 'deviceGroup')
ixNet.commit()
addedDGID = ixNet.remapIds(addedDG)[0]

addedEthernet = ixNet.add (addedDGID, 'ethernet')
ixNet.commit()
addedEthernetID = ixNet.remapIds(addedEthernet)[0]

addedIPv4 = ixNet.add(addedEthernetID, 'ipv4')
ixNet.commit()
addedIPv4ID = ixNet.remapIds(addedIPv4)[0]
#------------------------------------
# Configure 2st topology
#------------------------------------
addressMV = ixNet.getAttribute(addedIPv4[0], '-address')
ixNet.setMultiAttribute(addressMV + '/counter','-step','0.0.0.1','-start','201.1.1.1','-direction' ,'increment',)
ixNet.commit()

prefixMV = ixNet.getAttribute(addedIPv4[0], '-prefix')
ixNet.setMultiAttribute(prefixMV +'/singleValue','-value','16')
ixNet.commit()

gatewayMV =ixNet.getAttribute(addedIPv4[0],'-gatewayIp')
ixNet.setMultiAttribute(gatewayMV + '/counter','-step','0.0.0.1','-start','201.1.0.1','-direction' ,'increment',)
ixNet.commit()

topo1 = ixNet.getList(root, 'topology')[0]
topo2 = ixNet.getList(root, 'topology')[1]

print "Add ports to topologies"
vPorts = ixNet.getList(root, 'vport')
vport1 = vPorts[0]
vport2 = vPorts[1]
ixNet.setAttribute(topo1, '-vports', [vport1])
ixNet.setAttribute(topo2, '-vports', [vport2])
ixNet.commit()

#-------------------------------------------
# Create traffic item and add flows
#-------------------------------------------
print "Adding an AppLibrary traffic item and also adding flows"
data = {'trafficType':'ipv4ApplicationTraffic','trafficItemType':'applicationLibrary'}
addedTI = ixNet.add(root + '/traffic','trafficItem',data)
print '********* 2',addedTI
ixNet.commit()
addedTIID = ixNet.remapIds(addedTI)[0]

addedProfile = ixNet.add(addedTIID, 'appLibProfile')
ixNet.commit()
addedProfileID = ixNet.remapIds(addedProfile)[0]

ixNet.execute('addAppLibraryFlow', addedProfileID , ['Bandwidth_HTTP'] )
ixNet.execute('addAppLibraryFlow', addedProfileID , ['Echo_UDP'] )
ixNet.execute('addAppLibraryFlow', addedProfileID , ['Yahoo_Mail'] )
ixNet.execute('addAppLibraryFlow', addedProfileID , ['Bandwidth_IMAPv4'] )
ixNet.commit()

#-----------------------------------------------------
# Link the traffic item to the new topology set
#-----------------------------------------------------

print "Adding endpoints to the AppLibrary Traffic Item"
addedEndpointSet = ixNet.add(addedTIID, 'endpointSet')
ixNet.commit()
addedEndpointSetID =ixNet.remapIds(addedEndpointSet)[0]
ixNet.setMultiAttribute(addedEndpointSetID, '-sources' ,[topo1],'-destinations',[topo2])
ixNet.commit()

#----------------------------------------------------------
# Edit traffic item parameters for the added traffic item
#----------------------------------------------------------
print "\nConfiguring AppLibrary Traffic Item Basic Settings"
ixNet.setMultiAttribute(addedProfileID ,'-objectiveValue','133','-objectiveType','throughputMbps','-enablePerIPStats','True','-objctiveDistribution','applyFullObjectiveToEachPort')
ixNet.commit()
#----------------------------------------------------------
# Setting flow percentages
#----------------------------------------------------------
ixNet.setAttribute(root + '/traffic/trafficItem/1/appLibProfile/1/appLibFlow:"Bandwidth_IMAPv4"','-percentage','10')
ixNet.setAttribute(root + '/traffic/trafficItem/1/appLibProfile/1/appLibFlow:"Echo_UDP"', '-percentage','80')
ixNet.setAttribute(root + '/traffic/trafficItem/1/appLibProfile/1/appLibFlow:"Bandwidth_HTTP"', '-percentage','10')
ixNet.commit()
#----------------------------------------------------------
# Configuring connection parameters
#----------------------------------------------------------
print "Configuring connection parameters"
ixNet.setAttribute(root + '/traffic/trafficItem/1/appLibProfile/1/appLibFlow:"Bandwidth_HTTP"/connection/1/parameter:"serverPort"/number','-value','8080')
ixNet.setAttribute(root + '/traffic/trafficItem/1/appLibProfile/1/appLibFlow:"Echo_UDP"/connection/1/parameter:"enableTOS"/bool', '-value','True')
ixNet.setAttribute(root + '/traffic/trafficItem/1/appLibProfile/1/appLibFlow:"Echo_UDP"/connection/1/parameter:"tosValue"/hex', '-value','0x1')
ixNet.commit()
#----------------------------------------------------------
# Starting up protocols
#----------------------------------------------------------
print "\nStarting all protocols and waiting for all ranges to be up"
ixNet.execute('startAllProtocols')
time.sleep(5)
print "Protocols started"
#----------------------------------------------------------
# Apply and start traffic
#----------------------------------------------------------
print "\nApplying and starting AppLibrary Traffic"
ixNet.execute('applystatefultraffic',root + '/traffic')
time.sleep(15)
ixNet.execute('startstatefultraffic', root + '/traffic')
time.sleep(5)
print "AppLibrary traffic started"
#----------------------------------------------------------
# Clearing Statistics for AppLibrary Traffic
#----------------------------------------------------------
print "\nWaiting 10 seconds before clearing AppLibrary statistics ..."
time.sleep(10)
ixNet.execute('clearAppLibraryStats')
print "Statistics have been cleared"
#----------------------------------------------------------
# Stop traffic
#----------------------------------------------------------
time.sleep(20)
print "Stopping AppLibrary traffic"
ixNet.execute('stopstatefultraffic',root + '/traffic')
time.sleep(10)
################################################################################
# Checking Stats to see if traffic was sent OK
################################################################################
print "Checking Stats to check if traffic was sent OK"
print "Getting the object for view Traffic Item Statistics"
viewName = "Application Flow Initiator TCP Statistics"
views = ixNet.getList(root+'/statistics', 'view')
for view in views:
    if viewName == ixNet.getAttribute(view,"caption"):
         viewObj = view
         break
print "Getting the SYNs values"
txFrames = ixNet.execute('getColumnValues', viewObj, 'SYNs Sent')
rxFrames = ixNet.execute('getColumnValues', viewObj, 'SYN/SYN-ACKs Received')
for txStat, rxStat in zip(txFrames['result'], rxFrames['result']):
    print "SYNs Sent (%s) ~= SYN/SYN-ACKs Received (%s)" % (txStat, rxStat)
#----------------------------------------------------------
# Test END
#----------------------------------------------------------
print "##################"
print "Test run is PASSED"
print "##################"
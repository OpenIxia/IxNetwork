################################################################################
# Version 1.0    $Revision: 1 $                                                #
#                                                                              #
#    Copyright  1997  2015 by IXIA                                             #
#    All Rights Reserved.                                                      #
#                                                                              #
#    Revision Log:                                                             #
#    02/02/2015  Andrei Zamisnicu - created sample                             #
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

################################################################################
# Utils																		   #
################################################################################

print "\n\n\n#######################################"
print "Running AppLibrary Sample Workflow Script"
print "#######################################\n\n\n"


#---------------------------------------------------------
# Setting global variables for the sample run
#---------------------------------------------------------

chassisIP = "10.205.23.34" 									;# chassis IP
applicationVersion = '7.50' 								;# IxN version
tclPort = '8449' 											;# the TCL port on which the IxTcl Server is listening
port1 = ['2','3'] 											;# where values are: {<card> <port>}
port2 = ['2','4'] 											;# where values are: {<card> <port>}
PFCriteria_Higher = ['Initiator Tx Rate (Mbps)', '40'] 		;# statistic from Application Traffic item Statistics view that has to be higher than given value
PFCriteria_Lower = ['Flows Failed', '40'] 					;# statistic from Application Traffic item Statistics view that has to be lower than given value



#---------------------------------------------------------
# Connecting to TCL Server and loading required packages
#---------------------------------------------------------

from IxNetwork import IxNet


ixNet = IxNet()
import time

print "Connecting to TCL Server..."
ixNet.connect('127.0.0.1','-version', applicationVersion ,'-port','8449' )
ixNet.execute('newConfig')
root = ixNet.getRoot()
availableHW = ixNet.getRoot() + 'availableHardware'


#------------------------------------
# Adding chassis
#------------------------------------

print "Adding chassis to the configuration"
chassis1 = ixNet.add(availableHW ,'chassis')
chassis1ID = ixNet.remapIds(chassis1)[0]

ixNet.setAttribute(chassis1ID,'-hostname',chassisIP)
ixNet.commit()

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

print "Mapping offline ports to actual ports in chassis\n"
ixNet.setAttribute(vport1 ,'-connectedTo','/availableHardware/chassis:"' + chassisIP + '"/card:' + port1[0] + '/port:' + port1[1])
ixNet.setAttribute(vport2 ,'-connectedTo','/availableHardware/chassis:"' + chassisIP + '"/card:' + port2[0] + '/port:' + port2[1])
ixNet.commit()


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

ixNet.setAttribute(addedTopology_1, '-vports', root + 'vport:1')

addedEthernet = ixNet.add (addedDGID, 'ethernet')
ixNet.commit()
addedEthernetID = ixNet.remapIds(addedEthernet)[0]

addedIPv4 = ixNet.add(addedEthernetID, 'ipv4')
ixNet.commit()
addedIPv4ID = ixNet.remapIds(addedIPv4)[0]


#------------------------------------
# Configure 1st topology
#------------------------------------

addressMV = ixNet.getAttribute(addedIPv4, '-address')
ixNet.setMultiAttribute(addressMV + '/counter','-step','0.0.0.1','-start','201.1.0.1','-direction' ,'increment',)
ixNet.commit()

prefixMV = ixNet.getAttribute(addedIPv4, '-prefix')
ixNet.setMultiAttribute(prefixMV + '/singleValue', '-value','16')
ixNet.commit()

gatewayMV =ixNet.getAttribute(addedIPv4,'-gatewayIp')
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

ixNet.setAttribute(addedTopology_2, '-vports', root + 'vport:2')

addedEthernet = ixNet.add (addedDGID, 'ethernet')
ixNet.commit()
addedEthernetID = ixNet.remapIds(addedEthernet)[0]

addedIPv4 = ixNet.add(addedEthernetID, 'ipv4')
ixNet.commit()
addedIPv4ID = ixNet.remapIds(addedIPv4)[0]


#------------------------------------
# Configure 2st topology
#------------------------------------


addressMV = ixNet.getAttribute(addedIPv4, '-address')
ixNet.setMultiAttribute(addressMV + '/counter','-step','0.0.0.1','-start','201.1.1.1','-direction' ,'increment',)
ixNet.commit()

prefixMV = ixNet.getAttribute(addedIPv4, '-prefix')
ixNet.setMultiAttribute(prefixMV +'/singleValue','-value','16')
ixNet.commit()

gatewayMV =ixNet.getAttribute(addedIPv4,'-gatewayIp')
ixNet.setMultiAttribute(gatewayMV + '/counter','-step','0.0.0.1','-start','201.1.0.1','-direction' ,'increment',)
ixNet.commit()


#-------------------------------------------
# Create traffic item and add flows
#-------------------------------------------
print "Adding an AppLibrary traffic item and also adding flows"

addedTI = ixNet.add(root + '/traffic','trafficItem','-trafficType','ipv4ApplicationTraffic','-trafficItemType','applicationLibrary')
ixNet.commit()
addedTIID = ixNet.remapIds(addedTI)[0]

addedProfile = ixNet.add(addedTIID, 'appLibProfile')
ixNet.commit()
addedProfileID = ixNet.remapIds(addedProfile)[0]

ixNet.execute('addAppLibraryFlow', addedProfileID , 'Bandwidth_HTTP Echo_UDP Yahoo_Mail Bandwidth_IMAPv4' )
ixNet.commit()
ixNet.execute('removeAppLibraryFlow',addedProfileID,'Yahoo_Mail')
ixNet.commit()

#-----------------------------------------------------
# Link the traffic item to the new topology set
#-----------------------------------------------------

print "Adding endpoints to the AppLibrary Traffic Item"

addedEndpointSet = ixNet.add(addedTIID, 'endpointSet')
ixNet.commit()
addedEndpointSetID =ixNet.remapIds(addedEndpointSet)[0]

ixNet.setMultiAttribute(addedEndpointSetID, '-sources' ,'/topology:1','-destinations','/topology:2')
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

ixNet.setAttribute(root + '/traffic/trafficItem:1/appLibProfile:1/appLibFlow:"Bandwidth_IMAPv4"','-percentage','10')
ixNet.setAttribute(root + '/traffic/trafficItem:1/appLibProfile:1/appLibFlow:"Echo_UDP"', '-percentage','80')
ixNet.setAttribute(root + '/traffic/trafficItem:1/appLibProfile:1/appLibFlow:"Bandwidth_HTTP"', '-percentage','10')
ixNet.commit()

#----------------------------------------------------------
# Configuring connection parameters
#----------------------------------------------------------

print "Configuring connection parameters"


ixNet.setAttribute(root + '/traffic/trafficItem:1/appLibProfile:1/appLibFlow:"Bandwidth_HTTP"/connection:1/parameter:"serverPort"/number','-value','8080')
ixNet.setAttribute(root + '/traffic/trafficItem:1/appLibProfile:1/appLibFlow:"Echo_UDP"/connection:1/parameter:"enableTOS"/bool', '-value','True')
ixNet.setAttribute(root + '/traffic/trafficItem:1/appLibProfile:1/appLibFlow:"Echo_UDP"/connection:1/parameter:"tosValue"/hex', '-value','0x1')
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
ixNet.execute('applyApplicationTraffic',root + '/traffic')
time.sleep(15)
ixNet.execute('startApplicationTraffic', root + '/traffic')
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
# Drilling down per IP
#----------------------------------------------------------

time.sleep(10)
print "Drilling down to reveal per IP address flow activity"

viewsList = ixNet.getList(root + '/statistics','view')

target = viewsList[viewsList.index('::ixNet::OBJ-/statistics/view:"Application Traffic Item Statistics"')]

print "Configuring drill down per IP addresses"
ixNet.setAttribute(target + '/drillDown','-targetRowIndex','0')
ixNet.commit()
ixNet.setAttribute(target + '/drillDown','-targetDrillDownOption','Application Traffic:Per IPs')
ixNet.commit()
ixNet.setAttribute(target + '/drillDown','-targetRow','Traffic Item=Traffic Item')
ixNet.commit()

print"Launching the drill down per IP addresses view\n"
ixNet.execute('doDrillDown', target + '/drillDown')
time.sleep(3)

print "Refreshing statistics five times in a row"
viewsList = ixNet.getList(root + '/statistics','view')
target = viewsList[viewsList.index('::ixNet::OBJ-/statistics/view:"Application Traffic Drill Down"')]

i = 0
for i in range(5):
    ixNet.execute('refresh', target)
    time.sleep(5)
    print "Statistics refreshed..."


#----------------------------------------------------------
# Pass Fail Evaluation
#----------------------------------------------------------

# selecting the "Application Traffic Item Statistics view from all the views"
viewsList = ixNet.getList(root + '/statistics','view')
targetView = viewsList[viewsList.index('::ixNet::OBJ-/statistics/view:"Application Traffic Item Statistics"')]

# selecting the columns based on the configured criteria
targetColumnForHigh = ixNet.getAttribute(targetView + '/page','-columnCaptions').index(PFCriteria_Higher[0])
targetColumnForLow = ixNet.getAttribute(targetView + '/page','-columnCaptions').index(PFCriteria_Lower[0])

# measuring the selected statistic
measuredHigher =ixNet.getAttribute(targetView + '/page','-rowValues')[0][0][targetColumnForHigh]
measuredLower =ixNet.getAttribute(targetView + '/page','-rowValues')[0][0][targetColumnForLow]

# comparing with pass fail condition - second item in the PFCriteria list
if ( measuredHigher > PFCriteria_Higher[1] and measuredLower < PFCriteria_Lower[1]):
    testResult = 'Test run is PASSED'
else:
    testResult = 'Test run is FAILED: pass fail conditions -'+ PFCriteria_Higher[0]+ 'and' + PFCriteria_Lower[0] + '- configured in the start of the script are not met'
#----------------------------------------------------------
# Stop traffic
#----------------------------------------------------------

time.sleep(20)
print "Stopping AppLibrary traffic"
ixNet.execute('stopApplicationTraffic',root + '/traffic')

print testResult
#----------------------------------------------------------
# Test END
#----------------------------------------------------------

print "##################"
print "Test run is PASSED"
print "##################"


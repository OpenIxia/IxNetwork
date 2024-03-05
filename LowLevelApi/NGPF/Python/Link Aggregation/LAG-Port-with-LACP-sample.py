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
# omissions or error-free.                                                     #
# THE SCRIPT IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND AND IXIA         #
# DISCLAIMS ALL WARRANTIES EXPRESS IMPLIED STATUTORY OR OTHERWISE              #
# INCLUDING BUT NOT LIMITED TO ANY WARRANTY OF MERCHANTABILITY AND FITNESS FOR #
# A PARTICULAR PURPOSE OR OF NON-INFRINGEMENT.                                 #
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
# damages limitations set forth herein and will not obligate Ixia to provide   #
# any additional maintenance or support services.                              #
#                                                                              #
################################################################################

################################################################################
#                                                                              #
# Description:                                                                 #
#    This script intends to demonstrate how to use NGPF LAG API.               #
#	 Script uses four ports to demonstrate LAG properties	                   #
#                                                                              #
#    1. It will create 2 LACP topologies, each having an two port which are    #
#       LAG members. It will then modify the ActorSystemId and ActorKey	for    # 
#       both the LAG systems                                                   #
#    2. Start the LACP protocol                                                #
#    3. Retrieve protocol statistics and LACP per port statistics              #
#	 4. Disable Synchronization flag on port1 in RED-LAG                       # 
#	 5. Retrieve protocol statistics and LACP per port statistics              #
#	 6. Re-enable Synchronization flag on port1 in RED-LAG                     # 
#	 7. Retrieve protocol statistics and LACP per port statistics              #
#	 8. Perform StopPDU on port1 in RED-LAG                                    #
#	 9. Retrieve LACP global learned info              		                   #
#	 10. Perform StopPDU on port1 in RED-LAG                                   # 
#	 11. Retrieve LACP global learned info                                     #
#	 12. Stop All protocols                                                    # 
#                                                                              #
#                                                                              #
################################################################################
import os
import sys
import time

def assignPorts (ixNet, realPort1, realPort2, realPort3, realPort4) :
     chassis1 = realPort1[0]
     chassis2 = realPort2[0]
     card1    = realPort1[1]
     card2    = realPort2[1]
     port1    = realPort1[2]
     port2    = realPort2[2]
     chassis3 = realPort3[0]
     chassis4 = realPort4[0]
     card3    = realPort3[1]
     card4    = realPort4[1]
     port3    = realPort3[2]
     port4    = realPort4[2]
     
     root = ixNet.getRoot()
     vport1 = ixNet.add(root, 'vport')
     ixNet.commit()
     vport1 = ixNet.remapIds(vport1)[0]

     vport2 = ixNet.add(root, 'vport')
     ixNet.commit()
     vport2 = ixNet.remapIds(vport2)[0]
	 
     vport3 = ixNet.add(root, 'vport')
     ixNet.commit()
     vport3 = ixNet.remapIds(vport3)[0]
	 
     vport4 = ixNet.add(root, 'vport')
     ixNet.commit()
     vport4 = ixNet.remapIds(vport4)[0]

     chassisObj1 = ixNet.add(root + '/availableHardware', 'chassis')
     ixNet.setAttribute(chassisObj1, '-hostname', chassis1)
     ixNet.commit()
     chassisObj1 = ixNet.remapIds(chassisObj1)[0]

     if (chassis1 != chassis2) :
         chassisObj2 = ixNet.add(root + '/availableHardware', 'chassis')
         ixNet.setAttribute(chassisObj2, '-hostname', chassis2)
         ixNet.commit()
         chassisObj2 = ixNet.remapIds(chassisObj2)[0]
		 
         chassisObj3 = ixNet.add(root + '/availableHardware', 'chassis')
         ixNet.setAttribute(chassisObj3, '-hostname', chassis3)
         ixNet.commit()
         chassisObj3 = ixNet.remapIds(chassisObj3)[0]
		 
         chassisObj4 = ixNet.add(root + '/availableHardware', 'chassis')
         ixNet.setAttribute(chassisObj4, '-hostname', chassis4)
         ixNet.commit()
         chassisObj4 = ixNet.remapIds(chassisObj4)[0]
     else :
         chassisObj2 = chassisObj1
         chassisObj3 = chassisObj1
         chassisObj4 = chassisObj1
		 
     # end if

     cardPortRef1 = chassisObj1 + '/card:%s/port:%s' % (card1,port1)
     ixNet.setMultiAttribute(vport1, '-connectedTo', cardPortRef1,
         '-rxMode', 'captureAndMeasure', '-name', 'Ethernet - 001')
     ixNet.commit()

     cardPortRef2 = chassisObj2 + '/card:%s/port:%s' % (card2,port2)
     ixNet.setMultiAttribute(vport2, '-connectedTo', cardPortRef2,
         '-rxMode', 'captureAndMeasure', '-name', 'Ethernet - 002')
     ixNet.commit()
	 
     cardPortRef3 = chassisObj3 + '/card:%s/port:%s' % (card3,port3)
     ixNet.setMultiAttribute(vport3, '-connectedTo', cardPortRef3,
         '-rxMode', 'captureAndMeasure', '-name', 'Ethernet - 003')
     ixNet.commit()

     cardPortRef4 = chassisObj4 + '/card:%s/port:%s' % (card4,port4)
     ixNet.setMultiAttribute(vport4, '-connectedTo', cardPortRef4,
         '-rxMode', 'captureAndMeasure', '-name', 'Ethernet - 004')
     ixNet.commit()
# end def assignPorts

#proc to generate drill-down global learned info view for LACP
def gererateLacpLearnedInfoView ( viewName ):
    viewCaption = viewName
    protocol = 'LACP'
    drillDownType = 'Global Learned Info'
    root    = ixNet.getRoot()
    statistics = root + '/statistics'
    statsViewList = ixNet.getList(statistics, 'view')
	
   # Add a StatsView
    view = ixNet.add(statistics, 'view')
    ixNet.setAttribute(view, '-caption', viewCaption)
    ixNet.setAttribute(view, '-type', 'layer23NextGenProtocol')
    ixNet.setAttribute(view, '-visible', 'true')
    ixNet.commit()
    view = ixNet.remapIds(view)[0]

   # Set Filters        
    trackingFilter = ixNet.add(view, 'advancedCVFilters')
    ixNet.setAttribute(trackingFilter, '-protocol', protocol)
    ixNet.commit()
    #ixNet getAttr $trackingFilter -availableGroupingOptions        
    ixNet.setAttribute(trackingFilter, '-grouping', drillDownType)
    ixNet.commit()
    layer23NextGenProtocolFilter = view + '/' + 'layer23NextGenProtocolFilter'        
    ixNet.setAttribute(layer23NextGenProtocolFilter, '-advancedCVFilter', trackingFilter)
    ixNet.commit()

    # Enable Stats Columns to be displayed
    statsList = ixNet.getList(view, 'statistic')
    for stat in statsList :
        ixNet.setAttribute(stat, '-enabled', 'true')

    ixNet.commit()

    # Enable Statsview
    ixNet.setAttribute(view, '-enabled', 'true')
    ixNet.commit()
	
################################################################################
# Either feed the ixNetwork library path in the sys.path as below, or put the
# IxNetwork.pm file somewhere else where we python can autoload it.
# "IxNetwork.pm" is available in <IxNetwork_installer_path>\API\Python
################################################################################
ixNetPath = r'C:\Program Files (x86)\Ixia\IxNetwork\8.50.0.160-EB\API\Python'
sys.path.append(ixNetPath)
import IxNetwork

#################################################################################
# Give chassis/client/ixNetwork server port/ chassis port HW port information
# below
#################################################################################
ixTclServer = '10.205.28.122'
ixTclPort   = '8987'
ports       = [('10.205.28.173', '1', '1',), ('10.205.28.173', '1', '2',), ('10.205.28.173', '1', '3',), ('10.205.28.173', '1', '4',)]

# get IxNet class
ixNet = IxNetwork.IxNet()
print("Connecting to IxNetwork client")
ixNet.connect(ixTclServer, '-port', ixTclPort, '-version', '8.50',
     '-setAttribute', 'strict')

# cleaning up the old configfile, and creating an empty config
print("Cleaning up the old config file, and creating an empty config")
ixNet.execute('newConfig')

# assigning ports
assignPorts(ixNet, ports[0], ports[1], ports[2], ports[3])
time.sleep(5)

root    = ixNet.getRoot()
vportTx1 = ixNet.getList(root, 'vport')[0]
vportRx1 = ixNet.getList(root, 'vport')[1]
vportTx2 = ixNet.getList(root, 'vport')[2]
vportRx2 = ixNet.getList(root, 'vport')[3]
vportListLAG1 = [vportTx1, vportTx2]
vportListLAG2 = [vportRx1, vportRx2]

print("Adding 2 LAGS named RED-LAG and BLUE-LAG")
ixNet.add(root, 'lag', '-vports', vportListLAG1, '-name', 'RED-LAG')
ixNet.commit()
ixNet.add(root, 'lag', '-vports', vportListLAG2, '-name', 'BLUE-LAG')
ixNet.commit()

lags = ixNet.getList(ixNet.getRoot(), 'lag')
lag1 = lags[0]
lag2 = lags[1]

print "Adding LACP over RED-LAG & BLUE-LAG"
ixNet.add(lag1, 'protocolStack')
ixNet.commit()
ixNet.add(lag2, 'protocolStack')
ixNet.commit()

lag1stack = ixNet.getList(lag1, 'protocolStack')[0]
lag2stack = ixNet.getList(lag2, 'protocolStack')[0]

ixNet.add(lag1stack, 'ethernet')
ixNet.commit()
ixNet.add(lag2stack, 'ethernet')
ixNet.commit()

lag1eth = ixNet.getList(lag1stack, 'ethernet')[0]
lag2eth = ixNet.getList(lag2stack, 'ethernet')[0]

ixNet.add(lag1eth, 'lagportlacp')
ixNet.commit()
ixNet.add(lag2eth, 'lagportlacp')
ixNet.commit()

lag1lacp = ixNet.getList(lag1eth, 'lagportlacp')[0]
lag2lacp = ixNet.getList(lag2eth, 'lagportlacp')[0]

##################################################################################
# To ADD staticLAG as LAG protocol
#Command sets 
#ixNet.add(lag1eth, 'lagportstaticlag')
#ixNet.commit()
#ixNet.add(lag2eth, 'lagportstaticlag')
#ixNet.commit()
#lag1slag = ixNet.getList(lag1eth, 'lagportstaticlag')[0]
#lag2slag = ixNet.getList(lag2eth, 'lagportstaticlag')[0]
##################################################################################

# configure LACP ActorSystemID and ActorKey to user defined values
print("Configure LACP ActorSystemID and ActorKey to user defined values")

lag1lacpActKey = ixNet.getAttribute(lag1lacp, '-actorKey')
lag2lacpActKey = ixNet.getAttribute(lag2lacp, '-actorKey')

lag1lacpSysId = ixNet.getAttribute(lag1lacp, '-actorSystemId')
lag2lacpSysId = ixNet.getAttribute(lag2lacp, '-actorSystemId')

ixNet.setMultiAttribute(lag1lacpActKey, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.setMultiAttribute(lag2lacpActKey, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.commit()

ixNet.setMultiAttribute(lag1lacpActKey + '/singleValue', '-value', '666')
ixNet.setMultiAttribute(lag2lacpActKey + '/singleValue', '-value', '777')
ixNet.commit()

ixNet.setMultiAttribute(lag1lacpActKey, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.setMultiAttribute(lag2lacpSysId, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.commit()

ixNet.setMultiAttribute(lag1lacpActKey + '/singleValue', '-value', '11666')
ixNet.setMultiAttribute(lag2lacpSysId + '/singleValue', '-value', '11777')
ixNet.commit()

################################################################################
#  Start LAG protocol and wait for 60 seconds                                 #
################################################################################
print("Starting LAG and waiting for 60 seconds for sessions to come up")
ixNet.execute('startAllProtocols')
time.sleep(60)

################################################################################
# Retrieve protocol statistics and LACP per port statistics                    #
################################################################################
print ("\nFetching all Protocol Summary Stats\n")
viewPage  = '::ixNet::OBJ-/statistics/view:"Protocols Summary"/page'
statcap   = ixNet.getAttribute(viewPage, '-columnCaptions')
for statValList in ixNet.getAttribute(viewPage, '-rowValues') :
    for  statVal in statValList :
        print("***************************************************")
        index = 0
        for satIndv in statVal :
            print("%-30s:%s" % (statcap[index], satIndv))
            index = index + 1
        # end for
    # end for
# end for
print("***************************************************")

print ("\nFetching all LACP Per Port Stats\n")
viewPage  = '::ixNet::OBJ-/statistics/view:"LACP Per Port"/page'
statcap   = ixNet.getAttribute(viewPage, '-columnCaptions')
for statValList in ixNet.getAttribute(viewPage, '-rowValues') :
    for  statVal in statValList :
        print("***************************************************")
        index = 0
        for satIndv in statVal :
            print("%-30s:%s" % (statcap[index], satIndv))
            index = index + 1
        # end for
    # end for
# end for
print("***************************************************")

time.sleep(5)
################################################################################
# Disable Synchronization flag on port1 in RED-LAG                             #
################################################################################
print ("\n\nDisable Synchronization flag on port1 in RED-LAG")
redLagport1 = ixNet.getList(lag1lacp, 'port')[0]
redLagport1SyncFlag = ixNet.getAttribute(redLagport1, '-synchronizationFlag')
ixNet.setMultiAttribute(redLagport1SyncFlag, '-pattern', 'singleValue', '-clearOverlays', 'False')
ixNet.commit()
ixNet.setMultiAttribute(redLagport1SyncFlag + '/singleValue', '-value', 'false')
ixNet.commit()
globalObj = ixNet.getRoot() + '/globals'
topology  = globalObj + '/topology'
print ("Applying changes on the fly")
ixNet.execute('applyOnTheFly', topology)

time.sleep(90)
################################################################################
# Retrieve protocol statistics and LACP per port statistics                    #
################################################################################
print ("\nFetching all Protocol Summary Stats\n")
viewPage  = '::ixNet::OBJ-/statistics/view:"Protocols Summary"/page'
statcap   = ixNet.getAttribute(viewPage, '-columnCaptions')
for statValList in ixNet.getAttribute(viewPage, '-rowValues') :
    for  statVal in statValList :
        print("***************************************************")
        index = 0
        for satIndv in statVal :
            print("%-30s:%s" % (statcap[index], satIndv))
            index = index + 1
        # end for
    # end for
# end for
print("***************************************************")
print ("\nFetching all LACP Per Port Stats\n")
viewPage  = '::ixNet::OBJ-/statistics/view:"LACP Per Port"/page'
statcap   = ixNet.getAttribute(viewPage, '-columnCaptions')
for statValList in ixNet.getAttribute(viewPage, '-rowValues') :
    for  statVal in statValList :
        print("***************************************************")
        index = 0
        for satIndv in statVal :
            print("%-30s:%s" % (statcap[index], satIndv))
            index = index + 1
        # end for
    # end for
# end for
print("***************************************************")
time.sleep(5)
################################################################################
# Re-enable Synchronization flag on port1 in RED-LAG                  #
################################################################################
print ("\n\n Re-enable Synchronization flag on port1 in RED-LAG")
redLagport1 = ixNet.getList(lag1lacp, 'port')[0]
redLagport1SyncFlag = ixNet.getAttribute(redLagport1, '-synchronizationFlag')
ixNet.setMultiAttribute(redLagport1SyncFlag + '/singleValue', '-value', 'true')
ixNet.commit()
globalObj = ixNet.getRoot() + '/globals'
topology  = globalObj + '/topology'
print ("Applying changes on the fly")
ixNet.execute('applyOnTheFly', topology)
time.sleep(90)
################################################################################
# Retrieve protocol statistics                                                 #
################################################################################
print ("\nFetching all Protocol Summary Stats\n")
viewPage  = '::ixNet::OBJ-/statistics/view:"Protocols Summary"/page'
statcap   = ixNet.getAttribute(viewPage, '-columnCaptions')
for statValList in ixNet.getAttribute(viewPage, '-rowValues') :
    for  statVal in statValList :
        print("***************************************************")
        index = 0
        for satIndv in statVal :
            print("%-30s:%s" % (statcap[index], satIndv))
            index = index + 1
        # end for
    # end for
# end for
print("***************************************************")
print ("\nFetching all LACP Per Port Stats\n")
viewPage  = '::ixNet::OBJ-/statistics/view:"LACP Per Port"/page'
statcap   = ixNet.getAttribute(viewPage, '-columnCaptions')
for statValList in ixNet.getAttribute(viewPage, '-rowValues') :
    for  statVal in statValList :
        print("***************************************************")
        index = 0
        for satIndv in statVal :
            print("%-30s:%s" % (statcap[index], satIndv))
            index = index + 1
        # end for
    # end for
# end for
print("***************************************************")

time.sleep(5)
################################################################################
# Perform LACPDU stop on RED-LAG-LACP                                      #
################################################################################
print ("\n\nPerform LACPDU stop on RED-LAG-LACP ")
ixNet.execute('lacpStopPDU', lag1lacp)
time.sleep(90)

################################################################################
# Retrieve LACP global Learned Info                                            #
################################################################################
print ("\n\n Retrieve LACP global Learned Info")
viewName = 'LACP-global-learned-Info-TCLview'
gererateLacpLearnedInfoView(viewName)
viewPageName = '::ixNet::OBJ-/statistics/view:"LACP-global-learned-Info-TCLview"'
viewPage  = '::ixNet::OBJ-/statistics/view:"LACP-global-learned-Info-TCLview"/page'

ixNet.execute('refresh', viewPageName)
time.sleep(10)              
statcap   = ixNet.getAttribute(viewPage, '-columnCaptions')
for statValList in ixNet.getAttribute(viewPage, '-rowValues') :
    for  statVal in statValList :
        print("***************************************************")
        index = 0
        for satIndv in statVal :
            print("%-30s:%s" % (statcap[index], satIndv))
            index = index + 1
        # end for
    # end for
# end for
print("***************************************************")
time.sleep(5)
################################################################################
# Perform LACPDU start on RED-LAG                                     #
################################################################################
print ("\n\nPerform LACPDU start on RED-LAG ")
ixNet.execute('lacpStartPDU', lag1lacp)
time.sleep(90)

################################################################################
# Retrieve LACP global Learned Info                                            #
################################################################################
print ("\n\n Retrieve LACP global Learned Info")
viewPageName = '::ixNet::OBJ-/statistics/view:"LACP-global-learned-Info-TCLview"'
viewPage  = '::ixNet::OBJ-/statistics/view:"LACP-global-learned-Info-TCLview"/page'

ixNet.execute('refresh', viewPageName)
time.sleep(10)              
statcap   = ixNet.getAttribute(viewPage, '-columnCaptions')
for statValList in ixNet.getAttribute(viewPage, '-rowValues') :
    for  statVal in statValList :
        print("***************************************************")
        index = 0
        for satIndv in statVal :
            print("%-30s:%s" % (statcap[index], satIndv))
            index = index + 1
        # end for
    # end for
# end for
print("***************************************************")
time.sleep(5)
################################################################################
# Stop all protocols                                                           #
################################################################################
print ('Stopping protocols')
ixNet.execute('stopAllProtocols')

print ('!!! Test Script Ends !!!')

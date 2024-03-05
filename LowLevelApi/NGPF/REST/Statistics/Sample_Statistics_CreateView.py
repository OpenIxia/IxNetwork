################################################################################


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
#    This sample configures 10 IPv4 sessions on each of the two ports,         # 
#    adds a traffic Item that uses IPv4 endpoints, sends traffic and           #
#    create a new Advanced Filtering View for IPv4 statistics with             #
#    Device Group Level Grouping                                               #
#                                                                              #
################################################################################

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
import restAPI as rest

################################################################################
# Connect to IxNet client
################################################################################
ixNet = IxNet(py.ixTclServer, int(py.ixTclPort)+3000)
ixNet.connect()
root = ixNet.getRoot()
#############################################################################################################

#############################################################################################################
################################################################################
# Cleaning up IxNetwork
################################################################################
print "Cleaning up IxNetwork..."
ixNet.execute('newConfig')

################################################################################
# Adding ports to configuration
################################################################################
print "Adding ports to configuration"
root = ixNet.getRoot()
ixNet.add(root, 'vport')
ixNet.add(root, 'vport')
ixNet.commit()
vPorts = ixNet.getList(root, 'vport')
vport1 = vPorts[0]
vport2 = vPorts[1]

################################################################################
# Adding IPv4 endpoints to configuration
################################################################################
print "Add topologies"
ixNet.add(root, 'topology')
ixNet.add(root, 'topology')
ixNet.commit()

topo1 = ixNet.getList(root, 'topology')[0]
topo2 = ixNet.getList(root, 'topology')[1]

print "Add ports to topologies"
ixNet.setAttribute(topo1, '-vports', [vport1])
ixNet.setAttribute(topo2, '-vports', [vport2])
ixNet.commit()

print "Add device groups to topologies"
ixNet.add(topo1, 'deviceGroup')
ixNet.add(topo2, 'deviceGroup')
ixNet.commit()

dg1 = ixNet.getList(topo1, 'deviceGroup')[0]
dg2 = ixNet.getList(topo2, 'deviceGroup')[0]

print "Add ethernet stacks to device groups"
ixNet.add(dg1, 'ethernet')
ixNet.add(dg2, 'ethernet')
ixNet.commit()

mac1 = ixNet.getList(dg1, 'ethernet')[0]
mac2 = ixNet.getList(dg2, 'ethernet')[0]

print "Add ipv4 stacks to ethernets"
ixNet.add(mac1, 'ipv4')
ixNet.add(mac2, 'ipv4')
ixNet.commit()

ipv4_1 = ixNet.getList(mac1, 'ipv4')[0]
ipv4_2 = ixNet.getList(mac2, 'ipv4')[0]

print "Setting multi values for ipv4 addresses"
ixNet.setMultiAttribute(ixNet.getAttribute(ipv4_1, '-address') + '/counter', '-start', '22.1.1.1', '-step', '0.0.1.0')
ixNet.setMultiAttribute(ixNet.getAttribute(ipv4_1, '-gatewayIp') + '/counter', '-start', '22.1.1.2', '-step', '0.0.1.0')
ixNet.setMultiAttribute(ixNet.getAttribute(ipv4_1, '-resolveGateway') + '/singleValue', '-value', 'true')
ixNet.setMultiAttribute(ixNet.getAttribute(ipv4_2, '-address') + '/counter', '-start', '22.1.1.2', '-step', '0.0.1.0')
ixNet.setMultiAttribute(ixNet.getAttribute(ipv4_2, '-gatewayIp') + '/counter', '-start', '22.1.1.1', '-step', '0.0.1.0')
ixNet.setMultiAttribute(ixNet.getAttribute(ipv4_2, '-resolveGateway') + '/singleValue', '-value', 'true')
ixNet.commit()

################################################################################
# Create Traffic for IPv4
################################################################################
print ''
print "Creating Traffic for IPv4"

ixNet.add(ixNet.getRoot() + '/traffic', 'trafficItem')
ixNet.commit()
ti1 = ixNet.getList(ixNet.getRoot() + '/traffic', 'trafficItem')[0]
ixNet.setMultiAttribute( ti1,
        '-name'                 ,'Traffic IPv4',
        '-trafficType'          ,'ipv4',
        '-allowSelfDestined'    ,False,
        '-trafficItemType'      ,'l2L3',
        '-mergeDestinations'    ,True,
        '-egressEnabled'        ,False,
        '-srcDestMesh'          ,'manyToMany',
        '-enabled'              ,True,
        '-routeMesh'            ,'fullMesh',
        '-transmitMode'         ,'interleaved',
        '-biDirectional'        ,True,
        '-hostsPerNetwork'      ,1)
ixNet.commit()
ixNet.setAttribute(ti1, '-trafficType', 'ipv4')
ixNet.commit()
ixNet.add(ti1, 'endpointSet')
ixNet.setMultiAttribute(ti1+'/endpointSet/1',
        '-sources',             [topo1],
        '-destinations',        [topo2],
        '-name',                'ep-set1',
        '-sourceFilter',        '',
        '-destinationFilter',   '')

ixNet.commit()
print '*********** - ',ti1+'/endpointSet/1'

ixNet.commit()
ixNet.setMultiAttribute(ti1 + "/configElement/1/frameSize",
        '-type',        'fixed',
        '-fixedSize',   128)
ixNet.setMultiAttribute(ti1 + "/configElement/1/frameRate",
        '-type',        'framesPerSecond',
        '-rate',        100)
ixNet.setMultiAttribute(ti1 + "/configElement/1/transmissionControl",
        '-duration'               ,1,
        '-iterationCount'         ,5,
        '-startDelayUnits'        ,'bytes',
        '-minGapBytes'            ,12,
        '-frameCount'             ,1000,
        '-type'                   ,'continous',
        '-interBurstGapUnits'     ,'nanoseconds',
        '-interBurstGap'          , 0,
        '-enableInterBurstGap'    ,False,
        '-interStreamGap'         ,0,
        '-repeatBurst'            ,1,
        '-enableInterStreamGap'   ,False,
        '-startDelay'             ,0,
        '-burstPacketCount'       ,1,)
ixNet.setMultiAttribute(ti1 + "/tracking", '-trackBy', ['sourceDestValuePair0'])
ixNet.commit()

################################################################################
# Assign ports 
################################################################################
vports = ixNet.getList(ixNet.getRoot(), 'vport')
print "Assigning ports to " + str(vports) + " ..."
assignPorts=ixNet.execute('assignPorts',py.ports,[],vports,True )

################################################################################
# Start All Protocols
################################################################################
print "Starting All Protocols"
ixNet.execute('startAllProtocols')
print "Sleep 30sec for protocols to start"
time.sleep(30)

################################################################################
# Generate, apply, start traffic
################################################################################
ixNet.execute('generate', ti1)
ixNet.execute('apply', root+'/traffic')
ixNet.execute('start', root+'/traffic')
print "Sleep 30sec to send all traffic"
time.sleep(30)

print "#########################"
print "## Statistics Samples ##"
print "#########################"
print ""

################################################################################
# Define function to get the view object using the view name
################################################################################
def getViewObject(ixNet, viewName):
    views = ixNet.getList('/statistics', 'view')
    viewObj = ''
    editedViewName = '::ixNet::OBJ-/statistics/view:\"' + viewName + '\"'
    for view in views:
        if editedViewName == view:
             viewObj = view
             break
    return viewObj

################################################################################
# Define the create advanced filter custom view
################################################################################
def createAdvFilCustomView (ixNet, cvName,  protocol,  grLevel, sortExpr):
    print "- creating view %s, with protocol %s, grouping level %s" % ( cvName, protocol, grLevel )
    data = {"caption":cvName,"type":"layer23NextGenProtocol","visible":"true"}
    view=ixNet.add(ixNet.getRoot()+'/statistics', 'view',data)
    ixNet.commit()
    #print '------------------------------------------Here  -- 1'
    view    = ixNet.getList(ixNet.getRoot()+'/statistics', 'view')[-1]
    print '------------------------------------------Here  -- 1',view[-1]
    #view = ixNet.getList(ixNet.getRoot()+'/statistics', 'view')[-1]

    ################################################################################
    # add advanced filtering filter
    ################################################################################
    print ("\t - add advanced filtering filter ...")
    trackingFilter = ixNet.add (view, 'advancedCVFilters')

    ################################################################################
    # sett protocol for the filter
    ################################################################################
    print "\t - setting protocol %s for the filter." % protocol
    ixNet.setAttribute(trackingFilter, '-protocol', protocol)
    ixNet.commit()

    ################################################################################
    # select the grouping level for the filter.
    ################################################################################
    print "\t - selecting %s for the filter grouping level." % grLevel
    ixNet.setAttribute(trackingFilter, '-grouping', grLevel)
    ixNet.commit()

    ################################################################################
    # add filter expression and filter sorting stats.
    ################################################################################
    print ("\t - adding filter expression and filter sorting stats.")
    ixNet.setAttribute (trackingFilter, '-sortingStats', sortExpr)
    ixNet.commit()

    ################################################################################
    # set the filter
    ################################################################################
    print("\t - setting the filter.")
    fil     = ixNet.getList (view, 'layer23NextGenProtocolFilter')[0]
    ixNet.setAttribute (fil, '-advancedCVFilter', trackingFilter)
    ixNet.commit()

    ################################################################################
    # enable the stats columns to be displayed for the view
    ################################################################################
    print ("\t - enable the stats columns to be displayed for the view.")
    statsList = ixNet.getList (view, 'statistic')
    for stat in statsList:
        ixNet.setAttribute(stat, '-enabled', 'true')
    ixNet.commit()

    ################################################################################
    # enable the view going and start retrieving stats
    ################################################################################
    print ("\t - enabling the view going and start retrieving stats.")
    ixNet.setAttribute (view, '-enabled', 'true')
    ixNet.commit()

cvName      = 'Custom View - IPv4'
protocol    = 'IPv4'
grLevel     = 'Per Device Group'
sortExpr    = '[Device Group] = desc'

################################################################################
# Create the custom view for IPv4 NGPF
################################################################################
print "Create custom view for IPv4 NGPF"
createAdvFilCustomView (ixNet, cvName,  protocol,  grLevel, sortExpr)

################################################################################
# Refresh the created view
################################################################################
print "Refreshing the new view"
newview = getViewObject(ixNet, cvName)
ixNet.execute('refresh', newview)
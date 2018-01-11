################################################################################
# Version 1.0    $Revision: 1 $
# $Author: Mario Dicu $
#
#    Copyright © 1997 - 2015 by IXIA
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
#    This sample configures 10 IPv4 sessions on each of the two ports,         # 
#    adds a traffic Item that uses IPv4 endpoints, sends traffic and           #
#    create a new Advanced Filtering View for IPv4 statistics with             #
#    Device Group Level Grouping                                               #
#                                                                              #
################################################################################

if not Object.const_defined?('Py') then
    class TestFailedError < Exception
    end

    class Py
        @@ports = [['10.200.115.151', 4, 1], ['10.200.115.151', 4, 2]]
        @@ixApiServer = '10.200.115.203'
        @@ixApiPort = 8009

        def self.ports
            @@ports
        end

        def self.ixApiServer
            @@ixApiServer
        end

        def self.ixApiPort
            @@ixApiPort
        end
    end
end
################################################################################
# Import the IxNet library
################################################################################
$:.unshift 'C:\samples\IxNetwork.rb'
require 'IxNetwork'


@ixNet = IxNetwork.new

################################################################################
# Connect to IxNet client
################################################################################

@ixNet.connect(Py.ixApiServer, '-port', Py.ixApiPort, '-version', '7.40')

################################################################################
# Cleaning up IxNetwork
################################################################################
puts "Cleaning up IxNetwork..."
@ixNet.execute('newConfig')

################################################################################
# Adding ports to configuration
################################################################################
puts "Adding ports to configuration"
root = @ixNet.getRoot()
@ixNet.add(root, 'vport')
@ixNet.add(root, 'vport')
@ixNet.commit()
vPorts = @ixNet.getList(root, 'vport')
vport1 = vPorts[0]
vport2 = vPorts[1]

################################################################################
# Adding IPv4 endpoints to configuration
################################################################################
puts "Add topologies"
@ixNet.add(root, 'topology')
@ixNet.add(root, 'topology')
@ixNet.commit()

topo1 = @ixNet.getList(root, 'topology')[0]
topo2 = @ixNet.getList(root, 'topology')[1]

puts "Add ports to topologies"
@ixNet.setAttribute(topo1, '-vports', vport1)
@ixNet.setAttribute(topo2, '-vports', vport2)
@ixNet.commit()

puts "Add device groups to topologies"
@ixNet.add(topo1, 'deviceGroup')
@ixNet.add(topo2, 'deviceGroup')
@ixNet.commit()

dg1 = @ixNet.getList(topo1, 'deviceGroup')[0]
dg2 = @ixNet.getList(topo2, 'deviceGroup')[0]

puts "Add ethernet stacks to device groups"
@ixNet.add(dg1, 'ethernet')
@ixNet.add(dg2, 'ethernet')
@ixNet.commit()

mac1 = @ixNet.getList(dg1, 'ethernet')[0]
mac2 = @ixNet.getList(dg2, 'ethernet')[0]

puts "Add ipv4 stacks to ethernets"
@ixNet.add(mac1, 'ipv4')
@ixNet.add(mac2, 'ipv4')
@ixNet.commit()

ipv4_1 = @ixNet.getList(mac1, 'ipv4')[0]
ipv4_2 = @ixNet.getList(mac2, 'ipv4')[0]

puts "Setting multi values for ipv4 addresses"
@ixNet.setMultiAttribute(@ixNet.getAttribute(ipv4_1, '-address') + '/counter', '-start', '22.1.1.1', '-step', '0.0.1.0')
@ixNet.setMultiAttribute(@ixNet.getAttribute(ipv4_1, '-gatewayIp') + '/counter', '-start', '22.1.1.2', '-step', '0.0.1.0')
@ixNet.setMultiAttribute(@ixNet.getAttribute(ipv4_1, '-resolveGateway') + '/singleValue', '-value', 'true')
@ixNet.setMultiAttribute(@ixNet.getAttribute(ipv4_2, '-address') + '/counter', '-start', '22.1.1.2', '-step', '0.0.1.0')
@ixNet.setMultiAttribute(@ixNet.getAttribute(ipv4_2, '-gatewayIp') + '/counter', '-start', '22.1.1.1', '-step', '0.0.1.0')
@ixNet.setMultiAttribute(@ixNet.getAttribute(ipv4_2, '-resolveGateway') + '/singleValue', '-value', 'true')
@ixNet.commit()

################################################################################
# Create Traffic for IPv4
################################################################################
puts ''
puts "Creating Traffic for IPv4"

@ixNet.add(@ixNet.getRoot() + '/traffic', 'trafficItem')
@ixNet.commit()
ti1 = @ixNet.getList(@ixNet.getRoot() + '/traffic', 'trafficItem')[0]
@ixNet.setMultiAttribute( ti1,
        '-name'                 ,'Traffic IPv4',
        '-trafficType'          ,'ipv4',
        '-allowSelfDestined'    ,false,
        '-trafficItemType'      ,'l2L3',
        '-mergeDestinations'    ,true,
        '-egressEnabled'        ,false,
        '-srcDestMesh'          ,'manyToMany',
        '-enabled'              ,true,
        '-routeMesh'            ,'fullMesh',
        '-transmitMode'         ,'interleaved',
        '-biDirectional'        ,true,
        '-hostsPerNetwork'      ,1)
@ixNet.commit()
@ixNet.setAttribute(ti1, '-trafficType', 'ipv4')
@ixNet.commit()
@ixNet.add(ti1, 'endpointSet',
        '-sources',             ipv4_1,
        '-destinations',        ipv4_2,
        '-name',                'ep-set1',
        '-sourceFilter',        '',
        '-destinationFilter',   '')
@ixNet.commit()
@ixNet.setMultiAttribute(ti1 + "/configElement:1/frameSize",
        '-type',        'fixed',
        '-fixedSize',   128)
@ixNet.setMultiAttribute(ti1 + "/configElement:1/frameRate",
        '-type',        'percentLineRate',
        '-rate',        10)
@ixNet.setMultiAttribute(ti1 + "/configElement:1/transmissionControl",
        '-duration'               ,1,
        '-iterationCount'         ,1,
        '-startDelayUnits'        ,'bytes',
        '-minGapBytes'            ,12,
        '-frameCount'             ,10000,
        '-type'                   ,'fixedFrameCount',
        '-interBurstGapUnits'     ,'nanoseconds',
        '-interBurstGap'          , 0,
        '-enableInterBurstGap'    ,false,
        '-interStreamGap'         ,0,
        '-repeatBurst'            ,1,
        '-enableInterStreamGap'   ,false,
        '-startDelay'             ,0,
        '-burstPacketCount'       ,1)
@ixNet.setMultiAttribute(ti1 + "/tracking", '-trackBy', ['ipv4SourceIp0'])
@ixNet.commit()

################################################################################
# Assign ports 
################################################################################
vports = @ixNet.getList(@ixNet.getRoot(), 'vport')
puts "Assigning ports to " + vports.to_s + " ..."
assignPorts = @ixNet.execute('assignPorts', Py.ports, [], @ixNet.getList("/","vport"), true)
if assignPorts != vports then
    raise TestFailedError("FAILED assigning ports. Got " + assignPorts)
else
    puts("PASSED assigning ports. Got " + assignPorts.to_s)
end

################################################################################
# Start All Protocols
################################################################################
puts "Starting All Protocols"
@ixNet.execute('startAllProtocols')
puts "Sleep 30sec for protocols to start"
sleep(30)

################################################################################
# Generate, apply, start traffic
################################################################################
@ixNet.execute('generate', ti1)
@ixNet.execute('apply', '/traffic')
@ixNet.execute('start', '/traffic')
puts "Sleep 30sec to send all traffic"
sleep(30)

puts "#########################"
puts "## Statistics Samples ##"
puts "#########################"
puts ""

################################################################################
# Define function to get the view object using the view name
################################################################################
def getViewObject(ixNet, viewName)
    views = @ixNet.getList('/statistics', 'view')
    viewObj = ''
    editedViewName = '::ixNet::OBJ-/statistics/view:\"' + viewName + '\"'
    for view in views
        if editedViewName == view then
             viewObj = view
             break
        end
    end
    return viewObj
end

################################################################################
# Define the create advanced filter custom view
################################################################################
def createAdvFilCustomView (ixNet, cvName,  protocol,  grLevel, sortExpr)
    puts("- creating view "+cvName+", with protocol "+protocol+", grouping level "+grLevel)
    @ixNet.add(@ixNet.getRoot()+'/statistics', 'view')
    @ixNet.commit()

    mv      = @ixNet.getList(@ixNet.getRoot(), 'statistics')[0]
    view    = @ixNet.getList(mv, 'view')[-1]

    @ixNet.setAttribute(view, '-caption', cvName)
    @ixNet.setAttribute(view, '-type', 'layer23NextGenProtocol')
    @ixNet.setAttribute(view, '-visible', 'true')
    @ixNet.commit()

    view    = @ixNet.getList(mv, 'view')[-1]

    ################################################################################
    # add advanced filtering filter
    ################################################################################
    puts("\t - add advanced filtering filter ...")
    trackingFilter = @ixNet.add(view, 'advancedCVFilters')

    ################################################################################
    # sett protocol for the filter
    ################################################################################
    puts "\t - setting protocol %s for the filter." % protocol
    @ixNet.setAttribute(trackingFilter, '-protocol', protocol)
    @ixNet.commit()

    ################################################################################
    # select the grouping level for the filter.
    ################################################################################
    puts "\t - selecting %s for the filter grouping level." % grLevel
    @ixNet.setAttribute(trackingFilter, '-grouping', grLevel)
    @ixNet.commit()

    ################################################################################
    # add filter expression and filter sorting stats.
    ################################################################################
    puts("\t - adding filter expression and filter sorting stats.")
    @ixNet.setAttribute(trackingFilter, '-sortingStats', sortExpr)
    @ixNet.commit()

    ################################################################################
    # set the filter
    ################################################################################
    puts("\t - setting the filter.")
    fil     = @ixNet.getList(view, 'layer23NextGenProtocolFilter')[0]
    @ixNet.setAttribute(fil, '-advancedCVFilter', trackingFilter)
    @ixNet.commit()

    ################################################################################
    # enable the stats columns to be displayed for the view
    ################################################################################
    puts("\t - enable the stats columns to be displayed for the view.")
    statsList = @ixNet.getList(view, 'statistic')
    for stat in statsList
        @ixNet.setAttribute(stat, '-enabled', 'true')
        end
    @ixNet.commit()

    ################################################################################
    # enable the view going and start retrieving stats
    ################################################################################
    puts("\t - enabling the view going and start retrieving stats.")
    @ixNet.setAttribute(view, '-enabled', 'true')
    @ixNet.commit()
end
cvName      = 'Custom View - IPv4'
protocol    = 'IPv4'
grLevel     = 'Per Device Group'
sortExpr    = '[Device Group] = desc'

################################################################################
# Create the custom view for IPv4 NGPF
################################################################################
puts "Create custom view for IPv4 NGPF"
createAdvFilCustomView(ixNet, cvName,  protocol,  grLevel, sortExpr)

################################################################################
# Refresh the created view
################################################################################
puts "Refreshing the new view"
newview = getViewObject(ixNet, cvName)
@ixNet.execute('refresh', newview)
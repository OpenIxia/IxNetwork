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
#    and performs the following traffic actions                                #
#    - Creating 2 Traffic Items for IPv4                                       #
#    - Add 2 new Endpoint sets to TI 1 IPv4                                    #
#    - Remove last configured Endpoint set from TI 1 IPv4                      #
#    - Disable TI 1 IPv4                                                       #
#    - Enable TI 1 IPv4                                                        #
#    - Duplicate TI 1 IPv4 3 times                                             #
#    - Remove a Traffic Item copy                                              #
#    - Adding Ingress Tracking for bot Traffic Items                           #
#    - Adding Egress Tracking for both Traffic Items                           #
#    - Adding Latency Bins Tracking for both Traffic Items                     #
#    - Generate Traffic                                                        #
#    - Apply Traffic                                                           #
#    - Start Traffic                                                           #
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
# Defining the create IPv4 Traffic Item function
################################################################################
def createBasicIPv4TrafficItem(ixNet, name, sourceEP, destEP)
    puts("- creating traffic item: " + name)
    @ixNet.add(@ixNet.getRoot() + '/traffic', 'trafficItem')
    @ixNet.commit()
    trafficItem = @ixNet.getList(@ixNet.getRoot() + '/traffic', 'trafficItem')[-1]
    @ixNet.setMultiAttribute( trafficItem,
            '-name'                 ,name,
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
    @ixNet.setAttribute(trafficItem, '-trafficType', 'ipv4')
    @ixNet.commit()
    @ixNet.add(trafficItem, 'endpointSet',
            '-sources',             sourceEP,
            '-destinations',        destEP,
            '-name',                'ep-set1',
            '-sourceFilter',        '',
            '-destinationFilter',   '')
    @ixNet.commit()
    @ixNet.setMultiAttribute(trafficItem + "/configElement:1/frameSize",
            '-type',        'fixed',
            '-fixedSize',   128)
    @ixNet.setMultiAttribute(trafficItem + "/configElement:1/frameRate",
            '-type',        'percentLineRate',
            '-rate',        2)
    @ixNet.setMultiAttribute(trafficItem + "/configElement:1/transmissionControl",
            '-duration'               ,1,
            '-iterationCount'         ,1,
            '-startDelayUnits'        ,'bytes',
            '-minGapBytes'            ,12,
            '-frameCount'             ,10000,
            '-type'                   ,'continuous',
            '-interBurstGapUnits'     ,'nanoseconds',
            '-interBurstGap'          , 0,
            '-enableInterBurstGap'    ,false,
            '-interStreamGap'         ,0,
            '-repeatBurst'            ,1,
            '-enableInterStreamGap'   ,false,
            '-startDelay'             ,0,
            '-burstPacketCount'       ,1)
    @ixNet.commit()
end
################################################################################
# Defining the Ingress Tracking for Traffic Item set function
################################################################################
def setIngressTrackingForTI(ixNet, ti, trackingList)
    tiName = @ixNet.getAttribute(ti, '-name')
    puts("--- Traffic Item: "+tiName+" setting ingress tracking" + trackingList.to_s)
    @ixNet.setMultiAttribute(ti + "/tracking", '-trackBy', trackingList)
    @ixNet.commit()
end
################################################################################
# Defining the Egress Tracking for Traffic Item set function
################################################################################    
def setFirstEgressTrackingForTI(ixNet, ti, stack, field)
    tiName = @ixNet.getAttribute(ti, '-name')
    puts("--- Traffic Item: "+tiName+" setting eggress tracking to field "+field+" for stack"+stack)
    @ixNet.setAttribute(ti, '-egressEnabled', true)
    et = @ixNet.getList(ti, 'egressTracking')[0]
    @ixNet.setAttribute(et, '-encapsulation', 'Any: Use Custom Settings')
    @ixNet.setAttribute(et, '-offset', 'CustomByField')
    @ixNet.commit()
    stackList = @ixNet.getList(@ixNet.getList(ti, 'egressTracking')[0] + '/fieldOffset', 'stack')
    for mstack in stackList do
        if mstack.include?(stack) then
            fieldList = @ixNet.getList(mstack, 'field')
            for mfield in fieldList
                if mfield.include?(field) then
                    @ixNet.setAttribute(mfield, '-activeFieldChoice', true)
                    @ixNet.setAttribute(mfield, '-trackingEnabled', true)
                    @ixNet.setAttribute(mfield, '-valueType', 'valueList')
                    @ixNet.setAttribute(mfield, '-valueList', [4, 6])
                    @ixNet.commit()
                    break
                end
            end
        end
    end
end

################################################################################
# Defining the Latency Bins for Traffic Item set function
################################################################################
def setLatencyBinsTrackingForTI(ixNet, ti, binNo)
    tiName = @ixNet.getAttribute(ti, '-name')
    puts("--- Traffic Item: "+tiName+" setting latency bins tracking "+binNo.to_s)
    latencyBin = @ixNet.getList(ti + '/tracking', 'latencyBin')[0]
    @ixNet.setAttribute(latencyBin, '-enabled', true)
    @ixNet.setAttribute(latencyBin, '-numberOfBins', binNo)
    @ixNet.commit()
end
################################################################################
# Defining the Add EndpointSet function
################################################################################
def addEndpointSet(ixNet, trafficItem, epName, sourceEPs, destEPs)
    puts("- adding "+epName+" endpoint set")
    @ixNet.add(trafficItem, 'endpointSet',
            '-sources',             sourceEPs,
            '-destinations',        destEPs,
            '-name',                epName,
            '-sourceFilter',        '',
            '-destinationFilter',   '')
    @ixNet.commit()
end
################################################################################
# Defining the Remove EndpointSet function
################################################################################
def removeEndpointSet(ixNet, trafficItem, epName)
    puts("- removing "+epName+" endpoint set")
    eps = @ixNet.getList(trafficItem, 'endpointSet')
    for ep in eps
        mName = @ixNet.getAttribute(ep, '-name')
        if mName.to_s == epName.to_s then
            @ixNet.remove(ep)
            @ixNet.commit()
            break
        end
    end
end

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
# Configure IPv4 Endpoints to configuration
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

puts "Add Ethernet stacks to device groups"
@ixNet.add(dg1, 'ethernet')
@ixNet.add(dg2, 'ethernet')
@ixNet.commit()

mac1 = @ixNet.getList(dg1, 'ethernet')[0]
mac2 = @ixNet.getList(dg2, 'ethernet')[0]

puts "Add ipv4 stacks to Ethernets"
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
# Start protocols
################################################################################
puts "Starting All Protocols"
@ixNet.execute('startAllProtocols')
puts "Sleep 30sec for protocols to start"
sleep(30)

################################################################################
# Create 2 IPv4 Traffic Items
################################################################################
puts "######################"
puts "## Traffic Samples ##"
puts "######################"
puts ''
puts "Creating 2 Traffic Items for IPv4"
createBasicIPv4TrafficItem(@ixNet, "TI 1 IPv4", ipv4_1, ipv4_2)
createBasicIPv4TrafficItem(@ixNet, "TI 2 IPv4", ipv4_2, ipv4_1)

ti1 = @ixNet.getList('/traffic', 'trafficItem')[0]
ti2 = @ixNet.getList('/traffic', 'trafficItem')[1]
puts "Add 2 new Endpoint sets to TI 1 IPv4"
addEndpointSet(@ixNet, ti1, 'ep-set2', ipv4_2, ipv4_1)
addEndpointSet(@ixNet, ti1, 'ep-set3', ipv4_2, ipv4_1)
puts "Remove last configured Endpoint set from TI 1 IPv4"
removeEndpointSet(@ixNet, ti1, 'ep-set3')

################################################################################
# Performing the Traffic Actions Samples
################################################################################
puts "Traffic Actions Samples:"
puts "- Disable TI 1 IPv4"
@ixNet.setAttribute(ti1, '-enabled', false)
@ixNet.commit()
puts "- Enable TI 1 IPv4"
@ixNet.setAttribute(ti1, '-enabled', true)
@ixNet.commit()
puts "- Duplicate TI 1 IPv4 3 times"
@ixNet.execute('duplicate', ti1, 3)
puts "- Remove a Traffic Item copy"
ti_remove = @ixNet.getList('/traffic', 'trafficItem').drop(2)
@ixNet.remove(ti_remove)
@ixNet.commit()
puts "- Adding Ingress Tracking for bot Traffic Items"
trackingList = ['sourceDestValuePair0']
setIngressTrackingForTI(@ixNet, ti1, trackingList)
setIngressTrackingForTI(@ixNet, ti2, trackingList)
puts "- Adding Egress Tracking for both Traffic Items"
setFirstEgressTrackingForTI(@ixNet, ti1, "ipv4", "ipv4.header.version-1")
setFirstEgressTrackingForTI(@ixNet, ti2, "ipv4", "ipv4.header.version-1")
puts "- Adding Latency Bins Tracking for both Traffic Items"
setLatencyBinsTrackingForTI(@ixNet, ti1, 4)
setLatencyBinsTrackingForTI(@ixNet, ti2, 4)
puts "- Generate Traffic"
@ixNet.execute('generate', [ti1, ti2])
puts "- Apply Traffic"
@ixNet.execute('apply', '/traffic')
puts "- Start Traffic"
@ixNet.execute('start', '/traffic')
puts "Sleep 30sec then stop traffic"
sleep(30)
puts "- Stop Traffic"
@ixNet.execute('stop', '/traffic')

################################################################################
# Stop Protocols
################################################################################
puts "Stop All Protocols"
@ixNet.execute('stopAllProtocols')
puts "Sleep 30sec for protocols to stop"
sleep(30)
puts("script done")

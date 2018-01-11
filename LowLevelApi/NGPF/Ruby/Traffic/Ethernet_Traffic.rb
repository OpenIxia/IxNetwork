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
#    This sample configures 10 Ethernet sessions on each of the two ports,     #
#    adds a traffic Item that uses Ethernet endpoints, sends traffic and       #
#    checks the loss using the statistics                                      #
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
# Configuring Ethernet Endpoints
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

################################################################################
# Configure Ethernet Traffic
################################################################################
puts ''
puts "Creating Traffic for Eth"

@ixNet.add(@ixNet.getRoot() + '/traffic', 'trafficItem')
@ixNet.commit()
ti1 = @ixNet.getList(@ixNet.getRoot() + '/traffic', 'trafficItem')[0]
@ixNet.setMultiAttribute( ti1,
'-name'                 ,'Traffic Eth',
'-trafficType'          ,'ethernetVlan',
'-allowSelfDestined'    ,false,
'-trafficItemType'      ,'L2L3',
'-mergeDestinations'    ,true,
'-egressEnabled'        ,false,
'-srcDestMesh'          ,'manyToMany',
'-enabled'              ,true,
'-routeMesh'            ,'fullMesh',
'-transmitMode'         ,'interleaved',
'-biDirectional'        ,true,
'-hostsPerNetwork'      ,1)
@ixNet.commit()
@ixNet.setAttribute(ti1, '-trafficType', 'ethernetVlan')
@ixNet.commit()
@ixNet.add(ti1, 'endpointSet',
'-sources',             mac1,
'-destinations',        mac2,
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
@ixNet.setMultiAttribute(ti1 + "/tracking", '-trackBy', ['sourceDestValuePair0'])
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
# Generate, apply and start traffic
################################################################################
r = @ixNet.getRoot()
@ixNet.execute('generate', ti1)
@ixNet.execute('apply', r + '/traffic')
@ixNet.execute('start', r + '/traffic')
puts "Sleep 30sec to send all traffic"
sleep(30)

################################################################################
# Checking Stats to see if traffic was sent OK
################################################################################
puts "Checking Stats to check if traffic was sent OK"
puts "Getting the object for view Traffic Item Statistics"
viewName = "Traffic Item Statistics"
views = @ixNet.getList('/statistics', 'view')
viewObj = ''
editedViewName = '::ixNet::OBJ-/statistics/view:"' + viewName + '"'
for view in views
    if editedViewName == view then
        viewObj = view
        break
    end
end
puts("Getting the Tx/Rx Frames values from " + viewObj)
txFrames = @ixNet.execute('getColumnValues', viewObj, 'Tx Frames')
rxFrames = @ixNet.execute('getColumnValues', viewObj, 'Rx Frames')
txFrames.zip(rxFrames).each do |txStat, rxStat|
    if txStat != rxStat then
        puts("Rx Frames ("+txStat+") != Tx Frames ("+rxStat+")")
        raise TestFailedError('Fail the test')
    else
        puts("No loss found: Rx Frames ("+txStat+") = Tx Frames ("+rxStat+")")
    end
end
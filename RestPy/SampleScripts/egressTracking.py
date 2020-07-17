"""
DESCRIPTION
    Configures custom egress tracking on a receiving port.

    This sample shows how to create one ingress tracking and one egress tracking
    in the same custom egress statview tracking for VLAN ID.

    Tested with two Ixia ports connected back-2-back

    - Configure two VLAN/IPv4 Topology Groups
    - Start protocols
    - Create Traffic Item
    - Apply Traffic
    - Configures egress tracking for VLAN ID offset
    - Create egress tracking stat view
    - Start Traffic
    - Get stats

 To include an ingress tracking field:
    When you create your Traffic Item, you have the option to configure ingress trackings also.

 Available tracking filters for both ingress and egress...
 This script does a print with egressStatViewObj.AvailableTrackingFilter.find() to show the avialable tracking filters:
        ID: 1  VLAN:VLAN-ID (Ingress tracking)
        ID: 2  Flow Group  (Ingress tracking)
        ID: 3  Custom: (4 bits at offset 116)  <-- Egress tracking

 Sample egress stats:

 Row: 1
        Rx Port: 2/1
        VLAN:VLAN-ID: 103  <-- Ingress tracking the vlanID
        Egress Tracking: Custom: (4 bits at offset 116)
        Tx Frames: 100000
        Rx Frames: 100000
        Frames Delta: 0
        Loss %: 0
        Tx Frame Rate: 0
        Rx Frame Rate: 0
        Tx L1 Rate (bps): 0
        Rx L1 Rate (bps): 0
        Rx Bytes: 12800000
        Tx Rate (Bps): 0
        Rx Rate (Bps): 0
        Tx Rate (bps): 0
        Rx Rate (bps): 0
        Tx Rate (Kbps): 0
        Rx Rate (Kbps): 0
        Tx Rate (Mbps): 0
        Rx Rate (Mbps): 0
        Store-Forward Avg Latency (ns): 556418835
        Store-Forward Min Latency (ns): 9840
        Store-Forward Max Latency (ns): 1213352620
        First TimeStamp: 00:00:01.002
        Last TimeStamp: 00:00:02.510

Supports IxNetwork API servers:
   - Windows, Windows Connection Mgr and Linux

Requirements:
   - Minimum IxNetwork 8.50
   - Python 2.7 and 3+
   - pip install requests
   - pip install ixnetwork_restpy (minimum version 1.0.51)

RestPy Doc:
    https://www.openixia.github.io/ixnetwork_restpy

Usage:
   - Enter: python <script>

"""

import re, sys, os, time, traceback

# Import the RestPy module
from ixnetwork_restpy import SessionAssistant

# Egress tracking settings
egressTrackingPort='192.168.70.128/Card2/Port1'
offsetBits = 116
widthBits = 4
egressStatViewName = 'EgressStats'

# This is optional.
# Set to None if you don't want to include ingress tracking in the egress stat view that you're about to create for egress tracking.
#   - Initially, set to None since you don't know the filter name yet. In this example, VLAN:VLAN-ID. 
#   - Then run this script.
#   - On your terminal, you will see a list of tracking filter names like shown below:
#         ID: 1  VLAN:VLAN-ID  <-- For this example, going to track ingressing vlanID.
#         ID: 2  Flow Group
#         ID: 3  Custom: (4 bits at offset 116)  <-- This is your custom egress tracking filter name.
ingressTrackingFilterName = 'VLAN:VLAN-ID'
ingressTrackingFilterName = None

apiServerIp = '192.168.70.3'

ixChassisIpList = ['192.168.70.128']
portList = [[ixChassisIpList[0], 1, 1], [ixChassisIpList[0], 2, 1]]

# For Linux API server only
username = 'admin'
password = 'admin'

# For linux and connection_manager only. Set to True to leave the session alive for debugging.
debugMode = False

# Forcefully take port ownership if the portList are owned by other users.
forceTakePortOwnership = True


def configEgressCustomTracking(trafficItemObj, offsetBits, widthBits):
    """
    Description
       Configuring custom egress tracking and enable it. User must know the offset and the bits width to track.
       In most use cases, packets ingressing the DUT gets modified by the DUT and to track the
       correctness of the DUT's packet modification, use this API to verify the receiving port's packet
       offset and bit width.

    Parameter
        trafficItemObjList: <str obj>: traffic item objects to configure custom egress tracking
        offsetBits: <int>:
        widthBits: <int>:
    """
    # Safety check: Apply traffic or else configuring egress tracking won't work.
    ixNetwork.Traffic.Apply()

    tracking = trafficItemObj.Tracking.find()[0]
    tracking.Egress.Encapsulation = 'Any: Use Custom Settings'
    tracking.Egress.CustomOffsetBits = offsetBits
    tracking.Egress.CustomWidthBits = widthBits

    trafficItemObj.EgressEnabled = True
    trafficItemObj.Generate()
    ixNetwork.Traffic.Apply()


try:
    session = SessionAssistant(IpAddress=apiServerIp, RestPort=None, UserName='admin', Password='admin', 
                               SessionName=None, SessionId=None, ApiKey=None,  ClearConfig=True, LogLevel='all')

    ixNetwork = session.Ixnetwork

    # Assign ports
    portMap = session.PortMapAssistant()
    vport = dict()
    for index,port in enumerate(portList):
        portName = 'Port_{}'.format(index+1)
        vport[portName] = portMap.Map(IpAddress=port[0], CardId=port[1], PortId=port[2], Name=portName)

    portMap.Connect(forceTakePortOwnership)

    ixNetwork.info('Creating Topology Group 1')
    topology1 = ixNetwork.Topology.add(Name='Topo1', Ports=vport['Port_1'])
    deviceGroup1 = topology1.DeviceGroup.add(Name='DG1', Multiplier='1')
    ethernet1 = deviceGroup1.Ethernet.add(Name='Eth1')
    ethernet1.Mac.Increment(start_value='00:01:01:01:00:01', step_value='00:00:00:00:00:01')
    ethernet1.EnableVlans.Single(True)

    ixNetwork.info('Configuring vlanID')
    vlanObj = ethernet1.Vlan.find()[0].VlanId.Increment(start_value=103, step_value=0)

    ixNetwork.info('Configuring IPv4')
    ipv4 = ethernet1.Ipv4.add(Name='Ipv4')
    ipv4.Address.Increment(start_value='1.1.1.1', step_value='0.0.0.1')
    ipv4.GatewayIp.Increment(start_value='1.1.1.2', step_value='0.0.0.0')

    ixNetwork.info('Creating Topology Group 2')
    topology2 = ixNetwork.Topology.add(Name='Topo2', Ports=vport['Port_2'])
    deviceGroup2 = topology2.DeviceGroup.add(Name='DG2', Multiplier='1')

    ethernet2 = deviceGroup2.Ethernet.add(Name='Eth2')
    ethernet2.Mac.Increment(start_value='00:01:01:02:00:01', step_value='00:00:00:00:00:01')
    ethernet2.EnableVlans.Single(True)

    ixNetwork.info('Configuring vlanID')
    vlanObj = ethernet2.Vlan.find()[0].VlanId.Increment(start_value=103, step_value=0)

    ixNetwork.info('Configuring IPv4 2')
    ipv4 = ethernet2.Ipv4.add(Name='Ipv4-2')
    ipv4.Address.Increment(start_value='1.1.1.2', step_value='0.0.0.1')
    ipv4.GatewayIp.Increment(start_value='1.1.1.1', step_value='0.0.0.0')

    ixNetwork.StartAllProtocols(Arg1='sync')

    ixNetwork.info('Verify protocol sessions\n')
    protocolSummary = session.StatViewAssistant('Protocols Summary')
    protocolSummary.CheckCondition('Sessions Not Started', protocolSummary.EQUAL, 0)
    protocolSummary.CheckCondition('Sessions Down', protocolSummary.EQUAL, 0)
    ixNetwork.info(protocolSummary)

    ixNetwork.info('Create Traffic Item')
    trafficItemObj = ixNetwork.Traffic.TrafficItem.add(Name='BGP Traffic', BiDirectional=True, TrafficType='ipv4')

    ixNetwork.info('Add endpoint flow group')
    trafficItemObj.EndpointSet.add(Sources=topology1, Destinations=topology2)
    

    # Note: A Traffic Item could have multiple EndpointSets (Flow groups).
    #       Therefore, ConfigElement is a list.
    configElement = trafficItemObj.ConfigElement.find()[0]
    configElement.FrameRate.update(Type='percentLineRate', Rate=50)
    configElement.TransmissionControl.update(Type='fixedFrameCount', FrameCount=10000)
    configElement.FrameSize.FixedSize = 128
    trafficItemObj.Tracking.find()[0].TrackBy = ['flowGroup0', 'vlanVlanId0']

    # Configure egress tracking ...

    configEgressCustomTracking(trafficItemObj, offsetBits=offsetBits, widthBits=widthBits)

    egressTrackingOffsetFilter = 'Custom: ({0}bits at offset {1})'.format(int(widthBits), int(offsetBits))
    trafficItemName = trafficItemObj.Name

    # Create Egress Stats
    ixNetwork.info('\n\nCreating new statview for egress stats...')
    ixNetwork.Statistics.View.add(Caption=egressStatViewName, TreeViewNodeName='Egress Custom Views',
                                  Type='layer23TrafficFlow', Visible=True)

    egressStatViewObj = ixNetwork.Statistics.View.find(Caption=egressStatViewName)

    # Dynamically get the PortFilterId
    portFilterId = None
    for eachPortFilterId in egressStatViewObj.AvailablePortFilter.find():
        # 192.168.70.128/Card2/Port1

        ixNetwork.info('\n\nAvailable PortFilterId: %s\n' % eachPortFilterId.Name)
        # eachPortFilterId.Name: 192.168.70.128/Card2/Port1
        if eachPortFilterId.Name.strip() == egressTrackingPort:
            ixNetwork.info('\n\nLocated egressTrackingPort: {}\n'.format(egressTrackingPort))
            portFilterId = eachPortFilterId
            break

    if portFilterId == None:
        ixNetwork.debug('\n\nNo port filter ID found\n')

    ixNetwork.info('\n\nPortFilterId: {}'.format(portFilterId))

    # Dynamically get the Traffic Item Filter ID
    availableTrafficItemFilterId = []
    for eachTrafficItemFilterId in egressStatViewObj.AvailableTrafficItemFilter.find():
        if eachTrafficItemFilterId.Name == trafficItemName:
            availableTrafficItemFilterId.append(eachTrafficItemFilterId.href)

    if availableTrafficItemFilterId == []:
        ixNetwork.debug('No traffic item filter ID found.')

    ixNetwork.info('\n\navailableTrafficItemFilterId: {}\n'.format(availableTrafficItemFilterId))

    # # /api/v1/sessions/1/ixnetwork/statistics/view/12
    layer23TrafficFlowFilter = egressStatViewObj.Layer23TrafficFlowFilter.find()[0]
    layer23TrafficFlowFilter.EgressLatencyBinDisplayOption = 'showEgressRows'
    layer23TrafficFlowFilter.PortFilterIds = portFilterId
    layer23TrafficFlowFilter.TrafficItemFilterId = availableTrafficItemFilterId[0]
    layer23TrafficFlowFilter.TrafficItemFilterIds = availableTrafficItemFilterId

    # Get the egress tracking filter
    egressTrackingFilter = None
    ingressTrackingFilter = None

    # Show all the avaialable filter names/options
    for eachTrackingFilter in egressStatViewObj.AvailableTrackingFilter.find():
        ixNetwork.info('\n\nAvailable filter Name: {0}\n'.format(eachTrackingFilter.Name))

        # Name: Custom: (4 bits at offset 116)
        # TrackingType: kEgress
        # ValueType:  VLAN:VLAN-ID
        if bool(re.match('Custom:.*[0-9]+ *bits at offset *[0-9]+', eachTrackingFilter.Name)):
            egressTrackingFilter = eachTrackingFilter.href

        if ingressTrackingFilterName is not None:
            if eachTrackingFilter.Name == ingressTrackingFilterName:
                ingressTrackingFilter = eachTrackingFilter.href

    if egressTrackingFilter is None:
        ixNetwork.debug('Failed to locate your defined custom offsets: {0}'.format(egressTrackingOffsetFilter))

    # # /api/v1/sessions/1/ixnetwork/statistics/view/23/availableTrackingFilter/3
    ixNetwork.info('Located egressTrackingFilter: %s' % egressTrackingFilter)
    # egressTrackingFilter: /api/v1/sessions/1/ixnetwork/statistics/view/12/availableTrackingFilter/1
    layer23TrafficFlowFilter.EnumerationFilter.add(SortDirection='ascending', TrackingFilterId=egressTrackingFilter)

    # This will include ingress tracking in the egress statview.
    if ingressTrackingFilterName is not None:
        layer23TrafficFlowFilter.EnumerationFilter.add(SortDirection='ascending', TrackingFilterId=ingressTrackingFilter)

    for eachEgressStatCounter in egressStatViewObj.Statistic.find():
        eachStatCounterName = eachEgressStatCounter.Caption
        ixNetwork.info('Enabling egress stat counter: {}'.format(eachStatCounterName))
        eachEgressStatCounter.Enabled = True

    egressStatViewObj.Enabled = True

    ixNetwork.Traffic.StartStatelessTrafficBlocking()

    flowStatistics = session.StatViewAssistant(egressStatViewName)

    # StatViewAssistant could also filter by REGEX, LESS_THAN, GREATER_THAN, EQUAL. 
    # Examples:
    #    flowStatistics.AddRowFilter('Port Name', flowStatistics.REGEX, '^Port 1$')
    #    flowStatistics.AddRowFilter('Tx Frames', flowStatistics.LESS_THAN, 50000)

    ixNetwork.info('\n\n{}\n'.format(flowStatistics))

    if debugMode == False:
        # For linux and connection_manager only
        session.Session.remove()

except Exception as errMsg:
    print('\n%s' % traceback.format_exc(None, errMsg))
    if debugMode == False and 'session' in locals():
        session.Session.remove()

    

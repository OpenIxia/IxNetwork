"""
bgpNgpf.py:

   Tested with two back-2-back Ixia ports

   - Connect to the API server
   - Configure license server IP
   - Assign ports:
        - If variable forceTakePortOwnership is True, take over the ports if they're owned by another user.
        - If variable forceTakePortOwnership if False, abort test.
   - Configure two Topology Groups: IPv4/BGP
   - Configure Network Group for each topology for route advertising
   - Configure a Traffic Item
   - Start all protocols
   - Verify all protocols
   - Start traffic
   - Get Traffic Item
   - Get Flow Statistics stats

Supports IxNetwork API servers:
   - Windows, Windows Connection Mgr and Linux

Requirements:
   - IxNetwork 8.50
   - Python 2.7 and 3+
   - pip install requests
   - pip install -U --no-cache-dir ixnetwork_restpy
   - https://github.com/OpenIxia/IxNetwork/RestApi/Python/Restpy/Modules:
         - Statistics.py and PortMgmt.py

Script development API doc:
   - The doc is located in your Python installation site-packages/ixnetwork_restpy/docs/index.html
   - On a web browser:
         - If installed in Windows: enter: file://c:/<path_to_ixnetwork_restpy>/docs/index.html
         - If installed in Linux: enter: file:///<path_to_ixnetwork_restpy>/docs/index.html

Usage:
   # Defaults to Windows
   - Enter: python <script>

   # Connect to Windows Connection Manager
   - Enter: python <script> windowsConnectionMgr

   # Connect to Linux API server
   - Enter: python <script> linux
"""

from __future__ import absolute_import, print_function
import sys, os

# Adding some paths if you are not installing RestPy by Pip.
#sys.path.append(os.path.dirname(os.path.abspath(__file__).replace('SampleScripts', '')))
sys.path.append(os.path.dirname(os.path.abspath(__file__).replace('SampleScripts', 'Modules')))

# Import the main client module
from ixnetwork_restpy.testplatform.testplatform import TestPlatform


# Import modules containing helper functions
from StatisticsMgmt import Statistics
from PortMgmt import Ports

# Defaulting to windows
osPlatform = 'windows'

if len(sys.argv) > 1:
    # Command line input: windows, windowsConnectionMgr or linux
    osPlatform = sys.argv[1]

# Change API server values to use your setup
if osPlatform in ['windows', 'windowsConnectionMgr']:
    platform = 'windows'
    apiServerIp = '192.168.70.3'
    apiServerPort = 11009

# Change API server values to use your setup
if osPlatform == 'linux':
    platform = 'linux'
    apiServerIp = '192.168.70.12'
    apiServerPort = 443
    username = 'admin'
    password = 'admin'

# The IP address for your Ixia license server(s) in a list.
licenseServerIp = ['192.168.70.3']
# subscription, perpetual or mixed
licenseMode = 'subscription'

# For linux and windowsConnectionMgr only. Set to False to leave the session alive for debugging.
deleteSessionWhenDone = True

# Forcefully take port ownership if the portList are owned by other users.
forceTakePortOwnership = True

portList = [['192.168.70.128', 1, 1], ['192.168.70.128', 1, 2]]

try:
    testPlatform = TestPlatform(ip_address=apiServerIp, rest_port=apiServerPort, platform=platform, log_file_name='restpy.log')

    # Console output verbosity: None|request|'request response'
    testPlatform.Trace = 'request_response'

    if osPlatform == 'linux':
        testPlatform.Authenticate(username, password)

    session = testPlatform.Sessions.add()
    ixNetwork = session.Ixnetwork

    # Instantiate some helper class objects
    statObj = Statistics(ixNetwork)
    portObj = Ports(ixNetwork)

    if osPlatform == 'windows':
        ixNetwork.NewConfig()

    print('\nConfiguring license server')
    ixNetwork.Globals.Licensing.LicensingServers = licenseServerIp
    ixNetwork.Globals.Licensing.Mode = licenseMode

    # Create vports and name them so you could get the vports by the name when creating Topology.
    vport1 = ixNetwork.Vport.add(Name='Port1')
    vport2 = ixNetwork.Vport.add(Name='Port2')

    # getVportList=True because you already created vports.
    # If you did not create vports, then assignPorts will create them and name them with default names.
    portObj.assignPorts(portList, forceTakePortOwnership, getVportList=True)

    print('\nCreating Topology Group 1')
    topology1 = ixNetwork.Topology.add(Name='Topo1', Ports=vport1)
    deviceGroup1 = topology1.DeviceGroup.add(Name='DG1', Multiplier='1')
    ethernet1 = deviceGroup1.Ethernet.add(Name='Eth1')
    ethernet1.Mac.Increment(start_value='00:01:01:01:00:01', step_value='00:00:00:00:00:01')
    ethernet1.EnableVlans.Single(True)

    print('\nConfiguring vlanID')
    vlanObj = ethernet1.Vlan.find()[0].VlanId.Increment(start_value=103, step_value=0)

    print('\tConfiguring IPv4')
    ipv4 = ethernet1.Ipv4.add(Name='Ipv4')
    ipv4.Address.Increment(start_value='1.1.1.1', step_value='0.0.0.1')
    ipv4.GatewayIp.Increment(start_value='1.1.1.2', step_value='0.0.0.0')

    print('\tConfiguring BgpIpv4Peer 1')
    bgp1 = ipv4.BgpIpv4Peer.add(Name='Bgp1')
    bgp1.DutIp.Increment(start_value='1.1.1.2', step_value='0.0.0.0')
    bgp1.Type.Single('internal')
    bgp1.LocalAs2Bytes.Increment(start_value=101, step_value=0)

    print('\tConfiguring Network Group 1')
    networkGroup1 = deviceGroup1.NetworkGroup.add(Name='BGP-Routes1', Multiplier='100')
    ipv4PrefixPool = networkGroup1.Ipv4PrefixPools.add(NumberOfAddresses='1')
    ipv4PrefixPool.NetworkAddress.Increment(start_value='10.10.0.1', step_value='0.0.0.1')
    ipv4PrefixPool.PrefixLength.Single(32)

    print('\nCreating Topology Group 2')
    topology2 = ixNetwork.Topology.add(Name='Topo2', Ports=vport2)
    deviceGroup2 = topology2.DeviceGroup.add(Name='DG2', Multiplier='1')

    ethernet2 = deviceGroup2.Ethernet.add(Name='Eth2')
    ethernet2.Mac.Increment(start_value='00:01:01:02:00:01', step_value='00:00:00:00:00:01')
    ethernet2.EnableVlans.Single(True)

    print('\tConfiguring vlanID')
    vlanObj = ethernet2.Vlan.find()[0].VlanId.Increment(start_value=103, step_value=0)

    print('\tConfiguring IPv4 2')
    ipv4 = ethernet2.Ipv4.add(Name='Ipv4-2')
    ipv4.Address.Increment(start_value='1.1.1.2', step_value='0.0.0.1')
    ipv4.GatewayIp.Increment(start_value='1.1.1.1', step_value='0.0.0.0')

    print('\tConfiguring BgpIpv4Peer 2')
    bgp2 = ipv4.BgpIpv4Peer.add(Name='Bgp2')
    bgp2.DutIp.Increment(start_value='1.1.1.1', step_value='0.0.0.0')
    bgp2.Type.Single('internal')
    bgp2.LocalAs2Bytes.Increment(start_value=101, step_value=0)

    print('\tConfiguring Network Group 2')
    networkGroup2 = deviceGroup2.NetworkGroup.add(Name='BGP-Routes2', Multiplier='100')
    ipv4PrefixPool = networkGroup2.Ipv4PrefixPools.add(NumberOfAddresses='1')
    ipv4PrefixPool.NetworkAddress.Increment(start_value='20.20.0.1', step_value='0.0.0.1')
    ipv4PrefixPool.PrefixLength.Single(32)

    ixNetwork.StartAllProtocols(Arg1='sync')
    statObj.verifyAllProtocolSessions()

    print('\nCreate Traffic Item')
    trafficItem = ixNetwork.Traffic.TrafficItem.add(Name='BGP Traffic', BiDirectional=False, TrafficType='ipv4')

    print('\tAdd endpoint flow group')
    trafficItem.EndpointSet.add(Sources=topology1, Destinations=topology2)

    # Note: A Traffic Item could have multiple EndpointSets (Flow groups).
    #       Therefore, ConfigElement is a list.
    print('\tConfiguring config elements')
    trafficItem.ConfigElement.find()[0].FrameRate.Rate = 28
    trafficItem.ConfigElement.find()[0].FrameRate.Type = 'framesPerSecond'
    trafficItem.ConfigElement.find()[0].TransmissionControl.FrameCount = 10000
    trafficItem.ConfigElement.find()[0].TransmissionControl.Type = 'fixedFrameCount'
    trafficItem.ConfigElement.find()[0].FrameRateDistribution.PortDistribution = 'splitRateEvenly'
    trafficItem.ConfigElement.find()[0].FrameSize.FixedSize = 128
    trafficItem.Tracking.find()[0].TrackBy = ['flowGroup0']

    trafficItem.Generate()
    ixNetwork.Traffic.Apply()
    ixNetwork.Traffic.Start()

    # Get the Traffic Item name for getting Traffic Item statistics.
    trafficItemName = trafficItem.Name

    # Get and show the Traffic Item column caption names and stat values
    columnNames      = statObj.getStatViewResults(statViewName='Traffic Item Statistics', getColumnCaptions=True)
    trafficItemStats = statObj.getStatViewResults(statViewName='Traffic Item Statistics', rowValuesLabel=trafficItemName)
    txFramesIndex = columnNames.index('Tx Frames')
    rxFramesIndex = columnNames.index('Rx Frames')
    print('\nTraffic Item Stats:\n\tTxFrames: {0}  RxFrames: {1}\n'.format(trafficItemStats[txFramesIndex],
                                                                         trafficItemStats[rxFramesIndex]))

    # Get and show the Flow Statistics column caption names and stat values
    columnNamess =   statObj.getStatViewResults(statViewName='Flow Statistics', getColumnCaptions=True)
    flowStats = statObj.getFlowStatistics()
    print('\n', columnNamess)
    for statValues in flowStats:
        print('\n{0}'.format(statValues))
    print()

    if deleteSessionWhenDone:
        # For Linux and WindowsConnectionMgr only
        if osPlatform in ['linux', 'windowsConnectionMgr']:
            session.remove()

except Exception as errMsg:
    print('\nrestPy.Exception:', errMsg)
    if deleteSessionWhenDone and 'session' in locals():
        if osPlatform in ['linux', 'windowsConnectionMgr']:
            session.remove()





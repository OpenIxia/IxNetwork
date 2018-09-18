"""
loadJsonConfigFile.py:

   Tested with two back-2-back Ixia ports

   - Connect to the API server
   - Configure license server IP
   - Loads a saved .json config file that is in the same local directory: bgp.json
   - Configure license server IP
   - Optional: Assign ports or use the ports that are in the saved config file.
   - Demonstrate how to use XPATH to modify any part of the configuration.
   - Start all protocols
   - Verify all protocols
   - Start traffic 
   - Get Traffic Item
   - Get Flow Statistics stats

Supports IxNetwork API servers:
   - Windows, Windows Connection Mgr and Linux

Requirements
   - IxNetwork 8.50
   - Python 2.7 and 3+
   - pip install requests
   - pip install -U --no-cache-dir ixnetwork_restpy
   - https://github.com/OpenIxia/IxNetwork/RestApi/Python/Restpy/Modules:
         - Statistics.py and PortMgmt.py 

Script development API doc:
   - The doc is located in your Python installation site-packages/ixnetwork_restpy/index.html
   - On a web browser, enter: file:///<full_path_to_ixnetwork_restpy>/index.html
"""

from __future__ import absolute_import, print_function
import json, sys

# Import the main client module
from ixnetwork_restpy.testplatform.testplatform import TestPlatform
from ixnetwork_restpy.files import Files

# Import modules containing helper functions
sys.path.insert(0, (os.path.dirname(os.path.abspath(__file__).replace('SampleScripts', 'Modules'))))
from StatisticsMgmt import Statistics
from PortMgmt import Ports

if len(sys.argv) > 1:
    # Command line input: windows or linux
    osPlatform = sys.argv[1]
else:
    # Defaulting to windows
    osPlatform = 'windows'

# Are you using IxNetwork Connection Manager in a Windows server 2012/2016?
isWindowsConnectionMgr = False

# Change API server values to use your setup
if osPlatform == 'windows':
    apiServerIp = '192.168.70.3'
    apiServerPort = 11009

# Change API server values to use your setup
if osPlatform == 'linux':
    print('\n---- it is linux ----')
    apiServerIp = '192.168.70.121'
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

# A list of chassis to use
ixChassisIpList = ['192.168.70.120']
portList = [[ixChassisIpList[0], 1, 1], [ixChassisIpList[0], 1, 2]]

jsonConfigFile = 'bgp.json'

try:
    #testPlatform = TestPlatform(apiServerIp, rest_port=apiServerPort, platform=osPlatform)
    testPlatform = TestPlatform(apiServerIp, platform=osPlatform)

    # Console output verbosity: None|request|request_response
    testPlatform.Trace = 'request_response'

    if osPlatform == 'linux':
        testPlatform.Authenticate(username, password)

    if isWindowsConnectionMgr or osPlatform == 'linux':
        print('\n--- adding new session --')
        session = testPlatform.Sessions.add()
        sys.exit()
        session = testPlatform.Sessions.find()

        print('\n--- session:', session)
        #print('\n--- session find:', session.find())

    if osPlatform == 'windows':
        session = testPlatform.Sessions.find(Id=1)


    # ixNetwork is the root object to the IxNetwork API hierarchical tree.
    ixNetwork = session.Ixnetwork

    # Instantiate the helper class objects
    statObj = Statistics(ixNetwork)
    portObj = Ports(ixNetwork)

    print('\nConfiguring license server')
    # Must set the license server IP before loading the config file so ports could boot successfully.
    if forceTakePortOwnership == True:
        # To configure the license server IP, must release the ports first.
        portObj.releasePorts(portList)
        ixNetwork.Globals.Licensing.LicensingServers = licenseServerIp
        ixNetwork.Globals.Licensing.Mode = licenseMode

    print('\nLoading JSON config file: {0}'.format(jsonConfigFile))
    ixNetwork.ResourceManager.ImportConfigFile(Files(jsonConfigFile, local_file=True), Arg3=True)

    # Assigning ports after loading a saved config is optional because you could use the ports that
    # are saved in the config file. Optionally, reassign ports to use other chassis/ports on different testbeds.
    portObj.assignPorts(portList, getVportList=True)

    # Example: How to modify a loaded json config using XPATH
    data = json.dumps([{"xpath": "/traffic/trafficItem[1]", "name": 'Modified Traffic'}])
    ixNetwork.ResourceManager.ImportConfig(Arg2=data, Arg3=False)

    ixNetwork.StartAllProtocols(Arg1='sync')
    statObj.verifyAllProtocolSessions()

    # Get the Traffic Item name for getting Traffic Item statistics.
    trafficItem = ixNetwork.Traffic.TrafficItem.find()[0]
    trafficItemName = trafficItem.Name

    trafficItem.Generate()
    ixNetwork.Traffic.Apply()
    ixNetwork.Traffic.Start()

    # Get and show the Traffic Item column caption names and stat values
    columnCaptions =   statObj.getStatViewResults(statViewName='Traffic Item Statistics', getColumnCaptions=True)
    trafficItemStats = statObj.getStatViewResults(statViewName='Traffic Item Statistics', rowValuesLabel=trafficItemName)
    txFramesIndex = columnCaptions.index('Tx Frames')
    rxFramesIndex = columnCaptions.index('Rx Frames')
    print('\nTraffic Item Stats:\n\tTxFrames: {0}  RxFrames: {1}'.format(trafficItemStats[txFramesIndex],
                                                                         trafficItemStats[rxFramesIndex]))
    
    # Get and show the Flow Statistics column caption names and stat values
    columnCaptions =   statObj.getStatViewResults(statViewName='Flow Statistics', getColumnCaptions=True)
    flowStats = statObj.getFlowStatistics()
    print('\n', columnCaptions)
    for statValues in flowStats:
        print('\n{0}'.format(statValues))
    print()

    if deleteSessionWhenDone:
        # For Linux and WindowsConnectionMgr only
        if osPlatform == 'linux' or isWindowsConnectionMgr:
            session.remove()

except Exception as errMsg:
    print('\nrestPy.Exception:', errMsg)
    if deleteSessionWhenDone and 'session' in locals():
        if osPlatform == 'linux' or isWindowsConnectionMgr:
            session.remove()





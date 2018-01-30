
# PLEASE READ DISCLAIMER
#
#    This is a sample script for demo and reference purpose only.
#    It is subject to change for content updates without warning.
#
# REQUIREMENTS
#    - Python2.7/3.4
#    - Python modules: requests, paramiko
#    - IxNetRestApi.py
#
# DESCRIPTION
#    This sample script demonstrates:
#        - REST API configurations using two back-to-back Ixia ports.
#        - Connecting to Windows IxNetwork API server or Linux API server.
#
#        - Verify for sufficient amount of port licenses before testing.
#        - Verify port ownership.
#        - Configure two IPv4/BGP Topology Groups
#        - Start protocols
#        - Verify BGP protocol sessions
#        - Create a Traffic Item
#        - Apply Traffic
#        - Start Traffic
#        - Get stats
#
# USAGE
#    python <script>.py windows
#    python <script>.py linux
#
# TODO: help command usage when entering command + help
#       Call IxNetRestAPI directory
#       Add loading json config
#       showtopologies to include protocol sessions up/down

from __future__ import absolute_import, print_function, division
import sys, inspect, traceback, readline, platform
from collections import OrderedDict
sys.path.append('/home/hgee/Dropbox/MyIxiaWork/Rest/classObj')
from IxNetRestApi import *

# Default the API server to either windows or linux.
class middleware:
    #jsonConfigFile = '/home/hgee/Dropbox/MyIxiaWork/Rest/classObj/ShellMode/bgpConfig.json'
    apiServerType = None ;# Use connecttolinux() or connecttowindows() to set this.
    windowsApiServerIp = None
    windowsApiServerIpPort = 11009
    linuxApiServerIp = None
    linuxApiServerIpPort = 443
    username = 'admin'
    password = 'admin'
    licenseServerIp = ['192.168.70.127']
    licenseMode = 'subscription'
    licenseTier = 'tier3'
    forceTakePortOwnership = True
    deleteSessionAfterTest = True ;# For Linux only
    enableDebugTracing = False ;# Display error tracebacks

    # Internal variables.  Don't touch below variables.
    resume = False
    #nameObj = {}
    apiKey = None
    sessionId = None
    #trafficItemObjList = []
    linuxServerSessionId = None
    ixn = None

try:
    def help(command=None, showall=None):
        """Show all the API commands.

        param: showall: (None|showall): Enter "showall" to include the descriptions."""
        # pydoc.help(ixnetPyCli)
        if command == None:
            print('\nCommand list:\n')
        else:
            print('\tHelp on command usage: {0}'.format(command))

        for name,obj in inspect.getmembers(sys.modules[__name__]):
            #if inspect.isfunction(obj) and eval(name+'.__doc__') is not None:
            if inspect.isfunction(obj):
                parameters = inspect.getargspec(eval(name))
         
                if parameters[0] == []:
                    parameters = ''
                    if command is None:
                        print('\t{0}({1})'.format(name, parameters))
                else:
                    parameters = ' '.join(parameters[0][0:])
                    if command != None and name == command:
                        print('\n\t{0}({1})'.format(name, parameters))
                    if command == None:
                        print('\t{0} ({1})'.format(name, parameters))
                #print('\t{0}({1})'.format(name, parameters))
                if showall is not None:
                    print('\t{0}'.format(eval(name+'.__doc__')))
                    print()
        print()

        if command == None:
            print('\n\n  Example:')
            print('\t1> connect("bgpConfig.json")')
            print('\t2> configbgp()')
            print('\t3> starttraffic()')
            print('\t4> getstats()')
            print()

    def showpreferences():
        """Show all user defined preferences"""
        print()
        for property,value in middleware.__dict__.items():
            if property.startswith('_') and not callable(property): continue
            print('\t{0}: {1}'.format(property, value))
        print()

    def showconnecttoapiserver():
        """Show the type of the API server that is currently connecting to.
        Example: windows|windowsConnectionMgr|linux"""
        print('\n{0}'.format(middleware.apiServerType))

    def deletelinuxsession():
        """Delete the current session ID on the Linux API server.
        This command is only for connecting to the Linux API server."""
        middleware.ixn.linuxServerStopOperations(middleware.linuxServerSessionId)
        middleware.ixn.linuxServerDeleteSession(middleware.linuxServerSessionId)

    def connect(apiServerIp=None, apiServerIpPort=None, apiServerType=None, resume=False, 
                apiKey=None, sessionId=None, username='admin', password='admin', deleteSessionAfterTest=True):
        """Connect to an API server with a user defined JSON config file.
        You could use this API to change the API server IP that is different
        from the JSON config file. 

        param: apiServerType: windows|linux.
        param: resume: (True|False): To connect to an existing configuration.
                       If apiServerType is Linux, provide the apiServerIpAddress, apiServerIpPort, apiKey and sessionId number.
                       If apiServerType is windows, provide the apiServerIpAddress and apiServerIpPort.
        param: apiServerIp: (str): The IP address of the IxNetwork API server to connect to.
        param: apiServerIpPort: (int): The API server IP port number to use.
                        Windows default port = 11009.
                        Linux default port = 443. 
        param: apiKey: (str): For Linux API server only. The API-KEY of the Linux API server.
                        You could get this in the Web UI, under My Account, and in show API-KEY.
        param: sessionID: (int): For Linux API server only. The existing session ID to connect to.
        param: username: For Linux API serer only. The login username.
        param: password: For Linux API server only. The login password.

        Usage: To make a new Windows connection: apiServerType='windows', apiServerIp=<ip>, apiServerIpPort=<ipPort>
        Usage: To make a new Linux connection: apiServerType='linux', apiServerIp=<ip>, apiSeverIpPort=<ipPort>
        Usage: To resume on Linux: resume=True, apiKey=<apiKey>, sessionId=<session ID>,
        Usage: To resume on Windows with currently connected apiServerIp: resume=True, apiServerIp=<apiServerIp>
        Usage: To resume on Windows with a different apiServerIp: resume='windows', apiServerIp=<apiServerIp>, apiServerIpPort=<apiSeverIpPort>
        Usage: To resume on WindowConnectionMgr = Not supported yet."""

        if middleware.apiServerType == None and apiServerType == None:
            print('\nError: Use connecttowindows() or connecttolinux() to set the type of server first.\n')
            return

        if middleware.apiServerType == None and apiServerType != None:
            middleware.apiServerType = apiServerType

        if resume == True:
            middleware.resume = True
            if (apiKey is None and sessionId is None) or \
                (apiKey is None and sessionId is not None) or \
                (apiKey is not None and sessionId is None):
                    print('\nError: To resume on Linux API server, you must provide both apiKey and sessionId.\n')
                    return
        
        if resume == False:

            
            # Check to see if resuming on Windows
            if middleware.apiServerType == 'windows':
                if apiServerIp == None and middleware.windowsApiServerIp == None:
                    print('\nError: You must include apiServerIp\n') ;# return
                if apiServerIpPort == None and middleware.windowsApiServerIpPort == None:
                    print('\nError: You must include apiServerIpPort\n') ;# return

                if apiServerIp != None:            
                    middleware.windowsApiServerIp = apiServerIp
                if apiServerIpPort != None:
                    middleware.windowsApiServerIpPort = apiServerIpPort

            if middleware.apiServerType == 'linux':
                if apiServerIp == None and middleware.linuxApiServerIp == None:
                    print('\nError: You must include the apiServerIp\n') ;# return
                if apiServerIp == None and middleware.linuxApiServerIp == None:
                    print('\nError: You must include the apiServerIp\n') ;# return

                if apiServerIp != None:           
                    middleware.linuxApiServerIp = apiServerIp
                if apiServerIpPort != None:
                    middleware.linuxApiServerIpPort = apiServerIpPort

            # if apiKey and sessionId: 
            #     middleware.linuxApiServerIp = apiServerIp
            #     middleware.linuxApiServerIpPort = apiServerIpPort
            #     middleware.username = username
            #     middleware.password = password

        if middleware.apiServerType == 'windows':
            ixn = IxNetRestMain(apiServerIp=middleware.windowsApiServerIp,
                                serverIpPort=middleware.windowsApiServerIpPort,
                                serverOs='windows')

        if middleware.apiServerType == 'linux':
            ixn = IxNetRestMain(apiServerIp=middleware.linuxApiServerIp,
                                serverIpPort=str(middleware.linuxApiServerIpPort),
                                username=middleware.username,
                                password=middleware.password,
                                deleteSessionAfterTest=deleteSessionAfterTest,
                                serverOs='linux',
                                apiKey=apiKey,
                                sessionId=str(sessionId))

            # Record the current apiKey and sessionId
            middleware.apiKey = ixn.apiKey
            middleware.linuxServerSessionId = ixn.sessionId

        middleware.ixn = ixn

    # This is not the json import/export feature.
    def readjsonparamfile(jsonConfigFile):
        """Read and Load a JSON parameters file.

        Param: jsonConfigFile: The JSON config file to load."""
        if os.path.exists(jsonConfigFile) is False:
            raise IxNetRestApiException("JSON file doesn't exists: %s" % jsonConfigFile)
        middleware.params = json.load(open(jsonConfigFile), object_pairs_hook=OrderedDict)

    def runjsonconfig(jsonConfigFile, chassisIp=None, portList=None, licenseServerIp=None, licenseMode=None, licenseTier=None):
        """Load a saved JSON config file.

        param: jsonConfigFile: The IxNetwork saved configuration in JSON format.
        param: chassisIp: Ixia chassis IP address.
        param: portList: All the ports to use for this JSON configuration file. The amount of ports must match the 
                         amount of configured ports in the JSON config file.
                         Example:     portList = [[ixChassisIp, '1', '1'], [ixChassisIp, '2', '1']]
        param: licenseServerIp: The license server IP address.
        param: licenseMode: mixed|subscription|perpetual
        param: licenseTier: tier1, tier2, tier3""" 
        #middleware.loadJsonConfig = True
        if licenseServerIp:
            middleware.licenseServerIp = [licenseServerIp]
        if licenseMode:
            middleware.licenseMode = licenseMode
        if licenseTier:
            middleware.licenseTier = licenseTier

        jsonData = middleware.ixn.jsonReadConfig(jsonConfigFile)
        if portList != None:
            middleware.ixn.jsonAssignPorts(jsonData, portList)  

        if chassisIp is not None:
            chassisIp = jsonData['availableHardware']['chassis'][0]['hostname']

        # Need to support multiple chassis's.  If user passed in a string of chassis, convert it to a list.
        if chassisIp is not list:
            chassisIp = chassisIp.split(' ')
        for eachChassisIp in chassisIp:
            middleware.ixn.connectIxChassis(eachChassisIp)

        if middleware.ixn.arePortsAvailable(portList, raiseException=False) != 0:
            if middleware.forceTakePortOwnership == True:
                middleware.ixn.releasePorts(portList)
                middleware.ixn.clearPortOwnership(portList)
            else:
                raise IxNetRestApiException('Ports are owned by another user and forceTakePortOwnership is set to False')

        # Configuring license requires releasing all ports even for ports that is not used for this test.
        middleware.ixn.releaseAllPorts()
        middleware.ixn.configLicenseServerDetails(middleware.licenseServerIp, middleware.licenseMode, middleware.licenseTier)
        middleware.ixn.importJsonConfig(jsonData, type='newConfig')
        middleware.ixn.verifyPortState()
        middleware.ixn.startAllProtocols()
        middleware.ixn.verifyAllProtocolSessionsNgpf(timeout=120)
        middleware.ixn.regenerateTrafficItems()
        middleware.ixn.applyTraffic()
        middleware.ixn.startTraffic()
        middleware.ixn.getStats()

    def runixncfgconfig(ixncfgConfigFile, portList=None):
        """Load a saved ixncfg config file.

        param: ixncfgConfigFile: The IxNetwork saved configuration in ixncfg format.
        param: portList: The list of list containing [[ixChassisIp, 1, 1], [ixChassisIp, 1, 2]]
        """
        middleware.loadIxncfgConfig = True
        restObj.loadConfigFile(configFile)
        if portList != None:
            restObj.assignPorts(portList)
        middleware.ixn.verifyPortState()
        middleware.ixn.startAllProtocols()
        middleware.ixn.verifyAllProtocolSessionsNgpf(timeout=120)
        middleware.ixn.regenerateTrafficItems()
        middleware.ixn.applyTraffic()
        middleware.ixn.startTraffic()
        middleware.ixn.getStats()

    def connecttolinux():
        """Set connection to a Linux API server."""
        middleware.apiServerType = 'linux'

    def connecttowindows():
        """Set connection to a Windows API server."""
        middleware.apiServerType = 'windows'

    def showlinuxsession():
        print('\nAPI-KEY: {0}'.format(middleware.ixn.apiKey))
        print('Session ID: {0}'.format(middleware.ixn.sessionId.split('/')[-1]))
        print()

    def stoptopology(topologyName):
        """Stop a running Topology Group and all of its protocol stacks.

        param: topologyName: (int): The Topology Group name."""

        queryData = {'from': '/',
                    'nodes': [{'node': 'topology',    'properties': ['name'], 'where': [{'property': 'name', 'regex': topologyName}]}]
                    }
        queryResponse = middleware.ixn.query(data=queryData)
        try:
            topologyObj = queryResponse.json()['result'][0]['topology'][0]['href']
        except:
            print('\nError: Verify the topologyName', topologyName)
        middleware.ixn.stopTopology([topologyObj])

    def starttopology(topologyName):
        """Start a Topology Group and all of its protocol stacks.

        param: topologyName: (int): The Topology Group name."""

        queryData = {'from': '/',
                    'nodes': [{'node': 'topology',    'properties': ['name'], 'where': [{'property': 'name', 'regex': topologyName}]}]
                    }
        queryResponse = middleware.ixn.query(data=queryData)
        try:
            topologyObj = queryResponse.json()['result'][0]['topology'][0]['href']
        except:
            print('\nError: Verify the topologyName', topologyName)
        middleware.ixn.startTopology([topologyObj])
        middleware.ixn.verifyProtocolSessionsNgpf()

    def startbgp(topologyName, protocolName):
        """Start BGP protocol.

        param: topologyName: The Topology Group name.
        param: protocolName: The protocol stack name for the Topology Group. Not the protocol name."""
        # Query for the protocol obj and topology group obj by the protocolName
        queryData = {'from': '/',
                    'nodes': [{'node': 'topology',    'properties': ['name'], 'where': [{'property': 'name', 'regex': topologyName}]},
                              {'node': 'deviceGroup', 'properties': [], 'where': []},
                              {'node': 'ethernet',    'properties': [], 'where': []},
                              {'node': 'ipv4',        'properties': [], 'where': []},
                              {'node': 'bgpIpv4Peer', 'properties': ['name'], 'where': [{'property': 'name', 'regex': protocolName}]}
                            ]
                    }
        queryResponse = middleware.ixn.query(data=queryData)
        try:
            protocolObj = queryResponse.json()['result'][0]['topology'][0]['deviceGroup'][0]['ethernet'][0]['ipv4'][0]['bgpIpv4Peer'][0]['href']
        except IndexError:
            print('\nError: Verify the protocolName', protocolName)

        middleware.ixn.startProtocol(protocolObj)
        middleware.ixn.verifyProtocolSessionsNgpf()

    def stopbgp(topologyName, protocolName):
        """Stop BGP protocol.

        param: topologyName: The Topology Group name.
        param: protocolName: The protocol stack name for the Topology Group. Not the protocol name."""
        # Query for the protocol obj and topology group obj by the protocolName
        queryData = {'from': '/',
                    'nodes': [{'node': 'topology',    'properties': ['name'], 'where': [{'property': 'name', 'regex': topologyName}]},
                              {'node': 'deviceGroup', 'properties': [], 'where': []},
                              {'node': 'ethernet',    'properties': [], 'where': []},
                              {'node': 'ipv4',        'properties': [], 'where': []},
                              {'node': 'bgpIpv4Peer', 'properties': ['name'], 'where': [{'property': 'name', 'regex': protocolName}]}
                            ]
                    }
        queryResponse = middleware.ixn.query(data=queryData)
        try:
            protocolObj = queryResponse.json()['result'][0]['topology'][0]['deviceGroup'][0]['ethernet'][0]['ipv4'][0]['bgpIpv4Peer'][0]['href']
        except IndexError:
            raise IxNetRestApiException('\nError: Verify the protocolName', protocolName)

        middleware.ixn.stopProtocol(protocolObj)

    def disabletrafficitem(trafficItemName):
        """Disable a Traffic Item by its number.

        param: trafficItemNumber: (int): The number of the Traffic Item to disable."""
        middleware.ixn.disableTrafficItemByName(trafficItemName)

    def enabletrafficitem(trafficItemName):
        """Enable a Traffic Item by its number.

        param: trafficItemNumber: (int): The number of the Traffic Item to enable."""
        middleware.ixn.enableTrafficItemByName(trafficItemName)

    def starttraffic():
        """Start traffic."""
        middleware.ixn.regenerateTrafficItems()
        middleware.ixn.applyTraffic()
        middleware.ixn.startTraffic()

    def stoptraffic():
        """Stop traffic."""
        middleware.ixn.stopTraffic()

    def getstats(statName='Traffic Item Statistics', includeCrc=False):
        """Show statistics.

        param: statName: Defaults to "traffic Item Statistics".
                         Other choices: "Flow Statistics".
        param includeCrc: (True|False): To include CRC error stats"""
        if includeCrc:
            stats = middleware.ixn.getStats(viewName="Port Statistics")

        stats = middleware.ixn.getStats(viewName=statName)
        if statName == 'Flow Statistics':
            print('\n{txPort:10} {rxPort:10} {txFrames:15} {rxFrames:15} {frameLoss:10}'.format(
                txPort='txPort', rxPort='rxPort', txFrames='txFrames', rxFrames='rxFrames', frameLoss='frameLoss'))
            print('-'*90)
            for flowGroup,values in stats.items():
                txPort = values['Tx Port']
                rxPort = values['Rx Port']
                txFrames = values['Tx Frames']
                rxFrames = values['Rx Frames']
                frameLoss = values['Frames Delta']
                print('{txPort:10}  {rxPort:10} {txFrames:15} {rxFrames:15} {frameLoss:10} '.format(
                    txPort=txPort, rxPort=rxPort, txFrames=txFrames, rxFrames=rxFrames, frameLoss=frameLoss))

        if statName == 'Traffic Item Statistics':
            print('\n{trafficItemName:20} {txFrames:15} {rxFrames:15} {frameLoss:10}'.format(
                trafficItemName='TrafficItemName', txFrames='txFrames', rxFrames='rxFrames', frameLoss='frameLoss'))
            print('-'*90)
            for flowGroup,values in stats.items():
                trafficItemName = values['Traffic Item']
                txFrames = values['Tx Frames']
                rxFrames = values['Rx Frames']
                frameLoss = values['Frames Delta']

                print('{trafficItemName:20} {txFrames:15} {rxFrames:15} {frameLoss:10} '.format(
                    trafficItemName=trafficItemName, txFrames=txFrames, rxFrames=rxFrames, frameLoss=frameLoss))
        print()

    def showtrafficitemnames():
        """Show all the configured Traffic Item names."""

        trafficItems = middleware.ixn.getAllTrafficItemNames()
        print('\nAll Traffic Items:\n')
        for index, eachTrafficItem in enumerate(trafficItems):
            print('\t{0}: {1}'.format(int(index)+1, eachTrafficItem))
        print()

    def showtopologies():
        """Show all the configured Topologies and its protocol stacks."""
        middleware.ixn.showTopologies()

    def showtrafficitems():
        """Show all the configured Traffic Items."""
        middleware.ixn.showTrafficItems()

    def showerrors():
        """Show all global error messages on the chassis."""
        errorMessages = middleware.ixn.showErrorMessage(silentMode=True)
        if errorMessages:
            print(errorMessages)
        print()

    def setframesize(trafficItemName, frameSize):
        """Modify the frame size.

        param: trafficItemName: The name of the Traffic Item.
        param: frameSize: (int): The frame size to set."""
        queryData = {'from': '/traffic',
                    'nodes': [{'node': 'trafficItem', 'properties': ['name'], 'where': [{'property': 'name', 'regex': trafficItemName}]},
                                {'node': 'configElement', 'properties': [], 'where': []}]}
        queryResponse = middleware.ixn.query(data=queryData)
        configElementObj = queryResponse.json()['result'][0]['trafficItem'][0]['configElement'][0]['href']
        middleware.ixn.configTrafficItem(mode='modify', obj=configElementObj, configElements={'frameSize': frameSize})

    def setframerate(trafficItemName, frameRate):
        """Modify the frame rate.

        param: trafficItemName: The name of the Traffic Item.
        param: frameRate: (int): The frame rate to set."""
        queryData = {'from': '/traffic',
            'nodes': [{'node': 'trafficItem', 'properties': ['name'], 'where': [{'property': 'name', 'regex': trafficItemName}]},
                        {'node': 'configElement', 'properties': [], 'where': []}]}
        queryResponse = middleware.ixn.query(data=queryData)
        configElementObj = queryResponse.json()['result'][0]['trafficItem'][0]['configElement'][0]['href']
        middleware.ixn.configTrafficItem(mode='modify', obj=configElementObj, configElements={'frameRate': frameRate})

    def setframecount(trafficItemName, frameCount):
        """Modify the frame count to send.

        param: trafficItemName: The name of the Traffic Item.
        param: frameCount: (int): The total packets to send."""
        queryData = {'from': '/traffic',
            'nodes': [{'node': 'trafficItem', 'properties': ['name'], 'where': [{'property': 'name', 'regex': trafficItemName}]},
                        {'node': 'configElement', 'properties': [], 'where': []}]}
        queryResponse = middleware.ixn.query(data=queryData)
        configElementObj = queryResponse.json()['result'][0]['trafficItem'][0]['configElement'][0]['href']
        middleware.ixn.configTrafficItem(mode='modify', obj=configElementObj, configElements={'frameCount': frameCount})

    def settrafficcontinuous(trafficItemName):
        """Modify the transmission type to transmit continuously.
        
        param: trafficItemName: The name of the Traffic Item."""
        queryData = {'from': '/traffic',
            'nodes': [{'node': 'trafficItem', 'properties': ['name'], 'where': [{'property': 'name', 'regex': trafficItemName}]},
                        {'node': 'configElement', 'properties': [], 'where': []}]}
        queryResponse = middleware.ixn.query(data=queryData)
        configElementObj = queryResponse.json()['result'][0]['trafficItem'][0]['configElement'][0]['href']
        middleware.ixn.configTrafficItem(mode='modify', obj=configElementObj, configElements={'transmissionType': 'continuous'})
 
    def setfixedframes(trafficItemName):
        """Modify the transmission type to transmit a fixed frame count.
        
        param: trafficItemName: The name of the Traffic Item."""
        queryData = {'from': '/traffic',
            'nodes': [{'node': 'trafficItem', 'properties': ['name'], 'where': [{'property': 'name', 'regex': trafficItemName}]},
                        {'node': 'configElement', 'properties': [], 'where': []}]}
        queryResponse = middleware.ixn.query(data=queryData)
        configElementObj = queryResponse.json()['result'][0]['trafficItem'][0]['configElement'][0]['href']
        middleware.ixn.configTrafficItem(mode='modify', obj=configElementObj, configElements={'transmissionType': 'fixedFrameCount'})

    def flapbgp(topologyName=None, enableTrueOrFalse=True, ipInterfaceList='all', upTimeInSeconds=0, downTimeInSeconds=0):
        """Config BGP flapping.

        param: topologyName: The Topolgy Group name where the BGP stack resides in. 
        param: enableTrueOrFalse: (True|False): Enable or disable BGP flapping. 
        param: ipInterfaceList: (list): A list of the local BGP IP interface to configure for flapping.
        param: upTimeInSeconds: (int): The up time for BGP to remain up before flapping it down. 
        param: downTimeInSeconds: (int): The down time for BGP to remain down before flapping it back up."""
        queryData = {'from': '/',
                    'nodes': [{'node': 'topology', 'properties': [], 'where': []},
                                {'node': 'deviceGroup', 'properties': [], 'where': []},
                                {'node': 'ethernet', 'properties': [], 'where': []},
                                {'node': 'ipv4', 'properties': [], 'where': []},
                                {'node': 'bgpIpv4Peer', 'properties': [], 'where': []}]}
        queryResponse = middleware.ixn.query(data=queryData)
        bgpObject = queryResponse.json()['result'][0]['topology'][0]['deviceGroup'][0]['ethernet'][0]['ipv4'][0]['bgpIpv4Peer'][0]['href']
        middleware.ixn.flapBgpPeerNgpf(bgpObjHandle=bgpObject, enable=enableTrueOrFalse, flapList=ipInterfaceList,
                                         uptime=upTimeInSeconds, downtime=downTimeInSeconds)

    def configbgp(jsonConfigFile):
        """Configure BGP and Traffic Item from scratch.  Getting all the settings from the user
        defined JSON config file.
        
        param: jsonConfigFile: The JSON parameter file to load for this configuration."""
        readjsonparamfile(jsonConfigFile)
     
        middleware.ixn.connectIxChassis(middleware.params['ixChassisIp'])
        if middleware.ixn.arePortsAvailable(middleware.params['portList'], raiseException=False) != 0:
            if middleware.params['forceTakePortOwnership'] == True:
                middleware.ixn.releasePorts(middleware.params['portList'])
                middleware.ixn.clearPortOwnership(middleware.params['portList'])
            else:
                raise IxNetRestApiException('Ports are owned by another user and forceTakePortOwnership is set to False')

        # Configuring license requires releasing all ports even for ports that is not used for this test.
        middleware.ixn.releaseAllPorts()
        middleware.ixn.configLicenseServerDetails(middleware.params['licenseServerIp'], middleware.params['licenseMode'], middleware.params['licenseTier'])

        middleware.ixn.newBlankConfig()
        middleware.ixn.assignPorts(middleware.params['portList'], createVports=True)

        topologyObjects = {}
        for topology,properties in middleware.params['topologies'].items():
            if properties['enabled'] == False:
                continue

            print('\nCreating Topology: {0}\n'.format(topology))
            if middleware.params['topologies'][topology]['vlanId']['start'] is not 0:
                vlan = {"start": middleware.params['topologies'][topology]['vlanId']['start'],
                        "direction": middleware.params['topologies'][topology]['vlanId']['direction'],
                        "step": middleware.params['topologies'][topology]['vlanId']['step']
                        }
            else:
                vlan = None

            if middleware.params['topologies'][topology]['macAddress']['start'] is not 0:
                macAddress = {"start": middleware.params['topologies'][topology]['macAddress']['start'],
                            "direction": middleware.params['topologies'][topology]['macAddress']['direction'],
                            "step": middleware.params['topologies'][topology]['macAddress']['step']
                            }
            else:
                macAddress = None

            if middleware.params['topologies'][topology]['ipv4Address']['start'] is not 0:
                ipv4Address = {"start": middleware.params['topologies'][topology]['ipv4Address']['start'],
                            "direction": middleware.params['topologies'][topology]['ipv4Address']['direction'],
                            "step": middleware.params['topologies'][topology]['ipv4Address']['step']
                            }

                if middleware.params['topologies'][topology]['ipv4Address']['start'] is not 0:
                    ipv4Gateway = {"start": middleware.params['topologies'][topology]['ipv4Gateway']['start'],
                                "direction": middleware.params['topologies'][topology]['ipv4Gateway']['direction'],
                                "step": middleware.params['topologies'][topology]['ipv4Gateway']['step']
                                }
                else:
                    ipv4Gateway = None

            topologyObj = middleware.ixn.createTopologyNgpf(portList=properties['ports'],
                                                    topologyName='Topo-{0}'.format(topology))

            topologyObjects.update({'topology{0}'.format(topology): topologyObj})

            deviceGroupObj = middleware.ixn.createDeviceGroupNgpf(topologyObj,
                                                            multiplier=properties['totalIpInterfaces'],
                                                            deviceGroupName='DG1')

            ethernetObj = middleware.ixn.createEthernetNgpf(deviceGroupObj,
                                                    ethernetName='MyEth1',
                                                    macAddress=macAddress,
                                                    macAddressPortStep='disabled',
                                                    vlanId=vlan)

            if middleware.params['topologies'][topology]['ipv4Address']['start'] is not 0:
                ipv4Obj = middleware.ixn.createIpv4Ngpf(ethernetObj,
                                                ipv4Address=ipv4Address,
                                                ipv4AddressPortStep='disabled',
                                                gateway=ipv4Gateway,
                                                gatewayPortStep='disabled',
                                                prefix=properties['ipv4Prefix'],
                                                resolveGateway=True)

            # flap = true or false.
            #    If there is only one host IP interface, then single value = True or False.
            #    If there are multiple host IP interfaces, then single value = a list ['true', 'false']
            #           Provide a list of total true or false according to the total amount of host IP interfaces.
            if 'bgpDutIp' in properties:
                bgpObj = middleware.ixn.configBgp(ipv4Obj,
                                            name = 'bgp_{0}'.format(topology),
                                            enableBgp = True,
                                            holdTimer = 90,
                                            dutIp={'start': properties['bgpDutIp'],
                                                'direction': 'increment',
                                                'step': '0.0.0.0'},
                                            localAs2Bytes = properties['localAs2Bytes'],
                                            enableGracefulRestart = False,
                                            restartTime = 45,
                                            type = properties['bgpType'],
                                            enableBgpIdSameasRouterId = True,
                                            staleTime = 0,
                                            flap = False)
            if 'routeAdvertisements' in properties:
                print('Creating Network Group:', properties['totalAdvertisingRoutes'])
                networkGroupObj = middleware.ixn.configNetworkGroup(deviceGroupObj,
                                                            name=properties['routeAdvertisementName'],
                                                            multiplier = properties['totalAdvertisingRoutes'],
                                                            networkAddress = {'start': properties['routeAdvertisements'],
                                                                                'step': '0.0.0.1',
                                                                                'direction': 'increment'},
                                                            prefixLength = properties['routeAdvertisingPrefix'])

        middleware.ixn.startAllProtocols()
        middleware.ixn.verifyProtocolSessionsNgpf()

        isAnyTrafficItemConfigured = 0
        for trafficItemNum,properties in middleware.params['trafficItems'].items():
            if properties['enabled'] == False:
                continue

            isAnyTrafficItemConfigured = 1
            # For all parameter options, go to the API configTrafficItem.
            # mode = create or modify
            trafficStatus = middleware.ixn.configTrafficItem(mode='create',
                                                    trafficItem = {
                                                        'name':properties['name'],
                                                        'trafficType':'ipv4',
                                                        'biDirectional':properties['bidirectional'],
                                                        'srcDestMesh':'one-to-one',
                                                        'routeMesh':'oneToOne',
                                                        'allowSelfDestined':False,
                                                        'trackBy': ['flowGroup0']
                                                    },
                                                    endpoints = [{'name':'Flow-Group-1',
                                                                    'sources': [topologyObjects [middleware.params["trafficItems"][trafficItemNum]['srcEndpoint']]],
                                                                    'destinations': [topologyObjects[middleware.params["trafficItems"][trafficItemNum]['dstEndpoint']]]}],
                                                    configElements = [{'transmissionType': properties['transmissionType'],
                                                                        'frameCount': properties['frameCount'],
                                                                        'frameRate': properties['frameRate'],
                                                                        'frameRateType': properties['frameRateType'],
                                                                        'frameSize': properties['frameSize']}])

            # trafficItemObj   = trafficStatus[0]
            # endpointObj      = trafficStatus[1][0]
            # configElementObj = trafficStatus[2][0]
            # middleware.trafficItemObjList.append(trafficItemObj)
            # middleware.endpointObj = endpointObj
            # middleware.configElementObj = configElementObj

        if isAnyTrafficItemConfigured == 0: 
            raise IxNetRestApiException('No Traffic Item was enabled for configuring')

    def getInput(prompt):
        """Support Python 2 and 3 for input and raw_input.

        param: prompt: The input/raw_input prompt for user interaction.
        """
        if platform.python_version().startswith('3'):
            userInput = input('%s ' % prompt).strip()
        if platform.python_version().startswith('2'):
            userInput = raw_input('%s ' % prompt).strip()
        return userInput

    def completer(text, state):
        options = [x for x in commandList if x.startswith(text)]
        try:
            return options[state]
        except IndexError:
            return None
    
    if __name__ == "__main__":
        commandList = []
        for name,obj in inspect.getmembers(sys.modules[__name__]):
            commandList.append(name)

        readline.set_completer(completer)
        readline.parse_and_bind("tab: complete")

        while True:
            userInput = getInput('ixShell>')
            ixShellCommand = userInput.split(' ')[0]
            # If command has no args
            if len(userInput.split(' ')) == 1:
                ixShellCommandValues = None
            else:
                # Command has args. Need to verify for values that contains spaces.
                # Otherwise, when creating a list of values, the spaces will separate the sapces into elements.

                # 1> Parse out the parameters/values
                match = re.match('{0} +(.*)'.format(ixShellCommand), userInput)
                commandValues = match.group(1)

                # 2> re.sub all spaces with #
                #    Handle curly braces: portList={'192.168.70.11': [('vport1','1/1'), ('vport2', '2/1')]}
                match = re.sub(r'".+?"|{.+?}', lambda x:x.group().replace(" ","#"), commandValues)
                #match = re.sub(r'("[^ ]+) +([^ ]")', r'\1#\2', commandValues)

                # 3> Convert the commandValues from a string into a list
                #    From 'topologyName=Topo-1 protocolName="IPv4 1' to ['topologyName=Topo-1', 'protocolName="IPv4#1"']
                commandValuesList = match.split(' ')

                # 4> Create the final list by replacing all # with spaces, the way how the user defines the values.
                #    ['topologyName=Topo-1', 'protocolName="IPv4 1"']
                ixShellCommandValues = []
                for x in commandValuesList:
                    ixShellCommandValues.append(x.replace('#', ' '))

            if userInput in ['?', 'help']:
                help()
                continue

            elif ixShellCommand == '':
                continue

            elif ixShellCommand in commandList:
                # Making each ixShellCommand callable
                # method_name2 = 'installWithOptions("a","b")'
                # eval(method_name2)
                if ixShellCommandValues != None:
                    valueList = ixShellCommand+'('
                    for value in ixShellCommandValues:
                        print('\nvalue:', value)
                        if '=' in value:
                            argList = value.split('=')
                            param = argList[0].strip()
                            paramValue = argList[-1]

                            if '"' in paramValue:
                                value1 = argList[-1].strip()
                            else:
                                # If there is no double quotes, have to include them, but not for keywords, list and dict.
                                print('\nargList:', argList[-1], type(argList[-1]))
                                if argList[-1] not in ['True', 'False', 'None'] and \
                                    argList[-1].startswith('{') == False and argList[-1].startswith('[') == False and \
                                    argList[-1].startswith('(') == False:
                                    value1 = '"' + argList[-1].strip() + '"'
                                else:
                                    # Don't wrap quotations marks around keywords
                                    value1 = argList[-1]
                            finalValue = param + '=' + value1
                        
                        if '=' not in value:
                            if '"' in value:
                                finalValue = value
                            # Wrap double quotes around value, but don't wrap quotations around the value that already has quotations
                            # and avoid keywords, list and dict..
                            if '"' not in value:
                                #finalValue = '"' + value + '"'

                                print('\nValue:', value, type(value))
                                if value not in ['True', 'False', 'None'] and \
                                    value.startswith('{') == False and value.startswith('[') == False and value.startswith('(') == False:
                                    finalValue = '"' + value.strip() + '"'
                                else:
                                    # Don't wrap quotations marks around keywords
                                    finalValue = value

                        valueList = valueList + finalValue
                        if value != ixShellCommandValues[-1]:
                            valueList = valueList + ', '
                    valueList = valueList+')'
                    try:
                        print('\n\tEntering: {0}'.format(valueList))
                        eval(valueList)
                    except Exception as errMsg:
                        print('\n  Error:', errMsg)
                        # eval('help(command="%s")' % ixShellCommand)
                        # print('\n\t{0}\n'.format(eval(ixShellCommand+'.__doc__')))
                else:
                    try:
                        # No values.  Enter the command.
                        eval(ixShellCommand)()
                    except Exception as errMsg:
                        if middleware.ixn == None and ixShellCommand != 'connect':
                            print('\nError: You need to call connect first\n')
                        elif middleware.ixn == None and ixShellCommand == 'connect':
                            print('\nSyntax error: Example: connect "bgpConfig.json"\n')
                        else:
                            print('\n  Error:', errMsg)

            elif bool(re.match('exit|quit', ixShellCommand, re.I)):
                sys.exit()
            else:
                print('\nNo such command\n')

except (IxNetRestApiException, Exception, KeyboardInterrupt) as errMsg:
    if enableDebugTracing:
        print('\nGOT TO TRACIING')
        if not bool(re.search('ConnectionError', traceback.format_exc())):
            print('\n%s' % traceback.format_exc())
    print('\nException Error! %s\n' % errMsg)
    if 'ixn' in locals() and middleware.apiServerType == 'linux':
        ixn.linuxServerStopAndDeleteSession()
    if 'ixn' in locals() and middleware.onnectToApiServer in ['windows', 'windowsConnectionMgr']:
        if middleware.releasePortsWhenDone and middleware.forceTakePortOwnership:
            middleware.ixn.releasePorts(portList)
        if middleware.apiServerType == 'windowsConnectionMgr':
            middleware.ixn.deleteSession()



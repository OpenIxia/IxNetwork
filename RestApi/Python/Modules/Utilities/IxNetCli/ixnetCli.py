"""
PLEASE READ DISCLAIMER

    This is a sample script for demo and reference purpose only.
    It is subject to change for content updates without warning.

 REQUIREMENTS
    - Python2.7.9+
    - Python modules: requests
    - preference.py:  Set your preferences in this file.
    
    - All the IxNetwork ReST API modules:
         IxNetRestApi.py
         IxNetRestApiPortMgmt.py
         IxNetRestApiFileMgmt.py
         IxNetRestApiTraffic.py
         IxNetRestApiProtocol.py
         IxNetRestApiStatistics.py

 DESCRIPTION
    This sample script demonstrates:
        - REST API configurations using two back-to-back Ixia ports.
        - Connecting to Windows IxNetwork API server or Linux API server.

        - Verify for sufficient amount of port licenses before testing.
        - Verify port ownership.
        - Configure two IPv4/BGP Topology Groups
        - Start protocols
        - Verify BGP protocol sessions
        - Create a Traffic Item
        - Apply Traffic
        - Start Traffic
        - Get stats

 USAGE
    python <script>.py windows
    python <script>.py linux
"""
# TODO:
#    - Compare showsession and showlinuxsession()
#    - Fix showcommands() to exclude completer() and getInput()

from __future__ import absolute_import, print_function, division
import sys, inspect, traceback, platform
import importlib
from collections import OrderedDict

from IxNetRestApi import *
from IxNetRestApiPortMgmt import PortMgmt
from IxNetRestApiFileMgmt import FileMgmt
from IxNetRestApiTraffic import Traffic
from IxNetRestApiProtocol import Protocol
from IxNetRestApiStatistics import Statistics

# Default the API server to either windows or linux.
class middleware:
    # Internal variables.  Don't touch below variables.
    preference = None ;# The preference module object if user calls setpreference()
    resume = False
    connectedTo = None
    sessionId = None
    apiKey = None
    linuxServerSessionId = None
    params = None ;# Internal use only. From readjsonparamfile.
    ixn = None
    portMgmtObj = None
    fileMgmtObj = None
    trafficObj = None
    protocolObj = None
    statsObj = None

try:
    # The preference.py file has to be in the same directory as ixnetCli.py
    # Users are allowed to create preference file and overwrite the preference.py file.
    middleware.preference = importlib.import_module('preference')
except:
    pass

try:
    def showcommands(command=None, showall=None):
        """Show all the API commands.

        param: showall: None|showall: Enter "showall" to include the descriptions."""
        # pydoc.help(ixnetPyCli)
        if command == None:
            print('\nCommand list:\n')
        else:
            print('\tHelp on command usage: {0}'.format(command))

        for name,obj in inspect.getmembers(sys.modules[__name__]):
            if name in ['completer', 'getInput']: continue
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
            print('\t1> Windows: connecttowindows("192.168.70.127")')
            print('\t   Linux:   connecttolinux("192.168.70.144", "5443")')
            print()
            print('\t2> To load a saved config file:')
            print('\t      Option 1> runjsonconfig("json_config_file.json")')
            print('\t      Option 2> runixncfgconfig("ixncfg_file.ixncfg", ixChassisIp="1.1.1.1")')
            print()
            print('\t   To load a saved config file and use different chassis/ports:')
            print('\t      runjsonconfig("json_config_file.json", chassisIp=<ip>, ')
            print('\t                    portList=[[ixChassisIp, "1", "1"], [ixChassisIp, "2", "1"]])')
            #print('\t      Option 2> runixncfgconfig("ixncfg_file.ixncfg", ixChassisIp="1.1.1.1")')
            print()
            print('\t   To create a config from scratch:')
            print('\t      configbgp("bgp.json")')
            print()

    def setpreference(preferenceFile):
        if os.path.exists(preferenceFile) == False:
            print('\nError! No such preference file found: %s\n' % preferenceFile)
            return

        match = re.match('(.*/)?(preference.*).py', preferenceFile)
        if match:
            if match.group(1):
                sys.path.append(match.group(1))
            middleware.preference = importlib.import_module(match.group(2))

    def showpreference():
        """Show user defined preferences"""
        print()
        for property,value in middleware.preference.__dict__.items():
            if property.startswith('_') and not callable(property): continue
            print('\t{0}: {1}'.format(property, value))
        print()

    def showsession():
        """Show the current session ID.  If session is connected to 
        a Linux API server, then the API-KEY will be included."""
        for property,value in middleware.__dict__.items():
            if property.startswith('_') and not callable(property): continue
            if property in ['ixn', 'portMgmtObj', 'fileMgmtObj', 'protocolObj', 'statsObj']: continue
            print('\t{0}: {1}'.format(property, value))

    def showconnecttoapiserver():
        """Show the type of the API server that is currently connecting to.

        Example: windows|windowsConnectionMgr|linux"""
        print('\n{0}'.format(middleware.preference.apiServerType))

    def deletelinuxsession():
        """Delete the current session ID on the Linux API server.
        This command is only for connecting to the Linux API server."""
        if middleware.linuxServerSessionId != None:
            middleware.ixn.linuxServerStopOperations(middleware.linuxServerSessionId)
            middleware.ixn.linuxServerDeleteSession(middleware.linuxServerSessionId)
            middleware.linuxServerSessionId = None
            middleware.sessionId = None
        else:
            print('\nThere is currently no opened Linux sessions\n')

    def connecttolinux(apiServerIp=None, apiServerIpPort=None, resume=False,
                       apiKey=None, sessionId=None, username='admin', password='admin', deleteSessionAfterTest=True):
        """Connect to a Linux API server.

        :param apiServerIp: (str) The API server IP address.
        :param apiServerIpPort: (int) The API server TCP port.
        :param apiServerType: (str) windows|linux.
        :param resume: (bool) True|False: To connect to an existing session.
        :param apiKey: (str) The Linux API server user account's API Key.
        :param sessionId: (int) The session ID.
        :param username: (str) The login username.
        :param password: (str) The login password.
        :param deleteSessionAfterTest: (bool) True|False: To Delete the session when test is done."""
        middleware.preference.apiServerType = 'linux'
        connect(apiServerIp=apiServerIp, apiServerIpPort=apiServerIpPort,
                resume=resume, apiKey=apiKey, sessionId=sessionId, username=username, password=password,
                deleteSessionAfterTest=deleteSessionAfterTest)

    def connecttowindows(apiServerIp=None, apiServerIpPort=None, resume=False):
        """Connect to a Windows API server.

        :param apiServerIp: (str) The API server IP address.
        :param apiServerIpPort: (int) The API server TCP port.
        :param resume: (bool) True|False: To connect to an existing session.
        :param apiKey: (str) The Linux API server user account's API Key.
        :param sessionId: (int) The session ID.
        :param username: (str) The login username.
        :param password: (str) The login password.
        :param deleteSessionAfterTest: (bool) True|False: To Delete the session when test is done."""
        middleware.preference.apiServerType = 'windows'
        connect(apiServerIp=apiServerIp, apiServerIpPort=apiServerIpPort, resume=resume)

    def connect(apiServerIp=None, apiServerIpPort=None, resume=False,
                apiKey=None, sessionId=None, username='admin', password='admin', deleteSessionAfterTest=True):
        """Internal use only. Used by connecttowindows and connecttolinux.  Connect to an API server.

        :param apiServerType: (str) windows|linux.
        :param resume: (bool) True|False: To connect to an existing configuration.
                       If apiServerType is Linux, provide the apiServerIpAddress, apiServerIpPort, apiKey and sessionId number.
                       If apiServerType is windows, provide the apiServerIpAddress and apiServerIpPort.
        :param apiServerIp: (str): The IP address of the IxNetwork API server to connect to.
        :param apiServerIpPort: (int): The API server IP port number to use.
                        Windows default port = 11009.
                        Linux default port = 443.
        :param apiKey: (str): For Linux API server only. The API-KEY of the Linux API server.
                        You could get this in the Web UI, under My Account, and in show API-KEY.
        :param sessionID: (int): For Linux API server only. The existing session ID to connect to.
        :param username: For Linux API serer only. The login username.
        :param password: For Linux API server only. The login password.

        Example:
           - To make a new Windows connection: apiServerType='windows', apiServerIp=<ip>, apiServerIpPort=<ipPort>
           - To make a new Linux connection: apiServerType='linux', apiServerIp=<ip>, apiSeverIpPort=<ipPort>
           - To resume on Linux: resume=True, apiKey=<apiKey>, sessionId=<session ID>,
           - To resume on Windows with currently connected apiServerIp: resume=True, apiServerIp=<apiServerIp>
           - To resume on Windows with a different apiServerIp: resume='windows', apiServerIp=<apiServerIp>, apiServerIpPort=<apiSeverIpPort>
           - To resume on WindowConnectionMgr = Not supported yet."""
        if resume == True:
            middleware.resume = True
            if middleware.preference.apiServerType == 'linux':
                if (apiKey is None and sessionId is None) or \
                    (apiKey is None and sessionId is not None) or \
                    (apiKey is not None and sessionId is None):
                        print('\nError: To resume on Linux API server, you must provide both apiKey and sessionId.\n')
                        return

        if resume == False:
            # Check to see if resuming on Windows
            if middleware.preference.apiServerType == 'windows':
                if apiServerIp == None and middleware.preference.windowsApiServerIp == None:
                    print('\nError: You must include apiServerIp\n') ;# return
                if apiServerIpPort == None and middleware.preference.windowsApiServerIpPort == None:
                    print('\nError: You must include apiServerIpPort\n') ;# return

                if apiServerIp != None:
                    middleware.preference.windowsApiServerIp = apiServerIp
                if apiServerIpPort != None:
                    middleware.preference.windowsApiServerIpPort = apiServerIpPort

            if middleware.preference.apiServerType == 'linux':
                if apiServerIp == None and middleware.preference.linuxApiServerIp == None:
                    print('\nError: You must include the apiServerIp\n') ;# return
                if apiServerIp == None and middleware.preference.linuxApiServerIp == None:
                    print('\nError: You must include the apiServerIp\n') ;# return

                if apiServerIp != None:
                    middleware.preference.linuxApiServerIp = apiServerIp
                if apiServerIpPort != None:
                    middleware.preference.linuxApiServerIpPort = apiServerIpPort

        if middleware.preference.apiServerType == 'windows':
            ixn = Connect(apiServerIp=middleware.preference.windowsApiServerIp,
                          serverIpPort=middleware.preference.windowsApiServerIpPort,
                          serverOs='windows')
            middleware.connectedTo = 'windows'

        if middleware.preference.apiServerType == 'linux':
            ixn = Connect(apiServerIp=middleware.preference.linuxApiServerIp,
                          serverIpPort=str(middleware.preference.linuxApiServerIpPort),
                          username=middleware.preference.username,
                          password=middleware.preference.password,
                          deleteSessionAfterTest=deleteSessionAfterTest,
                          serverOs='linux',
                          apiKey=apiKey,
                          sessionId=str(sessionId))

            middleware.connectedTo = 'linux'
            # Record the current apiKey and sessionId
            middleware.apiKey = ixn.apiKey
            middleware.linuxServerSessionId = ixn.sessionId

        middleware.sessionId = ixn.sessionId.split('/')[-1]
        middleware.ixn = ixn
        middleware.portMgmtObj = PortMgmt(ixn)
        middleware.fileMgmtObj = FileMgmt(ixn)
        middleware.trafficObj = Traffic(ixn)
        middleware.protocolObj = Protocol(ixn, middleware.portMgmtObj)
        middleware.statsObj = Statistics(ixn)

    # This is not the json import/export feature.
    def readjsonparamfile(jsonConfigFile):
        """For internal use only and for building a config from scratch.
        Used by functions that creates configuration from scratch. Read and load a JSON parameters file.

        :param jsonConfigFile: (str) The JSON config file to load."""
        if os.path.exists(jsonConfigFile) is False:
            raise IxNetRestApiException("\nError: JSON config file doesn't exists: %s\n" % jsonConfigFile)

        middleware.params = json.load(open(jsonConfigFile), object_pairs_hook=OrderedDict)
        #middleware.params = json.load(open(jsonConfigFile))


    def runjsonconfig(jsonConfigFile=None, chassisIp=None, portList=None, licenseServerIp=None, licenseMode=None, licenseTier=None, includeCrc=False):
        """Loads an exported JSON config file, reassigns ports, verify protocols, start traffic and get stats.

        :param jsonConfigFile: (str) The IxNetwork saved configuration in JSON format.
        :param chassisIp: (str) Optional: Ixia chassis IP address.
                         Defaults to the JSON config chassis IP address.
        :param portList: (list) All the ports to use for this JSON configuration file.
                         The amount of ports must match the amount of configured ports in the JSON config file.
                         Defaults to using all the ports defined in the JSON config file.
                         Input example:  portList = [[ixChassisIp, '1', '1'], [ixChassisIp, '2', '1']]
        :param licenseServerIp: (str) The license server IP address.
        :param licenseMode: (str) mixed|subscription|perpetual
        :param licenseTier: (str) tier1, tier2, tier3"""
        '''
        if licenseServerIp:
            preference.licenseServerIp = [licenseServerIp]
        if licenseMode:
            preference.licenseMode = licenseMode
        if licenseTier:
            preference.licenseTier = licenseTier

        if preference.licenseServerIp == None:
            print('\nNo licenseServerIp is set or included on this command line')
            return
        '''
        if 'json' not in jsonConfigFile:
            print('\nError: The JSON config file doesn\'t have a .json extnesion. Please check your jsonConfigFile value: %s\n' % jsonConfigFile)
            return

        if licenseServerIp:
            middleware.preference.licenseServerIp = licenseServerIp
        if licenseMode:
            middleware.preference.licenseMode = licenseMode
        if licenseTier:
            middleware.preference.licenseTier = licenseTier

        if middleware.preference.licenseServerIp == None:
            print('\nNo licenseServerIp is set or included on this command line')
            return

        if jsonConfigFile == None:
            if middleware.preference.jsonConfigFile == None:
                print('\nYou must include a jsonConfigFile')
            if middleware.preference.jsonConfigFile != None:
                jsonConfigFile = middleware.preference.jsonConfigFile

        jsonData = middleware.fileMgmtObj.jsonReadConfig(jsonConfigFile)
        if portList != None:
            middleware.fileMgmtObj.jsonAssignPorts(jsonData, portList)

        if portList == None:
            if middleware.preference.portList == None:
                portList = middleware.fileMgmtObj.getJsonConfigPortList(jsonData)
                if portList == []:
                    raise IxNetRestApiException('\nFailed to get portList from JSON config data\n')
            if middleware.preference.portList != None:
                portList = middleware.preference.portList
            middleware.fileMgmtObj.jsonAssignPorts(jsonData, portList)

        if chassisIp is None:
            if middleware.preference.chassisIp != None:
                chassisIp = middleware.preference.chassisIp
            if middleware.preference.chassisIp == None:
                chassisIp = jsonData['availableHardware']['chassis'][0]['hostname']

        # Need to support multiple chassis's.  If user passed in a string of chassis, convert it to a list.
        if chassisIp is not list:
            chassisIp = chassisIp.split(' ')
        for eachChassisIp in chassisIp:
            middleware.ixn.connectIxChassis(eachChassisIp)

        if middleware.portMgmtObj.arePortsAvailable(portList, raiseException=False) != 0:
            if middleware.preference.forceTakePortOwnership == True:
                middleware.portMgmtObj.releasePorts(portList)
                middleware.portMgmtObj.clearPortOwnership(portList)
            else:
                raise IxNetRestApiException('Ports are owned by another user and forceTakePortOwnership is set to False')

        # Configuring license requires releasing all ports even for ports that is not used for this test.
        middleware.portMgmtObj.releaseAllPorts()
        middleware.ixn.configLicenseServerDetails([middleware.preference.licenseServerIp],
                                                  middleware.preference.licenseMode,
                                                  middleware.preference.licenseTier)
        middleware.fileMgmtObj.importJsonConfigObj(jsonData, type='newConfig')
        middleware.portMgmtObj.verifyPortState()
        middleware.protocolObj.startAllProtocols()
        middleware.protocolObj.verifyAllProtocolSessionsNgpf(timeout=120)
        middleware.trafficObj.regenerateTrafficItems()
        middleware.trafficObj.startTraffic()
        getstats(includeCrc=includeCrc)

    def runixncfgconfig(ixncfgConfigFile=None, chassisIp=None, portList=None, licenseServerIp=None, licenseMode=None, licenseTier=None, includeCrc=False):
        """Loads a saved ixncfg config file, reassign ports, start protocols, verify protocols, start traffic and get stats.

        :param ixncfgConfigFile: (str) The IxNetwork saved configuration in ixncfg format.
        :param chassisIp: (str) The chassis IP address.
        :param portList: (list) A list of list containing [[ixChassisIp, 1, 1], [ixChassisIp, 1, 2]]
                         Defaults to using ports configured in the saved config file.
        :param licenseServerIp: (str) The license server IP address.
        :param licenseMode: (str) subscription|perpetual.
        :param licenseTier: (str) tier1, tier2, tier3, ...
        :param includeCrc: (bool) True|False: To include CRC error stats."""
        if 'ixn cfg' not in ixncfgConfigFile:
            print('\nError: The .ixncfg config file doesn\'t have a .ixncfg extnesion. Please check your ixncfgConfigFile value: %s\n' % ixncfgConfigFile)
            return 

        if ixncfgConfigFile == None:
            if middleware.preference.ixncfgConfigFile == None:
                print('\nYou must provide an .ixncfg config file to load')
                return
            else:
                ixncfgConfigFile = middleware.preference.ixncfgConfigFile

        if licenseServerIp:
            middleware.preference.licenseServerIp = licenseServerIp
        if licenseMode:
            middleware.preference.licenseMode = licenseMode
        if licenseTier:
            middleware.preference.licenseTier = licenseTier

        if middleware.preference.licenseServerIp == None:
            print('\nNo licenseServerIp is set or included on this command line')
            return

        if chassisIp == None:
            if middleware.preference.chassisIp == None:
                print('\nYou must provide the ixChassisIp address')
                return
            else:
                chassisIp = middleware.preference.chassisIp

        '''
        middleware.ixn.connectIxChassis(chassisIp)
        if portList is not None and middleware.portMgmtObj.arePortsAvailable(portList, raiseException=False) != 0:
            if preference.forceTakePortOwnership == True:
                middleware.portMgmtObj.releasePorts(portList)
                middleware.portMgmtObj.clearPortOwnership(portList)
            else:
                raise IxNetRestApiException('Ports are owned by another user and forceTakePortOwnership is set to False')
        '''
        # Need to support multiple chassis's.  If user passed in a string of chassis, convert it to a list.
        if chassisIp is not list:
            chassisIp = chassisIp.split(' ')
        for eachChassisIp in chassisIp:
            middleware.ixn.connectIxChassis(eachChassisIp)

        if portList == None:
            if middleware.preference.portList != None:
                portList = middleware.preference.portList
            if middleware.preference.portList == None:
                print('\nYou must provide a portList')
            print('\nrunixncfgconfig portList:', portList)

        if middleware.portMgmtObj.arePortsAvailable(portList, raiseException=False) != 0:
            if middleware.preference.forceTakePortOwnership == True:
                middleware.portMgmtObj.releasePorts(portList)
                middleware.portMgmtObj.clearPortOwnership(portList)
            else:
                raise IxNetRestApiException('Ports are owned by another user and forceTakePortOwnership is set to False')


        # Uncomment this to configure license server.
        # Configuring license requires releasing all ports even for ports that is not used for this test.
        middleware.portMgmtObj.releaseAllPorts()
        middleware.ixn.configLicenseServerDetails([middleware.preference.licenseServerIp],
                                                  middleware.preference.licenseMode,
                                                  middleware.preference.licenseTier)
        middleware.ixn.loadIxncfgConfig = True
        middleware.fileMgmtObj.loadConfigFile(ixncfgConfigFile)
        if portList != None:
            middleware.portMgmtObj.assignPorts(portList)
        middleware.portMgmtObj.verifyPortState()
        middleware.protocolObj.startAllProtocols()
        middleware.protocolObj.verifyAllProtocolSessionsNgpf(timeout=120)
        middleware.trafficObj.regenerateTrafficItems()
        middleware.trafficObj.startTraffic()
        getstats(includeCrc=includeCrc)

    def showlinuxsession():
        """Show the Linux API server session ID"""
        print('\nAPI-KEY: {0}'.format(middleware.ixn.apiKey))
        print('Session ID: {0}'.format(middleware.ixn.sessionId.split('/')[-1]))
        print()

    def stoptopology(topologyName):
        """Stop a running Topology Group and all of its protocol stacks.

        :param topologyName: (str) The Topology Group name."""
        queryData = {'from': '/',
                    'nodes': [{'node': 'topology',    'properties': ['name'], 'where': [{'property': 'name', 'regex': topologyName}]}]
                    }
        queryResponse = middleware.ixn.query(data=queryData)
        try:
            topologyObj = queryResponse.json()['result'][0]['topology'][0]['href']
        except:
            print('\nError: Verify the topologyName', topologyName)
        middleware.protocolObj.stopTopology([topologyObj])

    def starttopology(topologyName):
        """Start a Topology Group and all of its protocol stacks.

        :param topologyName: (str) The Topology Group name."""
        queryData = {'from': '/',
                    'nodes': [{'node': 'topology',    'properties': ['name'], 'where': [{'property': 'name', 'regex': topologyName}]}]
                    }
        queryResponse = middleware.ixn.query(data=queryData)
        try:
            topologyObj = queryResponse.json()['result'][0]['topology'][0]['href']
        except:
            print('\nError: Verify the topologyName', topologyName)
        middleware.protocolObj.startTopology([topologyObj])
        middleware.protocolObj.verifyProtocolSessionsNgpf()

    def startbgp(topologyName, bgpName):
        """Start BGP protocol.

        :param topologyName: The Topology Group name.
        :param bgpName: The bgp stack name for the Topology Group."""
        # Query for the protocol obj and topology group obj by the protocolName
        queryData = {'from': '/',
                    'nodes': [{'node': 'topology',    'properties': ['name'],
                               'where': [{'property': 'name', 'regex': topologyName}]},
                              {'node': 'deviceGroup', 'properties': [], 'where': []},
                              {'node': 'ethernet',    'properties': [], 'where': []},
                              {'node': 'ipv4',        'properties': [], 'where': []},
                              {'node': 'bgpIpv4Peer', 'properties': ['name'],
                               'where': [{'property': 'name', 'regex': bgpName}]}
                            ]
                    }
        queryResponse = middleware.ixn.query(data=queryData)
        try:
            protocolObj = queryResponse.json()['result'][0]['topology'][0]['deviceGroup'][0]['ethernet'][0]['ipv4'][0]['bgpIpv4Peer'][0]['href']
        except IndexError:
            print('\nError: Verify the bgpName', bgpName)

        middleware.protocolObj.startProtocol(protocolObj)
        middleware.protocolObj.verifyProtocolSessionsNgpf()

    def stopbgp(topologyName, bgpName):
        """Stop BGP protocol.

        :param topologyName: The Topology Group name.
        :param bgpName: The protocol stack name for the Topology Group."""
        # Query for the protocol obj and topology group obj by the protocolName
        queryData = {'from': '/',
                    'nodes': [{'node': 'topology',    'properties': ['name'],
                               'where': [{'property': 'name', 'regex': topologyName}]},
                              {'node': 'deviceGroup', 'properties': [], 'where': []},
                              {'node': 'ethernet',    'properties': [], 'where': []},
                              {'node': 'ipv4',        'properties': [], 'where': []},
                              {'node': 'bgpIpv4Peer', 'properties': ['name'],
                               'where': [{'property': 'name', 'regex': bgpName}]}
                            ]
                    }
        queryResponse = middleware.ixn.query(data=queryData)
        try:
            protocolObj = queryResponse.json()['result'][0]['topology'][0]['deviceGroup'][0]['ethernet'][0]['ipv4'][0]['bgpIpv4Peer'][0]['href']
        except IndexError:
            raise IxNetRestApiException('\nError: Verify th bgpName', bgpName)

        middleware.protocolObj.stopProtocol(protocolObj)

    def disabletrafficitem(trafficItemName):
        """Disable a Traffic Item by its name.

        :param trafficItemName: (str) The Traffic Item name to disable."""
        middleware.trafficObj.disableTrafficItemByName(trafficItemName)

    def enabletrafficitem(trafficItemName):
        """Enable a Traffic Item by its name.

        :param trafficItemName: (str) The Traffic Item name to enable."""
        middleware.trafficObj.enableTrafficItemByName(trafficItemName)

    def starttraffic():
        """Start traffic."""
        middleware.trafficObj.regenerateTrafficItems()
        middleware.trafficObj.startTraffic()

    def stoptraffic():
        """Stop traffic."""
        middleware.trafficObj.stopTraffic()

    def getstats(statName='Traffic Item Statistics', includeCrc=False):
        """Show statistics.

        :param statName: Defaults to "traffic Item Statistics".
                         Other choice: "Flow Statistics".
        param includeCrc: (bool) True|False: To include CRC error stats"""
        if statName == 'Port Statistics' or includeCrc == True:
            stats = middleware.statsObj.getStats(viewName="Port Statistics", silentMode=True, displayStats=False)
            print('\n{port:31} {txFrames:15} {rxFrames:15} {CRC:15}'.format(
                port='port', txFrames='txFrames', rxFrames='rxFrames', CRC='CRC'))
            print('-'*75)
            for flowGroup,values in stats.items():
                port = values['Stat Name']
                txFrames = values['Frames Tx.']
                rxFrames = values['Valid Frames Rx.']
                try:
                    crc = values['CRC Errors']
                except:
                    print('No CRC stats for VM ports')
                    break
                print('{port:30}  {txFrames:15} {rxFrames:15} {CRC:15}'.format(
                    port=port, txFrames=txFrames, rxFrames=rxFrames, CRC=crc))

        stats = middleware.statsObj.getStats(viewName=statName, silentMode=True, displayStats=False)
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
            print('-'*70)
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
        trafficItems = middleware.trafficObj.getAllTrafficItemNames()
        print('\nAll Traffic Items:\n')
        for index, eachTrafficItem in enumerate(trafficItems):
            print('\t{0}: {1}'.format(int(index)+1, eachTrafficItem))
        print()

    def showtopologies():
        """Show all the configured Topologies and its protocol stacks."""
        middleware.protocolObj.showTopologies()

    def showtrafficitems():
        """Show all the configured Traffic Items."""
        middleware.trafficObj.showTrafficItems()

    def showerrors():
        """Show the global error messages on the chassis."""
        errorMessages = middleware.ixn.showErrorMessage(silentMode=True)
        if errorMessages:
            print(errorMessages)
        print()

    def setframesize(trafficItemName, frameSize):
        """Modify the frame size.

        :param trafficItemName: (str) The Traffic Item name.
        :param frameSize: (int) The frame size to set."""
        queryData = {'from': '/traffic',
                    'nodes': [{'node': 'trafficItem', 'properties': ['name'],
                               'where': [{'property': 'name', 'regex': trafficItemName}]},
                              {'node': 'configElement', 'properties': [], 'where': []}]}
        queryResponse = middleware.ixn.query(data=queryData)
        if queryResponse.json()['result'][0]['trafficItem'] == []:
            print('\nNo such Traffic Item name found: %s' % trafficItemName)
            return
        configElementObj = queryResponse.json()['result'][0]['trafficItem'][0]['configElement'][0]['href']
        middleware.trafficObj.configTrafficItem(mode='modify', obj=configElementObj, configElements={'frameSize': frameSize})

    def setframerate(trafficItemName, frameRate):
        """Modify the frame rate.

        :param trafficItemName: (str) The Traffic Item name.
        :param frameRate: (int) The frame rate to set."""
        queryData = {'from': '/traffic',
            'nodes': [{'node': 'trafficItem', 'properties': ['name'], 'where': [{'property': 'name', 'regex': trafficItemName}]},
                        {'node': 'configElement', 'properties': [], 'where': []}]}
        queryResponse = middleware.ixn.query(data=queryData)
        if queryResponse.json()['result'][0]['trafficItem'] == []:
            print('\nNo such Traffic Item name found: %s' % trafficItemName)
            return
        configElementObj = queryResponse.json()['result'][0]['trafficItem'][0]['configElement'][0]['href']
        middleware.trafficObj.configTrafficItem(mode='modify', obj=configElementObj, configElements={'frameRate': frameRate})

    def setframecount(trafficItemName, frameCount):
        """Modify the frame count.

        :param trafficItemName: (str) The Traffic Item name.
        :param frameCount: (int) The total packets to send."""
        queryData = {'from': '/traffic',
            'nodes': [{'node': 'trafficItem', 'properties': ['name'], 'where': [{'property': 'name', 'regex': trafficItemName}]},
                        {'node': 'configElement', 'properties': [], 'where': []}]}
        queryResponse = middleware.ixn.query(data=queryData)
        if queryResponse.json()['result'][0]['trafficItem'] == []:
            print('\nNo such Traffic Item name found: %s' % trafficItemName)
            return
        configElementObj = queryResponse.json()['result'][0]['trafficItem'][0]['configElement'][0]['href']
        middleware.trafficObj.configTrafficItem(mode='modify', obj=configElementObj, configElements={'frameCount': frameCount})

    def settrafficcontinuous(trafficItemName):
        """Modify the transmission type to transmit continuously.

        :param trafficItemName: (str) The Traffic Item name."""
        queryData = {'from': '/traffic',
            'nodes': [{'node': 'trafficItem', 'properties': ['name'], 'where': [{'property': 'name', 'regex': trafficItemName}]},
                        {'node': 'configElement', 'properties': [], 'where': []}]}
        queryResponse = middleware.ixn.query(data=queryData)
        if queryResponse.json()['result'][0]['trafficItem'] == []:
            print('\nNo such Traffic Item name found: %s' % trafficItemName)
            return
        configElementObj = queryResponse.json()['result'][0]['trafficItem'][0]['configElement'][0]['href']
        middleware.trafficObj.configTrafficItem(mode='modify', obj=configElementObj, configElements={'transmissionType': 'continuous'})

    def setfixedframes(trafficItemName):
        """Modify the transmission type to transmit a fixed frame count.

        :param trafficItemName: (str) The Traffic Item name."""
        queryData = {'from': '/traffic',
            'nodes': [{'node': 'trafficItem', 'properties': ['name'], 'where': [{'property': 'name', 'regex': trafficItemName}]},
                        {'node': 'configElement', 'properties': [], 'where': []}]}
        queryResponse = middleware.ixn.query(data=queryData)
        if queryResponse.json()['result'][0]['trafficItem'] == []:
            print('\nNo such Traffic Item name found: %s' % trafficItemName)
            return
        configElementObj = queryResponse.json()['result'][0]['trafficItem'][0]['configElement'][0]['href']
        middleware.trafficObj.configTrafficItem(mode='modify', obj=configElementObj, configElements={'transmissionType': 'fixedFrameCount'})

    def configcustompayload(trafficItemName=None, customRepeat=True, customPattern=None):
        """Configure custom frame payload.

        :param trafficItemName: (str) The Traffic Item name.
        :param customRepeat: (bool) True|False:  Repeate the frame custom pattern.
        :param customPattern: (str) The custom payload pattern."""
        queryData = {'from': '/traffic',
                    'nodes': [{'node': 'trafficItem', 'properties': ['name'],
                               'where': [{'property': 'name', 'regex': trafficItemName}]},
                              {'node': 'configElement', 'properties': [], 'where': []}
                          ]}
        queryResponse = middleware.ixn.query(data=queryData)
        configElementObj = queryResponse.json()['result'][0]['trafficItem'][0]['configElement'][0]['href']
        middleware.trafficObj.configFramePayload(configElementObj, payloadType='custom',
                                                 customRepeat=customRepeat, customPattern=customPattern)

    def flapbgp(topologyName=None, bgpName=None, enableTrueOrFalse=True, ipInterfaceList='all', upTimeInSeconds=0, downTimeInSeconds=0):
        """Config BGP flapping.

        :param topologyName: (str) The Topolgy Group name where the BGP stack resides in.
        :param enableTrueOrFalse: (bool) True|False: Enable or disable BGP flapping.
        :param ipInterfaceList: (list) A list of the local BGP IP interface to configure for flapping.
        :param upTimeInSeconds: (int) The up time for BGP to remain up before flapping it down.
        :param downTimeInSeconds: (int) The down time for BGP to remain down before flapping it back up."""
        queryData = {'from': '/',
                    'nodes': [{'node': 'topology', 'properties': ['name'], 'where': [{'property': 'name', 'regex': topologyName}]},
                              {'node': 'deviceGroup', 'properties': [], 'where': []},
                              {'node': 'ethernet', 'properties': [], 'where': []},
                              {'node': 'ipv4', 'properties': [], 'where': []},
                              {'node': 'bgpIpv4Peer', 'properties': ['name'], 'where': [{'property': 'name', 'regex': bgpName}]}]}
        queryResponse = middleware.ixn.query(data=queryData)
        if queryResponse.json()['result'][0]['topology'] == []:
            print('\nNo such Topology Group name found: %s' % topologyName)
            return
        if queryResponse.json()['result'][0]['topology'][0]['deviceGroup'][0]['ethernet'][0]['ipv4'][0]['bgpIpv4Peer'] == []:
            print('\nNo such bgpIpv4Peer name found %s' % bgpName)
            return
        bgpObject = queryResponse.json()['result'][0]['topology'][0]['deviceGroup'][0]['ethernet'][0]['ipv4'][0]['bgpIpv4Peer'][0]['href']
        middleware.protocolObj.flapBgpPeerNgpf(bgpObjHandle=bgpObject, enable=enableTrueOrFalse, flapList=ipInterfaceList,
                                         uptime=upTimeInSeconds, downtime=downTimeInSeconds)

    def configbgp(jsonConfigFile=None, licenseServerIp=None, licenseMode=None, licenseTier=None):
        """Configure BGP and Traffic Item from scratch.  Getting all the settings from the user
        defined JSON config file.

        :param jsonConfigFile: (str) The JSON parameter file to load for this configuration."""
        if jsonConfigFile == None:
            if middleware.preference.ixncfgConfigFile:
                readjsonparamfile(middleware.preference.ixncfgConfigFile)
            else:
                print('\nError: No json config file was provided to build configuration from scratch.\n')
                return
        else:
            readjsonparamfile(jsonConfigFile)

        '''
        middleware.ixn.connectIxChassis(middleware.params['ixChassisIp'])
        if middleware.portMgmtObj.arePortsAvailable(middleware.params['portList'], raiseException=False) != 0:
            if middleware.params['forceTakePortOwnership'] == True:
                middleware.portMgmtObj.releasePorts(middleware.params['portList'])
                middleware.portMgmtObj.clearPortOwnership(middleware.params['portList'])
            else:
                raise IxNetRestApiException('Ports are owned by another user and forceTakePortOwnership is set to False')

        # Configuring license requires releasing all ports even for ports that is not used for this test.
        middleware.portMgmtObj.releaseAllPorts()
        middleware.ixn.configLicenseServerDetails(middleware.params['licenseServerIp'],
                                                  middleware.params['licenseMode'], middleware.params['licenseTier'])
        '''
        if licenseServerIp:
            middleware.preference.licenseServerIp = licenseServerIp
        if licenseMode:
            middleware.preference.licenseMode = licenseMode
        if licenseTier:
            middleware.preference.licenseTier = licenseTier

        if middleware.preference.licenseServerIp == None:
            print('\nNo licenseServerIp is set or included on this command line')
            return

        if middleware.preference.chassisIp == None:
            middleware.preference.chassisIp = middleware.params['ixChassisIp']
        middleware.ixn.connectIxChassis(middleware.preference.chassisIp)
        if middleware.preference.portList == None:
            middleware.preference.portList = middleware.params['portList']

        if middleware.portMgmtObj.arePortsAvailable(middleware.preference.portList, raiseException=False) != 0:
            if middleware.preference.forceTakePortOwnership == True:
                middleware.portMgmtObj.releasePorts(middleware.preference.portList)
                middleware.portMgmtObj.clearPortOwnership(middleware.preference.portList)
            else:
                raise IxNetRestApiException('Ports are owned by another user and forceTakePortOwnership is set to False')

        # Configuring license requires releasing all ports even for ports that is not used for this test.
        middleware.portMgmtObj.releaseAllPorts()
        middleware.ixn.configLicenseServerDetails([middleware.preference.licenseServerIp],
                                                  middleware.preference.licenseMode,
                                                  middleware.preference.licenseTier)
        middleware.ixn.newBlankConfig()
        middleware.portMgmtObj.assignPorts(middleware.preference.portList, createVports=True)

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

            topologyObj = middleware.protocolObj.createTopologyNgpf(portList=properties['ports'],
                                                                    topologyName='Topo-{0}'.format(topology))
            
            topologyObjects.update({'topology{0}'.format(topology): topologyObj})

            deviceGroupObj = middleware.protocolObj.createDeviceGroupNgpf(topologyObj,
                                                                          multiplier=properties['totalIpInterfaces'],
                                                                          deviceGroupName='DG1')

            ethernetObj = middleware.protocolObj.createEthernetNgpf(deviceGroupObj,
                                                                    ethernetName='MyEth1',
                                                                    macAddress=macAddress,
                                                                    macAddressPortStep='disabled',
                                                                    vlanId=vlan)

            if middleware.params['topologies'][topology]['ipv4Address']['start'] is not 0:
                ipv4Obj = middleware.protocolObj.createIpv4Ngpf(ethernetObj,
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
                bgpObj = middleware.protocolObj.configBgp(ipv4Obj,
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
                print('Creating Network Group:', properties['routeAdvertisementName'])
                networkGroupObj = middleware.protocolObj.configNetworkGroup(
                    create=deviceGroupObj,
                    name=properties['routeAdvertisementName'],
                    multiplier = properties['totalAdvertisingRoutes'],
                    networkAddress = {'start': properties['routeAdvertisements'],
                                      'step': properties['routeAddressStep'],
                                      'direction': 'increment'},
                    prefixLength = properties['routeAdvertisingPrefix'])
                
        middleware.protocolObj.startAllProtocols()
        middleware.protocolObj.verifyProtocolSessionsNgpf()

        isAnyTrafficItemConfigured = 0
        for trafficItemNum,properties in middleware.params['trafficItems'].items():
            if properties['enabled'] == False:
                continue

            isAnyTrafficItemConfigured = 1
            # For all parameter options, go to the API configTrafficItem.
            # mode = create or modify
            trafficStatus = middleware.trafficObj.configTrafficItem(
                mode='create',
                trafficItem = {
                    'name':properties['name'],
                    'trafficType':'ipv4',
                    'biDirectional':properties['bidirectional'],
                    'srcDestMesh':'one-to-one',
                    'routeMesh':'oneToOne',
                    'allowSelfDestined':False,
                    'trackBy': ['flowGroup0']},
                endpoints = [({'name':'Flow-Group-1',
                               'sources': [topologyObjects[middleware.params["trafficItems"][trafficItemNum]['srcEndpoint']]],
                               'destinations': [topologyObjects[middleware.params["trafficItems"][trafficItemNum]['dstEndpoint']]]},
                              {'highLevelStreamElements': None})],
                configElements = [{'transmissionType': properties['transmissionType'],
                                   'frameCount': properties['frameCount'],
                                   'frameRate': properties['frameRate'],
                                   'frameRateType': properties['frameRateType'],
                                   'frameSize': properties['frameSize']}])
            
        if isAnyTrafficItemConfigured == 0:
            raise IxNetRestApiException('No Traffic Item was enabled for configuring')

    def configmpls(jsonConfigFile=None, chassisIp=None, portList=None,  licenseServerIp=None, licenseMode=None, licenseTier=None):
        """Configure MPLS raw Traffic Item.  Getting all the settings from the user
        defined JSON config file.

        :param jsonConfigFile: (str) The JSON parameter file to load for this configuration.
        :param chassisIp: (str) The Ixia chassis IP address.
        :param portList: (list) Example: [chassisIp, slotNumber, portNumber] => [["192.168.70.11", "1", "1"], ["192.168.70.11", "2", "1"]]
        """
        if jsonConfigFile == None:
            if middleware.preference.ixncfgConfigFile:
                readjsonparamfile(middleware.preference.ixncfgConfigFile)
            else:
                print('\nError: No json config file was provided to build configuration from scratch.\n')
                return
        else:
            readjsonparamfile(jsonConfigFile)

        if licenseServerIp:
            middleware.preference.licenseServerIp = licenseServerIp
        if licenseMode:
            middleware.preference.licenseMode = licenseMode
        if licenseTier:
            middleware.preference.licenseTier = licenseTier

        if middleware.preference.licenseServerIp == None:
            print('\nNo licenseServerIp is set or included on this command line')
            return

        if chassisIp == None:
            if middleware.preference.chassisIp == None:
                print('\nError: You must provide the chassisIp\n')
                return
        else:
            middleware.preference.chassisIp == chassisIp

        if portList == None:
            if middleware.preference.portList == None:
                print('\nError: You must provide a portList\n')
                return
        else:
            middleware.preference.portList = portList

        middleware.ixn.connectIxChassis(middleware.preference.chassisIp)

        if middleware.portMgmtObj.arePortsAvailable(middleware.preference.portList, raiseException=False) != 0:
            if middleware.preference.forceTakePortOwnership == True:
                middleware.portMgmtObj.releasePorts(middleware.preference.portList)
                middleware.portMgmtObj.clearPortOwnership(middleware.preference.portList)
            else:
                raise IxNetRestApiException('Ports are owned by another user and forceTakePortOwnership is set to False')

        # Configuring license requires releasing all ports even for ports that is not used for this test.
        middleware.portMgmtObj.releaseAllPorts()
        middleware.ixn.configLicenseServerDetails([middleware.preference.licenseServerIp],
                                                  middleware.preference.licenseMode,
                                                  middleware.preference.licenseTier)
        middleware.ixn.newBlankConfig()
        vportList = middleware.portMgmtObj.assignPorts(middleware.preference.portList, createVports=True, rawTraffic=True)

        for trafficItem in middleware.params['trafficItems']:
            if trafficItem['enabled'] == False:
                continue

            # For all parameter options, go to the API configTrafficItem.
            # mode = create or modify
            trafficStatus = middleware.trafficObj.configTrafficItem(
                mode='create',
                trafficItem = {
                    'name': trafficItem['name'],
                    'trafficType': 'raw',
                    'biDirectional': trafficItem['bidirectional'],
                    'srcDestMesh': 'one-to-one',
                    'routeMesh': 'oneToOne',
                    'allowSelfDestined': False,
                    'trackBy': trafficItem['trackBy']},
                endpoints = [({'name':'Flow-Group-1',
                               'sources': [vportList[0]],
                               'destinations': [vportList[1]]},
                              {'highLevelStreamElements': None})],
                configElements = [{'transmissionType': trafficItem['configElement']['transmissionType'],
                                   'frameCount': trafficItem['configElement']['frameCount'],
                                   'frameRate': trafficItem['configElement']['frameRate'],
                                   'frameRateType': trafficItem['configElement']['frameRateType'],
                                   'frameSize': trafficItem['configElement']['frameSize']
                               }])                

            trafficItem1Obj  = trafficStatus[0]
            endpointObj      = trafficStatus[1][0]
            configElementObj = trafficStatus[2][0]
            stackNumber = 1

            # This will show you all the available protocol header options to create
            #middleware.trafficObj.showProtocolTemplates(configElementObj)

            # Show the configured packet headers in sequential order to get the stack ID.
            #middleware.trafficObj.showTrafficItemPacketStack(configElementObj)
            # 1: Ethernet II
            # 2: MPLS
            # 3: IPv4
            # 4: FCS

            stackObj = middleware.trafficObj.getPacketHeaderStackIdObj(configElementObj, stackId=1)
            # Show a list of field names in order to know which field to configure the mac addresses.
            #middleware.trafficObj.showPacketHeaderFieldNames(stackObj)

            for stack in trafficItem['configElement']['stack'].keys():
                if stack == 'mac':
                    middleware.trafficObj.configPacketHeaderField(
                        stackObj,
                        fieldName='Destination MAC Address',
                        data={'valueType':  trafficItem['configElement']['stack']['mac']['dst']['direction'],
                              'startValue': trafficItem['configElement']['stack']['mac']['dst']['start'],
                              'stepValue':  trafficItem['configElement']['stack']['mac']['dst']['step'],
                              'countValue': trafficItem['configElement']['stack']['mac']['dst']['count']
                              })

                    middleware.trafficObj.configPacketHeaderField(
                        stackObj,
                        fieldName='Source MAC Address',
                        data={'valueType':  trafficItem['configElement']['stack']['mac']['src']['direction'],
                              'startValue': trafficItem['configElement']['stack']['mac']['src']['start'],
                              'stepValue':  trafficItem['configElement']['stack']['mac']['src']['step'],
                              'countValue': trafficItem['configElement']['stack']['mac']['src']['count']
                          })

                if stack == 'mpls':
                    for mplsStack in trafficItem['configElement']['stack']['mpls']:
                        stackObj = middleware.trafficObj.addTrafficItemPacketStack(
                            configElementObj, protocolStackNameToAdd='MPLS', stackNumber=stackNumber, action='append')
                        stackNumber += 1
                        # Just an example to show a list of field names in order to know which field to configure the IP addresses.
                        middleware.trafficObj.showPacketHeaderFieldNames(stackObj)
                        middleware.trafficObj.configPacketHeaderField(
                            stackObj,
                            fieldName='Label Value',
                            data={'valueType':  mplsStack['direction'],
                                  'startValue': mplsStack['start'],
                                  'stepValue':  mplsStack['step'],
                                  'countValue': mplsStack['count'],
                                  'auto': False})

                if stack == 'ipv4':
                    stackObj = middleware.trafficObj.addTrafficItemPacketStack(
                        configElementObj, protocolStackNameToAdd='IPv4', stackNumber=stackNumber, action='append')
                    middleware.trafficObj.showPacketHeaderFieldNames(stackObj)
                    middleware.trafficObj.configPacketHeaderField(
                        stackObj,
                        fieldName='Source Address',
                        data={'valueType':  trafficItem['configElement']['stack']['ipv4']['src']['direction'],
                              'startValue': trafficItem['configElement']['stack']['ipv4']['src']['start'],
                              'stepValue':  trafficItem['configElement']['stack']['ipv4']['src']['step'],
                              'countValue': trafficItem['configElement']['stack']['ipv4']['src']['count']})

                    middleware.trafficObj.configPacketHeaderField(
                        stackObj,
                        fieldName='Destination Address',
                        data={'valueType':  trafficItem['configElement']['stack']['ipv4']['dst']['direction'],
                              'startValue': trafficItem['configElement']['stack']['ipv4']['dst']['start'],
                              'stepValue':  trafficItem['configElement']['stack']['ipv4']['dst']['step'],
                              'countValue': trafficItem['configElement']['stack']['ipv4']['dst']['count']})
                                
    def getInput(prompt):
        """Support Python 2 and 3 for input and raw_input.

        :param prompt: The input/raw_input prompt for user interaction.
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

    """
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
    """

except (IxNetRestApiException, Exception, KeyboardInterrupt) as errMsg:
    if enableDebugTracing == True:
        print('\nGOT TO TRACIING')
        if not bool(re.search('ConnectionError', traceback.format_exc())):
            print('\n%s' % traceback.format_exc())
    print('\nException Error! %s\n' % errMsg)
    if 'ixn' in locals() and middleware.apiServerType == 'linux':
        ixn.linuxServerStopAndDeleteSession()
    if 'ixn' in locals() and middleware.onnectToApiServer in ['windows', 'windowsConnectionMgr']:
        if middleware.releasePortsWhenDone and middleware.forceTakePortOwnership:
            middleware.protocolObj.releasePorts(portList)
        if middleware.apiServerType == 'windowsConnectionMgr':
            middleware.ixn.deleteSession()


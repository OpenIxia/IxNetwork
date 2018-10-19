"""
PLEASE READ DISCLAIMER

    This is a sample script for demo and reference purpose only.
    It is subject to change for content updates without warning.

Author: Hubert Gee

 REQUIREMENTS
    - Python2.7.9+
    - Python modules: requests
    - preference.py:  
         - Make a copy of the preference.py template file and give it
           any name.
    
    - All the IxNetwork ReST API modules:
         IxNetRestApi.py
         IxNetRestApiPortMgmt.py
         IxNetRestApiFileMgmt.py
         IxNetRestApiTraffic.py
         IxNetRestApiProtocol.py
         IxNetRestApiStatistics.py

 DESCRIPTION
    This is a utility that emulates a CLI in a Python shell.
    Please read the DOC for all the details.

        - Connecting to a Windows IxNetwork API server or Linux API server.
        - Either create a config from scratch or load a saved config file (json or ixncfg).
        - Assign ports
        - Start protocols
        - Verify protocol sessions
        - Create a Traffic Item
        - Apply Traffic
        - Start Traffic
        - Get stats

 USAGE
    - Enter: python shell
    - Enter: from ixnetCli import *

    - Step 1 of 3:
         setpreferences(<preference file>)

    - Step 2 of 3:
         enter either: connecttowindows() or connecttolinux()

    - Step 3 of 3:
         Build a configuration with one of the options:
            1> config('file.py')
            2> loadsavedconfig('ConfigFiles/<saved config file>')

    - starttraffic()
    - getstats()

    - If you need help, enter: showcommands()

UTILITIES
    - showconfigfiles()
    - showpreferencefiles()
    - showtopologies()
    - showtrafficitems()
    - showallsessions()
"""

from __future__ import absolute_import, print_function, division
import os, sys, inspect, traceback, platform, subprocess
import importlib
from collections import OrderedDict

sys.path.insert(0, (os.path.dirname(os.path.abspath(__file__).replace('Utilities/IxNetCli', 'Modules'))))
sys.path.insert(0, (os.path.dirname(os.path.abspath(__file__))+'/Preferences'))
sys.path.insert(0, (os.path.dirname(os.path.abspath(__file__))+'/ConfigFiles'))
from IxNetRestApi import *
from IxNetRestApiPortMgmt import PortMgmt
from IxNetRestApiFileMgmt import FileMgmt
from IxNetRestApiTraffic import Traffic
from IxNetRestApiProtocol import Protocol
from IxNetRestApiStatistics import Statistics

class middleware:
    preference = None
    setpreferences = False
    resume = False
    connectedTo = None
    sessionId = None
    apiKey = None
    linuxServerSessionId = None
    sessionHeader = None ;# /api/v1/session/<id>/ixnetwork
    connected = False ;# Internal use only. Verify if user is connected to an api server.
    params = None ;# Internal use only. From readjsonparamfile.
    ixn = None
    portMgmtObj = None
    fileMgmtObj = None
    trafficObj = None
    protocolObj = None
    statsObj = None

try:
    def showquickhelp():
        print()
        print("\nStep 1> Enter: setpreferences('<preference file>')")
        print('        To see all preference files, enter: showpreferencefiles()')
        print()
        print('Step 2> Enter: connecttowindows()  or  connecttolinux()')
        print('        To connect to an existing session ID, enter: connecttolinux(resume=True, sessionId=<id>)')
        print()
        print('Step 3> Make your configuration:')
        print("        Enter: config('l2l3Params.py')") 
        print("        Enter: loadsavedconfig('ConfigFiles/<saved config file>')")
        print("        To see all config files, enter: showconfigfiles()")
        print()
        print("See all options, enter: showcommands()")
        print()
        
    def showcommands(command=None, showall=None):
        """Show all the API commands.

        param: showall: None|showall: Enter "showall" to include the descriptions."""
        # pydoc.help(ixnetPyCli)
        if command == None:
            print('\nCommand list:\n')
        else:
            print('\tHelp on command usage: {0}'.format(command))

        for name,obj in inspect.getmembers(sys.modules[__name__]):
            if name in ['completer', 'runixncfgconfig', 'runjsonconfig', 'getInput', 'configIxNetworkFromScratch']: continue
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

                if showall is not None:
                    print('\t{0}'.format(eval(name+'.__doc__')))
                    print()
        print()

        if command == None:
            print('\n\n  Example:')
            print('\tThe first thing you need to do is create a preference file in the /Preferences directory.')
            print('\tMake a copy of the provided template.py and give it a meaningful name.')
            print('\t   Ex: joe.py')

            print('\n\t1> Enter: setpreferences("Your preference file")')
            print('\n\t2> For Windows chassis connection, enter: connecttowindows()')
            print('\t   For Linux chassis connection, enter:   connecttolinux()')
            print('\t       To connect to an existing Linx session ID: connecttolinux(resume=True, sessionId=<id>)')
            print()    
            print('\t3> To load a saved config file and use the chassisIp/ports saved in the config file:')
            print('\t      Enter: loadsavedconfig("ConfigFiles/<config file>")')
            print()
            print('\t   To load a saved config file and optionally assign chassis and ports:')
            print('\t      Enter: loadsavedconfig("ConfigFiles/<config file>", chassisIp=<ip>, ')
            print('\t                             portList=[[ixChassisIp, "1", "1"], [ixChassisIp, "2", "1"]])')
            print()
            print('\t   To create a configuration from scratch:')
            print('\t      Enter: config("ConfigFiles/<params file>")')
            print()

    def setpreferences(preferenceFile):
        """Set user preferences.

        :param preferenceFile: A user defined preference file.
        """
        match = re.match('(.*/)?(.*).py', preferenceFile)
        if match:
            print('\nSetting preference file: %s\n' % match.group(2))
            try:
                middleware.preference = importlib.import_module(match.group(2))
            except:
                print('Error: No such prefernce file found: {}\n'.format(preferenceFile))

        middleware.setpreferences = True

    def showpreferences():
        """Show user defined preferences"""
        print()
        for property,value in middleware.preference.__dict__.items():
            if property.startswith('_') and not callable(property): continue
            print('\t{0}: {1}'.format(property, value))
        print()

    def showpreferencefiles():
        """Show all preference files in the /Preferences directory"""
        process = subprocess.check_output(['ls', os.path.dirname(os.path.abspath(__file__))+'/Preferences'])
        print()
        for eachFile in process.decode('utf-8').split('\n'):
            if '__' not in eachFile and '~' not in eachFile:
                print('   {}'.format(eachFile))

    def showconfigfiles():
        """Show all preference files in the /Preferences directory"""
        process = subprocess.check_output(['ls', os.path.dirname(os.path.abspath(__file__))+'/ConfigFiles'])
        print()
        for eachFile in process.decode('utf-8').split('\n'):
            if '__' not in eachFile and '~' not in eachFile:
                print('   {}'.format(eachFile))

    def showallsessions():
        allSessionId = middleware.ixn.getAllSessionId()

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

    def deletesession():
        """Delete the current session ID on the Linux API server.
        This command is only for connecting to the Linux API server."""
        if middleware.linuxServerSessionId != None:
            middleware.ixn.linuxServerStopOperations(middleware.linuxServerSessionId)
            middleware.ixn.linuxServerDeleteSession(middleware.linuxServerSessionId)
            middleware.linuxServerSessionId = None
            middleware.sessionId = None
        else:
            print('\nThere is currently no opened Linux sessions\n')

    def connecttolinux(apiServerIp=None, serverIpPort=None, resume=False,
                       apiKey=None, sessionId=None, username='admin', password='admin', deleteSessionAfterTest=True):
        """Connect to a Linux API server.

        :param apiServerIp: (str) The API server IP address.
        :param serverIpPort: (int) The API server TCP port.
        :param resume: (bool) True|False: To connect to an existing session.
        :param apiKey: (str) The Linux API server user account's API Key.
        :param sessionId: (int) The session ID.
        :param username: (str) The login username.
        :param password: (str) The login password.
        :param deleteSessionAfterTest: (bool) True|False: To Delete the session when test is done.
        """
        if middleware.setpreferences == False:
            print("\nError: You must enter setpreferences('<preference file>.py') prior to connecting\n")
            return

        middleware.preference.apiServerType = 'linux'

        connect(apiServerIp=apiServerIp, serverIpPort=serverIpPort,
                resume=resume, apiKey=apiKey, sessionId=sessionId, username=username, password=password,
                deleteSessionAfterTest=deleteSessionAfterTest)

    def connecttowindows(apiServerIp=None, serverIpPort=None, resume=False):
        """Connect to a Windows API server.

        :param serverIp: (str) The API server IP address.
        :param apiServerIpPort: (int) The API server TCP port.
        :param resume: (bool) True|False: To connect to an existing session.
        """
        middleware.preference.apiServerType = 'windows'
        connect(apiServerIp=apiServerIp, serverIpPort=serverIpPort, resume=resume)

    def connect(apiServerIp=None, serverIpPort=None, resume=False,
                apiKey=None, sessionId=None, username='admin', password='admin', deleteSessionAfterTest=True):
        """Internal use only. Used by connecttowindows and connecttolinux.  Connect to an API server.

        :param apiServerType: (str) windows|linux.
        :param resume: (bool) True|False: To connect to an existing configuration.
                       If apiServerType is Linux, provide the apiServerIpAddress, apiServerIpPort, apiKey and sessionId number.
                       If apiServerType is windows, provide the apiServerIpAddress and apiServerIpPort.
        :param apiServerIp: (str): The IP address of the IxNetwork API server to connect to.
        :param serverIpPort: (int): The API server IP port number to use.
                        Windows default port = 11009.
                        Linux default port = 443.
        :param apiKey: (str): For Linux API server only. The API-KEY of the Linux API server.
                        You could get this in the Web UI, under My Account, and in show API-KEY.
        :param sessionId: (int): For Linux API server only. The existing session ID to connect to.
        :param username: For Linux API serer only. The login username.
        :param password: For Linux API server only. The login password.

        Example:
           - To make a new Windows connection: apiServerType='windows', apiServerIp=<ip>, apiServerIpPort=<ipPort>
           - To make a new Linux connection: apiServerType='linux', apiServerIp=<ip>, apiSeverIpPort=<ipPort>
           - To resume on Linux: resume=True, apiKey=<apiKey>, sessionId=<session ID>,
           - To resume on Windows with currently connected apiServerIp: resume=True, apiServerIp=<apiServerIp>
           - To resume on Windows with a different apiServerIp: resume='windows', apiServerIp=<apiServerIp>, apiServerIpPort=<apiSeverIpPort>
           - To resume on WindowConnectionMgr = Not supported."""
        if resume == True:
            middleware.resume = True
            if middleware.preference.apiServerType == 'linux':
                if middleware.preference.apiKey == None and apiKey == None:
                    print('\nError: To resume on Linux API server, you must provide apiKey.\n')
                    return 

                if sessionId == None:
                    print('\nError: To resume on Linux API server, you must provide a sessionId to connect to.\n')
                    return

        if resume == False:
            # Check to see if resuming on Windows
            if middleware.preference.apiServerType == 'windows':
                if apiServerIp == None and middleware.preference.windowsApiServerIp == None:
                    print('\nError: You must include apiServerIp\n') ;# return
                if serverIpPort == None and middleware.preference.windowsApiServerIpPort == None:
                    print('\nError: You must include apiServerIpPort\n') ;# return

                if apiServerIp != None:
                    middleware.preference.windowsApiServerIp = apiServerIp
                if serverIpPort != None:
                    middleware.preference.windowsApiServerIpPort = apiServerIpPort

            if middleware.preference.apiServerType == 'linux':
                if apiServerIp == None and middleware.preference.linuxApiServerIp == None:
                    print('\nError: You must include the apiServerIp\n') ;# return
                if apiServerIp == None and middleware.preference.linuxApiServerIp == None:
                    print('\nError: You must include the apiServerIp\n') ;# return

                if apiServerIp != None:
                    middleware.preference.linuxApiServerIp = apiServerIp
                if serverIpPort != None:
                    middleware.preference.linuxApiServerIpPort = serverIpPort

        if middleware.preference.apiServerType == 'windows':
            ixnObj = Connect(apiServerIp=middleware.preference.windowsApiServerIp,
                          serverIpPort=middleware.preference.windowsApiServerIpPort,
                          serverOs='windows')

            middleware.connectedTo = 'windows'

        if middleware.preference.apiServerType == 'linux':
            if resume == True and apiKey == None:
                apiKey = middleware.preference.apiKey
                
            print('', middleware.preference.linuxApiServerIp, str(middleware.preference.linuxApiServerIpPort), 
                  middleware.preference.username, middleware.preference.password, str(sessionId))

            ixnObj = Connect(apiServerIp=middleware.preference.linuxApiServerIp,
                             serverIpPort=str(middleware.preference.linuxApiServerIpPort),
                             username=middleware.preference.username,
                             password=middleware.preference.password,
                             deleteSessionAfterTest=deleteSessionAfterTest,
                             serverOs='linux',
                             apiKey=apiKey,
                             sessionId=sessionId)

            middleware.connectedTo = 'linux'
            # Record the current apiKey and sessionId
            middleware.apiKey = ixnObj.apiKey
            middleware.linuxServerSessionId = ixnObj.sessionId
            

        middleware.connected = True
        middleware.sessionId = ixnObj.sessionId.split('/')[-1]
        middleware.ixn = ixnObj
        middleware.portMgmtObj = PortMgmt(ixnObj)
        middleware.fileMgmtObj = FileMgmt(ixnObj)
        middleware.trafficObj = Traffic(ixnObj)
        middleware.protocolObj = Protocol(ixnObj)
        middleware.statsObj = Statistics(ixnObj)

        match = re.match('http.*(/api.*ixnetwork)', middleware.ixn.sessionUrl)
        middleware.sessionHeader = match.group(1)
    # This is not the json import/export feature.

    def readjsonparamfile(jsonConfigFile):
        """For internal use only and for building a config from scratch.
        Used by functions that creates configuration from scratch. Read and load a JSON parameters file.

        :param jsonConfigFile: (str) The JSON config file to load."""
        if os.path.exists(jsonConfigFile) is False:
            raise IxNetRestApiException("\nError: JSON config file doesn't exists: %s\n" % jsonConfigFile)

        middleware.params = json.load(open(jsonConfigFile), object_pairs_hook=OrderedDict)
        #middleware.params = json.load(open(jsonConfigFile))

    def loadsavedconfig(configFile=None, chassisIp=None, portList=None, includeCrc=False):
        """A highlevel wrapper to run either a saved json config or an .ixncfg config."""
        if '.json' in configFile:
            runjsonconfig(configFile, chassisIp, portList, includeCrc)

        if '.ixncfg' in configFile:
            runixncfgconfig(configFile, chassisIp, portList, includeCrc)

    def runjsonconfig(jsonConfigFile=None, chassisIp=None, portList=None, includeCrc=False):
        """Loads an exported JSON config file, reassigns ports, verify protocols, start traffic and get stats.

        :param jsonConfigFile: (str) The IxNetwork saved configuration in JSON format.
        :param chassisIp: (str) Optional: Ixia chassis IP address.
                         Defaults to the JSON config chassis IP address.
        :param portList: (list) All the ports to use for this JSON configuration file.
                         The amount of ports must match the amount of configured ports in the JSON config file.
                         Defaults to using all the ports defined in the JSON config file.
                         Input example:  portList = [[ixChassisIp, '1', '1'], [ixChassisIp, '2', '1']]"""

        if middleware.connected == False:
            print('\nError: You must connect to an API server first.\n\tconnectowindows() or connecttolinux()\n')
            return

        if 'json' not in jsonConfigFile:
            print('\nError: The JSON config file doesn\'t have a .json extnesion. Please check your jsonConfigFile value: %s\n' % jsonConfigFile)
            return

        if middleware.preference.licenseServerIp == None:
            print('\nNo licenseServerIp is set or included on this command line')
            return

        if jsonConfigFile == None:
            if middleware.preference.jsonConfigFile == None:
                print('\nYou must include a jsonConfigFile')

            if middleware.preference.jsonConfigFile != None:
                jsonConfigFile = middleware.preference.jsonConfigFile

        # TODO: get only the chassis
        jsonData = middleware.fileMgmtObj.jsonReadConfig(jsonConfigFile)

        if portList == None:
            if middleware.preference.portList == None:
                portList = middleware.fileMgmtObj.getJsonConfigPortList(jsonData)
                if portList == []:
                    raise IxNetRestApiException('\nFailed to get portList from JSON config data\n')

            if middleware.preference.portList != None:
                portList = middleware.preference.portList

        if chassisIp is None:
            if middleware.preference.chassisIp != None:
                chassisIp = middleware.preference.chassisIp

            if middleware.preference.chassisIp == None:
                chassisIp = jsonData['availableHardware']['chassis'][0]['hostname']

        # Need to support multiple chassis's.  If user passed in a string of chassis, convert it to a list.
        if chassisIp is not list:
            chassisIp = chassisIp.split(' ')

        for eachChassisIp in chassisIp:
            middleware.portMgmtObj.connectIxChassis(eachChassisIp)

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
        middleware.fileMgmtObj.importJsonConfigObj(jsonData, option='newConfig')
        middleware.portMgmtObj.assignPorts(portList, configPortName=False)
        middleware.portMgmtObj.verifyPortState()
        middleware.protocolObj.startAllProtocols()
        middleware.protocolObj.verifyAllProtocolSessionsNgpf(timeout=120)
        middleware.trafficObj.startTraffic()
        #getstats(includeCrc=includeCrc)

    def runixncfgconfig(ixncfgConfigFile=None, chassisIp=None, portList=None, includeCrc=False):
        """Loads a saved ixncfg config file, reassign ports, start protocols, verify protocols,
        start traffic and get stats.

        :param ixncfgConfigFile: (str) The IxNetwork saved configuration in ixncfg format.
        :param chassisIp: (str) The chassis IP address.
        :param portList: (list) A list of list containing [[ixChassisIp, 1, 1], [ixChassisIp, 1, 2]]
                         Defaults to using ports configured in the saved config file.
        :param includeCrc: (bool): To include CRC error stats."""
        if middleware.connected == False:
            print('\nError: You must connect to an API server first.\n\tconnectowindows() or connecttolinux()\n')
            return

        if 'ixncfg' not in ixncfgConfigFile:
            print('\nError: The .ixncfg config file doesn\'t have a .ixncfg extension. Please check your ixncfgConfigFile value: %s\n' % ixncfgConfigFile)
            return 

        if ixncfgConfigFile == None:
            if middleware.preference.ixncfgConfigFile == None:
                print('\nYou must provide an .ixncfg config file to load')
                return
            else:
                ixncfgConfigFile = middleware.preference.ixncfgConfigFile

        if middleware.preference.licenseServerIp == None:
            print('\nNo licenseServerIp is set or included on this command line')
            return

        if chassisIp == None:
            if middleware.preference.chassisIp == None:
                print('\nYou must provide the ixChassisIp address')
                return
            else:
                chassisIp = middleware.preference.chassisIp

        # Need to support multiple chassis's.  If user passed in a string of chassis, convert it to a list.
        if chassisIp is not list:
            chassisIp = chassisIp.split(' ')
        for eachChassisIp in chassisIp:
            middleware.portMgmtObj.connectIxChassis(eachChassisIp)

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
                                                  middleware.preference.licenseMode)
             
        middleware.ixn.loadIxncfgConfig = True
        middleware.fileMgmtObj.loadConfigFile(ixncfgConfigFile)
        if portList != None:
            middleware.portMgmtObj.assignPorts(portList)
        middleware.portMgmtObj.verifyPortState()
        middleware.protocolObj.startAllProtocols()
        middleware.protocolObj.verifyProtocolSessionsUp()
        #middleware.trafficObj.startTraffic()
        #getstats(includeCrc=includeCrc)

    def showlinuxsession():
        """Show the Linux API server session ID"""
        print('\nAPI-KEY: {0}'.format(middleware.ixn.apiKey))
        print('Session ID: {0}'.format(middleware.ixn.sessionId.split('/')[-1]))
        print()

    def stoptopology(topologyName='all'):
        """Stop a running Topology Group and all of its protocol stacks.

        :param topologyName: (str) The Topology Group name. 'all' to stop all protocols."""
        if topologyName == 'all':
            middleware.protocolObj.stopAllProtocols()
            return

        queryData = {'from': '/',
                    'nodes': [{'node': 'topology',    'properties': ['name'], 'where': [{'property': 'name', 'regex': topologyName}]}]
                    }
        queryResponse = middleware.ixn.query(data=queryData)
        try:
            topologyObj = queryResponse.json()['result'][0]['topology'][0]['href']
        except:
            print('\nError: Verify the topologyName', topologyName)
        middleware.protocolObj.stopTopology([topologyObj])

    def starttopology(topologyName='all'):
        """Start a Topology Group and all of its protocol stacks.

        :param topologyName: (str) The Topology Group name. 'all' to start all protocols"""
        if topologyName == 'all':
            middleware.protocolObj.startAllProtocols()
            return

        queryData = {'from': '/',
                    'nodes': [{'node': 'topology',    'properties': ['name'], 'where': [{'property': 'name', 'regex': topologyName}]}]
                    }
        queryResponse = middleware.ixn.query(data=queryData)
        try:
            topologyObj = queryResponse.json()['result'][0]['topology'][0]['href']
        except:
            print('\nError: Verify the topologyName', topologyName)
        middleware.protocolObj.startTopology([topologyObj])
        #middleware.protocolObj.verifyProtocolSessionsNgpf()

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

    def starttraffic(applyTraffic=True, regenerateTraffic=True):
        """Start traffic."""
        middleware.trafficObj.startTraffic(applyTraffic=applyTraffic, regenerateTraffic=regenerateTraffic)

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

    def setfixedframes(trafficItemName, frameCount):
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
        middleware.trafficObj.configTrafficItem(mode='modify', obj=configElementObj, configElements={'frameCount': frameCount})

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

    def configIxNetworkFromScratch(chassisIp=None, portList=None):
        if middleware.connected == False:
            print('\nError: You must connect to an API server first.\n\tconnectowindows() or connecttolinux()\n')
            return

        if chassisIp:
            middleware.preference.chassisIp = chassisIp
        else:
            if middleware.preference.chassisIp == None:
                middleware.preference.chassisIp = middleware.params['ixChassisIp']

        middleware.portMgmtObj.connectIxChassis(middleware.preference.chassisIp)

        if portList:
            middleware.preference.portList = portList
        else:
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
                                              )

        if middleware.preference.apiServerType == 'windows' or middleware.resume == True:
            middleware.ixn.newBlankConfig()

        if 'trafficType' in middleware.params and middleware.params['trafficType'] == 'raw':
            vportList = middleware.portMgmtObj.assignPorts(middleware.preference.portList, createVports=True, rawTraffic=True)
        else:
            middleware.portMgmtObj.assignPorts(middleware.preference.portList)

        topologyObjects = {}
        if 'topology' in middleware.params:
            for topologyGroup in middleware.params['topology']:
                topologyObj = middleware.protocolObj.createTopologyNgpf(portList=topologyGroup['ports'],
                                                              topologyName=topologyGroup['name'])

                for deviceGroup in topologyGroup['deviceGroup']:
                    deviceGroupObj = middleware.protocolObj.createDeviceGroupNgpf(topologyObj,
                                                                                  multiplier=deviceGroup['multiplier'],
                                                                                  deviceGroupName=deviceGroup['name'])


                    for ethernet in deviceGroup['ethernet']:
                        ethernetObj = middleware.protocolObj.configEthernetNgpf(
                            deviceGroupObj,
                            name = ethernet['name'],
                            macAddress = {'start': ethernet['macAddress']['start'],
                                          'direction': ethernet['macAddress']['direction'],
                                          'step': ethernet['macAddress']['step']
                                      },
                            macAddressPortStep = ethernet['macAddressPortStep'],
                            vlanId = {'start': ethernet['vlanId']['start'],
                                      'direction': ethernet['vlanId']['direction'],
                                      'step': ethernet['vlanId']['step']
                                })

                        if 'ipv4'in ethernet:
                            for ipv4 in ethernet['ipv4']:
                                ipv4Obj = middleware.protocolObj.configIpv4Ngpf(ethernetObj,
                                                                                ipv4Address = {'start': ipv4['address']['start'],
                                                                                               'direction': ipv4['address']['direction'],
                                                                                               'step': ipv4['address']['step']},
                                                                                ipv4AddressPortStep = ipv4['ipv4AddressPortStep'],
                                                                                gateway = {'start': ipv4['gateway']['start'],
                                                                                           'direction': ipv4['gateway']['direction'],
                                                                                           'step': ipv4['gateway']['step']},
                                                                                gatewayPortStep = ipv4['gatewayPortStep'],
                                                                                prefix = ipv4['prefix'])

                                if 'bgp' in ipv4:
                                    for bgp in ipv4['bgp']:
                                        bgpObj = middleware.protocolObj.configBgp(ipv4Obj,
                                                                                  name = bgp['name'],
                                                                                  enableBgp = True,
                                                                                  dutIp = {'start': bgp['dutIp']['start'],
                                                                                           'direction': bgp['dutIp']['direction'],
                                                                                           'step': bgp['dutIp']['step']
                                                                                       },
                                                                                  localAs2Bytes = bgp['localAs2Bytes'],
                                                                                  type = bgp['type'])
                                if 'ospf' in ipv4:
                                    for ospf in ipv4['ospf']:
                                        ospfObj = middleware.protocolObj.configOspf(ipv4Obj,
                                                                                    name = ospf['name'],
                                                                                    areaId = ospf['areaId'],
                                                                                    neighborIp =ospf['neighborIp'],
                                                                                    helloInterval = ospf['helloInterval'],
                                                                                    areaIdIp = ospf['areaIp'],
                                                                                    networkType = ospf['networkType'],
                                                                                    deadInterval = ospf['deadInterval'])

                    if 'networkGroup' in deviceGroup:
                        for networkGroup in deviceGroup['networkGroup']:
                            networkGroupObj = middleware.protocolObj.configNetworkGroup(
                                create = deviceGroupObj,
                                name = networkGroup['name'],
                                multiplier = networkGroup['multiplier'],
                                networkAddress = {'start': networkGroup['routeRange']['start'],
                                                  'step': networkGroup['routeRange']['step'],
                                                  'direction': networkGroup['routeRange']['direction']
                                              },
                                prefixLength = networkGroup['prefix'])

            middleware.protocolObj.startAllProtocols()
            middleware.protocolObj.verifyProtocolSessionsUp()

        isAnyTrafficItemConfigured = 0
        endpointList = []

        rawTrafficVportIndex = 0 ;# Only used for raw traffic item
        for trafficItem in middleware.params['trafficItems']:
            isAnyTrafficItemConfigured = 1
            endpoints = {}
            endpoints['sources'] = []
            endpoints['destinations'] = []

            for endpoint in trafficItem['endpoints']:
                if 'name' in endpoint:
                    endpoints['name'] = endpoint['name']

                for sources in endpoint['sources']:
                    if 'trafficType' in middleware.params and middleware.params['trafficType'] == 'raw':
                        endpoints['sources'].append(vportList[rawTrafficVportIndex])
                        rawTrafficVportIndex += 1
                    else:
                        endpoints['sources'].append(middleware.sessionHeader + sources)

                for destinations in endpoint['destinations']:
                    if 'trafficType' in middleware.params and middleware.params['trafficType'] == 'raw':
                        endpoints['destinations'].append(vportList[rawTrafficVportIndex])
                        rawTrafficVportIndex += 1
                    else:
                        endpoints['destinations'].append(middleware.sessionHeader + destinations)

            endpointList.append(endpoints)

            trafficStatus = middleware.trafficObj.configTrafficItem(
                mode='create',            
                trafficItem = {
                    'name':          trafficItem['name'],
                    'trafficType':   trafficItem['trafficType'],
                    'biDirectional': trafficItem['bidirectional'],
                    'trackBy':       trafficItem['trackBy']
                },
                endpoints = endpointList,
                configElements = trafficItem['configElements']
            )

            configElementObj = trafficStatus[2][0]
            
            # Configure packet headers for RAW Traffic Item
            for configElement in trafficItem['configElements']:
                if 'packetHeaders' not in configElement:
                    continue
                
                stackNumber = 1
                for packetHeader in configElement['packetHeaders']:
                    if packetHeader == 'mac':
                        stackObj = middleware.trafficObj.getPacketHeaderStackIdObj(configElementObj, stackId=1)
                        if 'dest' in configElement['packetHeaders']['mac']:
                            middleware.trafficObj.configPacketHeaderField(stackObj,
                                                                          fieldName='Destination MAC Address',
                                                                          data=configElement['packetHeaders']['mac']['dest'])

                        if 'src' in configElement['packetHeaders']['mac']:
                            middleware.trafficObj.configPacketHeaderField(stackObj,
                                                                          fieldName='Source MAC Address',
                                                                          data=configElement['packetHeaders']['mac']['src'])
                            
                    if packetHeader == 'mpls':
                        for mplsHeader in configElement['packetHeaders']['mpls']:
                            stackObj = middleware.trafficObj.addTrafficItemPacketStack(configElementObj,
                                                                                       protocolStackNameToAdd='MPLS',
                                                                                       stackNumber=stackNumber, action='append')
                            stackNumber += 1
                            middleware.trafficObj.configPacketHeaderField(stackObj,
                                                                          fieldName='Label Value',
                                                                          data=mplsHeader)

                    if packetHeader == 'ipv4':
                        stackObj = middleware.trafficObj.addTrafficItemPacketStack(configElementObj,
                                                                                   protocolStackNameToAdd='IPv4',
                                                                                   stackNumber=stackNumber, action='append')
                        stackNumber += 1
                        middleware.trafficObj.configPacketHeaderField(stackObj,
                                                                      fieldName='Source Address',
                                                                      data=configElement['packetHeaders']['ipv4']['src'])

                        middleware.trafficObj.configPacketHeaderField(stackObj,
                                                                      fieldName='Destination Address',
                                                                      data=configElement['packetHeaders']['ipv4']['dest'])
 

        if isAnyTrafficItemConfigured == 0:
            raise IxNetRestApiException('No Traffic Item was enabled for configuring')
        
    def config(paramFile=None, chassisIp=None, portList=None):
        """Read a parameter file and onfigure NGPF and Traffic Item from scratch.

        :paramFile: (str) The Python dict parameter file to load for this configuration.
        :chassisIp: (str) The chassis IP address.
        :portList:  (list) [ixChassisIp, cardNumber, portNumber]
        """
        if paramFile == None:
            raise IxNetRestApiException('\nError: You must provide a paramFile\n')

        try:
            middleware.params = __import__(paramFile.split('.')[0]).params
        except:
            print('\nError: No config file found: {}'.format(paramFile))
            return

        # Allow users to overwrite param file chassisIp and portList from cli 
        if chassisIp == None:
            chassisIp = middleware.params['ixChassisIp']
            middleware.preference.chassisIp = chassisIp

        if portList == None:
            portList = middleware.params['portList']
            middleware.preference.portList = portList

        configIxNetworkFromScratch(chassisIp, portList)

    def configmpls(paramFile=None, chassisIp=None, portList=None):
        """Configure MPLS raw Traffic Item.  Getting all the settings from the user
        defined JSON config file.

        :param jsonConfigFile: (str) The JSON parameter file to load for this configuration.
        :param chassisIp: (str) The Ixia chassis IP address.
        :param portList: (list) Example: [chassisIp, slotNumber, portNumber] => [["192.168.70.11", "1", "1"], ["192.168.70.11", "2", "1"]]
        """
        if paramFile == None:
            raise IxNetRestApiException('\nError: You must provide a paramFile\n')

        if os.path.exists(paramFile) is False:
            raise IxNetRestApiException("Param file doesn't exists: %s" % paramFile)

        if middleware.connected == False:
            print('\nError: You must connect to an API server first.\n\tconnectowindows() or connecttolinux()\n')
            return
            
        middleware.params = __import__(paramFile.split('.')[0]).params

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
                    'trackBy': trafficItem['trackBy']
                },
                endpoints = [{'name':'Flow-Group-1',
                              'sources': [vportList[0]],
                              'destinations': [vportList[1]],
                              'highLevelStreamElements': None}
                         ],
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

    showquickhelp()


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


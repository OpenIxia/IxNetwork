"""
Description
   How to bulk modify an existing configuration.
   This sample shows how to use JSON XPath to modify any part of configuration.

Example
   If you want to bulk modify traffic item and vport:
       - trafficItem = fileMgmtObj.exportJsonConfigToDict(['/traffic/descendant-or-self::*'])
       - vport = fileMgmtObj.exportJsonConfigToDict(['/vport/descendant-or-self::*'])

       - Put each xpath and all the attributes that you want to modify in {}
       - You should have two. For example: {'xpath': '/traffic/trafficItem[1]', 'enabled': True}
                                           {'xpath': '/vport[1], 'name': Name}

       - Put them into a list called jsonData.
       - Use this function to send the bulk data to be modified at once:
            fileMgmtObj.importJsonConfigObj(dataObj=jsonData, option='modify')
"""

import re, os, sys, traceback, time

sys.path.insert(0, (os.path.dirname(os.path.abspath(__file__).replace('SampleScripts', 'Modules'))))
from IxNetRestApi import *
from IxNetRestApiProtocol import Protocol
from IxNetRestApiTraffic import Traffic
from IxNetRestApiFileMgmt import FileMgmt
from IxNetRestApiPortMgmt import PortMgmt
from IxNetRestApiStatistics import Statistics
from IxNetRestApiPacketCapture import PacketCapture

# Default the API server to either windows or linux.
osPlatform = 'windows'

try:
    #---------- Preference Settings --------------

    forceTakePortOwnership = True
    releasePortsWhenDone = False
    enableDebugTracing = True
    deleteSessionAfterTest = False ;# For Windows Connection Mgr and Linux API server only

    # If the licenses are activated in the Linux based XGS chassis or if the licenses are configured 
    # in the Windows IxNetwork GUI API server in preferences, then you won't need to config license.
    configLicense = True
    licenseServerIp = '172.16.101.3'
    licenseModel = 'subscription'
    licenseTier = 'tier3'

    ixChassisIp = '172.16.102.5'
    # [chassisIp, cardNumber, slotNumber]
    portList = [[ixChassisIp, '1', '1'],
                [ixChassisIp, '1', '2']]

    if osPlatform == 'linux':
        mainObj = Connect(apiServerIp='172.16.102.2',
                          serverIpPort='443',
                          username='admin',
                          password='admin',
                          deleteSessionAfterTest=deleteSessionAfterTest,
                          verifySslCert=False,
                          serverOs=osPlatform,
                          apiKey=None,
                          sessionId=None,
                          traceLevel='all'
                          )

    if osPlatform in ['windows']:
        mainObj = Connect(apiServerIp='172.16.101.3',
                          serverIpPort='11009',
                          serverOs=osPlatform,
                          deleteSessionAfterTest=deleteSessionAfterTest,
                          traceLevel='all'
                          )
    
    if osPlatform in ['windowsConnectionMgr']:
        mainObj = Connect(apiServerIp='172.16.101.3',
                          serverIpPort='11009',
                          serverOs=osPlatform,
                          deleteSessionAfterTest=deleteSessionAfterTest,
                          sessionId=None,
                          httpsSecured=False,
                          traceLevel='all'
                          )
    
    trafficObj = Traffic(mainObj)
    statObj = Statistics(mainObj)
    protocolObj = Protocol(mainObj)
    portObj = PortMgmt(mainObj)
    fileMgmtObj = FileMgmt(mainObj)

    # How to enable/disable many traffic items at once
    # Step 1of2: Get all the traffic item xpaths
    trafficItemJsonObj = fileMgmtObj.exportJsonConfigToDict(['/traffic/descendant-or-self::*'])
    jsonData = []
    for trafficItem in trafficItemJsonObj['traffic']['trafficItem']:
        data = {'xpath': trafficItem['xpath'], 'enabled': True}
        jsonData.append(data)
        
    # Step 2of2: Use API to send all the xpath data and modify them all at once.
    fileMgmtObj.importJsonConfigObj(dataObj=jsonData, option='modify')


except (IxNetRestApiException, Exception, KeyboardInterrupt) as errMsg:
    print('\nTest failed! {0}\n'.format(traceback.print_exc()))
    print(errMsg)
    if osPlatform == 'linux':
        mainObj.linuxServerStopAndDeleteSession()

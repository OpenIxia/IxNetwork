"""
PLEASE READ DISCLAIMER

    This is a sample script for demo and reference purpose only.
    It is subject to change for content updates without warning.

REQUIREMENTS
    - Python modules: requests

SUPPORTS
    - Python 2.7 and 3+
    - IxNetwork API servers: Windows, WindowsConnectionMgr and Linux

DESCRIPTION
     Capturing packets.
 
     This script assumes that a configuration exist already.
     For Linux API server connection, provide the sessionID and apiKey.
    
     Enable data plane and/or control plane capturing.
     Saved the .cap files (dataPlane and/or controlPlane) to local filesystem.
     Save packet capturing in wireshark style with header details.

     Set traffic to send at continuous mode.

     Tested on Windows and Linux API server.

SYNTAXES
     PATCH: /api/v1/sessions/5/ixnetwork/vport/2
     DATA: {'rxMode': 'captureAndMeasure'}

     PATCH: /api/v1/sessions/5/ixnetwork/vport/2/capture
     DATA: {'softwareEnabled': False, 'hardwareEnabled': True}
 
     # Set traffic item to send continuous packets
     PATCH: /api/v1/sessions/5/ixnetwork/traffic/trafficItem/1/configElement/1/transmissionControl
     DATA: {'type': 'continuous'}

     POST: /api/v1/sessions/5/ixnetwork/traffic/trafficItem/operations/generate
     DATA: {"arg1": ["/api/v1/sessions/5/ixnetwork/traffic/trafficItem/1"]}

     POST: /api/v1/sessions/5/ixnetwork/traffic/operations/apply
     DATA: {"arg1": "/api/v1/sessions/5/ixnetwork/traffic"}

     POST: /api/v1/sessions/5/ixnetwork/traffic/operations/start
     DATA: {"arg1": "https://192.168.70.12/api/v1/sessions/5/ixnetwork/traffic"}

     Start continuous traffic

     POST: /api/v1/sessions/4/ixnetwork/operations/startcapture
     POST: /api/v1/sessions/4/ixnetwork/operations/stopcapture
     POST: /api/v1/sessions/4/ixnetwork/operations/savecapturefiles
     DATA: {"arg1": "packetCaptureFolder"}  <-- This could be any name.  Just a temporary folder to store the captured file.

     Wait for the /operations/savecapturefiles to complete.  May take up to a minute.

     For Windows API server:
         POST: /ixnetwork/operations/copyfile
         DATA: {"arg1": "c:\\Results\\port2_HW.cap", "arg2": "/api/v1/sessions/1/ixnetwork/files/port2_HW.cap"}
         GET: /ixnetwork/files?filename=port2_HW.cap

     For Linux API server:
         POST: /ixnetwork/operations/copyfile
         DATA: {"arg1": "captures/packetCaptureFolder/port2_HW.cap", "arg2": "/api/v1/sessions/<id>/ixnetwork/files/port2_HW.cap"}
         GET: /ixnetwork/files?filename=captures/packetCaptureFolder/port2_HW.cap
 
USAGE
    python <script>.py windows|linux
"""

import re, sys, os, traceback, time

# These  modules are one level above.
sys.path.insert(0, (os.path.dirname(os.path.abspath(__file__).replace('SampleScripts', 'Modules'))))
from IxNetRestApi import *
from IxNetRestApiProtocol import Protocol
from IxNetRestApiTraffic import Traffic
from IxNetRestApiFileMgmt import FileMgmt
from IxNetRestApiPortMgmt import PortMgmt
from IxNetRestApiStatistics import Statistics
from IxNetRestApiPacketCapture import PacketCapture

osPlatform = 'windowsConnectionMgr'

try:
    #---------- Preference Settings --------------
    enableDebugTracing = True
    deleteSessionAfterTest = False

    apiServerIp = '172.16.101.3'
    apiServerIpPort = 11009
    ixChassisIp = '172.16.102.5'
    packetCapturePort = [ixChassisIp, '1', '2']

    if osPlatform in ['windows', 'windowsConnectionMgr']:
        mainObj = Connect(apiServerIp=apiServerIp,
                          serverIpPort=apiServerIpPort,
                          serverOs=osPlatform,
                          traceLevel='all',
                          sessionId=8020
                        )

    if osPlatform == 'linux':
        mainObj = Connect(apiServerIp='172.16.102.2',
                          username='admin',
                          password='admin',
                          deleteSessionAfterTest=deleteSessionAfterTest,
                          verifySslCert=False,
                          serverOs=osPlatform,
                          generateLogFile='ixiaDebug.log',
                          traceLevel='all',
                          sessionId=None,
                          apiKey=None
                      )
        
    #---------- Preference Settings End --------------

    trafficObj = Traffic(mainObj)
    pktCaptureObj = PacketCapture(mainObj)

    # response = mainObj.get(mainObj.sessionUrl+'/vport')
    # name = response.json()[0]['name']

    # Stop the traffic if it is running in order to configure the packet capture modes.
    if trafficObj.checkTrafficState(expectedState=['stopped'], timeout=1, ignoreException=True) == 1:
        trafficObj.stopTraffic()

    trafficObj.checkTrafficState(expectedState=['stopped'], timeout=1, ignoreException=False)

    # portRxMode: Options: capture|captureAndMeasure
    pktCaptureObj.packetCaptureConfigPortMode(port=packetCapturePort,
                                              portRxMode='captureAndMeasure',
                                              enableDataPlane=True, enableControlPlane=False)

    pktCaptureObj.packetCaptureClearTabs()

    # NOTE: Traffic must be sending continuous traffic.  Not fixedFrameCount.
    #       Bluntly modify the traffic item to send at continuous mode.
    trafficItemObj = trafficObj.getAllTrafficItemObjects(getEnabledTrafficItemsOnly=True)[0]
    configElementObj = trafficObj.getConfigElementObj(trafficItemObj=trafficItemObj)
    trafficObj.configTrafficItem(mode='modify',
                                 obj = configElementObj,
                                 configElements = {'transmissionType': 'continuous'})

    trafficObj.startTraffic(regenerateTraffic=True, applyTraffic=True)
    trafficObj.checkTrafficState(expectedState=['started'], timeout=45)

    pktCaptureObj.packetCaptureStart()
    mainObj.logInfo('Wait 10 seconds to capture some packets ...')
    time.sleep(10)
    pktCaptureObj.packetCaptureStop()

    trafficObj.stopTraffic()

    # For Windows API server only: Set saveToTempLocation to a temporary folder in the c: drive. For example: c:\\Results.
    #                              If there is no folder called c:\\Results, it will be created.
    # For Linux API server: Mandatory to state the value as 'linux'
    #
    # typeOfCapture: Options: data|control
    #
    if osPlatform in ['windows', 'windowsConnectionMgr']:
        pktCaptureObj.getCapFile(port=packetCapturePort, typeOfCapture='data', saveToTempLocation='c:\\Results',
                                 localLinuxLocation='.', appendToSavedCapturedFile=None)

    if osPlatform == 'linux':
        pktCaptureObj.getCapFile(port=packetCapturePort, typeOfCapture='data', localLinuxLocation='/home/hgee',
                                 saveToTempLocation='packetCaptureFolder', appendToSavedCapturedFile=None)

    # Optional: Wireshark style details
    pktCaptureObj.packetCaptureGetCurrentPackets(getUpToPacketNumber=5, capturePacketsToFile=True)

    pktCaptureObj.packetCaptureClearTabs()

    if osPlatform == 'linux':
        mainObj.linuxServerStopAndDeleteSession()

    if osPlatform == 'windowsConnectionMgr':
        mainObj.deleteSession()

except (IxNetRestApiException, Exception, KeyboardInterrupt):
    if enableDebugTracing:
        if not bool(re.search('ConnectionError', traceback.format_exc())):
            print('\n%s' % traceback.format_exc())

    if 'mainObj' in locals() and osPlatform == 'linux':
        if deleteSessionAfterTest:
            mainObj.linuxServerStopAndDeleteSession()

    if osPlatform == 'windowsConnectionMgr':
        if deleteSessionAfterTest:
            mainObj.deleteSession()

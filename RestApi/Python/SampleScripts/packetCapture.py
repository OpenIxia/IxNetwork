
# PLEASE READ DISCLAIMER
#
#    This is a sample script for demo and reference purpose only.
#    It is subject to change for content updates without warning.
#
# REQUIREMENTS
#    - Python modules: requests
#
# SUPPORTS
#    - Python 2.7 and 3+
#    - IxNetwork API servers: Windows, WindowsConnectionMgr and Linux
#
# DESCRIPTION
#     Capturing packets.
# 
#     This script assumes that a configuration exist already.
#     For Linux API server connection, provide the sessionID and apiKey.
#    
#     Enable data plane and/or control plane capturing.
#     Saved the .cap files (dataPlane and/or controlPlane) to local filesystem.
#     Save packet capturing in wireshark style with header details.
#
#     Set traffic to send at continuous mode.
#
#     Tested in Windows only.
# 
# USAGE
#    python <script>.py windows|linux

import sys, os, traceback, time

# These  modules are one level above.
sys.path.insert(0, (os.path.dirname(os.path.abspath(__file__).replace('SampleScripts', 'Modules'))))
from IxNetRestApi import *
from IxNetRestApiProtocol import Protocol
from IxNetRestApiTraffic import Traffic
from IxNetRestApiFileMgmt import FileMgmt
from IxNetRestApiPortMgmt import PortMgmt
from IxNetRestApiStatistics import Statistics
from IxNetRestApiPacketCapture import PacketCapture

osPlatform = 'windows'

if len(sys.argv) > 1:
    if sys.argv[1] not in ['windows', 'windowsConnectionMgr', 'linux']:
        sys.exit("\nError: %s is not a known option. Choices are 'windows' or 'linux'." % sys.argv[1])
    osPlatform = sys.argv[1]

try:
    #---------- Preference Settings --------------
    enableDebugTracing = True
    deleteSessionAfterTest = False

    apiServerIp = '192.168.70.3'
    apiServerIpPort = 11009
    ixChassisIp = '192.168.70.128'
    packetCapturePort = [ixChassisIp, '1', '2']

    if osPlatform in ['windows', 'windowsConnectionMgr']:
        mainObj = Connect(apiServerIp=apiServerIp,
                          serverIpPort=apiServerIpPort,
                          serverOs=osPlatform
        )

    if osPlatform == 'linux':
        mainObj = Connect(apiServerIp='192.168.70.12',
                          username='admin',
                          password='admin',
                          deleteSessionAfterTest=deleteSessionAfterTest,
                          verifySslCert=False,
                          serverOs=osPlatform,
                          generateLogFile='ixiaDebug.log',
                          sessionId=12,
                          apiKey='173c9e239c714c8ea73d549c0e62cc82'
                      )
        
    #---------- Preference Settings End --------------

    trafficObj = Traffic(mainObj)
    pktCaptureObj = PacketCapture(mainObj)

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

    # For Windows API server: If there is no folder called c:\\Results, it will be created.
    #                         c:\\Results is an example. Give any name you like for a folder to store the captured file.
    # For Linux API server:   Default location is /home/ixia_logs.
    # 
    # typeOfCapture: Options: data|control
    if osPlatform in ['windows', 'windowsConnectionMgr']:
        pktCaptureObj.getCapFile(port=packetCapturePort, typeOfCapture='data', saveToTempLocation='c:\\Results',
                                 localLinuxLocation='.', appendToSavedCapturedFile=None)

    if osPlatform == 'linux':
        pktCaptureObj.getCapFile(port=packetCapturePort, typeOfCapture='data', saveToTempLocation='Results',
                                 localLinuxLocation='/home/hgee', appendToSavedCapturedFile=None)

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


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
#     Capturing packets. Make sure traffic is configured for continuous mode.
#     Enable data plane and/or control plane capturing.
#     Saved the .cap files (dataPlane and/or controlPlane) to local filesystem.
#     Save packet capturing in wireshark style with header details.
#
#     Tested in Windows only.
# 
# USAGE
#    python <script>.py windows

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

    apiServerIp = '192.168.70.3'
    apiServerIpPort = 11009
    ixChassisIp = '192.168.70.11'
    packetCapturePort = [ixChassisIp, '2', '1']

    if osPlatform in ['windows', 'windowsConnectionMgr']:
        mainObj = Connect(apiServerIp=apiServerIp,
                          serverIpPort=apiServerIpPort,
                          serverOs=osPlatform
        )
        
    #---------- Preference Settings End --------------

    trafficObj = Traffic(mainObj)
    pktCaptureObj = PacketCapture(mainObj)

    # Stop the traffic if it is running in order to configure the packet capture modes.
    if trafficObj.checkTrafficState(expectedState=['stopped'], timeout=1, ignoreException=True) == 1:
        trafficObj.stopTraffic()

    # portRxMode: Options: capture|captureAndMeasure
    pktCaptureObj.packetCaptureConfigPortMode(port=packetCapturePort,
                                              portRxMode='captureAndMeasure',
                                              enableDataPlane=True, enableControlPlane=False)

    pktCaptureObj.packetCaptureClearTabs()
    trafficObj.startTraffic(regenerateTraffic=False, applyTraffic=True)
    trafficObj.checkTrafficState(expectedState=['started'], timeout=45)

    pktCaptureObj.packetCaptureStart()
    time.sleep(10)
    pktCaptureObj.packetCaptureStop()

    # If there is no folder called c:\\Results, it will be created.  c:\\Results is an example. Give any name you like.
    # typeOfCapture: Options: data|control
    pktCaptureObj.getCapFile(port=packetCapturePort, typeOfCapture='data', saveToTempLocation='c:\\Results',
                             localLinuxLocation='.', appendToSavedCapturedFile=None)

    # Optional: Wireshark style details
    pktCaptureObj.packetCaptureGetCurrentPackets(getUpToPacketNumber=5, capturePacketsToFile=True)

    pktCaptureObj.packetCaptureClearTabs()

except (IxNetRestApiException, Exception, KeyboardInterrupt):
    if enableDebugTracing:
        if not bool(re.search('ConnectionError', traceback.format_exc())):
            print('\n%s' % traceback.format_exc())


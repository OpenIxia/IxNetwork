
# PLEASE READ DISCLAIMER
#
#    This is a sample script for demo and reference purpose only.
#    It is subject to change for content updates without warning.
#
# REQUIREMENTS
#    - Python2.7 - Python 3.6
#    - Python module: requests
#
# DESCRIPTION
#     Capturing packets. Make sure traffic is running in continuous mode.
#     Enable data plane and/or control plane capturing.
#     Saved the .cap files (dataPlane and/or controlPlane) to local filesystem.
#     Save packet capturing in wireshark style with header details.
#
#     Tested in Windows only.
# 
# USAGE
#    python <script>.py windows

import sys, traceback, time

sys.path.insert(0, '../Modules')
from IxNetRestApi import *
from IxNetRestApiProtocol import Protocol
from IxNetRestApiTraffic import Traffic
from IxNetRestApiFileMgmt import FileMgmt
from IxNetRestApiPortMgmt import PortMgmt
from IxNetRestApiStatistics import Statistics
from IxNetRestApiPacketCapture import PacketCapture

connectToApiServer = 'windows'

try:
    #---------- Preference Settings --------------
    forceTakePortOwnership = True
    releasePortsWhenDone = False
    enableDebugTracing = True
    deleteSessionAfterTest = True ;# For Windows Connection Mgr and Linux API server only

    # Optional: Mainly for connecting to Linux API server.
    licenseServerIp = '192.168.70.3'
    licenseModel = 'subscription'
    licenseTier = 'tier3'

    ixChassisIp = '192.168.70.11'
    # [chassisIp, cardNumber, slotNumber]
    portList = [[ixChassisIp, '1', '1'],
                [ixChassisIp, '2', '1']]

    if connectToApiServer in ['windows', 'windowsConnectionMgr']:
        mainObj = Connect(apiServerIp='192.168.70.3',
                          serverIpPort='11009',
                          serverOs=connectToApiServer,
                          deleteSessionAfterTest=deleteSessionAfterTest)
        
    #---------- Preference Settings End --------------

    # NOTE: Make sure traffic is running continuously

    pktCaptureObj = PacketCapture(mainObj)
    pktCaptureObj.packetCaptureConfigPortMode([ixChassisIp, '2', '1'], enableDataPlane=True, enableControlPlane=False)
    pktCaptureObj.packetCaptureClearTabs()
    pktCaptureObj.packetCaptureStart()
    time.sleep(10)
    pktCaptureObj.packetCaptureStop()

    # If there is no folder called c:\\Results, it will be created.  c:\\Results is an example. Give any name you like.
    pktCaptureObj.getCapFile(port=[ixChassisIp, '2', '1'], typeOfCapture='data', saveToTempLocation='c:\\Results',
                             localLinuxLocation='.', appendToSavedCapturedFile=None)

    # Optional: Wireshark style details
    pktCaptureObj.packetCaptureGetCurrentPackets(getUpToPacketNumber=5, capturePacketsToFile=True)

    pktCaptureObj.packetCaptureClearTabs()

except (IxNetRestApiException, Exception, KeyboardInterrupt) as errMsg:
    if enableDebugTracing:
        if not bool(re.search('ConnectionError', traceback.format_exc())):
            print('\n%s' % traceback.format_exc())
    print('\nException Error! %s\n' % errMsg)
    if 'mainObj' in locals() and connectToApiServer in ['windows', 'windowsConnectionMgr']:
        if releasePortsWhenDone and forceTakePortOwnership:
            portObj.releasePorts(portList)
        if connectToApiServer == 'windowsConnectionMgr':
            if deleteSessionAfterTest:
                mainObj.deleteSession()

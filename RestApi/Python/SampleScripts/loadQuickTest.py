
# PLEASE READ DISCLAIMER
#
#    This is a sample script for demo and reference purpose only.
#    It is subject to change for content updates without warning.
#
# REQUIREMENTS
#    - Python2.7
#    - Python modules: requests
#    - NGPF configuration. (Classic Framework is not supported in REST)
#
# DESCRIPTION
#    This sample script demonstrates:
#        - REST API configurations using two back-to-back Ixia ports.
#        - Connecting to Windows IxNetwork API server or Linux API server.
#
#    - Verify for sufficient amount of port licenses before testing.
#    - Verify port ownership.
#    - Load a saved NGPF Quick Test config file.
#    - Reassign Ports:  Exclude calling assignPorts if it's unecessary.
#    - Verify port states.
#    - Apply Quick Test
#    - Start Quick Test
#    - Monitor Quick Test progress
#    - Get stats
#
#    This sample script supports both Windows IxNetwork API server and
#    Linux API server.  If connecting to a Linux API server and the API
#    server is newly installed, it configures the one time global license server settings.

import sys, traceback

sys.path.insert(0, '../Modules/Main')
from IxNetRestApi import *
from IxNetRestApiPortMgmt import PortMgmt
from IxNetRestApiFileMgmt import FileMgmt
from IxNetRestApiQuickTest import QuickTest
from IxNetRestApiStatistics import Statistics

# Default the API server to either windows or linux.
connectToApiServer = 'windows'

if len(sys.argv) > 1:
    if sys.argv[1] not in ['windows', 'windowsConnectionMgr', 'linux']:
        sys.exit("\nError: %s is not a known option. Choices are 'windows', 'windowsConnectionMgr or 'linux'." % sys.argv[1])
    connectToApiServer = sys.argv[1]

try:
    #---------- Preference Settings --------------

    forceTakePortOwnership = True
    releasePortsWhenDone = False
    enableDebugTracing = True
    deleteSessionAfterTest = True
    licenseServerIp = '192.168.70.3'
    licenseModel = 'subscription'
    licenseTier = 'tier3'
    configFile = 'QuickTestNgpf_vm8.20.ixncfg'
    quickTestNameToRun = 'QuickTest1'

    ixChassisIp = '192.168.70.11'
    # [chassisIp, cardNumber, slotNumber]
    portList = [[ixChassisIp, '1', '1'],
                [ixChassisIp, '2', '1']]

    if connectToApiServer == 'linux':
        mainObj = Connect(apiServerIp='192.168.70.108',
                          serverIpPort='443',
                          username='admin',
                          password='admin',
                          deleteSessionAfterTest=deleteSessionAfterTest,
                          verifySslCert=False,
                          serverOs=connectToApiServer
                          )

    if connectToApiServer in ['windows', 'windowsConnectionMgr']:
        mainObj = Connect(apiServerIp='192.168.70.3',
                          serverIpPort='11009',
                          serverOs=connectToApiServer,
                          deleteSessionAfterTest=deleteSessionAfterTest)

    #---------- Preference Settings End --------------

    portObj = PortMgmt(mainObj)
    portObj.connectIxChassis(ixChassisIp)

    if portObj.arePortsAvailable(portList, raiseException=False) != 0:
        if forceTakePortOwnership == True:
            portObj.releasePorts(portList)
            portObj.clearPortOwnership(portList)
        else:
            raise IxNetRestApiException('Ports are owned by another user and forceTakePortOwnership is set to False')

    # Uncomment this to configure license server.
    # Configuring license requires releasing all ports even for ports that is not used for this test.
    portObj.releaseAllPorts()
    mainObj.configLicenseServerDetails([licenseServerIp], licenseModel, licenseTier)

    fileMgmtObj = FileMgmt(mainObj)
    fileMgmtObj.loadConfigFile(configFile)
    portObj.assignPorts(portList, createVports=False)
    portObj.verifyPortState()

    quickTestObj = QuickTest(mainObj, fileMgmtObj) 
    quickTestHandle = quickTestObj.getQuickTestHandleByName(quickTestNameToRun)
    print('\nQuickTest Handle:', quickTestHandle)

    quickTestObj.applyQuickTest(quickTestHandle)
    quickTestObj.startQuickTest(quickTestHandle)
    quickTestObj.verifyQuickTestInitialization(quickTestHandle)
    quickTestObj.monitorQuickTestRunningProgress(quickTestHandle, getProgressInterval=3)

    # where: localWindows|remoteWindows|remoteLinux
    # Copy result files from Windows API server to local Windows.
    #quickTestObj.getQuickTestPdf(quickTestHandle, copyToLocalPath='C:\\Results', where='localWindows',
    #                             renameDestinationFile='rfc2544.pdf', includeTimestamp=True)
    #quickTestObj.getQuickTestCsvFiles(quickTestHandle, copyToPath='c:\\Results', csvFile='all')

    # Copy result files from Windows API server to remote Linux.
    quickTestObj.getQuickTestPdf(quickTestHandle, copyToLocalPath='/home/hgee', where='remoteLinux',
                                 renameDestinationFile='rfc2544.pdf', includeTimestamp=True)
    quickTestObj.getQuickTestCsvFiles(quickTestHandle, copyToPath='/home/hgee', csvFile='all')

    statObj = Statistics(mainObj)
    stats = statObj.getStats(viewName='Flow View')

    print('\n{txPort:15} {rxPort:15} {rxThruPut:10} {txFrames:15} {rxFrames:10} {frameLoss:10}'.format(
        txPort='txPort', rxPort='rxPort', rxThruPut='rxThruPut', txFrames='txFrames', rxFrames='rxFrames', frameLoss='frameLoss'))
    print('-'*90)

    for flowGroup,values in stats.items():
        txPort = values['Tx Port']
        rxPort = values['Rx Port']
        rxThroughput = values['Rx Throughput (% Line Rate)']
        txFrameCount = values['Tx Count (frames)']
        rxFrameCount = values['Rx Count (frames)']
        frameLoss = values['Frame Loss (frames)']

        print('{txPort:15} {rxPort:15} {rxThruPut:10} {txFrames:15} {rxFrames:10} {frameLoss:10}'.format(
            txPort=txPort, rxPort=rxPort, rxThruPut=rxThroughput, txFrames=txFrameCount, rxFrames=rxFrameCount, frameLoss=frameLoss))

        '''
        Sample Quick Test stat collection

        Tx Port: Ethernet - 001
        Rx Port: Ethernet - 002
        Traffic Item: Traffic Item 1
        IPv4 :Precedence: 0
        Flow Group: Traffic Item 1-EndpointSet-1 - Flow Group 0001
        Tx Rate (% Line Rate): 10
        Rx Throughput (% Line Rate): 4.701
        Rx Throughput (fps): 69955.021
        Rx Throughput (Mbps): 35.817
        Tx Count (frames): 1488095
        Rx Count (frames): 1488068
        Frame Loss (frames): 27
        Frame Loss (%): 0.002
        Min Latency (ns): 13120
        Max Latency (ns): 257539360
        Avg Latency (ns): 112147705
        RxPortPath: 192.168.70.10/Card02/Port01
        '''

    if releasePortsWhenDone == True:
        portObj.releasePorts(portList)

    if connectToApiServer == 'linux':
        mainObj.linuxServerStopAndDeleteSession()

    if connectToApiServer == 'windowsConnectionMgr':
        mainObj.deleteSession()

except (IxNetRestApiException, Exception, KeyboardInterrupt) as errMsg:
    if enableDebugTracing:
        if not bool(re.search('ConnectionError', traceback.format_exc())):
            print('\n%s' % traceback.format_exc())
    print('\nException Error! %s\n' % errMsg)
    if 'mainObj' in locals() and connectToApiServer == 'linux':
        mainObj.linuxServerStopAndDeleteSession()
    if 'mainObj' in locals() and connectToApiServer == 'windows':
        if releasePortsWhenDone and forceTakePortOwnership:
            portObj.releasePorts(portList)

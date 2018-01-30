
#
# Requirement:
#    IxNetwork 8.0+
#    - Python2.7/3.4
#    - Python modules: requests, paramiko
#    - IxNetRestApi.py
#
# Description:
#
#    Using REST API to connect to an existing Quick Test configuration.
#    If the variable userSelectQuickTestList is 'all', then execute all
#    the configured Quick Tests. Else, execute the list provided by
#    the user from the commandline.
#
#    Each Quick Test will retrieve its own AggregateResults.csv file and
#    includes a timestamp on it.
#
# Usage:
# ------
#    Enter: python loadQuickTestCmdlineRestApi.py help
#
#        -ixNetworkApiServerIp:   The IxNetwork API server
#        -ixNetworkPort:          The IxNetwork API server socket port number
#        -quickTestNamesToRun:     'all' or a list of all the Quick Test names to run wrapped inside double quotes
#                                 and separate each QT name with a comma
#                                 Example: "broadcast 2544, throughput"
#        -copyResultsToLinuxPath: The full path and file name to save the Quick Test results on
#                                 your local Linux.
#                                 Example: /automation/resultFolder
#        -quickTestCsvResultFile: The statistic result file to get when test is done
#        -resume:                 Don\'t load a config file. Resuming testing from an existing config.

from __future__ import absolute_import, print_function
import sys
import os

from IxNetRestApi import *

# Set default values
ixNetworkApiServer = '192.168.70.127'
ixNetworkApiServerPort = '11009'
userSelectQuickTestList = 'all'
loadConfig = True
copyResultFileToLocalLinuxPath = '/home/hgee'
quickTestCsvResultFile = 'AggregateResults.csv'
quickTestConfigFile = '/home/hgee/Dropbox/MyIxiaWork/Temp/QuickTest_vm8.30.ixncfg'

ixChassisIp = '192.168.70.11'
# Format = [chassisIp, slotNumber, portNumber]
portList = [[ixChassisIp, '1', '1'],
            [ixChassisIp, '2', '1']]

def help():
    os.system('clear')
    print('\n\nUsage:')
    print('-'*75)
    print()
    print('\t-ixNetworkApiServerIp:   The IxNetwork API server.')
    print('\t-ixNetworkPort:          The IxNetwork API server socket port number.')
    print('\t-quickTestNamesToRun:    \'all\' or a list of all the Quick Test names to run wrapped inside double quotes')
    print('\t                         and separate each QT name with a comma.')
    print('\t                         Example: \'broadcast 2544, throughput\'.')
    print('\t-copyResultsToLinuxPath: The full path and file name to save the Quick Test results on')
    print('\t                         your local Linux.')
    print('\t                         Example: /automation/resultFolder.')
    print('\t-quickTestCsvResultFile: The statistic result file to get when test is done.')
    print('\t-resume:                 Don\'t load a config file. Resuming testing from an existing config.')
    print()
    sys.exit()


parameters = sys.argv[1:]
argIndex = 0
while argIndex < len(parameters):
    currentArg = parameters[argIndex]
    if currentArg == '-ixNetworkApiServerIp':
        ixNetworkApiServerIp = parameters[argIndex + 1]
        argIndex += 2
    elif currentArg == '-ixNetworkPort':
        ixNetworkPort = parameters[argIndex + 1]
        argIndex += 2
    elif currentArg == '-quickTestNamesToRun':
        params = parameters[argIndex + 1]
        userSelectQuickTestList = [x.strip() for x in params.split(',')]
        argIndex += 2
    elif currentArg == '-copyResultsToLinuxPath':
        copyResultFileToLocalLinuxPath = parameters[argIndex + 1]
        argIndex += 2
    elif currentArg == '-quickTestCsvResultFile':
        quickTestCsvResultFile = parameters[argIndex + 1]
        argIndex += 2
    elif currentArg == '-resume':
        loadConfig = False
        argIndex += 1
    elif currentArg == 'help':
        help()
    else:
        sys.exit('No such parameter: %s' % currentArg)

try:
    restObj = Connect(apiServerIp=ixNetworkApiServer, serverIpPort=ixNetworkApiServerPort, serverOs=connectToApiServer)
    # You could set to False if have an existing configuration.
    if loadConfig is True:
        restObj.loadConfigFile(quickTestConfigFile)
    # If portList variable is defined, this means to reassign ports.
    if 'portList' in locals():
        restObj.assignPorts(portList, createVports=False)
    restObj.verifyPortState()

    if userSelectQuickTestList == 'all':
        configuredQuickTestList = restObj.getAllQuickTestHandles()
        if configuredQuickTestList:
            quickTestNameList = restObj.getAllQuickTestNames()
        else:
            raise IxNetRestApiException('No Quick Test configured found')
    else:
        # Verify user selected Quick Test to run
        restObj.verifyAllQuickTestNames(userSelectQuickTestList)
        quickTestNameList = userSelectQuickTestList

    print('\nList of Quick Tests to run ...')
    for quickTestToRun in quickTestNameList:
        print('\t', quickTestToRun)

    quickTestHandle = None
    for quickTestName in quickTestNameList:
        print('\nStarting Quick Test: %s...\n' % quickTestName)
        quickTestHandle = restObj.getQuickTestHandleByName(quickTestName)
        currentQuickTestName = restObj.getQuickTestNameByHandle(quickTestHandle)

        restObj.applyQuickTest(quickTestHandle)
        restObj.startQuickTest(quickTestHandle)
        restObj.verifyQuickTestInitialization(quickTestHandle)
        restObj.monitorQuickTestRunningProgress(quickTestHandle)

        # Optional: Display the final stats on the terminal when test completes.
        stats = restObj.getStats(viewName='Flow View')

        resultPath = restObj.getQuickTestResultPath(quickTestHandle)
        resultPath = resultPath+'\\'+quickTestCsvResultFile

        if copyResultFileToLocalLinuxPath.split('/')[:-1] == '/':
            copyResultFileToLocalLinuxPath = copyResultFileToLocalLinuxPath[:-1]

        quickTestStatsToGet = quickTestCsvResultFile.split('.')[0]
        resultFileName = quickTestStatsToGet+'_'+quickTestName.replace(' ', '')
        restObj.copyFileWindowsToLocalLinux(resultPath, copyResultFileToLocalLinuxPath, renameDestinationFile=resultFileName, includeTimestamp=True)
        print('\nQuick Test ended:', quickTestName)

except (IxNetRestApiException, Exception, KeyboardInterrupt) as errMsg:
    if not bool(re.search('ConnectionError', traceback.format_exc())):
        print('\n%s' % traceback.format_exc())
    print('\nException Error! %s\n' % errMsg)
    if quickTestHandle is not None:
        restObj.stopQuickTest(quickTestHandle)

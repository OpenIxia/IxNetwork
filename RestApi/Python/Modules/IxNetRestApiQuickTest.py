import re, time
from .IxNetRestApi import IxNetRestApiException
from .IxNetRestApiFileMgmt import FileMgmt

class QuickTest(object):
    def __init__(self, ixnObj=None, fileMgmtObj=None):
        self.ixnObj = ixnObj
        if fileMgmtObj:
            self.fileMgmtObj = fileMgmtObj
        else:
            self.fileMgmtObj = FileMgmt(ixnObj)

    def setMainObject(self, mainObject):
        # For Python Robot Framework support
        self.ixnObj = mainObject
        self.fileMgmtObj.setMainObject(mainObject)

    def getAllQuickTestHandles(self):
        """
        Description
            Get all the Quick Test object handles

        Returns:
            ['/api/v1/sessions/1/ixnetwork/quickTest/rfc2544throughput/2',
             '/api/v1/sessions/1/ixnetwork/quickTest/rfc2889broadcastRate/1',
             '/api/v1/sessions/1/ixnetwork/quickTest/rfc2889broadcastRate/2']
        """
        response = self.ixnObj.get(self.ixnObj.sessionUrl+'/quickTest')
        quickTestHandles = []
        for eachTestId in response.json()['testIds']:
            quickTestHandles.append(eachTestId)
        return quickTestHandles

    def getAllQuickTestNames(self):
        quickTestNameList = []
        for eachQtHandle in self.getAllQuickTestHandles():
            response = self.ixnObj.get(self.ixnObj.httpHeader+eachQtHandle)
            quickTestNameList.append(response.json()['name'])
        return quickTestNameList

    def getQuickTestHandleByName(self, quickTestName):
        """
        Description
            Get the Quick Test object handle by the name.

        Parameter
            quickTestName: The name of the Quick Test.
        """
        for quickTestHandle in self.getAllQuickTestHandles():
            response = self.ixnObj.get(self.ixnObj.httpHeader+quickTestHandle)
            currentQtName = response.json()['name']
            if (bool(re.match(quickTestName, currentQtName, re.I))):
                return quickTestHandle

    def getQuickTestNameByHandle(self, quickTestHandle):
        """
        quickTestHandle = /api/v1/sessions/1/ixnetwork/quickTest/rfc2544throughput/2
        """
        response = self.ixnObj.get(self.ixnObj.httpHeader + quickTestHandle)
        return response.json()['name']

    def getQuickTestDuration(self, quickTestHandle):
        """
        quickTestHandle = /api/v1/sessions/1/ixnetwork/quickTest/rfc2544throughput/2
        """
        response = self.ixnObj.get(self.ixnObj.httpHeader + quickTestHandle + '/testConfig')
        return response.json()['duration']

    def getQuickTestTotalFrameSizesToTest(self, quickTestHandle):
        """
        quickTestHandle = /api/v1/sessions/1/ixnetwork/quickTest/rfc2544throughput/2
        """
        response = self.ixnObj.get(self.ixnObj.httpHeader + quickTestHandle + '/testConfig')
        return response.json()['framesizeList']

    def applyQuickTest(self, qtHandle):
        """
        Description
            Apply Quick Test configurations

        Parameter
            qtHandle: The Quick Test object handle
        """
        response = self.ixnObj.post(self.ixnObj.sessionUrl+'/quickTest/operations/apply', data={'arg1': qtHandle})
        if self.ixnObj.waitForComplete(response, self.ixnObj.sessionUrl+'/quickTest/operations/apply/'+response.json()['id']) == 1:
            raise IxNetRestApiException('applyTraffic: waitForComplete failed')

    def getQuickTestCurrentAction(self, quickTestHandle):
        """
        quickTestHandle = /api/v1/sessions/1/ixnetwork/quickTest/rfc2544throughput/2
        """
        ixNetworkVersion = self.ixnObj.getIxNetworkVersion()
        match = re.match('([0-9]+)\.[^ ]+ *', ixNetworkVersion)
        if int(match.group(1)) >= 8:
            timer = 10
            for counter in range(1,timer+1):
                response = self.ixnObj.get(self.ixnObj.httpHeader+quickTestHandle+'/results', silentMode=True)
                if counter < timer and response.json()['currentActions'] == []:
                    self.ixnObj.logInfo('getQuickTestCurrentAction is empty. Waiting %s/%s' % (counter, timer))
                    time.sleep(1)
                    continue
                if counter < timer and response.json()['currentActions'] != []:
                    break
                if counter == timer and response.json()['currentActions'] == []:
                    IxNetRestApiException('getQuickTestCurrentActions: Has no action')

            return response.json()['currentActions'][-1]['arg2']
        else:
            response = self.ixnObj.get(self.ixnObj.httpHeader+quickTestHandle+'/results')
            return response.json()['progress']

    def verifyQuickTestInitialization(self, quickTestHandle):
        """
        quickTestHandle = /api/v1/sessions/1/ixnetwork/quickTest/rfc2544throughput/2
        """
        for timer in range(1,20+1):
            currentAction = self.getQuickTestCurrentAction(quickTestHandle)
            print('verifyQuickTestInitialization currentState: %s' % currentAction)
            if timer < 20:
                if currentAction == 'TestEnded' or currentAction == 'None':
                    self.ixnObj.logInfo('\nverifyQuickTestInitialization CurrentState = %s\n\tWaiting %s/20 seconds to change state' % (currentAction, timer))
                    time.sleep(1)
                    continue
                else:
                    break
            if timer >= 20:
                if currentAction == 'TestEnded' or currentAction == 'None':
                    self.ixnObj.showErrorMessage()
                    raise IxNetRestApiException('Quick Test is stuck at TestEnded.')

        ixNetworkVersionNumber = int(self.ixnObj.getIxNetworkVersion().split('.')[0])
        applyQuickTestCounter = 60
        for counter in range(1,applyQuickTestCounter+1):
            quickTestApplyStates = ['InitializingTest', 'ApplyFlowGroups', 'SetupStatisticsCollection']
            currentAction = self.getQuickTestCurrentAction(quickTestHandle)
            if currentAction == None:
                currentAction = 'ApplyingAndInitializing'

            print('\nverifyQuickTestInitialization: %s  Expecting: TransmittingFrames\n\tWaiting %s/%s seconds' % (currentAction, counter, applyQuickTestCounter))
            if ixNetworkVersionNumber >= 8:
                if counter < applyQuickTestCounter and currentAction != 'TransmittingFrames':
                    time.sleep(1)
                    continue

                if counter < applyQuickTestCounter and currentAction == 'TransmittingFrames':
                    self.ixnObj.logInfo('\nVerifyQuickTestInitialization is done applying configuration and has started transmitting frames\n')
                break

            if ixNetworkVersionNumber < 8:
                if counter < applyQuickTestCounter and currentAction == 'ApplyingAndInitializing':
                    time.sleep(1)
                    continue

                if counter < applyQuickTestCounter and currentAction == 'ApplyingAndInitializing':
                    self.ixnObj.logInfo('\nVerifyQuickTestInitialization is done applying configuration and has started transmitting frames\n')
                break

            if counter == applyQuickTestCounter:
                if ixNetworkVersionNumber >= 8 and currentAction != 'TransmittingFrames':
                    self.ixnObj.showErrorMessage()
                    if currentAction == 'ApplyFlowGroups':
                        self.ixnObj.logInfo('\nIxNetwork is stuck on Applying Flow Groups. You need to go to the session to FORCE QUIT it.\n')
                    raise IxNetRestApiException('\nVerifyQuickTestInitialization is stuck on %s. Waited %s/%s seconds' % (
                            currentAction, counter, applyQuickTestCounter))

                if ixNetworkVersionNumber < 8 and currentAction != 'Trial':
                    self.ixnObj.showErrorMessage()
                    raise IxNetRestApiException('\nVerifyQuickTestInitialization is stuck on %s. Waited %s/%s seconds' % (
                            currentAction, counter, applyQuickTestCounter))

    def startQuickTest(self, quickTestHandle):
        """
        Description
            Start a Quick Test

        Parameter
            quickTestHandle: The Quick Test object handle.
            /api/v1/sessions/{id}/ixnetwork/quickTest/rfc2544throughput/2

        Syntax
           POST: http://{apiServerIp:port}/api/v1/sessions/{1}/ixnetwork/quickTest/operations/start
                 data={arg1: '/api/v1/sessions/{id}/ixnetwork/quickTest/rfc2544throughput/2'}
                 headers={'content-type': 'application/json'}
        """
        url = self.ixnObj.sessionUrl+'/quickTest/operations/start'
        self.ixnObj.logInfo('\nstartQuickTest:%s' % url)
        response = self.ixnObj.post(url, data={'arg1': quickTestHandle})
        if self.ixnObj.waitForComplete(response, url+'/'+response.json()['id']) == 1:
            raise IxNetRestApiException

    def stopQuickTest(self, quickTestHandle):
        """
        Description
            Stop the Quick Test.

        Parameter
            quickTestHandle: The Quick Test object handle.
            /api/v1/sessions/{id}/ixnetwork/quickTest/rfc2544throughput/2

        Syntax
           POST: http://{apiServerIp:port}/api/v1/sessions/{1}/ixnetwork/quickTest/operations/stop
                 data={arg1: '/api/v1/sessions/{id}/ixnetwork/quickTest/rfc2544throughput/2'}
                 headers={'content-type': 'application/json'}
        """
        url = self.ixnObj.sessionUrl+'/quickTest/operations/stop'
        response = self.ixnObj.post(url, data={'arg1': quickTestHandle})
        if self.ixnObj.waitForComplete(response, url+'/'+response.json()['id']) == 1:
            raise IxNetRestApiException

    def monitorQuickTestRunningProgress(self, quickTestHandle, getProgressInterval=10):
        """
        Description
            monitor the Quick Test running progress.
            For Linux API server only, it must be a NGPF configuration. (Classic Framework is not supported in REST)

        Parameters
            quickTestHandle: /api/v1/sessions/{1}/ixnetwork/quickTest/rfc2544throughput/2
        """
        isRunningBreakFlag = 0
        trafficStartedFlag = 0
        waitForRunningProgressCounter = 0
        counter = 1

        while True:
            response = self.ixnObj.get(self.ixnObj.httpHeader+quickTestHandle+'/results', silentMode=True)
            isRunning = response.json()['isRunning']
            if isRunning == True:
                response = self.ixnObj.get(self.ixnObj.httpHeader+quickTestHandle+'/results', silentMode=True)
                currentRunningProgress = response.json()['progress']
                if bool(re.match('^Trial.*', currentRunningProgress)) == False:
                    if waitForRunningProgressCounter < 30:
                        self.ixnObj.logInfo('isRunning=True. Waiting for trial runs {0}/30 seconds'.format(waitForRunningProgressCounter))
                        waitForRunningProgressCounter += 1
                        time.sleep(1)
                    if waitForRunningProgressCounter == 30:
                        raise IxNetRestApiException('isRunning=True. No quick test stats showing.')
                else:
                    trafficStartedFlag = 1
                    self.ixnObj.logInfo(currentRunningProgress)
                    counter += 1
                    time.sleep(getProgressInterval)
                    continue
            else:
                if trafficStartedFlag == 1:
                    # We only care about traffic not running in the beginning.
                    # If traffic ran and stopped, then break out.
                    self.ixnObj.logInfo('\nisRunning=False. Quick Test is complete')
                    return 0
                if isRunningBreakFlag < 20:
                    print('isRunning=False. Wait {0}/20 seconds'.format(isRunningBreakFlag))
                    isRunningBreakFlag += 1
                    time.sleep(1)
                    continue
                if isRunningBreakFlag == 20:
                    raise IxNetRestApiException('Quick Test failed to start:', response.json()['status'])

    def getQuickTestResultPath(self, quickTestHandle):
        """
        quickTestHandle = /api/v1/sessions/1/ixnetwork/quickTest/rfc2544throughput/2
        """
        response = self.ixnObj.get(self.ixnObj.httpHeader + quickTestHandle + '/results')
        # "resultPath": "C:\\Users\\hgee\\AppData\\Local\\Ixia\\IxNetwork\\data\\result\\DP.Rfc2544Tput\\10694b39-6a8a-4e70-b1cd-52ec756910c3\\Run0001"
        return response.json()['resultPath']

    def getQuickTestResult(self, quickTestHandle, attribute):
        """
        Description
            Get Quick Test result attributes

        Parameter
            quickTestHandle: The Quick Test object handle

        attribute options to get:
           result - Returns pass
           status - Returns none
           progress - blank or Trial 1/1 Iteration 1, Size 64, Rate 10 % Wait for 2 seconds Wait 70.5169449%complete
           startTime - Returns 04/21/17 14:35:42
           currentActions
           waitingStatus
           resultPath
           isRunning - Returns True or False
           trafficStatus
           duration - Returns 00:01:03
           currentViews
        """
        response = self.ixnObj.get(quickTestHandle+'/results')
        return response.json()[attribute]

    def getQuickTestCsvFiles(self, quickTestHandle, copyToPath, csvFile='all'):
        """
        Description
            Copy Quick Test CSV result files to a specified path on either Windows or Linux.
            Note: Currently only supports copying from Windows.
                  Copy from Linux is coming in November.

        quickTestHandle: The Quick Test handle.
        copyToPath: The destination path to copy to.
                    If copy to Windows: c:\\Results\\Path
                    If copy to Linux: /home/user1/results/path

        csvFile: A list of CSV files to get: 'all', one or more CSV files to get:
                 AggregateResults.csv, iteration.csv, results.csv, logFile.txt, portMap.csv
        """
        resultsPath = self.getQuickTestResultPath(quickTestHandle)
        self.ixnObj.logInfo('\ngetQuickTestCsvFiles: %s' % resultsPath)
        if csvFile == 'all':
            getCsvFiles = ['AggregateResults.csv', 'iteration.csv', 'results.csv', 'logFile.txt', 'portMap.csv']
        else:
            if type(csvFile) is not list:
                getCsvFiles = [csvFile]
            else:
                getCsvFiles = csvFile

        for eachCsvFile in getCsvFiles:
            # Backslash indicates the results resides on a Windows OS.
            if '\\' in resultsPath:
                if bool(re.match('[a-z]:.*', copyToPath, re.I)):
                    self.fileMgmtObj.copyFileWindowsToLocalWindows(resultsPath+'\\{0}'.format(eachCsvFile), copyToPath)
                else:
                    self.fileMgmtObj.copyFileWindowsToLocalLinux(resultsPath+'\\{0}'.format(eachCsvFile), copyToPath)
            else:
                # TODO: Copy from Linux to Windows and Linux to Linux.
                pass

    def getQuickTestPdf(self, quickTestHandle, copyToLocalPath, where='remoteLinux', renameDestinationFile=None, includeTimestamp=False):
        """
        Description
           Generate Quick Test result to PDF and retrieve the PDF result file.

        Parameter
           where: localWindows|remoteWindows|remoteLinux. The destination.
           copyToLocalPath: The local destination path to store the PDF result file.
           renameDestinationFile: Rename the PDF file.
           includeTimestamp: True|False.  Set to True if you don't want to overwrite previous result file.
        """
        response = self.ixnObj.post(self.ixnObj.httpHeader+quickTestHandle+'/operations/generateReport', data={'arg1': quickTestHandle})
        if response.json()['url'] != '':
            if self.ixnObj.waitForComplete(response, self.ixnObj.httpHeader+response.json()['url']) == 1:
                raise IxNetRestApiException

            if where == 'localWindows':
                response = self.ixnObj.get(self.ixnObj.httpHeader+response.json()['url'])
                self.fileMgmtObj.copyFileWindowsToLocalWindows(response.json()['result'], copyToLocalPath, renameDestinationFile, includeTimestamp)
            if where == 'remoteWindows':
                # TODO: Work in progress.  Not sure if this is possible.
                resultPath = self.getQuickTestResultPath(quickTestHandle)
                #self.ixnObj.copyFileWindowsToRemoteWindows(response.json()['result'], copyToLocalPath, renameDestinationFile, includeTimestamp)
                self.fileMgmtObj.copyFileWindowsToRemoteWindows(resultPath, copyToLocalPath, renameDestinationFile, includeTimestamp)
            if where == 'remoteLinux':
                linuxResultPath = self.getQuickTestResultPath(quickTestHandle)
                self.fileMgmtObj.copyFileWindowsToLocalLinux(linuxResultPath+'\\TestReport.pdf', copyToLocalPath, renameDestinationFile, includeTimestamp)
        else:
            self.ixnObj.logInfo('\ngetQuickTestPdf failed. Result path = %s' % response.json()['result'])


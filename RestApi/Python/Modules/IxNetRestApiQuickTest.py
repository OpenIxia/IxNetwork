import re
import time
from IxNetRestApi import IxNetRestApiException
from IxNetRestApiFileMgmt import FileMgmt


class QuickTest(object):
    def __init__(self, ixnObj=None, fileMgmtObj=None):
        self.ixnObj = ixnObj
        self.ixNetwork = ixnObj.ixNetwork
        if fileMgmtObj:
            self.fileMgmtObj = fileMgmtObj
        else:
            self.fileMgmtObj = FileMgmt(ixnObj)

    def setMainObject(self, mainObject):
        self.ixnObj = mainObject
        self.fileMgmtObj.setMainObject(mainObject)

    def getAllQuickTestHandles(self):
        """
        Description
            Get all the Quick Test object handles

        Returns:
            [   <ixnetwork_restpy.testplatform.sessions.ixnetwork.quicktest
                    .openflowlayer2learningrate_3db88746f7f375303f2eda376386a9a8
                    .OpenFlowLayer2LearningRate object at 0x03AAE2B0>]
        """
        quickTestObjects = []
        for testId in self.ixNetwork.QuickTest.TestIds:
            qtType = testId.split("/")[-2]
            qtType = qtType[0].upper() + qtType[1:]
            qtObj = getattr(self.ixNetwork.QuickTest, qtType)
            quickTestObjects.append(qtObj.find())
        return quickTestObjects

    def getAllQuickTestNames(self):
        """
        Description
            Get all the Quick Test name.
        """
        quickTestNameList = []
        for eachQtHandle in self.getAllQuickTestHandles():
            qtName = eachQtHandle.Name
            if qtName:
                quickTestNameList.append(qtName)
        return quickTestNameList

    def getQuickTestHandleByName(self, quickTestName):
        """
        Description
            Get the Quick Test object handle by the name.
        Parameter
            quickTestName: The name of the Quick Test.
        """
        for quickTestHandle in self.getAllQuickTestHandles():
            if bool(re.match(quickTestName, quickTestHandle.Name, re.I)):
                return quickTestHandle
        else:
            raise Exception("Unable to find quicktest with name {}".format(quickTestName))

    def getQuickTestNameByHandle(self, quickTestHandle):
        """
        Description :
            Get the Quick Test Name by quick test Handle
        Parameter :
            quickTestHandle = <ixnetwork_restpy.testplatform.sessions.ixnetwork.quicktest
                                    .rfc2544throughput_5a77c9a28f5fa2bb9ce9f4280eb5122f
                                    .Rfc2544throughput object at 0x03800D00>
        """
        if quickTestHandle.Name:
            return quickTestHandle.Name
        else:
            raise Exception("Unable to find quicktest name for given handle")

    def getQuickTestDuration(self, quickTestHandle):
        """
        Description :
            Get Quick Test Test Duration Time in Sec
        Parameter :
            quickTestHandle = <ixnetwork_restpy.testplatform.sessions.ixnetwork.quicktest
                                    .rfc2544throughput_5a77c9a28f5fa2bb9ce9f4280eb5122f
                                    .Rfc2544throughput object at 0x03800D00>
        """

        return quickTestHandle.TestConfig.Duration

    def getQuickTestTotalFrameSizesToTest(self, quickTestHandle):
        """
        Description :
            Get Quick Test Test Total Frame Sizes
        Parameter :
            quickTestHandle = <ixnetwork_restpy.testplatform.sessions.ixnetwork.quicktest
                                    .rfc2544throughput_5a77c9a28f5fa2bb9ce9f4280eb5122f
                                    .Rfc2544throughput object at 0x03800D00>
        """

        return quickTestHandle.TestConfig.FramesizeList

    def applyQuickTest(self, qtHandle):
        """
        Description
            Apply Quick Test configurations

        Parameter
            qtHandle: The Quick Test object handle
        """
        try:
            qtHandle.Apply()
        except Exception as err:
            raise Exception("Operation apply quicktest failed with error :\n {}".format(err))

    def getQuickTestCurrentAction(self, quickTestHandle):
        """
        Description :
            Returns current action like 'InitializingTest', 'ApplyFlowGroups',
            'SetupStatisticsCollection', etc.
        Parameter :
            quickTestHandle = <ixnetwork_restpy.testplatform.sessions.ixnetwork.quicktest
                                    .rfc2544throughput_5a77c9a28f5fa2bb9ce9f4280eb5122f
                                    .Rfc2544throughput object at 0x03800D00>
        """
        timer = 10
        currentActions = None
        for counter in range(1, timer+1):
            currentActions = quickTestHandle.Results.CurrentActions
            self.ixnObj.logInfo('\n\ngetQuickTestCurrentAction:\n')
            for eachCurrentAction in quickTestHandle.Results.CurrentActions:
                self.ixnObj.logInfo('\t{}'.format(eachCurrentAction['arg2']))
            self.ixnObj.logInfo('\n')
            if counter < timer and currentActions == []:
                self.ixnObj.logInfo(
                    '\n getQuickTestCurrentAction is empty. Waiting %s/%s \n' % (counter, timer))
                time.sleep(1)
                continue
            if counter < timer and currentActions != []:
                break
            if counter == timer and currentActions == []:
                raise Exception('\n\ngetQuickTestCurrentActions: Has no action')

        return currentActions[-1]['arg2']

    def verifyQuickTestInitialization(self, quickTestHandle):
        """
        Parameter :
            quickTestHandle = <ixnetwork_restpy.testplatform.sessions.ixnetwork.quicktest
                                    .rfc2544throughput_5a77c9a28f5fa2bb9ce9f4280eb5122f
                                    .Rfc2544throughput object at 0x03800D00>
        """

        for timer in range(1, 20+1):
            currentAction = self.getQuickTestCurrentAction(quickTestHandle)
            self.ixnObj.logInfo('verifyQuickTestInitialization currentState: %s' % currentAction)
            if timer < 20:
                if currentAction == 'TestEnded' or currentAction == 'None':
                    self.ixnObj.logInfo(
                        '\nverifyQuickTestInitialization CurrentState = %s\n\tWaiting %s/20 '
                        'seconds to change state' % (currentAction, timer))
                    time.sleep(1)
                    continue
                else:
                    break
            if timer >= 20:
                if currentAction == 'TestEnded' or currentAction == 'None':
                    raise IxNetRestApiException('Quick Test is stuck at TestEnded.')

        applyQuickTestCounter = 60
        for counter in range(1, applyQuickTestCounter+1):
            currentAction = self.getQuickTestCurrentAction(quickTestHandle)
            if currentAction is None:
                currentAction = 'ApplyingAndInitializing'

            self.ixnObj.logInfo(
                '\n verifyQuickTestInitialization: %s  Expecting: TransmittingFrames\n\tWaiting'
                ' %s/%s seconds' % (currentAction, counter, applyQuickTestCounter))
            if counter < applyQuickTestCounter and currentAction != 'TransmittingFrames':
                time.sleep(1)
                continue

            if counter < applyQuickTestCounter and currentAction == 'TransmittingFrames':
                self.ixnObj.logInfo(
                    '\n VerifyQuickTestInitialization is done applying configuration and'
                    ' has started transmitting frames\n')
                break

            if counter == applyQuickTestCounter:
                if currentAction == 'ApplyFlowGroups':
                    self.ixnObj.logInfo(
                        '\nIxNetwork is stuck on Applying Flow Groups. You need to go to the '
                        'session to FORCE QUIT it.\n')
                raise IxNetRestApiException(
                    '\nVerifyQuickTestInitialization is stuck on %s. Waited %s/%s seconds' % (
                        currentAction, counter, applyQuickTestCounter))

    def startQuickTest(self, quickTestHandle):
        """
        Description
            Start a Quick Test

        Parameter
            quickTestHandle: The Quick Test object handle.

        """
        try:
            quickTestHandle.Apply()
            quickTestHandle.Start()
        except Exception as err:
            self.ixnObj.logInfo("Error : \n {}".format(err))
            raise Exception("Failed Starting QuickTest for {}".format(quickTestHandle.Name))

    def stopQuickTest(self, quickTestHandle):
        """
        Description
            Stop the Quick Test.

        Parameter
            quickTestHandle: The Quick Test object handle.

        """
        try:
            quickTestHandle.Stop()
        except Exception as err:
            self.ixnObj.logInfo("Error in stop quicktest : \n {}".format(err))
            raise Exception("Failed Stopping QuickTest for {}".format(quickTestHandle.Name))

    def monitorQuickTestRunningProgress(self, quickTestHandle, getProgressInterval=10):
        """
        Description
            monitor the Quick Test running progress.
            For Linux API server only, it must be a NGPF configuration.

        Parameters
            quickTestHandle: quick test handle
        """
        isRunningBreakFlag = 0
        trafficStartedFlag = 0
        waitForRunningProgressCounter = 0
        counter = 1

        while True:
            isRunning = quickTestHandle.Results.IsRunning
            if isRunning:
                currentRunningProgress = quickTestHandle.Results.Progress
                self.ixnObj.logInfo(currentRunningProgress)
                if not bool(re.match('^Trial.*', currentRunningProgress)):
                    if waitForRunningProgressCounter < 30:
                        self.ixnObj.logInfo('isRunning=True. Waiting for trial runs {0}/30 '
                                            'seconds'.format(waitForRunningProgressCounter))
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
                    self.ixnObj.logInfo('isRunning=False. Wait {0}/20 seconds'.format(
                        isRunningBreakFlag))
                    isRunningBreakFlag += 1
                    time.sleep(1)
                    continue
                if isRunningBreakFlag == 20:
                    raise IxNetRestApiException('Quick Test failed to start:')

    def getQuickTestResultPath(self, quickTestHandle):
        """
        quickTestHandle = The quick test handle
        """
        resultsPath = quickTestHandle.Results.ResultPath
        if not resultsPath:
            raise Exception("no result path found for quicktest {}".format(quickTestHandle.Name))
        return resultsPath

    def getQuickTestResult(self, quickTestHandle, attribute):
        """
        Description
            Get Quick Test result attributes

        Parameter
            quickTestHandle: The Quick Test object handle

        attribute options to get:
           result - Returns pass
           status - Returns none
           progress - blank or Trial 1/1 Iteration 1, Size 64,
                      Rate 10 % Wait for 2 seconds Wait 70.5169449%complete
           startTime - Returns 04/21/17 14:35:42
           currentActions
           waitingStatus
           resultPath
           isRunning - Returns True or False
           trafficStatus
           duration - Returns 00:01:03
           currentViews
        """
        attribute = attribute[0].upper() + attribute[1:]
        result = getattr(quickTestHandle.Results, attribute)
        return result

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
        resultsPath = quickTestHandle.Results.ResultPath
        self.ixnObj.logInfo('\ngetQuickTestCsvFiles: %s' % resultsPath)

        if csvFile == 'all':
            getCsvFiles = ['AggregateResults.csv',
                           'iteration.csv', 'results.csv', 'logFile.txt', 'portMap.csv']
        else:
            if type(csvFile) is not list:
                getCsvFiles = [csvFile]
            else:
                getCsvFiles = csvFile

        for eachCsvFile in getCsvFiles:
            # Backslash indicates the results resides on a Windows OS.
            if '\\' in resultsPath:
                windowsSource = resultsPath + '\\{0}'.format(eachCsvFile)
                if '\\' in copyToPath:
                    self.fileMgmtObj.copyFileWindowsToLocalWindows(windowsSource, copyToPath)
                else:
                    self.fileMgmtObj.copyFileWindowsToLocalLinux(windowsSource, copyToPath)

            else:
                linuxSource = resultsPath + '/{0}'.format(eachCsvFile)
                self.fileMgmtObj.copyFileLinuxToLocalLinux(linuxSource, copyToPath)

    def getQuickTestPdf(self, quickTestHandle, copyToLocalPath, where='remoteLinux',
                        renameDestinationFile=None, includeTimestamp=False):
        """
        Description
           Generate Quick Test result to PDF and retrieve the PDF result file.

        Parameter
           where: localWindows|remoteWindows|remoteLinux. The destination.
           copyToLocalPath: The local destination path to store the PDF result file.
           renameDestinationFile: Rename the PDF file.
           includeTimestamp: True|False.  Set to True if you don't want to overwrite previous
           result file.
        """

        try:
            reportFile = quickTestHandle.GenerateReport()
        except Exception as err:
            raise Exception("Generate quicktest report file failed. Error : \n {}".format(err))

        if where == 'localWindows':
            self.fileMgmtObj.copyFileWindowsToLocalWindows(reportFile, copyToLocalPath,
                                                           renameDestinationFile, includeTimestamp)
        if where == 'remoteWindows':
            self.fileMgmtObj.copyFileWindowsToRemoteWindows(reportFile, copyToLocalPath,
                                                            renameDestinationFile, includeTimestamp)
        if where == 'remoteLinux':
            self.fileMgmtObj.copyFileWindowsToLocalLinux(reportFile, copyToLocalPath,
                                                         renameDestinationFile, includeTimestamp)

    def runQuickTest(self, quickTestName, timeout=90):
        """
        Description
            Run the Quick test

        Parameter
            quickTestName: <str>: name of the quick test to run
            timeout: <int>: timeout duration handles internally in Restpy

        Example
            runQuickTest("Macro_17_57_14_294", timeout=180)

        Return

        Note: operation run will keep checking the status of execution for the specified timeout
        """
        eventSchedulerHandle = self.getQuickTestHandleByName(quickTestName)
        try:
            eventSchedulerHandle.Run()
        except Exception as err:
            raise Exception("Run quicktest operation failed with error : \n {}".format(err))

    def deleteQuickTest(self, quickTestName):
        """
        Description
            Delete the  Quick test.

        Parameter
            quickTestName: <str>: name of the quick test to delete

        Example
            deleteQuickTest("Macro_17_57_14_294")

        Return
        """
        eventSchedulerHandle = self.getQuickTestHandleByName(quickTestName)
        try:
            eventSchedulerHandle.remove()
        except Exception as err:
            raise Exception("Delete quicktest by quicktest name failed with error : \n {}"
                            .format(err))

    def configQuickTest(self, quickTestName, numOfTrials=1):
        """
        Description
            Configure a quick test

        Parameter
            quickTestName: <str>: name of the quick test to configure
            numOfTrials: <int>: number of iterations to run the quick test, default is 1

        Example
            configQuickTest("Macro_17_57_14_294")
            configQuickTest("Macro_17_57_14_294", numOfTrials=2)

        Return
            event scheduler handle on success or exception on failure
        """
        try:
            eventSchedulerHandle = self.ixNetwork.QuickTest.EventScheduler.add()
            eventSchedulerHandle.Name = quickTestName
            eventSchedulerHandle.Mode = "existingMode"
            eventSchedulerHandle.ForceApplyQTConfig = True
            eventSchedulerHandle.TestConfig.NumTrials = numOfTrials
            return eventSchedulerHandle
        except Exception as err:
            raise Exception("Unable to configure quick test. Error : \n {}".format(err))

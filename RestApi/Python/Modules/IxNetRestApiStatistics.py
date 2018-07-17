import re, time
from IxNetRestApi import IxNetRestApiException
from IxNetRestApiFileMgmt import FileMgmt

class Statistics(object):
    def __init__(self, ixnObj=None):
        self.ixnObj = ixnObj

        # For takesnapshot()
        self.fileMgmtObj = FileMgmt(self.ixnObj)

    def setMainObject(self, mainObject):
        """
        Description
            For Python Robot Framework support.
        """
        self.ixnObj = mainObject

    def getStats(self, viewObject=None, viewName='Flow Statistics', csvFile=None, csvEnableFileTimestamp=False, displayStats=True,
                 silentMode=True, ignoreError=False):
        """
        Description
            Get stats by the statistic name or get stats by providing a view object handle.

        Parameters
            csvFile = None or <filename.csv>.
                      None will not create a CSV file.
                      Provide a <filename>.csv to record all stats to a CSV file.
                      Example: getStats(sessionUrl, csvFile='Flow_Statistics.csv')

            csvEnableFileTimestamp = True or False. If True, timestamp will be appended to the filename.

            displayStats: True or False. True=Display stats.

            ignoreError: True or False.  Returns None if viewName is not found.

            viewObject: The view object: http://{apiServerIp:port}/api/v1/sessions/2/ixnetwork/statistics/view/13
                        A view object handle could be obtained by calling getViewObject().

            viewName options (Not case sensitive):
               NOTE: Not all statistics are listed here.
                  You could get the statistic viewName directly from the IxNetwork GUI in the statistics.

            'Port Statistics'
            'Tx-Rx Frame Rate Statistics'
            'Port CPU Statistics'
            'Global Protocol Statistics'
            'Protocols Summary'
            'Port Summary'
            'BGP Peer Per Port'
            'OSPFv2-RTR Drill Down'
            'OSPFv2-RTR Per Port'
            'IPv4 Drill Down'
            'L2-L3 Test Summary Statistics'
            'Flow Statistics'
            'Traffic Item Statistics'
            'IGMP Host Drill Down'
            'IGMP Host Per Port'
            'IPv6 Drill Down'
            'MLD Host Drill Down'
            'MLD Host Per Port'
            'PIMv6 IF Drill Down'
            'PIMv6 IF Per Port'
            'Flow View'

         Note: Not all of the viewNames are listed here. You have to get the exact names from
               the IxNetwork GUI in statistics based on your protocol(s).

         Return a dictionary of all the stats: statDict[rowNumber][columnName] == statValue
           Get stats on row 2 for 'Tx Frames' = statDict[2]['Tx Frames']
        """
        if viewObject == None:
            viewList = self.ixnObj.get('%s/%s/%s' % (self.ixnObj.sessionUrl, 'statistics', 'view'), silentMode=silentMode)
            views = ['%s/%s/%s/%s' % (self.ixnObj.sessionUrl, 'statistics', 'view', str(i['id'])) for i in viewList.json()]
            if silentMode is False:
                self.ixnObj.logInfo('\ngetStats: Searching for viewObj for viewName: %s' % viewName)
            for view in views:
                #print('\nview:', view)
                # GetAttribute
                response = self.ixnObj.get('%s' % view, silentMode=silentMode)
                captionMatch = re.match(viewName, response.json()['caption'], re.I)
                if captionMatch:
                    # viewObj: sessionUrl + /statistics/view/11'
                    viewObject = view
                    break

            if viewObject == None and ignoreError == False:
                raise IxNetRestApiException("viewObj wasn't found for viewName: %s" % viewName)
            if viewObject == None and ignoreError == True:
                return None

        if silentMode is False:
            self.ixnObj.logInfo('\nviewObj: %s' % viewObject)

        for counter in range(0,31):
            response = self.ixnObj.get(viewObject+'/page', silentMode=silentMode)
            totalPages = response.json()['totalPages']
            if totalPages == 'null':
                self.ixnObj.logInfo('\nGetting total pages is not ready yet. Waiting %d/30 seconds' % counter, timestamp=False)
                time.sleep(1)
            if totalPages != 'null':
                break
            if totalPages == 'null' and counter == 30:
                self.ixnObj.logInfo('\ngetStats failed: Getting total pages')
                return 1

        if csvFile != None:
            import csv
            csvFileName = csvFile.replace(' ', '_')
            if csvEnableFileTimestamp:
                import datetime
                timestamp = datetime.datetime.now().strftime('%H%M%S')
                if '.' in csvFileName:
                    csvFileNameTemp = csvFileName.split('.')[0]
                    csvFileNameExtension = csvFileName.split('.')[1]
                    csvFileName = csvFileNameTemp+'_'+timestamp+'.'+csvFileNameExtension
                else:
                    csvFileName = csvFileName+'_'+timestamp

            csvFile = open(csvFileName, 'w')
            csvWriteObj = csv.writer(csvFile)

        # Get the stat column names
        columnList = response.json()['columnCaptions']
        if csvFile != None:
            csvWriteObj.writerow(columnList)

        flowNumber = 1
        statDict = {}
        # Get the stat values
        for pageNumber in range(1,totalPages+1):
            self.ixnObj.patch(viewObject+'/page', data={'currentPage': pageNumber}, silentMode=silentMode)
            response = self.ixnObj.get(viewObject+'/page', silentMode=silentMode)
            statValueList = response.json()['pageValues']
            for statValue in statValueList:
                if csvFile != None:
                    csvWriteObj.writerow(statValue[0])
                if displayStats:
                    self.ixnObj.logInfo('\nRow: %d' % flowNumber, timestamp=False)
                statDict[flowNumber] = {}
                index = 0
                for statValue in statValue[0]:
                    statName = columnList[index]
                    statDict[flowNumber].update({statName: statValue})
                    if displayStats:
                        self.ixnObj.logInfo('\t%s: %s' % (statName, statValue), timestamp=False)
                    index += 1
                flowNumber += 1

        if csvFile != None:
            csvFile.close()
        return statDict

        # Flow Statistics dictionary output example
        '''
        Flow: 50
            Tx Port: Ethernet - 002
            Rx Port: Ethernet - 001
            Traffic Item: OSPF T1 to T2
            Source/Dest Value Pair: 2.0.21.1-1.0.21.1
            Flow Group: OSPF T1 to T2-FlowGroup-1 - Flow Group 0002
            Tx Frames: 35873
            Rx Frames: 35873
            Packet Loss Duration (ms):  11.106
            Frames Delta: 0
            Loss %: 0
            Tx Frame Rate: 3643.5
            Rx Frame Rate: 3643.5
            Tx L1 Rate (bps): 4313904
            Rx L1 Rate (bps): 4313904
            Rx Bytes: 4591744
            Tx Rate (Bps): 466368
            Rx Rate (Bps): 466368
            Tx Rate (bps): 3730944
            Rx Rate (bps): 3730944
            Tx Rate (Kbps): 3730.944
            Rx Rate (Kbps): 3730.944
            Tx Rate (Mbps): 3.731
            Rx Rate (Mbps): 3.731
            Store-Forward Avg Latency (ns): 0
            Store-Forward Min Latency (ns): 0
            Store-Forward Max Latency (ns): 0
            First TimeStamp: 00:00:00.722
            Last TimeStamp: 00:00:10.568
        '''

    def removeAllTclViews(self):
        """
        Description
           Removes all created stat views.
        """
        removeAllTclViewsUrl = self.ixnObj.sessionUrl+'/operations/removealltclviews'
        response = self.ixnObj.post(removeAllTclViewsUrl)
        self.ixnObj.waitForComplete(response, removeAllTclViewsUrl+'/'+response.json()['id'])

    def clearStats(self):
        """
        Description
           Clears all stats

        Syntax
           POST = https://{apiServerIp:port}/api/v1/sessions/<id>/ixnetwork/operations/clearstats
        """
        self.ixnObj.post(self.ixnObj.sessionUrl+'/operations/clearstats')

    def takeSnapshot(self, viewName='Flow Statistics', windowsPath=None, localLinuxPath=None,
                     renameDestinationFile=None, includeTimestamp=False, mode='overwrite'):
        """
        Description
            Take a snapshot of the vieweName statistics.  This is a two step process.
            1> Take a snapshot of the statistics and store it in the C: drive.
            2> Copy the statistics from the c: drive to remote Linux.

        Parameters
            viewName: The name of the statistics to get.
            windowsPath: A C: drive + path to store the snapshot: c:\\Results
            localLinuxPath: None|A path. If None, this API won't copy the stat file to local Linux.
                       The stat file will remain on Windows c: drive.
            renameDestinationFile: None or a name of the file other than the viewName.
            includeTimestamp: True|False: To include a timestamp at the end of the file.
            mode: append|overwrite: append=To append stats to an existing stat file.
                                    overwrite=Don't append stats. Create a new stat file.

        Example:
            takeSnapshot(viewName='Flow Statistics', windowsPath='C:\\Results', localLinuxPath='/home/hgee',
                        renameDestinationFile='my_renamed_stat_file.csv', includeTimestamp=True)
        """
        # TODO: For Linux API server
        #    POST /api/v1/sessions/1/ixnetwork/operations/getdefaultsnapshotsettings
        #    "Snapshot.View.Csv.Location: \"/root/.local/share/Ixia/IxNetwork/data/logs/Snapshot CSV\""

        if windowsPath is None:
            raise IxNetRestApiException('\nMust include windowsPath\n')

        if mode == 'append':
            mode = 'kAppendCSVFile'
        if mode == 'overwrite':
            mode = 'kOverwriteCSVFile'

        data = {'arg1': [viewName], 'arg2': [
                            "Snapshot.View.Contents: \"allPages\"",
                            "Snapshot.View.Csv.Location: \"{0}\"".format(windowsPath),
                            "Snapshot.View.Csv.GeneratingMode: \"%s\"" % mode,
                            "Snapshot.View.Csv.StringQuotes: \"True\"",
                            "Snapshot.View.Csv.SupportsCSVSorting: \"False\"",
                            "Snapshot.View.Csv.FormatTimestamp: \"True\"",
                            "Snapshot.View.Csv.DumpTxPortLabelMap: \"False\"",
                            "Snapshot.View.Csv.DecimalPrecision: \"3\""
                            ]
                }
        url = self.ixnObj.sessionUrl+'/operations/takeviewcsvsnapshot'
        response = self.ixnObj.post(url, data=data)
        self.ixnObj.waitForComplete(response, url+'/'+response.json()['id'])

        #response = self.ixnObj.get(self.ixnObj.sessionUrl+'/files?filename=Flow Statistics.csv&absolute=c:\\Results', ignoreError=True)
        if localLinuxPath:
            # Get the snapshot. Use the csvFilename that was specified and the location
            self.fileMgmtObj.copyFileWindowsToLocalLinux('{0}\\{1}.csv'.format(windowsPath, viewName), localLinuxPath,
                                                    renameDestinationFile=renameDestinationFile, includeTimestamp=includeTimestamp)

    def getViewObject(self, viewName='Flow Statistics'):
        """
        Description
            To get just the statistic view object.
            Mainly used by internal APIs such as takeCsvSnapshot that
            requires the statistics view object handle.

        Parameter
         viewName:  Options (case sensitive):
            "Port Statistics"
            "Tx-Rx Frame Rate Statistics"
            "Port CPU Statistics"
            "Global Protocol Statistics"
            "Protocols Summary"
            "Port Summary"
            "OSPFv2-RTR Drill Down"
            "OSPFv2-RTR Per Port"
            "IPv4 Drill Down"
            "L2-L3 Test Summary Statistics"
            "Flow Statistics"
            "Traffic Item Statistics"
        """
        self.ixnObj.logInfo('\ngetStats: %s' % viewName)
        viewList = self.ixnObj.get("%s/%s/%s" % (self.ixnObj.sessionUrl, "statistics", "view"))
        views = ["%s/%s/%s/%s" % (self.ixnObj.sessionUrl, "statistics", "view", str(i["id"])) for i in viewList.json()]
        for view in views:
            # GetAttribute
            response = self.ixnObj.get(view)
            caption = response.json()["caption"]
            if viewName == caption:
                # viewObj: sessionUrl + "/statistics/view/11"
                viewObj = view
                return viewObj
        return None

    def clearStats(self):
        """
        Description
            Clear all stats and wait for API server to finish.
        """
        url = self.ixnObj.sessionUrl + '/operations/clearStats'
        response = self.ixnObj.post(url, data={'arg1': ['waitForPortStatsRefresh']})

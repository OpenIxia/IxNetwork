import re, time

class Statistics(object):
    def __init__(self, ixNetObj):
        self.ixNetObj = ixNetObj

    def getStatView(self, caption):
        """
        Get a statistics view.

        :param caption: <str>: The statistics view caption name.
                           Example: Protocols Summary, Flow Statistics, etc.

        Return
           The statistics view object attributes.
        """
        viewResults = []
        counterStop = 60
        for counter in range(1, counterStop+1): 
            print('\nWaiting for statview: {0}\n'.format(caption))
            viewResults = self.ixNetObj.Statistics.View.find(Caption=caption)
            if counter < counterStop and len(viewResults) == 0:
                print('\n{0} is not ready yet. Wait {1}/{2} seconds\n'.format(caption, counter, counterStop))
                time.sleep(1)
                continue

            if counter < counterStop and len(viewResults) != 0:
                print('\n{0} is ready\n'.format(caption))
                return viewResults

            if counter == counterStop and len(viewResults) == 0 :
                raise Exception('\nAPI server failed to provide stat views')

    def getStatViewResults(self, statViewName=False, getColumnCaptions=False, getPageValues=False,
                           rowValuesLabel=None, getTotalPages=False):
        """
        Wait for a statistic view to be ready with stats. Cannot assume the stats are ready.
        For example, if startAllProtocols was executed, protocol summary stats may not be ready
        provided by the API server.
    
        This function takes in statViewName as a mandatory parameter.
        
        Note:
           Getting stats is always a two step process.  You normally need to get the statview and then
           get the stat page values.  You must verify each seperately for readiness.

        :param statViewName: <Mandatory>: The name of the stat view sucha as:
                         Protocols Summary, Port Statistics, Flow Statistics, Traffic Item Statistics, etc.

        :param getColumnCaptions: <bool>: Optional: Returns the statViewName column caption names in a list.
        :param getPageValues: <bool>: Optional: Returns the statViewName page values in a list.
        :param rowValuesLabel: <str>: Optional: Return the stats for just the row's label name. 
        :param getTotalPages: <bool>: Optional: Return the total amount of pages for the statview.

        Example 1:
           # Wait for statViewName='Protocols Summary' to be ready and return the data.
           results = self.getStatView(caption='Protocols Summary')
   
        Example 2:
           # Wait for each statViewName to be ready.
           # Then get the column captions, which are the names of the stats 
           # and get the page values, which are the stat values for each caption.
           columnCaptions = self.getStatViewResults(statViewName='Protocols Summary', getColumnCaptions=True)
           pageValues = self.getStatViewResults(statViewName='Protocols Summary', getPageValues=True)

        Example 3:
            columnCaptions= statObj.getStatViewResults(statViewName='Traffic Item Statistics', getColumnCaptions=True)
            trafficItemStats = statObj.getStatViewResults(statViewName='Traffic Item Statistics',
                                                          rowValuesLabel=trafficItemName)
            txFramesIndex = columnCaptions.index('Tx Frames')
            rxFramesIndex = columnCaptions.index('Rx Frames')
        """
        # Verify for statViewName readiness first
        self.getStatView(caption=statViewName)

        viewResults = []
        counterStop = 60
        for counter in range(1, counterStop+1): 
            if getColumnCaptions:
                print('\nWaiting for {0} Data.ColumnCaptions\n'.format(statViewName))
                viewResults = self.ixNetObj.Statistics.View.find(Caption=statViewName)[0].Data.ColumnCaptions
                deeperView = 'Data.ColumnCaptions'

            if getPageValues:
                print('\nWaiting for {0} Data.PageValues\n'.format(statViewName))
                viewResults = self.ixNetObj.Statistics.View.find(Caption=statViewName)[0].Data.PageValues
                deeperView = 'Data.PageValues'

            if getTotalPages:
                print('\nWaiting for {0} Data.TotalPages\n'.format(statViewName))
                return self.ixNetObj.Statistics.View.find(Caption=statViewName)[0].Data.TotalPages

            if rowValuesLabel is not None:
                print('\nWaiting for {0} Data.GetRowValues\n'.format(statViewName))
                viewResults = self.ixNetObj.Statistics.View.find(Caption=statViewName)[0].GetRowValues(Arg2=rowValuesLabel)
                deeperView = 'GetRowValues'

            if counter < counterStop and len(viewResults) == 0:
                print('\n{0} {1}: is not ready yet.\n\tWait {2}/{3} seconds\n'.format(statViewName, deeperView,
                                                                                        counter, counterStop))
                time.sleep(1)
                continue

            if counter < counterStop and len(viewResults) != 0:
                print('\n{0} {1}: is ready\n'.format(statViewName, deeperView))
                return viewResults

            if counter == counterStop and len(viewResults) == 0 :
                raise Exception('\nAPI server failed to provide stat views for {0} {1}'.format(statViewName, deeperView))

    def verifyAllProtocolSessions(self, timeout=60):
        """
        Verify all configured protocols summary sessions for up.
        """

        # Verify for Protocols Summary stats readiness
        self.getStatView(caption='Protocols Summary')

        columnCaptions = self.getStatViewResults(statViewName='Protocols Summary', getColumnCaptions=True)
        counterStop = timeout
        for counter in range(1, counterStop+1): 
            pageValues = self.getStatViewResults(statViewName='Protocols Summary', getPageValues=True)
            
            print('\n%-16s %-14s %-16s %-23s' % \
                  (columnCaptions[0], columnCaptions[1], columnCaptions[2], columnCaptions[3]))
            print('%s' % '-' * 70)

            sessionDownFlag = 0
            sessionNotStartedFlag = 0
            sessionFailedFlag = 0

            for pageValue in pageValues:
                pageValue = pageValue[0]
                protocol = pageValue[0]
                sessionsUp = int(pageValue[1])
                sessionsDown = int(pageValue[2])
                sessionsNotStarted = int(pageValue[3])

                print('%-16s %-14s %-16s %-23s' % (protocol, sessionsUp, sessionsDown, sessionsNotStarted))
                if sessionsNotStarted != 0:
                    sessoinNotStartedFlag = 1

                if counter < counterStop and sessionsDown != 0:
                    sessionDownFlag = 1

                if counter == counterStop and sessionsDown != 0:
                    sessionFailedFlag = 1

            if sessionNotStartedFlag == 1:
                if counter < 30:
                    sessionNotStartedFlag = 0
                    print('Protocol sessions are not started yet. Waiting {0}/30 seconds'.format(counter))
                    time.sleep(1)
                    continue

                if counter == 30:
                    raise Exception('Protocol session is not started')

            if sessionDownFlag == 1:
                print('\nWaiting {0}/{1} seconds'.format(counter, counterStop))
                time.sleep(1)
                continue

            if counter < counterStop and sessionDownFlag == 0:
                print('\nProtocol sessions are all up')
                break

            if sessionFailedFlag == 1:
                raise Exception('Protocol session failed to come up')

    def getStatsByRowLabelName(self, statViewName=None, rowLabelName='all'):
        """
        This is an internal helper function for: getTrafficItemStats, getPortStatistics, getProtocolsSummary,
                                                 getGlobalProtocolStatistics, getDataPlanePortStatistics.

        These stats are identified by a label name for each row shown in the GUI.
        The label name is the first column value shown in the GUI.

        :param statViewName: 'Port Statistics', 'Traffic Item Statistics', 'Protocols Summary', 'Port CPU Statistics'
                             'Global Protocol Statistics', 'Data Plane Statistics'

        :param rowLabelName: <str|list|all>: If you look at the IxNetwork GUI for any of the statViewName listed above, 
                                             their rowLabelName is the first in the column stats.

                             If you're just getting one specific stat, pass in the rowLabelName.
                             If you want to get multiple stats, pass in a list of rowLabelName.
                             Defaults to return all the row of stats.

        Return
           A dict: stats
        """
        columnNames = self.getStatViewResults(statViewName=statViewName, getColumnCaptions=True)
        totalPages = self.getStatViewResults(statViewName=statViewName, getTotalPages=True)
        stats = {}

        if type(rowLabelName) == list or rowLabelName == 'all':
            for pageNumber in range(1, totalPages+1):
                self.ixNetObj.Statistics.View.find(Caption=statViewName)[0].Data.CurrentPage = pageNumber

                statViewValues = self.getStatViewResults(statViewName=statViewName, getPageValues=True)

                if type(rowLabelName) == list:
                    # Get the specified list of traffic item's stats
                    for eachViewStats in statViewValues:
                        currentRowLabelName = eachViewStats[0][0]
                        if currentRowLabelName in rowLabelName:
                            stats[currentRowLabelName] = {}
                            for columnName, statValue in zip(columnNames, eachViewStats[0]):
                                stats[currentRowLabelName][columnName] = statValue

                else:
                    # Get all the traffic items
                    for eachViewStat in statViewValues:
                        currentRowLabelName = eachViewStat[0][0]
                        stats[currentRowLabelName] = {}                
                        for columnName, statValue in zip(columnNames, eachViewStat[0]):
                            stats[currentRowLabelName][columnName] = statValue
        else:
            # Get just one traffic item stat
            statViewValues = self.getStatViewResults(statViewName=statViewName, rowValuesLabel=rowLabelName)
            if statViewValues == 'kVoid':
                raise Exception('No such port name found.  Verify for typo: {}'.format(rowLabelName))

            stats[rowLabelName] = {}
            for columnName, statValue in zip(columnNames, statViewValues):
                stats[rowLabelName][columnName] = statValue

        return stats

    def getFlowStatistics(self):
        """
        Get Flow Statistics and put each row in a list.

        Return
           A dict of Flow Statistics: flowStatistics[rowNumber][columnName] = value
        """
        columnNames =   self.getStatViewResults(statViewName='Flow Statistics', getColumnCaptions=True)
        totalPages = self.getStatViewResults(statViewName='Flow Statistics', getTotalPages=True)

        flowStatistics = {}
        rowNumber = 1
        for pageNumber in range(1, totalPages+1):
            self.ixNetObj.Statistics.View.find(Caption='Flow Statistics')[0].Data.CurrentPage = pageNumber
            pageValues = self.getStatViewResults(statViewName='Flow Statistics', getPageValues=True)
            for eachRowValue in pageValues:

                flowStatistics[rowNumber] = {}
                for columnName, rowValue in zip(columnNames, eachRowValue[0]):
                    flowStatistics[rowNumber][columnName] = rowValue
                rowNumber += 1

        return flowStatistics

    def getTrafficItemStats(self, trafficItemName='all'):
        """
        Get Traffic Item statistics.

        :param trafficItemName: <str|list>: The Traffic Item name. 
                                If you're just getting one traffic item stat, pass in a string name.
                                If you want to get multiple traffic item stats, pass in a list.
                                Defaults to return all Traffic Item stats.

        Return
           A dict of all the TrafficItem statistics
        """
        return self.getStatsByRowLabelName(statViewName='Traffic Item Statistics', rowLabelName=trafficItemName)


    def getPortStatistics(self, rowLabelName='all'):
        """
        Get port statistics.

        :param rowLabelName: <str|list>: Format: '192.168.70.128/Card01/Port01'
                             If you're just getting one stat, pass in a rowLabelName.
                             If you want to get multiple port stats, pass in a list of rowLabelName.
                             Defaults to return all stats.

        Return
           dict
        """
        return self.getStatsByRowLabelName(statViewName='^Port Statistics$', rowLabelName=rowLabelName)


    def getPortCpuStatistics(self, rowLabelName='all'):
        """
        Get port cpu statistics.

        :param rowLabelName: <str|list>: Format: '192.168.70.128/Card01/Port01' 
                             If you're just getting one port stat, pass in a rowLabelName.
                             If you want to get multiple port stats, pass in a list of rowLabelName.
                             Defaults to return all stats.

        Return
           A dict of Port statistics in rows: portStatistics[statName]
        """
        return self.getStatsByRowLabelName(statViewName='Port CPU Statistics', rowLabelName=rowLabelName)


    def getGlobalProtocolStatistics(self, rowLabelName='all'):
        """
        Get global protocol statistics.

        :param rowLabelName: <str|list>: Format: '192.168.70.128/Card01/Port01' 
                             If you're just getting one protocol stat, pass in a string rowLabelName.
                             If you want to get multiple protocol stats, pass in a list of rowLabelName.
                             Defaults to return all stats.

        Return
           dict
        """
        return self.getStatsByRowLabelName(statViewName='Global Protocol Statistics', rowLabelName=rowLabelName)


    def getDataPlanePortStatistics(self, rowLabelName='all'):
        """
        Get data plane port statistics.

        :param rowLabelName: <str|list>: The port name
                             If you're just getting one port stat, pass in the port name.
                             If you want to get multiple port  stats, pass in a list of port names.
                             Defaults to return all stats.

        Return
           dict
        """
        return self.getStatsByRowLabelName(statViewName='Data Plane Port Statistics', rowLabelName=rowLabelName)

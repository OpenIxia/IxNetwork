""" Assistant class to simplify access to statistics views
"""

from ixnetwork_restpy.assistants.statistics.row import Row
from ixnetwork_restpy.testplatform.sessions.ixnetwork.ixnetwork import Ixnetwork
from ixnetwork_restpy.errors import *
from ixnetwork_restpy.files import Files
import re
import os
import time


class StatViewAssistant(object):
    REGEX = 'regex'
    LESS_THAN = '<'
    LESS_THAN_OR_EQUAL = '<='
    EQUAL = '=='
    NOT_EQUAL = '!='
    GREATER_THAN = '>'
    GREATER_THAN_OR_EQUAL = '>='

    @staticmethod
    def GetViewNames(IxNetwork):
        """Get a list of all view names.
        """
        assert(isinstance(IxNetwork, Ixnetwork))
        view_names = []
        for view in IxNetwork.Statistics.View.find():
            view_names.append(view.Caption)
        return view_names

    def __init__(self, IxNetwork, ViewName, Timeout=180):
        """
        Args:
            IxNetwork (obj (ixnetwork_restpy.testplatform.sessions.ixnetwork.Ixnetwork)): An Ixnetwork object
            ViewName (str): The name of a statistics view, supports regex
            Timeoout (int): The timeout in seconds to wait for the ViewName to be available and/or ready
        """
        assert(isinstance(IxNetwork, Ixnetwork))
        self._IxNetwork = IxNetwork
        self._ViewName = ViewName
        self._root_directory = self._IxNetwork._connection._read('%s/files' % self._IxNetwork.href)['absolute']
        self._Statistics = IxNetwork.Statistics
        self._View = None
        self._Timeout = Timeout
        self.ClearRowFilters()
        self._is_view_ready

    def _take_csv_snapshot(self):
        self._Statistics.CsvSnapshot.CsvStringQuotes = False
        self._Statistics.CsvSnapshot.SnapshotViewContents = 'allPages'
        self._Statistics.CsvSnapshot.SnapshotViewCsvGenerationMode = 'overwriteCSVFile'
        self._Statistics.CsvSnapshot.CsvLocation = self._root_directory
        self._Statistics.CsvSnapshot.CsvName = 'ixnetwork.restpy.%s' % (self._View.Caption)
        self._Statistics.CsvSnapshot.Views = self._View
        self._Statistics.CsvSnapshot.TakeCsvSnapshot()
        return self._IxNetwork._connection._get_file(self._IxNetwork.href, '%s.csv' % self._Statistics.CsvSnapshot.CsvName)

    @property
    def _is_view_ready(self):
        start = time.time()
        while self._View is None:
            view = self._Statistics.View.find(Caption='^%s$' % self._ViewName)
            if (len(view)) == 1:
                self._View = view
                break
            if time.time() - start > self._Timeout:
                raise NotFoundError('After %s seconds the %s view does not exist.' % (self._Timeout, self._ViewName))
            time.sleep(2)
        while True:
            if self._View.Data.IsReady is True:
                break
            if time.time() - start > self._Timeout:
               raise NotFoundError('After %s seconds the %s view has no data available.' % (self._Timeout, self._View.Caption))
            time.sleep(2)

    def _validate_filters(self):
        for index in self._filters:
            if self._filters[index]['columnName'] not in self.ColumnHeaders:
                raise NotFoundError('Column name %s is not valid for this view' % self._filters[index]['columnName'])

    @property
    def Rows(self):
        """Returns a snaphost of the all the rows in the view that match any filters that have been added.
        If no filters have been added then all rows are returned.

        Returns:
            obj (ixnetwork_restpy.assistants.statistics.row.Row): An iterable class encapsulating row data
        """
        self._is_view_ready
        self._validate_filters
        local_filename = self._take_csv_snapshot()
        rows = []
        column_headers = []
        with open(local_filename, 'r') as fid:
            column_headers = fid.readline()[:-1].split(',')
            for row in fid:
                row = row[:-1].split(',')
                match = True
                for column_index in range(len(row)):
                    if column_index in self._filters.keys():
                        comparator = self._filters[column_index]['comparator']
                        filter_value = self._filters[column_index]['filterValue']
                        if comparator == StatViewAssistant.REGEX:
                            if filter_value.search(row[column_index]) is None:
                                match = False
                        else:
                            expression = '%s %s %s' % (row[column_index], comparator, filter_value)
                            match = eval(expression)
                if match is True:
                    rows.append(row)
        os.remove(local_filename)
        return Row(self._View.Caption, column_headers, rows)

    @property
    def ColumnHeaders(self):
        """Returns a list of all the column headers in the view.
        """
        return self._View.Page.ColumnCaptions

    def AddRowFilter(self, ColumnName, Comparator, FilterValue):
        """Add a filter that reduces the Row resultset

        Args:
            ColumnName (str): A valid column name for this view
            Comparator (enum(REGEX|EQUAL|NOT_EQUAL)): A StatViewAssistant comparator constant
            FilterValue (str): Only those rows where the column matches this value will be returned 
        """
        if Comparator == StatViewAssistant.REGEX:
            FilterValue = re.compile(FilterValue)
        self._filters[self.ColumnHeaders.index(ColumnName)] = {
            'columnName': ColumnName,
            'comparator': Comparator,
            'filterValue': FilterValue
        }
        return self

    def ClearRowFilters(self):
        """Remove all filters that have been added using the AddFilter method.
        """
        self._filters = {}
        return self

    def CheckCondition(self, ColumnName, Comparator, ConditionValue, Timeout=90, CheckInterval=2, RaiseException=True):
        """Check that all the ColumnName cells in the view meet the comparator and condition value. 

        Args:
            ColumnName (str): A valid column name from which filtered cells will be compared
            Comparator (str): The comparator of the condition
            ConditionValue (str): The value of the condition to be met
            Timeout (int): The time to wait for the condition to be met
            CheckInterval (int): The time to wait between each check attempt
            RaiseException (bool): Raise an exception if the condition is not met otherwise return a bool result
        
        Returns:
            bool: True if the condition is met, False if the condition is not met
        
        Raises:
            obj(ixnetwork_restpy.errors.NotFoundError): If the condition is not met and the RaiseException is True 
        """
        self._validate_filters
        start = time.time()
        while time.time() - start < Timeout:
            match = True
            for row in self.Rows:
                expression = '%s %s %s' % (row[ColumnName], Comparator, ConditionValue)
                match = eval(expression)
                if match is False:
                    break
            if match is False:
                time.sleep(CheckInterval)
            else:
                return True
        if RaiseException is True:
            raise NotFoundError('Condition: [%s %s %s] has not been met after %s seconds.' % (ColumnName, Comparator, ConditionValue, Timeout))
        else:
            return False

    def DrillDownOptions(self):
        """Use one of the following available drill down options as the input to the DrillDown method
        
        Returns:
            list(str): A list of available drill down options
        """
        drill_down = self._View.Drilldown.Find()
        return drill_down.AvailableDrillDownOptions

    def TargetRowFilters(self):
        """Use one of the following available target row filters as the input to the DrillDown method
        
        Returns:
            list(str): A list of available target row filters
        """
        drill_down = self._View.Drilldown.Find()
        return drill_down.TargetRowFilters

    def Drilldown(self, TargetRowIndex, DrillDownOption, TargetRowFilter):
        """Drilldown on an existing view to get a new StatViewAssistant

        Args:
            TargetRowIndex (int): the 0 based index of the row that you are interested in drilling down into
            DrillDownOption (str): drill down options are dynamic and are based on tracking options selected during traffic item creation
            TargetRowFilter (str): drill down filters are dynamic and are based on tracking options selected during traffic item creation

        Returns:
            obj(ixnetwork_restpy.assistants.statistics.statviewassistant.StatViewAssistant)
        """
        drill_down = self._View.Drilldown.Find()
        drill_down.TargetRowIndex = TargetRowIndex
        drill_down.TargetDrillDownOption = DrillDownOption
        drill_down.TargetRowFilter = TargetRowFilter
        drill_down.DoDrillDown()
        return StatViewAssistant('User Defined Statistics')

    def __str__(self):
        """Return a string with all the rows in the current view
        """
        statistics = ''
        for row in self.Rows:
            statistics += row.__str__()
        return statistics

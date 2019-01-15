"""Rows class to simplify access to statistics views data
"""

from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.view import View
from ixnetwork_restpy.errors import *
import datetime


try:
    basestring
except NameError:
    basestring = str


class Row(object):
    def __init__(self, view_name, column_headers, row_data):
        """
        Args:
            view_name (str): The name of the statistics view
            column_headers (list(str)): A list of column headers
            row_data (list(list)): 
        """
        self._sample_time = datetime.datetime.utcnow()
        self._view_name = view_name
        self._column_headers = column_headers
        self._row_data = row_data
        self._index = -1

    def __iter__(self):
        self._index = -1
        return self

    def next(self):
        return self.__next__()

    def __next__(self):
        if self._index + 1 >= len(self._row_data):
            raise StopIteration
        else:
            self._index += 1
        return self

    def __getitem__(self, index):
        """Set the row index or return a cell value

        Cell retrieval on a row is accomplished by using an index
        # specifying an ordinal sets the row index
        # specifying a regex that is not a valid column label also sets the row index based on the first match
        # the regex can be used to match the contents of many cells in the row and it will return the first row that matches
        # if the index is a valid column header label then the cell value for the current row and column header label will be returned
        """
        if isinstance(index, basestring):
            if index in self._column_headers:
                return self._row_data[self._index][self._column_headers.index(index)]
            import re
            regex = re.compile(index)
            for row_index in range(len(self._row_data)):
                for cell in self._row_data[row_index]:
                    if regex.search(cell) is not None:
                        self._index = row_index
                        return self
            raise IndexError
        if index >= len(self._row_data):
            raise IndexError		
        else:
            self._index = index
        return self
    
    def __len__(self):
        return len(self._row_data)

    def __str__(self):
        if self._index == -1 or self._index >= len(self._row_data):
            return 'No row data'
        row = 'Row:%s  View:%s  Sampled:%s UTC\n' % (self._index, self._view_name, self._sample_time)
        for column_index in range(len(self._column_headers)):
            row += '\t%s: %s\n' % (self._column_headers[column_index], self._row_data[self._index][column_index])
        return row 

    @property
    def Columns(self):
        """Returns (list(str)): list of column headers for the encapsulated rows"""
        return self._column_headers

    @property
    def RawData(self):
        """Returns (list(list(str))): list of rows, where each row is a list of cells"""
        return self._row_data
    
    @property
    def SampleTime(self):
        """Returns (str): utc datetime of when the sample was taken from the server
        """
        return self._sample_time



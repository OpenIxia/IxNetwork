"""Demonstrates how to use the StatViewAssist class

This sample requires an already loaded configuration with at least 2 connected vports.

"""

from ixnetwork_restpy.testplatform.testplatform import TestPlatform
from ixnetwork_restpy.assistants.statistics.statviewassistant import StatViewAssistant
from ixnetwork_restpy.errors import *


# connect to a windows test platform using the default api server rest port
test_platform = TestPlatform('127.0.0.1', rest_port=11009, platform='windows')

# use the default session and get the root node of the hierarchy
ixnetwork = test_platform.Sessions.find().Ixnetwork

ixnetwork.info('negative test')
try:
    StatViewAssistant(ixnetwork, 'my test view', Timeout=5)
except NotFoundError as e:
    ixnetwork.info(e)

# get a list of all current statistic views that can be used in the StatViewAssistant
print(StatViewAssistant.GetViewNames(ixnetwork))

# create a stat view assistant for a statistics view
port_statistics = StatViewAssistant(ixnetwork, 'Port Statistics')

# print all the rows for a statistics view
print(port_statistics)

# add a filter so that only a single row is retrieved
port_statistics.AddRowFilter('Port Name', StatViewAssistant.REGEX, 'Port 1$')
print(port_statistics)

# demonstrate cell access
port_statistics.ClearRowFilters()
rows = port_statistics.Rows

# get the cell value at row 0, column 'Port Name'
print(rows[0]['Port Name'])

# get the cell value at row 1, column 'Stat Name'
print(rows[1]['Stat Name'])

# get the cell value at the first row that matches a regex of 'case insensitive endswith port 1', column 'Frames Tx.'
print(rows['(?i)port 1$']['Frames Tx.'])

ixnetwork.info('check that all ipv4 protocols are up')
protocols_summary = StatViewAssistant(ixnetwork, 'Protocols Summary')
protocols_summary.AddRowFilter('Protocol Type', StatViewAssistant.REGEX, '(?i)^ipv4?')
protocols_summary.CheckCondition('Sessions Not Started', StatViewAssistant.EQUAL, 0)
protocols_summary.CheckCondition('Sessions Down', StatViewAssistant.EQUAL, 0)

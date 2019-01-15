"""Demonstrates drilling down on an already established statistics view.
This sample requires a running ixnetwork instance that has traffic being transmitted.
"""

from time import sleep
from ixnetwork_restpy.testplatform.testplatform import TestPlatform


# connect to a test platform, create a session and get the root IxNetwork object
test_platform = TestPlatform('127.0.0.1', rest_port=11009)
test_platform.Trace = 'request_response'
sessions = test_platform.Sessions.find(Id=1)
ixnetwork = sessions.Ixnetwork

# get the view you want to drill down on
caption = 'Traffic Item Statistics'
view = ixnetwork.Statistics.View.find(Caption=caption)
assert(len(view) == 1)

# get the drill down node for the view
drill_down = view.DrillDown.find()

# prior to getting the drill down options the target row index must be set
# the target row index is the 0 based index of the row that you are interested in drilling down into
drill_down.TargetRowIndex = 0

# print the drill down options for the view
# drill down options are dynamic and are based on tracking options selected during traffic item creation
for drill_down_option in drill_down.AvailableDrillDownOptions:
	print(drill_down_option)
drill_down.TargetDrillDownOption = drill_down.AvailableDrillDownOptions[1]
for drill_down_filter in drill_down.AvailableTargetRowFilters:
	print(drill_down_filter)
if len(drill_down.AvailableTargetRowFilters) > 0:
	drill_down.TargetRowFilter = drill_down.AvailableTargetRowFilters[0]

# perform the drill down operation
drill_down.DoDrillDown()

# the drill down operation populates the read only 'User Defined Statistics' view
# get the resulting drill down view
user_defined_statistics = ixnetwork.Statistics.View.find(Caption='User Defined Statistics')

# wait for data to become available
attempts = 0
while user_defined_statistics.Data.IsReady is False and attempts < 10:
    sleep(1)
    attempts += 1

# print the column headers
print(' '.join(user_defined_statistics.Data.ColumnCaptions))

# print the ingress and egress rows
for ingress_egress_rows in user_defined_statistics.Data.PageValues:
    for row in ingress_egress_rows:
        print(' '.join(row))

import sys
import os
sys.path[0] = os.path.abspath(sys.path[0] + '\\..\\..\\')

from ixnetwork_restpy.testplatform.testplatform import TestPlatform

# default output is to the sys.stdout
# to output to a log file, use the log_file_name param
# default tracing is 'none' which is no tracing of request and response messages
test_platform = TestPlatform('127.0.0.1', rest_port=11009, log_file_name='test.log')
sessions = test_platform.Sessions.add()

# trace requests
# the next add vport should show a debug message for the request
print('LOG REQUEST ONLY')
test_platform.Trace='request'
sessions.Ixnetwork.Vport.add()

# trace requests and responses
# the next add vport should show debug messages for the request and response
print('LOG REQUEST AND RESPONSES')
test_platform.Trace='request_response'
sessions.Ixnetwork.Vport.add()

# turn off tracing
# the next add vport should not show debug messages for the request and response
print('LOG NOTHING')
test_platform.Trace='none'
sessions.Ixnetwork.Vport.add()

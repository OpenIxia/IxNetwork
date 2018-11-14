"""Demonstrates file handling.

The Files object determines how file content is uploaded/downloaded.
Prior to an operation if local_file=True is specified the content will be pushed to the server if the content exists locally.
If the file does not exist locally an empty file using only the file name will be created on the server. 
After the operation the Files object also determines how file content is downloaded
If local_file=True the content will be downloaded to the client and saved with the file path/name specified

"""

from ixnetwork_restpy.testplatform.testplatform import TestPlatform
from ixnetwork_restpy.files import Files


# connect to a test platform, create a session and get the root IxNetwork object
test_platform = TestPlatform('127.0.0.1', rest_port=11009)
test_platform.Trace = 'request_response'
sessions = test_platform.Sessions.find(Id=1)
ixnetwork = sessions.Ixnetwork

ixnetwork.SaveConfig(Files('sample.ixncfg', local_file=True))

# 
ixnetwork.LoadConfig(Files('c:/temp/sample.ixncfg', local_file=True))




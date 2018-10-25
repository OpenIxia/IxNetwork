"""Demonstrates different methods of configuration the TestPlatform object 
in order to connect to different IxNetwork test platforms.

"""

from ixnetwork_restpy.testplatform.testplatform import TestPlatform


# connect to a windows platform using the default api server rest port
test_platform = TestPlatform('127.0.0.1', rest_port=11009, platform='windows')

# connect to a windows connection manager platform using the default api server rest port
test_platform = TestPlatform('127.0.0.1', platform='windows')

# connect to a linux api server platform using the default api server rest port
test_platform = TestPlatform('127.0.0.1', platform='linux')



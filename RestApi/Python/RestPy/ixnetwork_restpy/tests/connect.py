"""Demonstrates different methods of connecting to IxNetwork test platforms
"""
import sys
import os
sys.path[0] = os.path.abspath(sys.path[0] + '\\..\\..\\')
from ixnetwork_restpy.testplatform.testplatform import TestPlatform


# connect to a windows platform using the default api server rest port
test_platform = TestPlatform('127.0.0.1', rest_port=11009, platform='windows')

# connect to a windows connection manager platform using the default api server rest port
test_platform = TestPlatform('127.0.0.1', platform='windows')

# connect to a linux api server platform using the default api server rest port
test_platform = TestPlatform('127.0.0.1', platform='linux')



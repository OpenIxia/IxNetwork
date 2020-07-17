"""
connectToExistingConfig.py

   Connecting to an existing session.

Supports IxNetwork API servers:
   - Windows, Windows Connection Mgr and Linux

Requirements
   - Minimum IxNetwork 8.50
   - Python 2.7 and 3+
   - pip install requests
   - pip install ixnetwork_restpy (minimum version 1.0.51)

RestPy Doc:
    https://www.openixia.github.io/ixnetwork_restpy
"""

import os, sys, time, traceback

# Import the RestPy module
from ixnetwork_restpy import SessionAssistant, Files

try:
    session = SessionAssistant(IpAddress='192.168.70.3', RestPort=None, UserName='admin', Password='admin', 
                               SessionName=None, SessionId=1, ApiKey=None, ClearConfig=False, LogLevel='info')

    ixNetwork = session.Ixnetwork

except Exception as errMsg:
    print('\nError: %s' % traceback.format_exc())
    print('\nrestPy.Exception:', errMsg)

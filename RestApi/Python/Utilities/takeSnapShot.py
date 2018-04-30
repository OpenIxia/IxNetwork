
"""
Description
   Take snapshot of any statistics by the statview name.
   If mode == overwrite, create a new file every time.
   If mode == append, append stats to the existing stat file.

   To view all the feature options, take a look at the statistics module
   IxNetRestApiStatistics.py under takeSnapshot() function.

Requirements
   - Python 2.7 - 3+
   - requests module

Example:
    statObj = Statistics(mainObj)
    statObj.takeSnapshot(viewName='Traffic Item Statistics', windowsPath='c:\\Results', mode='append')
    statObj.takeSnapshot(viewName='Flow Statistics', windowsPath='c:\\Results', mode='overwrite')
"""

import sys, traceback, time

sys.path.insert(0, '../Modules')
from IxNetRestApi import *
from IxNetRestApiStatistics import Statistics

# Default the API server to either windows or linux.
connectToApiServer = 'windows'

if len(sys.argv) > 1 and sys.argv[1] not in ['windows', 'linux']:
    sys.exit("\nError: %s is not a known option. Choices are 'windows' or 'linux'." % sys.argv[1])
if len(sys.argv) > 1:
    connectToApiServer = sys.argv[1]

try:
    enableDebugTracing = True

    if connectToApiServer == 'linux':
        mainObj = Connect(apiServerIp='192.168.70.108',
                          serverIpPort='443',
                          username='admin',
                          password='admin',
                          deleteSessionAfterTest=deleteSessionAfterTest,
                          verifySslCert=False,
                          serverOs=connectToApiServer
        )
        
    if connectToApiServer == 'windows':
        mainObj = Connect(apiServerIp='192.168.70.3', serverIpPort='11009')

    statObj = Statistics(mainObj)
    # mode: append|overwrite
    statObj.takeSnapshot(viewName='Traffic Item Statistics', windowsPath='c:\\Results', mode='append')
    
    #statObj.takeSnapshot(viewName='Flow Statistics', windowsPath='c:\\Results', mode='append')


except (IxNetRestApiException, Exception, KeyboardInterrupt) as errMsg:
    if enableDebugTracing:
        if not bool(re.search('ConnectionError', traceback.format_exc())):
            print('\n%s' % traceback.format_exc())

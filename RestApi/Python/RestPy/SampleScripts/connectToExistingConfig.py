import sys, time

from ixnetwork_restpy.testplatform.testplatform import TestPlatform
import RestpyUtils

sys.path.insert(0, (os.path.dirname(os.path.abspath(__file__).replace('SampleScripts', 'Modules'))))
from StatisticsMgmt import Statistics
from PortMgmt import Ports

osPlatform = 'windows'

if osPlatform in ['windows', 'windowsConnectionMgr']:
    insecure = True
    apiServerIp = '192.168.70.3'
    apiServerPort = 11009

if osPlatform == 'linux':
    insecure = False
    apiServerIp = '192.168.70.121'
    apiServerPort = 443

licenseServerIp = ['192.168.70.3']
licenseMode = 'subscription'

ixChassisIp = '192.168.70.120'
portList = [[ixChassisIp, 1, 1], [ixChassisIp, 1, 2]]

if osPlatform == 'windows':
    insecure = True
if osPlatform == 'linux':
    insecure = False

try:
    if osPlatform == 'windows':
        testPlatform = TestPlatform(apiServerIp, rest_port=apiServerPort, insecure=insecure)
        testPlatform.Trace = True
        session = testPlatform.add_Sessions()
        ixNetwork = session.Ixnetwork
    
    if osPlatform == 'linux':
        testPlatform = TestPlatform(apiServerIp, rest_port=apiServerPort, insecure=insecure)
        testPlatform.Trace = True

        # How to connect to an existing session ID
        ixNetwork.ApiKey = '9277fc8fe92047f6a126f54481ba07fc'
        session = ixNetwork.Sessions(Id=6)
        ixNetwork = session.Ixnetwork


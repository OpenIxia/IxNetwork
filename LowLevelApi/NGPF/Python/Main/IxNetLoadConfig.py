#!/opt/ActivePython-2.7/bin/python

# The IxNetwork module is the file IxNetwork.py
# located in /IxNetwork_7.0_EA/PythonApi
# Users have to manually copy this file to their
# Python location because each Unix platform has
# Python installed in different locations.

import IxNetwork
import time
import sys
import os

class IxTopoNamespace: pass
ixTopo = IxTopoNamespace()

ixTopo.portList = ['(2 1)', '(2 2)', '(2 3)']
ixTopo.ixNetTclServer = '10.205.1.42'
ixTopo.ixChassis = '10.205.4.35'
ixTopo.ixNetTclPort = '8009'
ixTopo.ixNetVersion = '7.0'
ixTopo.ixNetworkCfgFile = '/home/hgee/MyIxiaWork/Temp/WorstPerformers.ixncfg'

print (ixTopo.portList, ixTopo.ixNetTclServer)

ixNet = IxNetwork.IxNet()
print ('Verifying ixNetwork.IxNet() :', ixNet)

getNull = ixNet.getNull()
print ('Verifying ixNet.getNull() :', getNull) ;# getNull = ::ixNet::OBJ-null

connect = ixNet.connect(ixTopo.ixNetTclServer, 'port', ixTopo.ixNetTclPort, '-version', ixTopo.ixNetVersion)
print ('Verifying ixNet.connect() :', connect) ;# ::ixNet::OK

getVersion = ixNet.getVersion()
print ('Verifying ixNet.getVersion() :', getVersion) ;# 6.30.701.16

setSessionParameter = ixNet.setSessionParameter('setAttr', 'strict')
print ('Verifying ixNet.setSessionParameter() :', setSessionParameter) ;# ::ixNet::OK

print('\nCreating a new blank config\n')
ixNet.execute('newConfig')

if not os.path.exists(ixTopo.ixNetworkCfgFile):
    print('\nNo such ixncfg file: ', ixTopo.ixNetworkCfgFile, '\n')
    sys.exit()
else:
    print('\nLoading the ixncfg config file ...\n')
    #ixNet exec loadConfig [ixNet readFrom $ixNetworkCfgFile]] != "::ixNet::OK"
    readFromResult = ixNet.execute('loadConfig', ixNet.readFrom(ixTopo.ixNetworkCfgFile))
    if readFromResult != '::ixNet::OK':
        print('\nLoading config file failed:', readFromResult, '\n')
        sys.exit()
    else:
        print('\nSuccessfully loaded config file: ')
        print(ixTopo.ixNetworkCfgFile)

getRoot = ixNet.getRoot()
print('Verifying getRoot: ', getRoot)

vPortList = ixNet.getList(getRoot, 'vport')
print('vPortList: ', vPortList)

if len(vPortList) != len(ixTopo.portList):
    print("\nvPortList and portList don't match")
    sys.exit()
else:
    print('\nvPortList is equal length with portList', '\n')
    

trafficItemList = ixNet.getList(getRoot+'/traffic', 'trafficItem')
for x in trafficItemList:
    print('ti: ' + x.split('/')[2])


disconnect = ixNet.disconnect()
print ('Verifying disconnection: ', disconnect)

sys.exit()

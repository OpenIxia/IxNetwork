#!/usr/local/python3.4.6/bin/python3.4

# DISCLAIMER
#
#    This is a sample script for demo and reference purpose only.
#    It is subject to change for content updates without warning.
#
# Description:
#
#    - Load a saved Quick Test config file.
#    - Reassign Ports:  Exclude calling assignPorts if it's unecessary.
#    - Verify port states.
#    - Apply Quick Test
#    - Start Quick Test
#    - Monitor Quick Test progress
#    - Get stats
#
#    This sample script supports both Windows IxNetwork API server and 
#    Linux API server.  If connecting to a Linux API server and the API
#    server is newly installed, it configures the one time global license server settings.

import sys
import requests
import json
import os
import time
import re
import traceback
import IxN_RestApiPy3

configFile = '/Temp/QuickTest_vm8.20.ixncfg'

# Which REST API server do you want to connect to: linux or windows
connectToApiServer = 'windows'

# Settings for Windows 
if connectToApiServer == 'windows':
    ixNetRestServerIp = '192.168.70.127'
    ixNetRestServerPort = '11009'
    ixChassisIp = '192.168.70.10'

# Setitngs for Linux API Server
if connectToApiServer == 'linux':
    linuxServerIp = '192.168.70.137'
    username = 'admin'
    password = 'admin'
    deleteLinuxSessionWhenDone = True
    
    # Set to True if the Linux API Server is newly installed.
    # We need to set the license server settings once. 
    isLinuxApiServerNewlyInstalled = False
    
    licenseServerIp = '192.168.70.127'
    licenseMode = 'subscription' ;# IxVM uses subscription. Physical chassis uses perpetual.
    licenseTier = 'tier3'
    linuxServerUrl = 'https://%s' % linuxServerIp
    
portList = [[ixChassisIp, '1', '1'],
            [ixChassisIp, '2', '1']]

# For connecting to Linux API server that supports SSL. Provide your SSL certificate here.
verifySslCert = False

try:    
    # If connecting to Linux API server
    if connectToApiServer == 'linux':
        # This will disable all the SSL warnings on your terminal.
        requests.packages.urllib3.disable_warnings()

        returnList = IxN_RestApiPy3.connectToLinuxApiServer(linuxServerIp, username=username, password=password)
        sessionUrl, sessionId, apiKey = returnList

        if isLinuxApiServerNewlyInstalled:
            IxN_RestApiPy3.linuxServerConfigGlobalLicenseServer(linuxServerIp, licenseServerIp,
                                                                licenseMode, licenseTier,
                                                                apiKey, verifySslCert=verifySslCert)
        IxN_RestApiPy3.linuxServerConfigNewSessionLicense(sessionUrl, linuxServerIp, apiKey, verifySslCert=verifySslCert)

    # If connecting to Windows API server
    if connectToApiServer == 'windows':
        sessionUrl = IxN_RestApiPy3.getSessionUrl(ixNetRestServerIp, ixNetRestServerPort)
        apiKey=None
        sessionId = sessionUrl.split('/ixnetwork')[0]


    IxN_RestApiPy3.loadConfigFile(sessionUrl, configFile, apiKey=apiKey, verifySslCert=verifySslCert)
    IxN_RestApiPy3.assignPorts(sessionUrl, portList, apiKey=apiKey, verifySslCert=verifySslCert)
    IxN_RestApiPy3.verifyPortState(sessionUrl, apiKey=apiKey, verifySslCert=verifySslCert)

    quickTestHandle = IxN_RestApiPy3.getQuickTestHandleByName(sessionUrl, 'QuickTest1',
                                                              apiKey=apiKey, verifySslCert=False)

    IxN_RestApiPy3.applyQuickTest(sessionUrl, quickTestHandle, apiKey=apiKey, verifySslCert=False)
    IxN_RestApiPy3.startQuickTest(quickTestHandle, apiKey=apiKey, verifySslCert=False)

    IxN_RestApiPy3.monitorQuickTestRunningProgress(quickTestHandle, getProgressInterval=3,
                                                      apiKey=apiKey, verifySslCert=False)

    stats = IxN_RestApiPy3.getStats(sessionUrl, viewName='Flow Statistics', apiKey=apiKey,
                                    verifySslCert=verifySslCert)

    print('\n{txPort:10} {txFrames:15} {rxPort:10} {rxFrames:15} {frameLoss:10}'.format(
        txPort='txPort', txFrames='txFrames', rxPort='rxPort', rxFrames='rxFrames', frameLoss='frameLoss'))
    print('-'*90)

    for flowGroup,values in stats.items():
        txPort = values['Tx Port']
        rxPort = values['Rx Port']
        txFrames = values['Tx Frames']
        rxFrames = values['Rx Frames']
        frameLoss = values['Frames Delta']

        print('{txPort:10} {txFrames:15} {rxPort:10} {rxFrames:15} {frameLoss:10} '.format(
            txPort=txPort, txFrames=txFrames, rxPort=rxPort, rxFrames=rxFrames, frameLoss=frameLoss))

        #if txFrames != rxFrames:
        #    print('\nFrame loss error:', int(txFrames) - int(rxFrames))

    if jsonData['connectToApiServer'] == 'linux' and jsonData['deleteLinuxSessionWhenDone'] == True:
        linuxServerStopAndDeleteSession(sessionId, apiKey=apiKey, verifySslCert=verifySslCert)

except IxNetRestUtilityException as errMsg:
    print('\nTest failed! {0}\n'.format(errMsg))
    if 'sessionId' in locals() and jsonData['deleteLinuxSessionWhenDone'] == True:
        linuxServerStopAndDeleteSession(sessionId, apiKey=apiKey, verifySslCert=verifySslCert)

except Exception as errMsg:
    print('\nTest failed! {0}\n'.format(traceback.print_exc()))
    if 'sessionId' in locals() and jsonData['deleteLinuxSessionWhenDone'] == True:
        linuxServerStopAndDeleteSession(sessionId, apiKey=apiKey, verifySslCert=verifySslCert)

except KeyboardInterrupt:
    print('\nAborting ...')
    if 'sessionId' in locals() and jsonData['deleteLinuxSessionWhenDone'] == True:
        linuxServerStopAndDeleteSession(sessionId, apiKey=apiKey, verifySslCert=verifySslCert)

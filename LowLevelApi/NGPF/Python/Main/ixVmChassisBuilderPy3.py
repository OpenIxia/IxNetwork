#!/usr/local/python3.4.6/bin/python3.4

# Description
#
#   When installing or upgrading virtual chassis and virtual line cards,
#   you need to create Chassis Topology.  This means to add a vChassis
#   and virtual cards before you could connect to the ports.
# 
# POST: /api/v1/sessions/1/ixnetwork/operations/connecttochassis
# DATA: {"arg1": "192.168.70.10"}
#
# POST: /api/v1/sessions/1/ixnetwork/availableHardware/virtualChassis/ixVmCard
# DATA: {"cardId": "1", "managementIp": "192.168.70.130"}
# POST: /api/v1/sessions/1/ixnetwork/availableHardware/virtualChassis/ixVmCard
# DATA: {"cardId": "2", "managementIp": "192.168.70.131"}
#   

import time
import requests
import json
import sys
import traceback

import IxN_RestApiPy3

# Which REST API server do you want to connect to: linux or windows
connectToApiServer = 'windows'

if connectToApiServer == 'windows':
    ixChassisIp = '192.168.70.10'
    ixNetworkVersion = '8.20'
    ixNetRestServerIp = '192.168.70.127'
    ixNetRestServerPort = '11009'
    vLoadModuleType = 'vmware' ;# vmware or qemu

# Setitngs for Linux
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

ixvmCardPortList = [[1, '192.168.70.130'], [2, '192.168.70.131']]
verifySslCert = False

httpHeader = 'http://%s:%s' % (ixNetRestServerIp, ixNetRestServerPort)

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


    # Example #1:
    #    These eare steps to create IxVM cards/ports by a list.
    IxN_RestApiPy3.connectToVChassis(sessionUrl, ixChassisIp, apiKey=apiKey, verifySslCert=False)

    # Example #1: Add IxVM CardId/PortId in a tuple list of (cardId, mgmtIp).
    IxN_RestApiPy3.ixVmAddCardIdPortId(sessionUrl, ixvmCardPortList,
                                       apiKey=apiKey, verifySslCert=verifySslCert)

    chassisUrl = IxN_RestApiPy3.connectIxChassis(sessionUrl, ixChassisIp,
                                                 apiKey=apiKey, verifySslCert=verifySslCert)
    

    '''
    # Example #2:
    #    These are steps to create IxVM card/port individually.
    #
    # POST: /api/v1/sessions/1/ixnetwork/operations/connecttochassis
    # DATA: {"arg1": "192.168.70.10"}
    IxN_RestApiPy3.connectToVChassis(sessionUrl, ixChassisIp, apiKey=apiKey, verifySslCert=False)

    # Add IxVM CardId/PortId individually to the Chassis Topology.
    # POST: /api/v1/sessions/1/ixnetwork/availableHardware/virtualChassis/ixVmCard
    # DATA: {"cardId": "1", "managementIp": "192.168.70.130"}
    card1Obj = IxN_RestApiPy3.ixVmConfigCardId(sessionUrl=sessionUrl, cardId=1, mgmtIp='192.168.70.130',
                                               apiKey=apiKey, verifySslCert=verifySslCert)
    card2Obj = IxN_RestApiPy3.ixVmConfigCardId(sessionUrl=sessionUrl, cardId=2, mgmtIp='192.168.70.131',
                                               apiKey=apiKey, verifySslCert=verifySslCert)

    # Configure the IxVM cards/ports:
    # POST: /api/v1/sessions/1/ixnetwork/availableHardware/virtualChassis/ixVmCard/1/ixVmPort
    # DATA: {"portId": "1", "mtu": "1500", "promiscMode": "false", "interface": "eth1"}
    card1Port1Obj = IxN_RestApiPy3.ixVmConfigPortId(httpHeader+card1Obj, 
                                                    apiKey=apiKey, verifySslCert=verifySslCert)
    card2Port1Obj = IxN_RestApiPy3.ixVmConfigPortId(httpHeader+card2Obj,
                                                    apiKey=apiKey, verifySslCert=verifySslCert)
    IxN_RestApiPy3.ixVmGetListCardId(sessionUrl, apiKey=apiKey, verifySslCert=verifySslCert)

    # Connect the chassis for usage.  Next will be assigning ports.
    chassisUrl = IxN_RestApiPy3.connectIxChassis(sessionUrl, ixChassisIp,
                                                 apiKey=apiKey, verifySslCert=verifySslCert)
    '''

except IxN_RestApiPy3.IxNetRestUtilityException as errMsg:
    print('\nTest failed! {0}\n'.format(errMsg))
    if 'sessionId' in locals() and deleteLinuxSessionWhenDone == True:
        IxN_RestApiPy3.linuxServerStopAndDeleteSession(sessionId, apiKey=apiKey, verifySslCert=verifySslCert)

except Exception as errMsg:
    print('\nTest failed! {0}\n'.format(traceback.print_exc()))
    if 'sessionId' in locals() and deleteLinuxSessionWhenDone == True:
        IxN_RestApiPy3.linuxServerStopAndDeleteSession(sessionId, apiKey=apiKey, verifySslCert=verifySslCert)

except KeyboardInterrupt:
    print('\nAborting ...')
    if 'sessionId' in locals() and deleteLinuxSessionWhenDone == True:
        IxN_RestApiPy3.linuxServerStopAndDeleteSession(sessionId, apiKey=apiKey, verifySslCert=verifySslCert)


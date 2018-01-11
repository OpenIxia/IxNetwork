
# PLEASE READ DISCLAIMER
#
#    This class demonstrates sample IxNetwork REST API usage for
#    demo and reference purpose only.
#    It is subject to change for updates without warning.
#
# REQUIREMENTS
#    - Python 2.7.9+
#    - Python modules: requests
#

from __future__ import absolute_import, print_function, division
import os, re, sys, requests, json, time, subprocess, traceback

class IxNetRestApiException(Exception): pass

class Connect(object):
    def __init__(self, apiServerIp=None, serverIpPort=None, serverOs='windows',
                 username=None, password='admin', licenseServerIp=None, licenseMode=None, licenseTier=None,
                 deleteSessionAfterTest=True, verifySslCert=False, includeDebugTraceback=True, sessionId=None,
                 apiKey=None, generateRestLogFile=False):
        """
        Description
            Class Connect()
            Initial settings for this Class.

        Parameters
            serverIp: The REST API server IP address.
            serverPort: The server IP address socket port.
            apiServer: windows, windowsConnectionMgr or linux
            includeDebugTraceback: True or False.
                                   If True, traceback messsages are included in raised exceptions.
                                   If False, no traceback.  Less verbose.

            The rest of the parameters are for connecting to a Linux API server only.
               username: The login username.
               password: The login password.
               licenseServerIp: The license server IP address.
               licenseMode: subscription, perpetual or mixed.
               licenseTier: tier1, tier2, tier3.
               isLinuxApiServerNewlyInstalled: True or False.
                                               If True, then configure the global license server settings also.
               deleteSessionAfterTest: True or False.
                                       If True, delete the session.
                                       If False, session is not deleted for debugging or for viewing.
               verifySslCert: Include your SSL certificate for added access security.
               apiServerPlatform: windows or linux.  Defaults to windows.
               includeDebugTraceback: True or False. If True, include tracebacks in raised exceptions
               sessionId: To session ID on the Linux API server to connect to.
               apiKey: The Linux API server user API-KEY to use for the sessionId connection.

       Class Variables:
            apiServerPlatform: windows, windowsConnectionMgr, linux
            sessionUrl: The session's URL: http://{apiServerIp:11009}/api/v1/sessions/1/ixnetwork
            sessionId : http://{apiServerIp:11009}/api/v1/sessions/1
            jsonHeader: The default URL header: {"content-type": "application/json"}
            apiKey: For Linux API server only. Automatically provided by the server when connecting and authenticating.
                    You could also provide an API-Key to connect to an existing session. Get the API-Key from the Linux API server.
        """
        from requests.exceptions import ConnectionError
        from requests.packages.urllib3.connection import HTTPConnection

        self.jsonHeader = {"content-type": "application/json"}
        self.apiKey = None
        self.verifySslCert = verifySslCert
        self.linuxApiServerIp = apiServerIp
        self.apiServerPort = serverIpPort
        self.generateRestLogFile = generateRestLogFile
        if generateRestLogFile:
            self.restLogFile = 'restApiLog.txt'
            with open(self.restLogFile, 'w') as restLogFile:
                restLogFile.write('')

        if serverOs in ['windows', 'windowsConnectionMgr']:
            self.apiServerPlatform = serverOs
            self.getSessionUrl(apiServerIp, serverIpPort)

        if serverOs == 'linux':
            # Disable SSL warning messages
            requests.packages.urllib3.disable_warnings()
            if self.apiServerPort == None:
                self.apiServerPort == 443
            self.apiServerPlatform = 'linux'

            # Connect to an existing session on the Linux API server
            if apiKey != None and sessionId == None:
                raise IxNetRestApiException('Providing an apiKey must also provide a sessionId.')
            if apiKey and sessionId:
                self.sessionId = 'https://{0}:{1}/api/v1/sessions/{2}'.format(self.linuxApiServerIp, self.apiServerPort, str(sessionId))
                self.sessionUrl = 'https://{0}:{1}/api/v1/sessions/{2}/ixnetwork'.format(self.linuxApiServerIp, self.apiServerPort, sessionId)
                self.httpHeader = self.sessionUrl.split('/api')[0]
                self.apiKey = apiKey
                self.jsonHeader = {'content-type': 'application/json', 'x-api-key': self.apiKey}

            self.connectToLinuxApiServer(apiServerIp, username=username, password=password, verifySslCert=verifySslCert)

            if licenseServerIp or licenseMode or licenseTier:
                self.configLicenseServerDetails(licenseServerIp, licenseMode, licenseTier)

        # For Linux API Server only: Delete the session when script is done.
        self.deleteSessionAfterTest = deleteSessionAfterTest

        if includeDebugTraceback == False:
            sys.tracebacklimit = 0

    def get(self, restApi, data={}, stream=False, silentMode=False, ignoreError=False):
        """
        Description
           A HTTP GET function to send REST APIs.

        Parameters
           restApi: The REST API URL.
           data: The data payload for the URL.
           silentMode: True or False.  To display URL, data and header info.
           ignoreError: True or False.  If False, the response will be returned.
        """
        if silentMode is False or self.generateRestLogFile is True:
            #print('\nGET:', restApi)
            #print('HEADERS:', self.jsonHeader)
            self.logInfo('\nGET: {0}'.format(restApi))
            self.logInfo('HEADERS: {0}'.format(self.jsonHeader))

        try:
            # For binary file
            if stream:
                response = requests.get(restApi, stream=True, headers=self.jsonHeader, verify=self.verifySslCert)
            if stream == False:
                response = requests.get(restApi, headers=self.jsonHeader, verify=self.verifySslCert)

            if silentMode is False:
                self.logInfo('STATUS CODE: {0}'.format(response.status_code))
            if not re.match('2[0-9][0-9]', str(response.status_code)):
                if ignoreError == False:
                    if 'message' in response.json() and response.json()['messsage'] != None:
                        self.logWarning('\n%s' % response.json()['message'])
                    raise IxNetRestApiException('GET error:{0}\n'.format(response.text))
            return response

        except requests.exceptions.RequestException as errMsg:
            raise IxNetRestApiException('GET error: {0}\n'.format(errMsg))

    def post(self, restApi, data={}, headers=None, silentMode=False, noDataJsonDumps=False, ignoreError=False):
        """
        Description
           A HTTP POST function to mainly used to create or start operations.

        Parameters
           restApi: The REST API URL.
           data: The data payload for the URL.
           headers: The special header to use for the URL.
           silentMode: True or False.  To display URL, data and header info.
           noDataJsonDumps: True or False. If True, use json dumps. Else, accept the data as-is.
           ignoreError: True or False.  If False, the response will be returned. No exception will be raised.
        """

        if headers != None:
            originalJsonHeader = self.jsonHeader
            self.jsonHeader = headers

        if noDataJsonDumps == True:
            data = data
        else:
            data = json.dumps(data)

        if silentMode == False or self.generateRestLogFile is True:
            self.logInfo('\nPOST: %s' % restApi)
            self.logInfo('DATA: %s' % data)
            self.logInfo('HEADERS: %s' % self.jsonHeader)

        try:
            response = requests.post(restApi, data=data, headers=self.jsonHeader, verify=self.verifySslCert)
            # 200 or 201
            if silentMode == False:
                self.logInfo('STATUS CODE: %s' % response.status_code)
            if not re.match('2[0-9][0-9]', str(response.status_code)):
                if ignoreError == False:
                    if 'message' in response.json() and response.json()['messsage'] != None:
                        self.logWarning('\n%s' % response.json()['message'])
                    self.showErrorMessage()
                    raise IxNetRestApiException('POST error: {0}\n'.format(response.text))

            # Change it back to the original json header
            if headers != None:
                self.jsonHeader = originalJsonHeader
            return response
        except requests.exceptions.RequestException as errMsg:
            raise IxNetRestApiException('POST error: {0}\n'.format(errMsg))

    def patch(self, restApi, data={}, silentMode=False):
        """
        Description
           A HTTP PATCH function to modify configurations.

        Parameters
           restApi: The REST API URL.
           data: The data payload for the URL.
           silentMode: True or False.  To display URL, data and header info.
        """

        if silentMode == False:
            self.logInfo('\nPATCH: %s' % restApi)
            self.logInfo('DATA: %s' % data)
            self.logInfo('HEADERS: %s' % self.jsonHeader)

        try:
            response = requests.patch(restApi, data=json.dumps(data), headers=self.jsonHeader, verify=self.verifySslCert)
            if silentMode == False:
                print('STATUS CODE:', response.status_code)
            if not re.match('2[0-9][0-9]', str(response.status_code)):
                if 'message' in response.json() and response.json()['messsage'] != None:
                    self.logWarning('\n%s' % response.json()['message'])
                self.showErrorMessage()
                raise IxNetRestApiException('PATCH error: {0}\n'.format(response.text))
            return response
        except requests.exceptions.RequestException as errMsg:
            raise IxNetRestApiException('PATCH error: {0}\n'.format(errMsg))

    def delete(self, restApi, data={}, headers=None):
        """
        Description
           A HTTP DELETE function to delete the session.
           For Linux API server only.

        Parameters
           restApi: The REST API URL.
           data: The data payload for the URL.
           headers: The header to use for the URL.
        """

        if headers != None:
            self.jsonHeader = headers

        self.logInfo('\nDELETE: %s' % restApi)
        self.logInfo('DATA: %s' % data)
        self.logInfo('HEADERS: %s' % self.jsonHeader)
        try:
            response = requests.delete(restApi, data=json.dumps(data), headers=self.jsonHeader, verify=self.verifySslCert)
            print('STATUS CODE:', response.status_code)
            if not re.match('2[0-9][0-9]', str(response.status_code)):
                self.showErrorMessage()
                raise IxNetRestApiException('DELETE error: {0}\n'.format(response.text))
            return response
        except requests.exceptions.RequestException as errMsg:
            raise IxNetRestApiException('DELETE error: {0}\n'.format(errMsg))

    def getSessionUrl(self, ixNetRestServerIp, ixNetRestServerPort=11009):
        """
        Description
            Connect to a Windows IxNetwork API Server to create a session URL.
            http://{apiServerIp:port}/api/v1/sessions/1/ixnetwork

         ixNetRestServerIp: The IxNetwork API Server IP address.
         ixNetRestServerPort: Provide a port number to connect to your non Linux API Server.
                              On a Linux API Server, a socket port is not needed. State "None".
        """
        url = 'http://{0}:{1}/api/v1/sessions'.format(ixNetRestServerIp, ixNetRestServerPort)
        serverAndPort = ixNetRestServerIp+':'+str(ixNetRestServerPort)

        if self.apiServerPlatform == 'windowsConnectionMgr':
            # For Connection Manager, requires a POST to automatically get the next session.
            # {'links': [{'href': '/api/v1/sessions/8020', 'method': 'GET', 'rel': 'self'}]}
            self.logInfo('\nPlease wait while IxNetwork starts up...')
            response = self.post(url)
            # Just get the session ID number
            sessionId = response.json()['links'][0]['href'].split('/')[-1]

        if self.apiServerPlatform == 'windows':
            response = self.get(url)
            sessionId = response.json()[0]['id']

        self.sessionUrl = 'http://{apiServer}:{port}/api/v1/sessions/{id}/ixnetwork'.format(apiServer=ixNetRestServerIp,
                                                                                            port=ixNetRestServerPort,
                                                                                            id=sessionId)
        # http://192.168.70.127:11009
        self.httpHeader = self.sessionUrl.split('/api')[0]
        # http://192.168.70.127:11009/api/v1/sessions/1
        self.sessionId = self.sessionUrl.split('/ixnetwork')[0]
        return self.sessionUrl

    def deleteSession(self):
        # Mainly for Windows Connection Manager
        if self.deleteSessionAfterTest:
            self.delete(self.sessionId)

    def logInfo(self, msg, end='\n'):
        print('{0}'.format(msg), end=end)
        if self.generateRestLogFile:
            with open(self.restLogFile, 'a') as restLogFile:
                restLogFile.write(msg+end)

    def logWarning(self, msg, end='\n'):
        print('Warning: {0}'.format(msg), end=end)

    def logError(self, msg, end='\n'):
        print('\nERROR: {0}'.format(msg), end=end)

    def getIxNetworkVersion(self):
        response = self.get(self.sessionUrl+'/globals', silentMode=True)
        return response.json()['buildNumber']

    def showErrorMessage(self, silentMode=False):
        """
        Description
            Show all the error messages from IxNetwork.

        Syntax
            GET: http://{apiServerIp:port}/api/v1/sessions/{id}/globals/appErrors/error
        """

        errorList = []
        response = self.get(self.sessionUrl+'/globals/appErrors/error', silentMode=silentMode)
        print()
        for errorId in response.json():
            if errorId['errorLevel'] == 'kError':
                print('CurrentErrorMessage: {0}'.format(errorId['name']))
                print('\tDescription: {0}'.format(errorId['lastModified']))
                errorList.append(errorId['name'])
        print()
        return errorList

    def waitForComplete(self, response='', url='', silentMode=True, timeout=90):
        """
        Description
            Wait for an operation progress to complete.

        Parameters
            response: The POST action response.  Generally, after an /operations action.
                      Such as /operations/startallprotocols, /operations/assignports
            silentMode: True or False. If True, display info messages.
            timeout: The time allowed to wait for success completion in seconds.
        """
        if silentMode == False:
            self.logInfo('\nwaitForComplete...')
        if response.json() == []:
            raise IxNetRestApiException('waitForComplete: response is empty.')
        if 'errors' in response.json():
            self.logInfo(response.json()["errors"][0])
            return 1
        if silentMode == False:
            self.logInfo("\tState: %s " %response.json()["state"])
        if response.json()['state'] == "SUCCESS":
            if silentMode == False:
                self.logInfo('\n')
            return 0
        if response.json()['state'] == "ERROR":
            self.showErrorMessage()
            return 1
        if response.json()['state'] == "EXCEPTION":
            self.logInfo('waitForComplete: %s' % response.text)
            return 1

        while True:
            response = self.get(url, silentMode=silentMode)
            state = response.json()["state"]
            if silentMode == False:
                self.logInfo("\tState: {0}".format(state))
            if response.json()["state"] == "IN_PROGRESS" or response.json()["state"] == "down":
                if timeout == 0:
                    return 1
                time.sleep(1)
                continue
            if timeout > 0 and state == 'SUCCESS':
                break
            elif timeout > 0 and state == 'ERROR':
                self.showErrorMessage()
                return 1
            elif timeout > 0 and state == 'EXCEPTION':
                print('\n', response.text)
                return 1
            elif timeout == 0 and state != 'SUCCESS':
                return 1
            else:
                if silentMode == False:
                    self.logInfo("\tState: {0} {1} seconds remaining".format(state, timeout))
                timeout = timeout-1
                continue
        if silentMode == False:
            self.logInfo('\n')

    def connectIxChassis(self, chassisIp):
        """
        Description
           Connect to an Ixia chassis.
           This needs to be done prior to assigning ports for testing.

        Syntax
           /api/v1/sessions/1/ixnetwork/availableHardware/chassis

        Parameter
           chassisIp: The chassis IP address.
        """
        url = self.sessionUrl+'/availableHardware/chassis'
        data = {'hostname': chassisIp}
        response = self.post(url, data=data)
        chassisIdObj = response.json()['links'][0]['href']
        # Chassis states: down, polling, ready
        for timer in range(1,61):
            response = self.get(self.httpHeader + chassisIdObj, silentMode=True)
            currentStatus = response.json()['state']
            self.logInfo('connectIxChassis {0}: Status: {1}'.format(chassisIp, currentStatus))
            if currentStatus != 'ready' and timer < 60:
                time.sleep(1)
            if currentStatus != 'ready' and timer == 60:
                raise IxNetRestApiException('connectIxChassis: Connecting to chassis {0} failed'.format(chassisIp))
            if currentStatus == 'ready' and timer < 60:
                break

        # http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/availableHardware/chassis/1
        return self.httpHeader + chassisIdObj

    def disconnectIxChassis(self, chassisIp):
        """
        Description
            Disconnect the chassis (both hardware or virtualChassis).

        Syntax
            http://{apiServerIp:11009}/api/v1/sessions/1/ixnetwork/availableHardware/chassis/<id>

        Parameter
            chassisIp: The chassis IP address.
        """
        url = self.sessionUrl+'/availableHardware/chassis'
        response = self.get(url)
        for eachChassisId in response.json():
            if eachChassisId['hostname'] == chassisIp:
                chassisIdUrl = eachChassisId['links'][0]['href']
                self.logInfo('\ndisconnectIxChassis: %s' % chassisIdUrl)
                response = self.delete(self.httpHeader+chassisIdUrl)

    def connectToLinuxApiServer(self, linuxServerIp, username='admin', password='admin', verifySslCert=False):
        """
        Description
            Connect to a secured access Linux API server.

        Parameters
            linuxServerIp: The Linux API server IP address.
            username: Login username. Default = admin.
            password: Login password. Default = admin.
            verifySslCert: The SSL Certificate to secure access verification.

        Syntax
            POST: 'https://{linuxApiServerIp}/api/v1/auth/session'
        """
        self.verifySslCert = verifySslCert

        if self.apiKey is None:
            # 1: Connect to the Linux API server
            url = 'https://{0}/api/v1/auth/session'.format(linuxServerIp)
            self.logInfo('\nconnectToLinuxApiServer: %s' % url)
            response = self.post(url, data={'username': username, 'password': password}, ignoreError=True)
            print('\n---- connecctToLinuxApiServer status 1:', response.status_code)
            print('\n---- connectToLinuxApiServer response 1:', response.json())
            if not str(response.status_code).startswith('2'):
            #if not re.match('2[0-9][0-9]', str(response.status_code)):
                raise IxNetRestApiException('\nLogin username/password failed\n')
            self.apiKey = response.json()['apiKey']

            # 2: Create new session
            if self.apiServerPort != None:
                linuxServerIp = linuxServerIp + ':' + self.apiServerPort

            url = 'https://{0}/api/v1/sessions'.format(linuxServerIp)
            data = {'applicationType': 'ixnrest'}
            self.jsonHeader = {'content-type': 'application/json', 'x-api-key': self.apiKey}
            self.logInfo('\nlinuxServerCreateSession')
            response = self.post(url, data=data, headers=self.jsonHeader)
            print('\n---- connecctToLinuxApiServer status 2:', response.status_code)
            print('\n---- connectToLinuxApiServer response 2:', response.json())


            sessionId = response.json()['id']
            self.sessionId = 'https://{0}/api/v1/sessions/{1}'.format(linuxServerIp, sessionId)
            self.sessionUrl = 'https://{0}/api/v1/sessions/{1}/ixnetwork'.format(linuxServerIp, sessionId)
            self.httpHeader = self.sessionUrl.split('/api')[0]

            # 3: Start the new session
            self.logInfo('\nlinuxServerStartSession: %s' % self.sessionId)
            response = self.post(self.sessionId+'/operations/start')
            print('\n---- connecctToLinuxApiServer status 3:', response.status_code)
            print('\n---- connectToLinuxApiServer response 3:', response.json())

            if self.linuxServerWaitForSuccess(response.json()['url'], timeout=60) == 1:
                raise IxNetRestApiException

        # If an API-Key is provided, then verify the session ID connection.
        if self.apiKey:
            self.get(self.sessionId)

        self.logInfo('sessionId: %s' % self.sessionId)
        self.logInfo('\nsessionUrl: %s' % self.sessionUrl)
        self.logInfo('apiKey: %s' % self.apiKey)

    def linuxServerConfigGlobalLicenseServer(self, linuxServerIp, licenseServerIp, licenseMode, licenseTier):
        """
        Description
           On a new Linux API Linux installation, you need to set the global license server once.
           When a new session is created, it will check the global license settings and config the
           license settings on the new session.

        Parameters
            linuxServerIp: IP address of the Linux API server.
            licenseServerIp: Type = list. [IP address of the license server]
            licenseMode: subscription, perpetual or mixed
            licenseier: tier1, tier2, tier3

        Syntax
           PATCH: https://<apiServerIp>/api/v1/sessions/9999/ixnetworkglobals/license
           DATA:  {'servers': list(licenseServerIp),
                   'mode': str(licenseMode),
                   'tier': str(licenseTier)
                  }
        """

        staticUrl = 'https://{linuxServerIp}/api/v1/sessions/9999/ixnetworkglobals/license'.format(linuxServerIp=linuxServerIp)
        self.logInfo('\nlinuxServerConfigGlobalLicenseServer:\n\t{0}\n\t{1}\n\t{2}\n'. format(licenseServerIp,
                                                                                       licenseMode,
                                                                                       licenseTier))
        response = self.patch(staticUrl, data={'servers': [licenseServerIp], 'mode': licenseMode, 'tier': licenseTier})
        response = self.get(staticUrl)
        licenseServerIp = response.json()['servers'][0]
        licenseServerMode = response.json()['mode']
        licenseServerTier = response.json()['tier']
        self.logInfo('\nLinuxApiServer static license server:')
        self.logInfo('\t', licenseServerIp)
        self.logInfo('\t', licenseServerMode)
        self.logInfo('\t', licenseServerTier)

    def linuxServerGetGlobalLicense(self, linuxServerIp):
        """
        Description
            Get the global license server details from the Linux API server.

        Parameter
            linuxServerIp: The IP address of the Linux API server.

        Syntax
            GET: 'https://{linuxServerIp}/api/v1/sessions/9999/ixnetworkglobals/license'
        """
        staticUrl = 'https://{linuxServerIp}/api/v1/sessions/9999/ixnetworkglobals/license'.format(linuxServerIp=linuxServerIp)
        self.logInfo('\nlinuxServerGetGlobalLicense: %s ' % linuxServerIp)
        response = self.get(staticUrl, silentMode=False)
        licenseServerIp = response.json()['servers'][0]
        licenseServerMode = response.json()['mode']
        licenseServerTier = response.json()['tier']
        self.logInfo('\nlinuxServerGetGlobalLicenses:')
        self.logInfo('\t%s' % licenseServerIp)
        self.logInfo('\t%s' % licenseServerMode)
        self.logInfo('\t%s' % licenseServerTier)
        return licenseServerIp,licenseServerMode,licenseServerTier

    def configLicenseServerDetails(self, licenseServer=None, licenseMode=None, licenseTier=None):
        """
        Description
           Configure license server details: license server IP, license mode and license tier.

        Parameter
            licenseServer: License server IP address(s) in a list.
            licenseMode: subscription|perpetual}mixed
            licenseTier: tier1, tier2, tier3 ...

        Syntax
           PATCH: https://{apiServerIp}/api/v1/sessions/{id}/ixnetwork/globals/licensing
        """
        # Each new session requires configuring the new session's license details.
        data = {}
        if licenseServer:
            data.update({'licensingServers': licenseServer})
        if licenseMode:
            data.update({'mode': licenseMode})
        if licenseTier:
            data.update({'tier': licenseTier})

        response = self.patch(self.sessionUrl+'/globals/licensing', data=data)
        self.showLicenseDetails()

    def showLicenseDetails(self):
        """
        Description
            Verify the new session's license details.
        """

        response = self.get(self.sessionUrl+'/globals/licensing')
        self.logInfo('\nVerifying sessionId license server: %s' % self.sessionUrl)
        self.logInfo('\t%s' % response.json()['licensingServers'])
        self.logInfo('\t%s'%  response.json()['mode'])
        self.logInfo('\t%s' % response.json()['tier'])

    def linuxServerStopAndDeleteSession(self):
        """
        Description
           Wrapper to stop and delete the session ID on the Linux API server.

        Requirements
           * linuxServerStopOperations()
           * linuxServerDeleteSession()

        Syntax
           GET = https://{apiServerIp}/api/v1/sessions/{id}
        """
        if self.apiServerPlatform == 'linux' and self.deleteSessionAfterTest==True:
            self.linuxServerStopOperations()
            self.linuxServerDeleteSession()

    def linuxServerStopOperations(self, sessionId=None):
        """
        Description
            Stop the session ID on the Linux API server
        """
        if sessionId != None:
            sessionId = sessionId
        else:
            sessionId = self.sessionId

        self.logInfo('\nlinuxServerStopOperations: %s' % sessionId)
        response = self.post(sessionId+'/operations/stop')
        if self.linuxServerWaitForSuccess(response.json()['url'], timeout=30) == 1:
            raise IxNetRestApiException

    def linuxServerDeleteSession(self, sessionId=None):
        """
        Description
            Delete the session ID on the Linux API server.

        Syntax
            DELETE: https://{linuxApiServerIp}/api/v1/sessions/{id}/operations/stop
        """
        if sessionId != None:
            sessionId = sessionId
        else:
            sessionId = self.sessionId

        self.logInfo('\nlinuxServerDeleteSession: Deleting...%s' % sessionId)
        response = self.delete(sessionId)

    def linuxServerWaitForSuccess(self, url, timeout=120):
        """
        Description
            Wait for success completion on the Linux API server.

        Parameter
            url: The URL's ID of the operation to verify
        """
        data = {'applicationType': 'ixnrest'}
        jsonHeader = {'content-type': 'application/json', 'x-api-key': self.apiKey}
        for counter in range(1,timeout+1):
            response = self.get(url, data=data, silentMode=True)
            currentStatus = response.json()['message']
            self.logInfo('CurrentStatus: {0}  {1}/{2} seconds'.format(currentStatus, counter, timeout))
            if counter < timeout+1 and currentStatus != 'Operation successfully completed':
                time.sleep(1)
            if counter == timeout+1 and currentStatus != 'Operation successfully completed':
                return 1
            if counter < timeout+1 and currentStatus == 'Operation successfully completed':
                return 0

    def newBlankConfig(self):
        """
        Description
            Start a new blank configuration.

        Note
            Requires waitForComplete API also.

        Syntax: http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/operations/newconfig
        """
        url = self.sessionUrl+'/operations/newconfig'
        self.logInfo('\nnewBlankConfig:', url)
        response = self.post(url)
        if response == 1: return 1
        url = self.sessionUrl+'/operations/newconfig/'+response.json()['id']
        if self.waitForComplete(response, url) == 1:
            raise IxNetRestApiException()

    def refreshHardware(self, chassisObj):
        """
        Description
            Refresh the chassis

        Syntax
            http://{apiServerIp:11009}/availableHardware/chassis/operations/refreshinfo

        Parameter
            chassisObj:  The chassis object
                         Ex: '/api/v1/sessions/1/ixnetwork/availableHardware/chassis/1'
        """
        response = self.post(self.sessionUrl+'/availableHardware/chassis/operations/refreshinfo', data={'arg1': [chassisObj]})
        if self.waitForComplete(response, self.sessionUrl+'/availableHardware/chassis/operations/refreshinfo') == 1:
            raise IxNetRestApiException

    def query(self, data, silentMode=True):
        """
        Description
           To query for the object in order to modify the configuration.

        Parameter
            # Assuming this is a BGP configuration, which has two Topologies. Below demonstrates how to query the BGP host object by
            # drilling down the Topology by its name and the specific the BGP attributes to modify at the
            # BGPIpv4Peer node: flap, downtimeInSec, uptimeInSec.
            # The from '/' is the entry point to the API tree.
            # Notice all the node. This represents the API tree from the / entry point and starting at Topology level to the BGP
            # host level.
            # NOTE: Use the API Browser tool on the IxNetwork GUI to view the API tree.
            data: {'from': '/',
                    'nodes': [{'node': 'topology',    'properties': ['name'], 'where': [{'property': 'name', 'regex': 'Topo1'}]},
                              {'node': 'deviceGroup', 'properties': [], 'where': []},
                              {'node': 'ethernet',    'properties': [], 'where': []},
                              {'node': 'ipv4',        'properties': [], 'where': []},
                              {'node': 'bgpIpv4Peer', 'properties': ['flap', 'downtimeInSec', 'uptimeInSec'], 'where': []}]
                }

        Example:
            response = restObj.query(data=queryData)
            bgpHostAttributes = response.json()['result'][0]['topology'][0]['deviceGroup'][0]['ethernet'][0]['ipv4'][0]['bgpIpv4Peer'][0]

            # GET THE BGP ATTRIBUTES TO MODIFY
            bgpHostFlapMultivalue = bgpHostAttributes['flap']
            bgpHostFlapUpTimeMultivalue = bgpHostAttributes['uptimeInSec']
            bgpHostFlapDownTimeMultivalue = bgpHostAttributes['downtimeInSec']

            restObj.configMultivalue(bgpHostFlapMultivalue, multivalueType='valueList', data={'values': ['true', 'true']})
            restObj.configMultivalue(bgpHostFlapUpTimeMultivalue, multivalueType='singleValue', data={'value': '60'})
            restObj.configMultivalue(bgpHostFlapDownTimeMultivalue, multivalueType='singleValue', data={'value': '30'})
        """

        url = self.sessionUrl+'/operations/query'
        reformattedData = {'selects': [data]}
        response = self.post(url, data=reformattedData, silentMode=silentMode)
        if self.waitForComplete(response, url+'/'+response.json()['id']) == 1:
            raise IxNetRestApiException
        return response

    def configMultivalue(self, multivalueUrl, multivalueType, data):
        """
        Description
            Configure multivalues.

        Parameters
            multivalueUrl: The multivalue href. Ex: /api/v1/sessions/1/ixnetwork/multivalue/1
            multivalueType: counter|singleValue|valueList
            data = In Python Dict format. Ex:
                   If singleValue, data={'value': '1.1.1.1'})
                   If valueList,   data needs to be in a [list]:  data={'values': [list]}
                   If counter,     data={'start': value, 'direction': increment|decrement, 'step': value}
        """
        if multivalueType == 'counter':
            # Example: macAddress = {'start': '00:01:01:00:00:01', 'direction': 'increment', 'step': '00:00:00:00:00:01'}
            #          data=macAddress)
            self.patch(self.httpHeader+multivalueUrl+'/counter', data=data)

        if multivalueType == 'singleValue':
            # data={'value': value}
            self.patch(self.httpHeader+multivalueUrl+'/singleValue', data=data)

        if multivalueType == 'valueList':
            # data={'values': ['item1', 'item2']}
            self.patch(self.httpHeader+multivalueUrl+'/valueList', data=data)

    def getMultivalueValues(self, multivalueObj, silentMode=False):
        """
        Description
            A more efficient method to get the multivalue values.

        Parameters
            multivalueObj: The multivalue object: /api/v1/sessions/1/ixnetwork/multivalue/208
            silentMode: True|False: True=Display the GET and status code. False=Don't display.
        """
        response = self.get(self.httpHeader+multivalueObj+'?includes=count', silentMode=silentMode)
        count = response.json()['count']
        if silentMode == False:
            self.logInfo('\ngetMultivalueValues: {0} Count={1}'.format(multivalueObj, count))
        data = {'arg1': multivalueObj,
                'arg2': 0,
                'arg3': count
                }
        response = self.post(self.sessionUrl+'/multivalue/operations/getValues', data=data, silentMode=silentMode)
        if self.waitForComplete(response, self.sessionUrl+'/operations/multivalue/getValues'+response.json()['id']) == 1:
            raise IxNetRestApiException
        return response.json()['result']

    @staticmethod
    def prettyprintAllOperations(sessionUrl):
        # Dispaly all the operation commands and its description:
        #    http://192.168.70.127:11009/api/v1/sessions/1/ixnetwork/operations

        response = requests.get(sessionUrl+'/operations')
        for item in response.json():
            if 'operation' in item.keys():
                print('\n', item['operation'])
                print('\t%s' % item['description'])
                if 'args' in item.keys():
                    for nestedKey,nestedValue in item['args'][0].items():
                        print('\t\t%s: %s' % (nestedKey, nestedValue))

    @staticmethod
    def printDict(obj, nested_level=0, output=sys.stdout):
        """
        Self.LogInfo each dict key with indentions for readability.
        """
        spacing = '   '
        spacing2 = ' '
        if type(obj) == dict:
            print( '%s' % ((nested_level) * spacing), file=output)
            for k, v in obj.items():
                if hasattr(v, '__iter__'):
                    print('%s%s:' % ( (nested_level+1) * spacing, k), file=output, end='')
                    IxNetRestMain.printDict(v, nested_level+1, output)
                else:
                    print('%s%s: %s' % ( (nested_level + 1) * spacing, k, v), file=output)

            print('%s' % (nested_level * spacing), file=output)
        elif type(obj) == list:
            print('%s[' % ((nested_level) * spacing), file=output)
            for v in obj:
                if hasattr(v, '__iter__'):
                    IxNetRestMain.printDict(v, nested_level + 1, file=output)
                else:
                    print('%s%s' % ((nested_level + 1) * spacing, v), file=output)
            print('%s]' % ((nested_level) * spacing), output)
        else:
            print('%s%s' % ((nested_level * spacing2), obj), file=output)

    def placeholder():
        pass



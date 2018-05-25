
# PLEASE READ DISCLAIMER
#
#    This class demonstrates sample IxNetwork REST API usage for
#    demo and reference purpose only.
#    It is subject to change for updates without warning.
#
# REQUIREMENTS
#    - Python 2.7 (Supports Python 2 and 3)
#    - Python modules: requests
#

from __future__ import absolute_import, print_function, division
import os, re, sys, requests, json, time, subprocess, traceback, time

class IxNetRestApiException(Exception): pass

class Connect:
    def __init__(self, apiServerIp=None, serverIpPort=None, serverOs='windows', connectToLinuxChassisIp=None,
                 webQuickTest=False, username=None, password='admin', licenseServerIp=None, licenseMode=None, licenseTier=None,
                 deleteSessionAfterTest=True, verifySslCert=False, includeDebugTraceback=True, sessionId=None,
                 apiKey=None, generateRestLogFile=True, robotFrameworkStdout=False, httpInsecure=True):
        """
        Description
           Initializing default parameters and making a connection to the API server

        Notes
            Starting IxNetwork 8.50, https will be enforced even for Windows connection.
            If you still want to use http, you need to add -restInsecure to the IxNetwork.exe appliaction under "target".

        Examples  
            Right click on "IxNetwork API server", select properties and under target 
            ixnetwork.exe -restInsecure -restPort 11009 -restOnAllInterfaces -tclPort 8009

        Parameters
           apiServerIp: (str): The API server IP address.
           serverIpPort: (str): The API server IP address socket port.
           serverOs: (str): windows|windowsConnectionMgr|linux
           connectToLinuxChassis: (str): Connect to a Linux OS chassis IP address.
           webQuickTest: (bool): True: Using IxNetwork Web Quick Test. Otherwise, using IxNetwork.
           includeDebugTraceback: (bool):
                                   True: Traceback messsages are included in raised exceptions.
                                   False: No traceback.  Less verbose for debugging.
           username: (str): The login username. For Linux API server only.
           password: (str): The login password. For Linux API server only.
           licenseServerIp: (str): The license server IP address.
           licenseMode: (str): subscription | perpetual | mixed
           licenseTier: (str): tier1 | tier2 | tier3
           deleteSessionAfterTest: (bool): True: Delete the session.
                                           False: Don't delete the session.
           verifySslCert: (str): Optional: Include your SSL certificate for added security.
           serverOs: (str): Defaults to windows. windows|windowsConnectionMgr|linux.
           includeDebugTraceback: (bool): True: Include tracebacks in raised exceptions.
           sessionId: (str): The session ID on the Linux API server or Windows Connection Mgr to connect to.
           apiKey: (str): The Linux API server user account API-Key to use for the sessionId connection.
           generateRestLogFile: True|False|<log file name>.  If you want to generate a log file, provide 
                                the log file name.
                                True = Then the log file default name is ixNetRestApi_debugLog.txt
                                False = Disable generating a log file.
                                <log file name> = The full path + file name of the log file to create.
           robotFrameworkStdout: (bool):  True = Print to stdout.
           httpInsecure: (bool): This parameter is only for Windows connections.
                                     True: Using http.  False: Using https.
                                     Starting 8.50: IxNetwork defaults to use https.
                                     If you are using versions prior to 8.50, it needs to be a http connection.
                                     In this case, set httpInsecure=True.

        Notes
            Class attributes
               self.serverOs: windows|windowsConnectionMgr|linux
               self.httpHeader: http://{apiServerIp}:{port}
               self.sessionId : http://{apiServerIp}:{port}/api/v1/sessions/{id}
               self.sessionUrl: http://{apiServerIp}:{port}/api/v1/sessions/{id}/ixnetwork
               self.apiSessionId: /api/v1/sessions/{id}/ixnetwork
               self.jsonHeader: The default header: {"content-type": "application/json"}
               self.apiKey: For Linux API server only. Automatically provided by the server when login 
                            successfully authenticated.
                            You could also provide an API-Key to connect to an existing session.
                            Get the API-Key from the Linux API server user account.

        Examples:
           Steps to connect to Linux API server steps:
               1> POST: https://{apiServerIp}/api/v1/auth/session
                  DATA: {"username": "admin", "password": "admin"}
                  HEADERS: {'content-type': 'application/json'}
        
               2> POST: https://{apiServerIp:{port}/api/v1/sessions
                  DATA: {"applicationType": "ixnrest"}
                  HEADERS: {'content-type': 'application/json', 'x-api-key': 'd9f4da46f3c142f48dddfa464788hgee'}

               3> POST: https://{apiServerIp}:443/api/v1/sessions/4/operations/start
                  DATA: {}
                  HEADERS: {'content-type': 'application/json', 'x-api-key': 'd9f4da46f3c142f48dddfa464788hgee'}

               sessionId = https://{apiServerIp}:443/api/v1/sessions/{id}

           Steps to connect to Linux Web Quick Test:
               1> POST: https://{apiServerIp}:443/api/v1/auth/session
                  DATA: {"username": "admin", "password": "admin"}
                  HEADERS: {'content-type': 'application/json'}

               2> POST: https://{apiServeIp}:443/api/v1/sessions
                  DATA: {'applicationType': 'ixnetwork'}

               3> POST: https://{apiServerIp}:443/api/v1/sessions/2/operations/start
                  DATA: {'applicationType': 'ixnetwork'}

            sessionId = https://{apiServerIp}/ixnetworkweb/api/v1/sessions/{id}

           Notes
              To connect to an existing configuration.
                 Windows: Nothing special to include. The session ID is always "1".
                 Linux API server: Include the api-key and sessionId that you want to connect to.
                 Windows Connection Manager: Include just the sessionId: For example: 8021.
        """
        from requests.exceptions import ConnectionError
        from requests.packages.urllib3.connection import HTTPConnection

        # Disable SSL warnings
        requests.packages.urllib3.disable_warnings()

        # Disable non http connections.
        from requests.packages.urllib3.exceptions import InsecureRequestWarning
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        self.serverOs = serverOs ;# windows|windowsConnectionMgr|linux
        self.jsonHeader = {"content-type": "application/json"}
        self.httpInsecure = httpInsecure
        self.username = username
        self.password = password
        self.apiKey = apiKey
        self.verifySslCert = verifySslCert
        self.linuxApiServerIp = apiServerIp
        self.apiServerPort = serverIpPort
        self.webQuickTest = webQuickTest
        self.generateRestLogFile = generateRestLogFile
        self.robotFrameworkStdout = robotFrameworkStdout
        self.connectToLinuxChassisIp = connectToLinuxChassisIp

        if generateRestLogFile:
            if generateRestLogFile == True:
                # Default the log file name
                self.restLogFile = 'ixNetRestApi_debugLog.txt'

            if type(generateRestLogFile) != bool:
                self.restLogFile = generateRestLogFile

            # Instantiate a new log file here.
            with open(self.restLogFile, 'w') as restLogFile:
                restLogFile.write('')

        # Make Robot print to stdout
        if self.robotFrameworkStdout:
            from robot.libraries.BuiltIn import _Misc
            self.robotStdout = _Misc()

        if connectToLinuxChassisIp:
            self.connectToLinuxIxosChassis(self.connectToLinuxChassisIp, self.username, self.password)
            return

        if serverOs == 'windows':
            self.createWindowsSession(apiServerIp, serverIpPort)

        if serverOs == 'windowsConnectionMgr':
            # User connecting to existing sessionId
            if sessionId:
                self.sessionId = 'http://{0}:{1}/api/v1/sessions/{2}'.format(apiServerIp, serverIpPort, str(sessionId))
                self.sessionUrl = 'http://{0}:{1}/api/v1/sessions/{2}/ixnetwork'.format(apiServerIp, serverIpPort, str(sessionId))
                self.apiSessionId = '/api/v1/sessions/{0}/ixnetwork'.format(str(sessionId))
                self.httpHeader = self.sessionUrl.split('/api')[0]
            else:
                # Create a new session
                self.createWindowsSession(apiServerIp, serverIpPort)

        if serverOs == 'linux':
            if self.apiServerPort == None:
                self.apiServerPort == 443

            if apiKey != None and sessionId == None:
                raise IxNetRestApiException('Providing an apiKey must also provide a sessionId.')

            # Connect to an existing session on the Linux API server
            if apiKey and sessionId:
                self.jsonHeader = {'content-type': 'application/json', 'x-api-key': self.apiKey}

                response = self.get('https://{0}:{1}/api/v1/sessions/{2}'.format(self.linuxApiServerIp, self.apiServerPort, str(sessionId)))

                if self.webQuickTest == False:
                    # https://192.168.70.108/ixnetworkweb/api/v1/sessions/4
                    self.sessionId = response.json()['links'][0]['href']
                    # Remove the redirect /ixnetworkweb from the URL. IxNetwork 8.50 will resolve this.
                    self.sessionId = self.sessionId.replace('ixnetworkweb/', '')

                    # https://192.168.70.108/ixnetworkweb/api/v1/sessions/4/ixnetork
                    self.sessionUrl = self.sessionId + '/ixnetwork'

                    # /api/v1/sessions/4/ixnetwork
                    match = re.match('.*(/api.*)', self.sessionId)
                    self.apiSessionId = match.group(1) + '/ixnetwork'

                    # https://10.10.10.1:443
                    matchHeader = re.match('(https://[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+(:[0-9]+)?)', self.sessionId)
                    self.httpHeader = matchHeader.group(1)

                if self.webQuickTest:
                    self.sessionId = 'https://{0}:{1}/ixnetworkweb/api/v1/sessions/{2}'.format(self.linuxApiServerIp,
                                                                                               self.apiServerPort, str(sessionId))
                    self.sessionUrl = self.sessionId
                    self.httpHeader = self.sessionUrl.split('/ixnetworkweb')[0]

            # Create new session: connectToLinuxApiServer API knows whether to create a new session or connect to an existing
            #                     session by looking at the self.apiKey.
            if apiKey == None and sessionId == None:
                self.connectToLinuxApiServer(self.linuxApiServerIp, self.apiServerPort, username=username, password=password, verifySslCert=verifySslCert)

            if licenseServerIp or licenseMode or licenseTier:
                self.configLicenseServerDetails(licenseServerIp, licenseMode, licenseTier)

        # For Linux API Server and Windoww Connection Mgr only: Delete the session when script is done if deleteSessionAfterTest = True.
        self.deleteSessionAfterTest = deleteSessionAfterTest

        if includeDebugTraceback == False:
            sys.tracebacklimit = 0

    def get(self, restApi, data={}, stream=False, silentMode=False, ignoreError=False):
        """
        Description
            A HTTP GET function to send REST APIs.

        Parameters
           restApi: (str): The REST API URL.
           data: (dict): The data payload for the URL.
           silentMode: (bool):  To display on stdout: URL, data and header info.
           ignoreError: (bool): True: Don't raise an exception.  False: The response will be returned.

        Syntax
            /api/v1/sessions/1/ixnetwork/operations
        """
        if silentMode is False:
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
            if not str(response.status_code).startswith('2'):
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
           A HTTP POST function to create and start operations.

        Parameters   
           restApi: (str): The REST API URL.
           data: (dict): The data payload for the URL.
           headers: (str): The special header to use for the URL.
           silentMode: (bool):  To display on stdout: URL, data and header info.
           noDataJsonDumps: (bool): True: Use json dumps. False: Accept the data as-is.
           ignoreError: (bool): True: Don't raise an exception.  False: The response will be returned.
        """
        if headers != None:
            originalJsonHeader = self.jsonHeader
            self.jsonHeader = headers

        if noDataJsonDumps == True:
            data = data
        else:
            data = json.dumps(data)

        if silentMode == False:
            self.logInfo('\nPOST: %s' % restApi)
            self.logInfo('DATA: %s' % data)
            self.logInfo('HEADERS: %s' % self.jsonHeader)

        try:
            if self.connectToLinuxChassisIp and json.loads(data) == {}:
                # Interacting with LinuxOS chassis doesn't like empty data payload. So excluding it here.
                response = requests.post(restApi, headers=self.jsonHeader, allow_redirects=True, verify=self.verifySslCert)
            else:
                response = requests.post(restApi, data=data, headers=self.jsonHeader, allow_redirects=True, verify=self.verifySslCert)

            # 200 or 201
            if silentMode == False:
                self.logInfo('STATUS CODE: %s' % response.status_code)
            if str(response.status_code).startswith('2') == False:
                if ignoreError == False:
                    if 'errors' in response.json():
                        raise IxNetRestApiException('POST error: {0}\n'.format(response.json()['errors'][0]['detail']))
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
           restApi: (str): The REST API URL.
           data: (dict): The data payload for the URL.
           silentMode: (bool):  To display on stdout: URL, data and header info.
        """
        if silentMode == False:
            self.logInfo('\nPATCH: %s' % restApi)
            self.logInfo('DATA: %s' % data)
            self.logInfo('HEADERS: %s' % self.jsonHeader)

        try:
            response = requests.patch(restApi, data=json.dumps(data), headers=self.jsonHeader, verify=self.verifySslCert)
            if silentMode == False:
                self.logInfo('STATUS CODE: %s' % response.status_code)
            if not str(response.status_code).startswith('2'):
                if 'message' in response.json() and response.json()['messsage'] != None:
                    self.logWarning('\n%s' % response.json()['message'])

                raise IxNetRestApiException('PATCH error: {0}\n'.format(response.text))
            return response
        except requests.exceptions.RequestException as errMsg:
            raise IxNetRestApiException('PATCH error: {0}\n'.format(errMsg))

    def delete(self, restApi, data={}, headers=None):
        """
        Description
           A HTTP DELETE function to delete the session.
           For Linux and Windows Connection Mgr API server only.

        Paramters
           restApi: (str): The REST API URL.
           data: (dict): The data payload for the URL.
           headers: (str): The headers to use for the URL.
        """
        if headers != None:
            self.jsonHeader = headers

        self.logInfo('\nDELETE: %s' % restApi)
        self.logInfo('DATA: %s' % data)
        self.logInfo('HEADERS: %s' % self.jsonHeader)
        try:
            response = requests.delete(restApi, data=json.dumps(data), headers=self.jsonHeader, verify=self.verifySslCert)
            self.logInfo('STATUS CODE: %s' % response.status_code)
            if not str(response.status_code).startswith('2'):
                self.showErrorMessage()
                raise IxNetRestApiException('DELETE error: {0}\n'.format(response.text))
            return response
        except requests.exceptions.RequestException as errMsg:
            raise IxNetRestApiException('DELETE error: {0}\n'.format(errMsg))

    def getSelfObject(self):
        """
        Description
           For Robot Framework support only.
        
        Return
           The instance object.
        """
        return self

    def createWindowsSession(self, ixNetRestServerIp, ixNetRestServerPort='11009'):
        """
        Description
           Connect to a Windows IxNetwork API Server to create a session URL. This is 
           for both Windows and Windows server with IxNetwork Connection Manager.
           This will set up the session URL to use throughout the test.

        Parameter
          ixNetRestServerIp: (str): The Windows IxNetwork API Server IP address.
          ixNetRestServerPort: (str): Default: 11009.  Provide a port number to connect to.
                               On a Linux API Server, a socket port is not needed. State "None".

        """
        if self.httpInsecure:
            httpVerb = 'http'
        else:
            httpVerb = 'https'

        # Handle __import__(IxNetRestApi) to not error out
        if ixNetRestServerIp == None: return

        url = '{0}://{1}:{2}/api/v1/sessions'.format(httpVerb, ixNetRestServerIp, ixNetRestServerPort)
        serverAndPort = '{0}:{1}'.format(ixNetRestServerIp, str(ixNetRestServerPort))

        if self.serverOs == 'windowsConnectionMgr':
            # For Connection Manager, requires a POST to automatically get the next session.
            # {'links': [{'href': '/api/v1/sessions/8020', 'method': 'GET', 'rel': 'self'}]}
            self.logInfo('\nPlease wait while IxNetwork Connection Mgr starts up an IxNetwork session...')
            response = self.post(url)
            # Just get the session ID number
            sessionIdNumber = response.json()['links'][0]['href'].split('/')[-1]
            sessionIdUrl = url+'/'+sessionIdNumber
            response = self.get(url)
            if response.json()[0]['state'] != 'ACTIVE':
                raise IxNetRestApiException('\nError: New Windows session state failed to become ACTVIE state')

            # Windows connection mgr takes additional time after becoming ACTIVE.
            self.logInfo('\tWait for Windows session to become ready')
            time.sleep(20)

        if self.serverOs == 'windows':
            # windows sessionId is always 1 because it only supports one session.
            sessionIdNumber = 1

        self.sessionUrl = '{http}://{apiServer}:{port}/api/v1/sessions/{id}/ixnetwork'.format(http=httpVerb,
                                                                                              apiServer=ixNetRestServerIp,
                                                                                              port=ixNetRestServerPort,
                                                                                              id=sessionIdNumber)

        # http://192.168.70.127:11009
        self.httpHeader = self.sessionUrl.split('/api')[0]

        # http://192.168.70.127:11009/api/v1/sessions/1
        self.sessionId = self.sessionUrl.split('/ixnetwork')[0]
        self.apiSessionId = '/api/v1/sessions/{0}/ixnetwork'.format(sessionIdNumber)

    def deleteSession(self):
        """
        Description
           Delete the instance session ID. For Linux and Windows Connection Manager only.
        """
        if self.deleteSessionAfterTest:
            self.delete(self.sessionId)

    def logInfo(self, msg, end='\n'):
        """
        Description
           An internal function to print info to stdout
        
        Parameters
           msg: (str): The message to print.
        """
        print('{0}'.format(msg), end=end)
        if self.generateRestLogFile:
            with open(self.restLogFile, 'a') as restLogFile:
                restLogFile.write(msg+end)

        if self.robotFrameworkStdout:
            self.robotStdout.log_to_console(msg)

    def logWarning(self, msg, end='\n'):
        """
        Description
           An internal function to print warnings to stdout.
        
        Parameter
           msg: (str): The message to print.
        """
        print('Warning: {0}'.format(msg), end=end)
        if self.generateRestLogFile:
            with open(self.restLogFile, 'a') as restLogFile:
                restLogFile.write('Warning: '+msg+end)

        if self.robotFrameworkStdout:
            self.robotStdout.log_to_console(msg)

    def logError(self, msg, end='\n'):
        """
        Description
           An internal function to print error to stdout.
        
        Parameter
           msg: (str): The message to print.
        """
        print('\nERROR: {0}'.format(msg), end=end)
        if self.generateRestLogFile:
            with open(self.restLogFile, 'a') as restLogFile:
                restLogFile.write('Error: '+msg+end)

        if self.robotFrameworkStdout:
            self.robotStdout.log_to_console(msg)

    def getIxNetworkVersion(self):
        """
        Description
           Get the IxNetwork version.

        Syntax
            GET: /api/v1/sessions/{id}/globals
        """
        response = self.get(self.sessionUrl+'/globals', silentMode=True)
        return response.json()['buildNumber']

    def showErrorMessage(self, silentMode=False):
        """
        Description
           Show all the error messages from IxNetwork.

        Parameter
          silentMode: (bool): True: Don't print the REST API on stdout.

        Syntax
            GET: /api/v1/sessions/{id}/globals/appErrors/error
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

    def waitForComplete(self, response='', url='', silentMode=False, timeout=90):
        """
        Description
           Wait for an operation progress to complete.

        Parameters
           response: (json response/dict): The POST action response.  Generally, after an /operations action.
                         Such as /operations/startallprotocols, /operations/assignports.
           silentMode: (bool):  If True, display info messages on stdout.
           timeout: (int): The time allowed to wait for success completion in seconds.
        """
        if silentMode == False:
            self.logInfo('\nwaitForComplete:')
            self.logInfo("\tState: %s " %response.json()["state"])

        if response.json() == []:
            raise IxNetRestApiException('waitForComplete: response is empty.')

        if response.json() == '' and response.json()['state'] == 'SUCCESS':
            return 

        if 'errors' in response.json():
            raise IxNetRestApiException(response.json()["errors"][0])

        if response.json()['state'] == "SUCCESS":
            return 0

        if response.json()['state'] in ["ERROR", "EXCEPTION"]:
            raise IxNetRestApiException('\nWaitForComplete: STATE=%s: %s' % (response.json()['state'], response.text))

        for counter in range(1,timeout+1):
            response = self.get(url, silentMode=True)
            state = response.json()["state"]
            if state != 'SUCCESS':
                self.logInfo("\tState: {0}: Wait {1}/{2} seconds".format(state, counter, timeout))
            if state == 'SUCCESS':
                self.logInfo("\tState: {0}".format(state))

            if counter < timeout and state in ["IN_PROGRESS", "down"]:
                time.sleep(1)
                continue

            if counter < timeout and state in ["ERROR"]:
                raise IxNetRestApiException('\n%s' % response.text)

            if counter < timeout and state == 'SUCCESS':
                return response

            if counter == timeout and state != 'SUCCESS':
                raise IxNetRestApiException('\n%s' % response.text)

    def connectIxChassis(self, chassisIp):
        """
        Description
           Connect to an Ixia chassis.

        Paramter
           chassisIp: (str): The chassis IP address.  This could be hardware and virtual chassis.

        Syntax
           /api/v1/sessions/{id}/ixnetwork/availableHardware/chassis
        """
        url = self.sessionUrl+'/availableHardware/chassis'
        data = {'hostname': chassisIp}
        self.logInfo('\nConnect to Ixia chassis')
        response = self.post(url, data=data)
        chassisIdObj = response.json()['links'][0]['href']
        # Chassis states: down, polling, ready
        self.logInfo('\nWait for chassis connection to come up\n')
        for timer in range(1,61):
            response = self.get(self.httpHeader + chassisIdObj, silentMode=True)
            currentStatus = response.json()['state']
            self.logInfo('\tconnectIxChassis {0}: Status: {1}'.format(chassisIp, currentStatus))
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
           Disconnect the chassis (For both hardware or virtualChassis).

        Parameter
           chassisIp: (str): The chassis IP address.

        Syntax
            DELETE: /api/v1/sessions/{id}/ixnetwork/availableHardware/chassis/{id}
        """
        url = self.sessionUrl+'/availableHardware/chassis'
        response = self.get(url)
        for eachChassisId in response.json():
            if eachChassisId['hostname'] == chassisIp:
                chassisIdUrl = eachChassisId['links'][0]['href']
                self.logInfo('\ndisconnectIxChassis: %s' % chassisIdUrl)
                response = self.delete(self.httpHeader+chassisIdUrl)

    def connectToLinuxIxosChassis(self, chassisIp, username, password):
        url = 'https://{0}/platform/api/v1/auth/session'.format(chassisIp)
        response = self.post(url, data={'username': username, 'password': password})
        self.apiKey = response.json()['apiKey']
        self.jsonHeader = {'content-type': 'application/json', 'x-api-key': self.apiKey}

        # userAccountUrl: https://{ip}/platform/api/v1/auth/users/{id}
        self.userSessionId = response.json()['userAccountUrl']

        self.ixosHeader = 'https://{0}/chassis/api/v2/ixos'.format(chassisIp)
        self.diagnosticsHeader = 'https://{0}/chassis/api/v1/diagnostics'.format(chassisIp)
        self.authenticationHeader = 'https://{0}/chassis/api/v1/auth'.format(chassisIp)
        self.sessionUrl = self.ixosHeader

    def connectToLinuxApiServer(self, linuxServerIp, linuxServerIpPort, username='admin', password='admin', verifySslCert=False):
        """
        Description
           Connect to a Linux API server.

        Parameters
           linuxServerIp: (str): The Linux API server IP address.
           username: (str): Login username. Default = admin.
           password: (str): Login password. Default = admin.
           verifySslCert: (str): Defalt: None.  The SSL Certificate for secure access verification.
 
       Syntax
            POST: /api/v1/auth/session
        """
        self.verifySslCert = verifySslCert

        if self.apiKey is None:
            # 1: Connect to the Linux API server
            url = 'https://{0}:{1}/api/v1/auth/session'.format(linuxServerIp, linuxServerIpPort)
            self.logInfo('\nconnectToLinuxApiServer: %s' % url)
            response = self.post(url, data={'username': username, 'password': password}, ignoreError=True)
            if not str(response.status_code).startswith('2'):
                raise IxNetRestApiException('\nLogin username/password failed\n')
            self.apiKey = response.json()['apiKey']

            # 2: Create new session
            #if self.apiServerPort != None:
            #    linuxServerIp = linuxServerIp + ':' + str(self.apiServerPort)

            url = 'https://{0}:{1}/api/v1/sessions'.format(linuxServerIp, linuxServerIpPort)
            if self.webQuickTest == False:
                data = {'applicationType': 'ixnrest'}
            if self.webQuickTest == True:
                data = {'applicationType': 'ixnetwork'}

            self.jsonHeader = {'content-type': 'application/json', 'x-api-key': self.apiKey}
            self.logInfo('\nlinuxServerCreateSession')
            response = self.post(url, data=data, headers=self.jsonHeader)

            self.sessionIdNumber = response.json()['id']
            response = self.get(url+'/'+str(self.sessionIdNumber))

            # https://192.168.70.108/ixnetworkweb/api/v1/sessions/7
            self.sessionId = response.json()['links'][0]['href']
            # Remove the redirect /ixnetworkweb from the URL. IxNetwork 8.50 will resolve this.
            self.sessionId = self.sessionId.replace('ixnetworkweb/', '')

            # https://10.10.10.1:443
            matchHeader = re.match('(https://[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+(:[0-9]+)?)', self.sessionId)
            self.httpHeader = matchHeader.group(1)

            if ':' not in self.httpHeader:
                self.httpHeader + '/' + linuxServerIpPort
            
            self.sessionUrl = self.sessionId+'/ixnetwork'
            #self.sessionUrl = 'https://{0}/api/v1/sessions/{1}/ixnetwork'.format(linuxServerIp, self.sessionIdNumber)
            #self.httpHeader = self.sessionUrl.split('/api')[0]

            # /api/v1/sessions/4/ixnetwork
            match = re.match('.*(/api.*)', self.sessionId)
            self.apiSessionId = match.group(1) + '/ixnetwork'
            
            # 3: Start the new session
            self.logInfo('\nlinuxServerStartSession: %s' % self.sessionId)
            response = self.post(self.sessionId+'/operations/start')
            if self.linuxServerWaitForSuccess(response.json()['url'], timeout=60) == 1:
                raise IxNetRestApiException

            if self.webQuickTest == True:
                self.sessionId = 'https://{0}/ixnetworkweb/api/v1/sessions/{1}'.format(linuxServerIp, self.sessionIdNumber)
                self.sessionUrl = 'https://{0}/ixnetworkweb/api/v1/sessions/{1}/ixnetwork'.format(linuxServerIp, self.sessionIdNumber)
                self.httpHeader = self.sessionUrl.split('/api')[0]

        # If an API-Key is provided, then verify the session ID connection.
        if self.apiKey:
            self.get(self.sessionId)

        self.logInfo('sessionId: %s' % self.sessionId)
        self.logInfo('\nsessionUrl: %s' % self.sessionUrl)
        self.logInfo('apiKey: %s' % self.apiKey)

    def linuxServerConfigGlobalLicenseServer(self, linuxServerIp, licenseServerIp, licenseMode, licenseTier):
        """
        Description
           Configure a license server in the global setting.

        Parameters
           linuxServerIp: (str): IP address of the Linux API server.
           licenseServerIp: (list): IP address of all the license server in a list.
           licenseMode: (str): subscription |  perpetual | mixed
           licenseTier: (str): tier1 | tier2 | tier3

        Syntax
           PATCH: /api/v1/sessions/9999/ixnetworkglobals/license
           DATA:  {'servers': [list(licenseServerIp]), 'mode': licenseMode, 'tier': licenseTier}
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

        Paramters
           linuxServerIp: (str): The IP address of the Linux API server.

        Syntax
            GET: /api/v1/sessions/9999/ixnetworkglobals/license
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

        Parameters
           licenseServer: (str): License server IP address(s) in a list.
           licenseMode: (str): subscription | perpetual | mixed
           licenseTier: (str): tier1 | tier2 | tier3 ...

        Syntax
           PATCH: /api/v1/sessions/{id}/ixnetwork/globals/licensing
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
           Display the new session's license details.

        Syntax
            GET: /api/v1/sessions/{id}/globals/licensing
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
           linuxServerStopOperations()
           linuxServerDeleteSession()

        Syntax
           GET = /api/v1/sessions/{id}
        """
        if self.serverOs == 'linux' and self.deleteSessionAfterTest==True:
            self.linuxServerStopOperations()
            self.linuxServerDeleteSession()

    def linuxServerStopOperations(self, sessionId=None):
        """
        Description
           Stop the session ID on the Linux API server.

        Parameter
           sessionId: (str): The session ID to stop.

        Requirement
           self.linuxServerWaitForSuccess()

        Syntax
            POST: /api/v1/sessions/{id}/operations/stop
        """
        if sessionId != None:
            sessionId = sessionId
        else:
            sessionId = self.sessionId

        self.logInfo('\nlinuxServerStopOperations: %s' % sessionId)
        response = self.post(sessionId+'/operations/stop')
        if self.linuxServerWaitForSuccess(response.json()['url'], timeout=90) == 1:
            raise IxNetRestApiException

    def linuxServerDeleteSession(self, sessionId=None):
        """
        Description
           Delete the session ID on the Linux API server.

        Paramter
          sessionId: (str): The session ID to delete on the Linux API server.

        Syntax
            DELETE: /api/v1/sessions/{id}/operations/stop
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
           Wait for a success completion on the Linux API server.

        Paramters
           url: (str): The URL's ID of the operation to verify.
           timeout: (int): The timeout value.
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

        Requirement
            self.waitForComplete()

        Syntax:
           /api/v1/sessions/{1}/ixnetwork/operations/newconfig
        """
        url = self.sessionUrl+'/operations/newconfig'
        self.logInfo('\nnewBlankConfig')
        response = self.post(url)
        url = self.sessionUrl+'/operations/newconfig/'+response.json()['id']
        self.waitForComplete(response, url)

    def refreshHardware(self, chassisObj):
        """
        Description
           Refresh the chassis

        Parameter
           chassisObj: (str):The chassis object.
                           Ex: /api/v1/sessions/{1}/ixnetwork/availableHardware/chassis/1

        Requirement
           self.waitForComplete()

        Syntax
            /api/v1/sessions/{1}/ixnetwork/availableHardware/chassis/operations/refreshinfo
        """
        response = self.post(self.sessionUrl+'/availableHardware/chassis/operations/refreshinfo', data={'arg1': [chassisObj]})
        self.waitForComplete(response, self.sessionUrl+'/availableHardware/chassis/operations/refreshinfo')

    def query(self, data, silentMode=True):
        """
        Description
           Query for objects using filters.

        Paramater
           silentMode: (bool): True: Don't display any output on stdout.

        Notes
            Assuming this is a BGP configuration, which has two Topologies.
            Below demonstrates how to query the BGP host object by
            drilling down the Topology by its name and the specific the BGP attributes to modify at the
            BGPIpv4Peer node: flap, downtimeInSec, uptimeInSec.
            The from '/' is the entry point to the API tree.
            Notice all the node. This represents the API tree from the / entry point and starting at 
            Topology level to the BGP host level.

        Notes
           Use the API Browser tool on the IxNetwork GUI to view the API tree.
            data: {'from': '/',
                    'nodes': [{'node': 'topology',    'properties': ['name'], 'where': [{'property': 'name', 'regex': 'Topo1'}]},
                              {'node': 'deviceGroup', 'properties': [], 'where': []},
                              {'node': 'ethernet',    'properties': [], 'where': []},
                              {'node': 'ipv4',        'properties': [], 'where': []},
                              {'node': 'bgpIpv4Peer', 'properties': ['flap', 'downtimeInSec', 'uptimeInSec'], 'where': []}]
                }

        Requirements
            self.waitForComplete()

        Examples
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
        self.waitForComplete(response, url+'/'+response.json()['id'])
        return response

    def configMultivalue(self, multivalueUrl, multivalueType, data):
        """
        Description
           Configure multivalues.

        Parameters
           multivalueUrl: (str): The multivalue: /api/v1/sessions/{1}/ixnetwork/multivalue/1
           multivalueType: (str): counter|singleValue|valueList
           data: (dict): singleValue: data={'value': '1.1.1.1'})
                             valueList:   data needs to be in a [list]:  data={'values': [list]}
                             counter:     data={'start': value, 'direction': increment|decrement, 'step': value}
        """
        if multivalueType == 'counter':
            # Examples: macAddress = {'start': '00:01:01:00:00:01', 'direction': 'increment', 'step': '00:00:00:00:00:01'}
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
           Get the multivalue values.

        Parameters
           multivalueObj: (str): The multivalue object: /api/v1/sessions/{1}/ixnetwork/multivalue/208
           silentMode: (bool): True=Display the GET and status code. False=Don't display.
        
        Requirements
           self.waitForComplete()
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
        self.waitForComplete(response, self.sessionUrl+'/operations/multivalue/getValues'+response.json()['id'])
        return response.json()['result']

    def getAttributeValue(self, obj, attribute):
        """
        Description
           Based on the object handle, get the attribute and return the value.
        
        Parameter
           obj: <str:obj>: An object handle: 
                For example: If you want the ethernet MTU, then pass in the ethernet object handle:
                            /api/v1/sessions/{id}/ixnetwork/topology/{id}/deviceGroup/{id}/ethernet/{id}
                            and set attribute='mtu'

        Note:
           Where to get the object's attribute names:
              - Use the API browser and go to your object.
              - All the attributes are listed on the right pane.
        """
        response = self.get(self.httpHeader + obj)
        
        # value: Could be /api/v1/sessions/{id}/ixnetwork/multivalue/{id} or the actual value
        value = response.json()[attribute]
        if type(value) == str and 'multivalue' in value:
            multivalueObj = value
            value = self.getMultivalueValues(multivalueObj)
            return value
        else:
            return value

    def stdoutRedirect(self):
        """
        Description
           For Robot Framework.  Robot captures the stdout. This stdoutRedirect
           will redirect the output back to stdout so you could see the test progress
           and to troubleshoot.
        """
        for attr in ('stdin', 'stdout', 'stderr'):
            setattr(sys, attr, getattr(sys, '__%s__' %attr))        
            
    @staticmethod
    def prettyprintAllOperations(sessionUrl):
        """
        Description
           A staticmethod to rendering a nice output of an operations options and descriptions.

        Parameter
           sessionUrl: (str): http://{apiServerIp}:{port}/api/v1/sessions/1/ixnetwork

        Syntax:
            /api/v1/sessions/{1}/ixnetwork/operations
        """
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
        Description
           Print each dict key with indentions for human readability.
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



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
import sys
import requests
import datetime
import platform
import time
from ixnetwork_restpy import TestPlatform


class IxNetRestApiException(Exception):
    def __init__(self, msg=None):
        if platform.python_version().startswith('3'):
            super().__init__(msg)

        if platform.python_version().startswith('2'):
            super(IxNetRestApiException, self).__init__(msg)

        if Connect.robotStdout is not None:
            Connect.robotStdout.log_to_console(msg)

        showErrorMsg = '\nIxNetRestApiException error: {0}\n\n'.format(msg)
        print(showErrorMsg)
        if Connect.enableDebugLogFile:
            with open(Connect.debugLogFile, 'a') as restLogFile:
                restLogFile.write(showErrorMsg)


class Connect:
    # For IxNetRestApiException
    debugLogFile = None
    enableDebugLogFile = False
    robotStdout = None

    def __init__(self, apiServerIp=None, serverIpPort=None,
                 serverOs='windows', linuxChassisIp=None,
                 manageSessionMode=False, webQuickTest=False,
                 username=None, password='admin', licenseServerIp=None,
                 licenseMode=None, licenseTier=None,
                 deleteSessionAfterTest=True, verifySslCert=False,
                 includeDebugTraceback=True, sessionId=None,
                 httpsSecured=None, apiKey=None,
                 generateLogFile=True, robotFrameworkStdout=False,
                 linuxApiServerTimeout=120):
        """
        Description
           Initializing default parameters and making a connection to the API server

        Examples
            Right click on "IxNetwork API server", select properties and under target
            ixnetwork.exe -restInsecure -restPort 11009 -restOnAllInterfaces -tclPort 8009

        Parameters
           apiServerIp: (str): The API server IP address.
           serverIpPort: (str): The API server IP address socket port.
           serverOs: (str): windows|windowsConnectionMgr|linux
           linuxChassisIp: (str): Connect to a Linux OS chassis IP address.
           webQuickTest: (bool): True: Using IxNetwork
                                 Web Quick Test. Otherwise, using IxNetwork.
           includeDebugTraceback: (bool):
                                   True: Traceback messsages are
                                   included in raised exceptions.
                                   False: No traceback.
                                   Less verbose for debugging.
           username: (str): The login username. For Linux API server only.
           password: (str): The login password. For Linux API server only.
           licenseServerIp: (str): The license server IP address.
           licenseMode: (str): subscription | perpetual | mixed
           licenseTier: (str): tier1 | tier2 | tier3
           linuxApiServerTimeout: (int): For Linux API server start operation timeout. Defaults
           to 120 seconds.
           deleteSessionAfterTest: (bool): True: Delete the session.
                                           False: Don't delete the session.
           verifySslCert: (str): Optional: Include your SSL certificate for added security.
           httpsSecured: (bool): This parameter is only used by Connection Mgr when user wants to
           connect to an existing session.
                                True = IxNetwork ReST API server is using HTTPS
                                This parameter must also include sessionId
                                and serverIpPort=<the ssl port number>

           serverOs: (str): Defaults to windows.
                            windows|windowsConnectionMgr|linux.
           includeDebugTraceback: (bool): True: Include tracebacks in raised exceptions.
           sessionId: (str): The session ID on the Linux API server or Windows Connection Mgr to
           connect to.
           apiKey: (str): The Linux API server user account API-Key to use for the sessionId
           connection.
           generateLogFile: True|False|<log file name>.
                            If you want to generate a log file, provide the log file name.
                            True = Then the log file default name is ixNetRestApi_debugLog.txt
                            False = Disable generating a log file.
                            <log file name> = The full path + file name of the log file to create.
           robotFrameworkStdout: (bool):  True = Print to stdout.
           httpInsecure: (bool): This parameter is only for Windows connections.
                                True: Using http.  False: Using https.
                                Starting 8.50: IxNetwork defaults to use https.
                                If you are using versions prior to 8.50, it needs to be a http
                                connection. In this case, set httpInsecure=True.

           Notes
              To connect to an existing configuration.
                Windows: Nothing special to include. The session ID is always "1".
                Linux API server: Include the api-key and sessionId that you want to connect to.
                Windows Connection Manager: Include just the sessionId: For example: 8021.
        """

        # Disable SSL warnings
        requests.packages.urllib3.disable_warnings()

        # Disable non http connections.
        from requests.packages.urllib3.exceptions import InsecureRequestWarning
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        self._session = requests.Session()

        self.serverOs = serverOs  # windows|windowsConnectionMgr|linux
        self.username = username
        self.password = password
        self.apiKey = apiKey
        self.verifySslCert = verifySslCert
        self.linuxApiServerIp = apiServerIp
        self.manageSessionMode = manageSessionMode
        self.apiServerPort = serverIpPort
        self.webQuickTest = webQuickTest
        self.generateLogFile = generateLogFile
        self.robotFrameworkStdout = robotFrameworkStdout
        self.linuxChassisIp = linuxChassisIp
        self.linuxApiServerTimeout = linuxApiServerTimeout
        self.sessionId = sessionId

        # Make Robot print to stdout
        if self.robotFrameworkStdout:
            from robot.libraries.BuiltIn import _Misc
            self.robotStdout = _Misc()
            Connect.robotStdout = self.robotStdout

        if generateLogFile:
            # Default the log file name
            self.restLogFile = 'ixNetRestApi_debugLog.txt'
            Connect.enableDebugLogFile = True
            Connect.debugLogFile = self.restLogFile

        if type(generateLogFile) != bool:
            self.restLogFile = generateLogFile

        if self.serverOs == 'windows':
            if self.apiServerPort is None:
                self.apiServerPort = 11009
            else:
                self.apiServerPort = serverIpPort
            self.testPlatform = TestPlatform(ip_address=self.linuxApiServerIp,
                                             rest_port=self.apiServerPort,
                                             platform=self.serverOs,
                                             verify_cert=verifySslCert,
                                             log_file_name=self.restLogFile)
            self.session = self.testPlatform.Sessions.add()
            self.sessionId = self.session.Id
            self.ixNetwork = self.session.Ixnetwork

        if self.serverOs == 'windowsConnectionMgr':
            if self.sessionId:
                self.testPlatform = TestPlatform(
                    ip_address=self.linuxApiServerIp,
                    rest_port=self.apiServerPort,
                    platform=self.serverOs,
                    verify_cert=verifySslCert,
                    log_file_name=self.restLogFile)

        if self.serverOs == 'linux':
            if self.apiServerPort is None:
                self.apiServerPort = 443

            if username is None or password is None:
                self.username = 'admin'
                self.password = 'admin'

            self.testPlatform = TestPlatform(ip_address=self.linuxApiServerIp,
                                             rest_port=self.apiServerPort,
                                             platform=self.serverOs,
                                             verify_cert=verifySslCert,
                                             log_file_name=self.restLogFile)
            self.testPlatform.Authenticate(self.username, self.password)

            if apiKey is not None and sessionId is None:
                raise IxNetRestApiException('Providing an apiKey must also provide a sessionId.')
                # Connect to an existing session on the Linux API server
            if apiKey and sessionId:
                self.session = self.testPlatform.Sessions.find(Id=sessionId)
                self.ixNetwork = self.session.Ixnetwork

            if apiKey is None and sessionId:
                self.session = self.testPlatform.Sessions.find(Id=sessionId)
                self.ixNetwork = self.session.Ixnetwork

            if apiKey is None and sessionId is None:
                self.session = self.testPlatform.Sessions.add()
                self.sessionId = self.session.Id
                self.ixNetwork = self.session.Ixnetwork

            if licenseServerIp or licenseMode or licenseTier:
                self.configLicenseServerDetails(
                    licenseServerIp, licenseMode, licenseTier)

            # For Linux API Server and Windoww Connection Mgr only:
            # Delete the session when script is done
            self.deleteSessionAfterTest = deleteSessionAfterTest
            if includeDebugTraceback is False:
                sys.tracebacklimit = 0

    def get(self, restApi, data={}, stream=False, silentMode=False, ignoreError=False,
            maxRetries=5):
        """
        Description
            A HTTP GET function to send REST APIs.

        Parameters
           restApi: (str): The REST API URL.
           data: (dict): The data payload for the URL.
           silentMode: (bool):  To display on stdout: URL, data and header info.
           ignoreError: (bool): True: Don't raise an exception.
                                False: The response will be returned.
           maxRetries: <int>: The maximum amount of GET retries before declaring as server
           connection failure.

        Note:
            This API is not needed in RestPY, Added pass to avoid exception
        """
        pass

    def post(self, restApi, data={}, headers=None, silentMode=False, noDataJsonDumps=False,
             ignoreError=False, maxRetries=5):
        """
        Description
           A HTTP POST function to create and start operations.

        Parameters
           restApi: (str): The REST API URL.
           data: (dict): The data payload for the URL.
           headers: (str): The special header to use for the URL.
           silentMode: (bool):  To display on stdout: URL, data and header info.
           noDataJsonDumps: (bool): True: Use json dumps.
                            False: Accept the data as-is.
           ignoreError: (bool): True: Don't raise an exception.
                                False: The response will be returned.
           maxRetries: <int>: The maximum amount of GET retries before declaring as server
           connection failure.
        Note:
            This API is not needed in RestPY, Added pass to avoid exception
        """
        pass

    def patch(self, restApi, data={}, silentMode=False, ignoreError=False, maxRetries=5):
        """
        Description
           A HTTP PATCH function to modify configurations.

        Parameters
           restApi: (str): The REST API URL.
           data: (dict): The data payload for the URL.
           silentMode: (bool):  To display on stdout: URL, data and header info.
           ignoreError: (bool): True: Don't raise an exception.
                                False: The response will be returned.
           maxRetries: <int>: The maximum amount of GET retries before declaring as server
           connection failure.
        Note:
            This API is not needed in RestPY, Added pass to avoid exception
        """
        pass

    def options(self, restApi, data={}, silentMode=False, ignoreError=False, maxRetries=5):
        """
        Description
            A HTTP OPTIONS function to send REST APIs.

        Parameters
           restApi: (str): The REST API URL.
           silentMode: (bool):  To display on stdout: URL, data and header info.
           ignoreError: (bool): True: Don't raise an exception.
                                False: The response will be returned.
           maxRetries: <int>: The maximum amount of GET retries before declaring as server
           connection failure
        Note:
            This API is not needed in RestPY, Added pass to avoid exception
        """
        pass

    def delete(self, restApi, data={}, headers=None, maxRetries=5):
        """
        Description
           A HTTP DELETE function to delete the session.
           For Linux and Windows Connection Mgr API server only.

        Paramters
           restApi: (str): The REST API URL.
           data: (dict): The data payload for the URL.
           headers: (str): The headers to use for the URL.
           maxRetries: <int>: The maximum amount of GET retries before declaring as server
           connection failure.
        Note:
            This API is not needed in RestPY, Added pass to avoid exception
        """
        pass

    def getDate(self):
        dateAndTime = str(datetime.datetime.now()).split(' ')
        return dateAndTime[0]

    def getTime(self):
        dateAndTime = str(datetime.datetime.now()).split(' ')
        return dateAndTime[1]

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
           Connect to a Windows IxNetwork API Server. This is for both Windows and Windows server
           with IxNetwork Connection Manager. This will set up the session URL to use throughout
           the test.

        Parameter
          ixNetRestServerIp: (str): The Windows IxNetwork API Server IP address
          ixNetRestServerPort: (str): Default: 11009. Provide a port number to connect to.
          On a Linux API Server, a socket port is not needed. State "None".
        Note:
            This API is not needed in RestPY, since class constructor is handling creation of
            sessions
        """
        pass

    def deleteSession(self):
        """
        Description
           Delete the instance session ID.
           For Linux and Windows Connection Manager only.
        """
        if self.deleteSessionAfterTest:
            session = self.testPlatform.Sessions.find(Id=self.sessionId)
            session.remove()

    def logInfo(self, msg, end='\n', timestamp=True):
        """
        Description
           An internal function to print info to stdout

        Parameters
           msg: (str): The message to print.
        """
        currentTime = self.getTime()

        if timestamp:
            msg = '\n' + currentTime + ': ' + msg
        else:
            msg = msg

        print('{0}'.format(msg), end=end)
        if self.generateLogFile:
            with open(self.restLogFile, 'a') as restLogFile:
                restLogFile.write(msg + end)

        if self.robotFrameworkStdout:
            self.robotStdout.log_to_console(msg)

    def logWarning(self, msg, end='\n', timestamp=True):
        """
        Description
           An internal function to print warnings to stdout.

        Parameter
           msg: (str): The message to print.
        """
        currentTime = self.getTime()

        if timestamp:
            msg = '\n{0}: Warning: {1}'.format(currentTime, msg)
        else:
            msg = msg

        print('{0}'.format(msg), end=end)
        if self.generateLogFile:
            with open(self.restLogFile, 'a') as restLogFile:
                restLogFile.write('Warning: ' + msg + end)

        if self.robotFrameworkStdout:
            self.robotStdout.log_to_console(msg)

    def logError(self, msg, end='\n', timestamp=True):
        """
        Description
           An internal function to print error to stdout.

        Parameter
           msg: (str): The message to print.
        """
        currentTime = self.getTime()

        if timestamp:
            msg = '\n{0}: Error: {1}'.format(currentTime, msg)
        else:
            msg = '\nError: {0}'.format(msg)

        print('{0}'.format(msg), end=end)
        if self.generateLogFile:
            with open(self.restLogFile, 'a') as restLogFile:
                restLogFile.write('Error: ' + msg + end)

        if self.robotFrameworkStdout:
            self.robotStdout.log_to_console(msg)

    def getIxNetworkVersion(self):
        """
        Description
           Get the IxNetwork version.

        """
        buildNumber = self.ixNetwork.Globals.BuildNumber
        return buildNumber

    def getAllSessionId(self):
        """
        Show all opened session IDs.

        Return
           A list of opened session IDs.

           {4: {'startedOn': '2018-10-06 12:09:18.333-07:00',
              'state': 'Active',
              'subState': 'Ready',
              'userName': 'admin'},
            5: {'startedOn': '2018-10-06 18:49:05.691-07:00',
              'state': 'Active',
              'subState': 'Ready',
              'userName': 'admin'}
           }
        """
        sessionId = {}
        sessions = self.testPlatform.Sessions.find()
        for session in sessions:
            sessionId.update({session.Id: {
                'state': session.State,
                'UserName': session.UserName
            }})

        return sessionId

    def showErrorMessage(self, silentMode=False):
        """
        Description
           Show all the error messages from IxNetwork.

        Parameter
          silentMode: (bool): True: Don't print the REST API on stdout.

        """
        errorList = []
        errorObj = self.ixNetwork.Globals.AppErrors.find().Error.find()

        print()
        for errorId in errorObj:
            if errorId.ErrorLevel == 'kError':
                print('CurrentErrorMessage: {0}'.format(errorId.Name))
                print('\tDescription: {0}'.format(errorId.LastModified))
                errorList.append(errorId.Name)
        print()
        return errorList

    def waitForComplete(self, response='', url='', silentMode=False, ignoreException=False,
                        httpAction='get', timeout=90):
        """
        Description
           Wait for an operation progress to complete.

        Parameters
           response: (json response/dict): The POST action response. Generally, after an
           /operations action. Such as /operations/startallprotocols,
                     /operations/assignports.
           silentMode: (bool):  If True, display info messages on stdout.
           ignoreException: (bool): ignoreException is for assignPorts. Don't want to exit test.
                            Verify port connectionStatus for: License Failed and Version Mismatch to
                             report problem immediately.

           httpAction: (get|post): Defaults to GET.
                       For chassisMgmt, it uses POST.
           timeout: (int): The time allowed to wait for success completion in seconds.
        Note:
            This API is not needed in RestPY, Added pass to avoid exception
        """
        pass

    def connectToLinuxIxosChassis(self, chassisIp, username, password):
        """
        Description
            Connect to a Linux IxOS Chassis

        Parameters
            chassisIp: The Linux chassis IP address
            username: Login username.
            password: Login password
        """
        self.ixNetwork.ConnectToChassis(Arg1=chassisIp)

    def connectToLinuxApiServer(self, linuxServerIp, linuxServerIpPort, username='admin',
                                password='admin', verifySslCert=False, timeout=120):
        """
        Description
           Connect to a Linux API server.

        Parameters
           linuxServerIp: (str): The Linux API server IP address.
           username: (str): Login username. Default = admin.
           password: (str): Login password. Default = admin.
           verifySslCert: (str): Default: None. The SSL Certificate for secure access verification.
           timeout: (int): Default:120.  The timeout to wait for the Linux API server to start up.
                           Problem: In case the linux api server is installed in a chassis and
                           the DNS is misconfigured, it takes longer to start up.

        Note:
            This API is not needed in RestPY,as RestPy API is already available
        """
        pass

    def linuxServerGetGlobalLicense(self, linuxServerIp):
        """
        Description
           Get the global license server details from the Linux API server.

        Paramters
           linuxServerIp: (str): The IP address of the Linux API server.

        """
        licenseServerIp = self.ixNetwork.Globals.Licensing.LicensingServers
        licenseServerMode = self.ixNetwork.Globals.Licensing.Mode
        licenseServerTier = self.ixNetwork.Globals.Licensing.Tier
        return licenseServerIp, licenseServerMode, licenseServerTier

    def configLicenseServerDetails(self, licenseServer=None, licenseMode=None, licenseTier=None):
        """
        Description
           Configure license server details: license server IP, license mode and license tier.

        Parameters
           licenseServer: (str): License server IP address(s) in a list.
           licenseMode: (str): subscription | perpetual | mixed
           licenseTier: (str): tier1 | tier2 | tier3 ...

        """
        # Each new session requires configuring the
        # new session's license details.

        if licenseServer:
            self.ixNetwork.Globals.Licensing.LicensingServers = [licenseServer]
        if licenseMode:
            self.ixNetwork.Globals.Licensing.Mode = licenseMode
        if licenseTier:
            self.ixNetwork.Globals.Licensing.Tier = licenseTier

        self.showLicenseDetails()

    def showLicenseDetails(self):
        """
        Description
           Display the new session's license details.

        """
        self.logInfo('\nVerifying sessionId license server: %s' % self.ixNetwork.href,
                     timestamp=False)
        self.logInfo('\tLicensce Servers: %s' % self.ixNetwork.Globals.Licensing.LicensingServers,
                     timestamp=False)
        self.logInfo('\tLicensing Mode: %s' % self.ixNetwork.Globals.Licensing.Mode,
                     timestamp=False)
        self.logInfo('\tTier Level: %s' % self.ixNetwork.Globals.Licensing.Tier, timestamp=False)

    def getAllOpenSessionIds(self):
        """
        Description
           Get a list of open session IDs and some session metas.

        Return
            A dict
        """
        activeSessionDict = {}
        availableSessions = self.testPlatform.Sessions.find()

        for session in availableSessions:
            if session.State == 'ACTIVE':
                activeSessionDict.update({session.Id: {'id': session.Id,
                                                       'sessionIdUrl': session.href,
                                                       'username': session.UserName,
                                                       'state': session.State
                                                       }
                                          }
                                         )
        return activeSessionDict

    def linuxServerStopAndDeleteSession(self):
        """
        Description
           Wrapper to stop and delete the session ID on the Linux API server.

        Requirements
           linuxServerStopOperations()
           linuxServerDeleteSession()

        """

        if self.serverOs == 'linux' and self.deleteSessionAfterTest:
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

        """
        if sessionId is not None:
            sessionId = sessionId
        else:
            sessionId = self.sessionId
        print("removing sesionId", sessionId)
        self.testPlatform.Sessions.find(Id=sessionId).remove()

    def linuxServerDeleteSession(self, sessionId=None):
        """
        Description
           Delete the session ID on the Linux API server.

        Paramter
          sessionId: (str): The session ID to delete on the Linux API server.

        """
        if sessionId is not None:
            sessionId = sessionId
        else:
            sessionId = self.sessionId
        self.testPlatform.Sessions.find(Id=sessionId).remove()

    def linuxServerWaitForSuccess(self, url, timeout=120):
        """
        Description
           Wait for a success completion on the Linux API server.

        Paramters
           url: (str): The URL's ID of the operation to verify.
           timeout: (int): The timeout value.
        """
        foundUrl = False
        session = None
        availableSessions = self.testPlatform.Sessions.find()
        for session in availableSessions:
            if url in session.href:
                foundUrl = True
                break

        if foundUrl:
            for counter in range(1, timeout + 1):
                currentStatus = session.State
                self.logInfo('\tCurrentStatus: {0}: {1}/{2} seconds. SessionId {3}'.format(
                    currentStatus, counter, timeout, session.Id), timestamp=False)
                if counter < timeout + 1 and currentStatus != 'ACTIVE':
                    time.sleep(1)

                if counter == timeout + 1 and currentStatus != 'ACTIVE':
                    return 1

                if counter < timeout + 1 and currentStatus == 'ACTIVE':
                    return 0
        else:
            self.logInfo('\tUrl not found {0}'.format(url))

    def newBlankConfig(self):
        """
        Description
           Start a new blank configuration.

        Requirement
            self.waitForComplete()

        """
        self.ixNetwork.NewConfig()

    def refreshHardware(self, chassisObj):
        """
        Description
           Refresh the chassis

        Parameter
           chassisObj: (str):The chassis object.

        Requirement
           self.waitForComplete()

        """
        chassisObj.RefreshInfo()

    def query(self, data, silentMode=False):
        """
        Description
           Query for objects using filters.

        Paramater
           silentMode: (bool): True: Don't display any output on stdout.

        Notes
            Assuming this is a BGP configuration, which has two Topologies. Below demonstrates
            how to query the BGP host object by drilling down the Topology by its name and the
            specific the BGP attributes to modify at the BGPIpv4Peer node: flap, downtimeInSec,
            uptimeInSec. The from '/' is the entry point to the API tree. Notice all the node.
            This represents the API tree from the / entry point and starting at Topology level to
            the BGP host level.

        Requirements
            self.waitForComplete()

        Examples
            # GET THE BGP ATTRIBUTES TO MODIFY
            bgpHostFlapMultivalue = bgpHostAttributes['flap']
            bgpHostFlapUpTimeMultivalue = bgpHostAttributes['uptimeInSec']
            bgpHostFlapDownTimeMultivalue = bgpHostAttributes['downtimeInSec']

            restObj.configMultivalue(bgpHostFlapMultivalue, multivalueType='valueList',
            data={'values': ['true', 'true']})
            restObj.configMultivalue(bgpHostFlapUpTimeMultivalue, multivalueType='singleValue',
            data={'value': '60'})
            restObj.configMultivalue(bgpHostFlapDownTimeMultivalue, multivalueType='singleValue',
            data={'value': '30'})
        Note:
            This API is not needed in RestPY, Added pass to avoid exception
        """
        pass

    def select(self, data):
        """
        Description
           Using the Select operation to query for objects using filters.

        Note:
            This API is not needed in RestPY, Added pass to avoid exception
        """
        pass

    def configMultivalue(self, multivalueUrl, multivalueType, data):
        """
        Description
           Configure multivalues.

        Parameters
           multivalueUrl: (str): The multivalue
           multivalueType: (str): counter|singleValue|valueList
           data: (dict): singleValue: data={'value': '1.1.1.1'})
                         valueList:data needs to be in a [list]: data={'values': [list]}
                         counter:data={'start': value, 'direction': increment|decrement,
                         'step': value}
        """
        if multivalueType.lower() == "counter":
            if data['direction'] == "increment":
                multivalueUrl.Increment(start_value=data['start'], step_value=data['step'])
            if data['direction'] == "decrement":
                multivalueUrl.Decrement(start_value=data['start'], step_value=data['step'])
        elif multivalueType.lower() == "singlevalue":
            multivalueUrl.Single(data['value'])
        elif multivalueType.lower() == "valuelist":
            multivalueUrl.ValueList(data['values'])
        elif multivalueType.lower() == "randomrange":
            multivalueUrl.RandomRange(min_value=data['min_value'], max_value=data['max_value'],
                                      step_value=data['step_value'], seed=data['seed'])
        elif multivalueType.lower() == "custom":
            multivalueUrl.Custom(start_value=data['start_value'], step_value=data['step_value'],
                                 increments=data['increments'])
        elif multivalueType.lower() == "alternate":
            multivalueUrl.Alternate(data['alternating_value'])
        elif multivalueType.lower() == "distributed":
            multivalueUrl.Distributed(algorithm=data['algorithm'], mode=data['mode'],
                                      values=data['values'])
        elif multivalueType.lower() == "randommask":
            multivalueUrl.RandomMask(fixed_value=data['fixed_value'], mask_value=data['mask_value'],
                                     seed=data['seed'], count=data['count'])
        elif multivalueType.lower() == "string":
            multivalueUrl.String(string_pattern=data['string_pattern'])

    def getMultivalueValues(self, multivalueObj, silentMode=False):
        """
        Description
           Get the multivalue values.

        Parameters
           multivalueObj: <str>: The multivalue object
           silentMode: <bool>: True=Display the GET and status code.
                               False=Don't display.

        Requirements
           self.ixnObj.waitForComplete()

        Return
           The multivalue values
        """
        return multivalueObj.Values

    def getObjAttributeValue(self, obj, attribute):
        """
        Description
           Based on the object handle, get any property attribute and return the value.

        Parameter
           obj: <str:obj>: An object handle:

        Note:
           Where to get the object's attribute names:
              - Use the API browser and go to your object.
              - All the attributes are listed on the right pane.
        """
        try:
            attribute = attribute[0].capitalize() + attribute[1:]
            value = eval("obj." + attribute)
            values = self.getMultivalueValues(value)
            return values
        except AttributeError:
            value = getattr(obj, attribute)
            return value

    def stdoutRedirect(self):
        """
        Description
           For Robot Framework.  Robot captures the stdout. This stdoutRedirect will redirect the
           output back to stdout so you could see the test progress and to troubleshoot.
        """
        for attr in ('stdin', 'stdout', 'stderr'):
            setattr(sys, attr, getattr(sys, '__%s__' % attr))

    @staticmethod
    def prettyprintAllOperations(sessionUrl):
        """
        Description
           A staticmethod to rendering a nice output of an operations options and descriptions.

        Note:
            This API is not needed in RestPY, Added pass to avoid exception
        """
        pass

    @staticmethod
    def printDict(obj, nested_level=0, output=sys.stdout):
        """
        Description
           Print each dict key with indentions for human readability.
        """
        spacing = '   '
        spacing2 = ' '
        if type(obj) == dict:
            print('%s' % (nested_level * spacing), file=output)
            for k, v in obj.items():
                if hasattr(v, '__iter__'):
                    print('%s%s:' % ((nested_level + 1) * spacing, k), file=output, end='')
                    Connect.printDict(v, nested_level + 1, output)
                else:
                    print('%s%s: %s' % ((nested_level + 1) * spacing, k, v), file=output)

            print('%s' % (nested_level * spacing), file=output)
        elif type(obj) == list:
            print('%s[' % (nested_level * spacing), file=output)
            for v in obj:
                if hasattr(v, '__iter__'):
                    Connect.printDict(v, nested_level + 1, output)
                else:
                    print('%s%s' % ((nested_level + 1) * spacing, v), file=output)
            print('%s]' % (nested_level * spacing), output)
        else:
            print('%s%s' % ((nested_level * spacing2), obj), output)

    def placeholder(self):
        """
        Note:
            This API is not needed in RestPY, Added pass to avoid exception
        """
        pass

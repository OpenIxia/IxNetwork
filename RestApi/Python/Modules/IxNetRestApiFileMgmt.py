import sys, re, os, json, platform, io
from IxNetRestApi import IxNetRestApiException

class FileMgmt(object):
    def __init__(self, ixnObj=None):
        """
        Description
           Initialize default attributes.

        Parameter
           ixnObj: (Object): The parent object.
        """
        self.ixnObj = ixnObj

    def setMainObject(self, mainObject):
        """
        Description
           For Robot support only. Setting the parent object.

        Parameter
           mainObject: (Object): The parent object.
        """
        self.ixnObj = mainObject

    def loadConfigFile(self, configFile, localFile=True):
        """
        Description
            Load a saved config file.

        Parameters
            configFile: (str): The full path including the saved config filename.
                               If the config file is in a Windows filesystem, the format is c:\\path\\bgp.ixncfg
                               If you are executing the script from Linux and the config file is in local Linux filesystem,
                               the format is /path/bgp.ixncfg and localFile=True.

            localFile: (bool): For Windows API server and Connection Mgr running on a Windows server only.
                               Set to False if the config file is in the Windows API server filesystem.
        """
        # Verify if the config file is a letter drive: c:\\path\\
        # If it is, get the config file from Windows path to the IxNetwork API server common path.
        #if bool(re.match('^[a-zA-Z]+:', configFile)):
        #    localFile = True
        #else:
        #    localFile = False

        if localFile == False:
            # The config file is located in Windows
            fileName = configFile.split('\\')[-1]
            copyFileUrl = self.ixnObj.sessionUrl+'/operations/copyfile'            
            destinationPath = '{0}/ixnetwork/files/'.format(self.ixnObj.headlessSessionId) + fileName
            response = self.ixnObj.post(copyFileUrl,data={"arg1": configFile, "arg2": destinationPath})
            self.ixnObj.waitForComplete(response, copyFileUrl+'/'+response.json()['id'], silentMode=False, timeout=30)

        if localFile == True:
            if os.path.exists(configFile) is False:
                raise IxNetRestApiException("Config file doesn't exists: %s" % configFile)

            if self.ixnObj.serverOs == 'linux':
                octetStreamHeader = {'content-type': 'application/octet-stream', 'x-api-key': self.ixnObj.apiKey}
            else:
                octetStreamHeader = {'content-type': 'application/octet-stream'}

            fileName = configFile.split('/')[-1]

            # Read the config file
            self.ixnObj.logInfo('\nReading saved config file')
            with open(configFile, mode='rb') as file:
                configContents = file.read()
                configContents = io.BytesIO(configContents)

                # Upload it to the server and give it any name you want for the filename
                uploadFile = self.ixnObj.sessionUrl+'/files?filename='+fileName
                self.ixnObj.logInfo('\nUploading file to server: %s' % uploadFile)
                response = self.ixnObj.post(uploadFile, data=configContents, noDataJsonDumps=True, headers=octetStreamHeader, silentMode=False)

        loadConfigUrl = self.ixnObj.sessionUrl+'/operations/loadconfig'

        # Set the payload to load the given filename:  /api/v1/sessions/{id}/ixnetwork/files/ospfNgpf_8.10.ixncfg
        payload = {'arg1': '{0}/ixnetwork/files/{1}'.format(self.ixnObj.headlessSessionId, fileName)}

        # Tell the server to load the config file
        if localFile == True:
            response = self.ixnObj.post(loadConfigUrl, data=payload, headers=octetStreamHeader)

        if localFile == False:
            response = self.ixnObj.post(loadConfigUrl, data=payload)

        self.ixnObj.waitForComplete(response, loadConfigUrl+'/'+response.json()['id'], silentMode=False, timeout=140)

    def copyFileWindowsToRemoteWindows(self, windowsPathAndFileName, localPath, renameDestinationFile=None, includeTimestamp=False):
        """
        Description
            Copy files from the IxNetwork API Server c: drive to local Linux filesystem.
            The filename to be copied will remain the same filename unless you set renameDestinationFile to something you otherwise preferred.
            You could also include a timestamp for the destination file.

        Parameters
            windowsPathAndFileName: (str): The full path and filename to retrieve from Windows API server.
            localPath: (str): The remote Windows destination path to put the file to.
            renameDestinationFile: (str): You could rename the destination file.
            includeTimestamp: (bool):  If False, each time you copy the same file will be overwritten.
        """
        import datetime

        self.ixnObj.logInfo('\ncopyFileWindowsToRemoteWindows: From: %s to %s\n' % (windowsPathAndFileName, localPath))
        windowsPathAndFileName = windowsPathAndFileName.replace('\\', '\\\\')
        fileName = windowsPathAndFileName.split('\\')[-1]
        fileName = fileName.replace(' ', '_')
        # Default location: "C:\\Users\\<user name>\\AppData\\Local\\sdmStreamManager\\common"
        destinationPath = '{0}/ixnetwork/files/'.format(self.ixnObj.headlessSessionId) + fileName
        currentTimestamp = datetime.datetime.now().strftime('%H%M%S')

        # Step 1 of 2:
        response = self.ixnObj.post(self.ixnObj.sessionUrl+'/operations/copyfile',
                             data={"arg1": windowsPathAndFileName, "arg2": destinationPath})

        # curl http://{apiServerIp:port}/api/v1/sessions/1/ixnetwork/files/AggregateResults.csv -O -H "Content-Type: application/octet-stream" -output /home/hgee/AggregateResults.csv

        # Step 2 of 2:
        requestStatus = self.ixnObj.get(self.ixnObj.sessionUrl+'/files/%s' % (fileName), stream=True, ignoreError=True)
        if requestStatus.status_code == 200:
            if renameDestinationFile is not None:
                fileName = renameDestinationFile

            contents = requestStatus.raw.read()

            if includeTimestamp:
                tempFileName = fileName.split('.')
                if len(tempFileName) > 1:
                    extension = fileName.split('.')[-1]
                    fileName = tempFileName[0]+'_' + currentTimestamp + '.' + extension
                else:
                    fileName = tempFileName[0]+'_' + currentTimestamp

                localPath = localPath+'/'+fileName
            else:
                localPath = localPath+'/'+fileName

            with open(localPath, 'wb') as downloadedFileContents:
                downloadedFileContents.write(contents)

            response = self.ixnObj.get(self.ixnObj.sessionUrl+'/files')

            self.ixnObj.logInfo('\nA copy of your saved file/report is in:\n\t%s' % (windowsPathAndFileName))
            self.ixnObj.logInfo('\ncopyFileWindowsToLocalLinux: %s' % localPath)
        else:
            self.ixnObj.logInfo('\ncopyFileWindowsToLocalLinux Error: Failed to download file from IxNetwork API Server.')

    def copyFileWindowsToLocalLinux(self, windowsPathAndFileName, localPath, renameDestinationFile=None, includeTimestamp=False):
        """
        Description
            Copy files from the IxNetwork API Server c: drive to local Linux filesystem.
            The filename to be copied will remain the same filename unless you set renameDestinationFile to something you otherwise preferred.
            You could also include a timestamp for the destination file.

        Parameters
            windowsPathAndFileName: (str): The full path and filename to retrieve from Windows client.
            localPath: (str): The Linux destination path to put the file to.
            renameDestinationFile: (str): You could rename the destination file.
            includeTimestamp: (bool):  If False, each time you copy the same file will be overwritten.

        Syntax
            post: /api/v1/sessions/1/ixnetwork/operations/copyfile
            data: {'arg1': windowsPathAndFileName, 'arg2': '/api/v1/sessions/1/ixnetwork/files/'+fileName'}
        """
        import datetime

        self.ixnObj.logInfo('\ncopyFileWindowsToLocalLinux: From: %s to %s\n' % (windowsPathAndFileName, localPath))
        fileName = windowsPathAndFileName.split('\\')[-1]
        fileName = fileName.replace(' ', '_')
        destinationPath = '{0}/ixnetwork/files/'.format(self.ixnObj.headlessSessionId) + fileName
        currentTimestamp = datetime.datetime.now().strftime('%H%M%S')

        # Step 1 of 2:
        url = self.ixnObj.sessionUrl+'/operations/copyfile'
        response = self.ixnObj.post(url,
                             data={"arg1": windowsPathAndFileName, "arg2": destinationPath})

        # curl http://{apiServerIp:port}/api/v1/sessions/1/ixnetwork/files/AggregateResults.csv -O -H "Content-Type: application/octet-stream" -output /home/hgee/AggregateResults.csv

        # Step 2 of 2:
        #requestStatus = self.ixnObj.get(self.ixnObj.sessionUrl+'/files/%s' % (fileName), stream=True, ignoreError=True)
        url = self.ixnObj.sessionUrl+'/files?filename=%s' % (fileName)
        requestStatus = self.ixnObj.get(url, stream=True, ignoreError=True)
        if requestStatus.status_code == 200:
            if renameDestinationFile is not None:
                fileName = renameDestinationFile

            contents = requestStatus.raw.read()
            if includeTimestamp:
                tempFileName = fileName.split('.')
                if len(tempFileName) > 1:
                    extension = fileName.split('.')[-1]
                    fileName = tempFileName[0]+'_' + currentTimestamp + '.' + extension
                else:
                    fileName = tempFileName[0]+'_' + currentTimestamp

                localPath = localPath+'/'+fileName
            else:
                localPath = localPath+'/'+fileName

            with open(localPath, 'wb') as downloadedFileContents:
                downloadedFileContents.write(contents)

            self.ixnObj.logInfo('\nA copy of your saved file/report is in:\n\t%s' % (windowsPathAndFileName))
            self.ixnObj.logInfo('\ncopyFileWindowsToLocalLinux: %s' % localPath)
        else:
            self.ixnObj.logInfo('\ncopyFileWindowsToLocalLinux Error: Failed to download file from IxNetwork API Server.')

    def copyFileWindowsToLocalWindows(self, windowsPathAndFileName, localPath, renameDestinationFile=None, includeTimestamp=False):
        """
        Description
            Copy files from the Windows IxNetwork API Server to a local c: drive destination.
            The filename to be copied will remain the same filename unless you set renameDestinationFile to something you otherwise preferred.
            You could include a timestamp for the destination file.

        Parameters
            windowsPathAndFileName: (str): The full path and filename to retrieve from Windows client.
            localPath: (str): The Windows local filesystem. Ex: C:\\Results.
            renameDestinationFile: (str): You could name the destination file.
            includeTimestamp: (bool):  If False, each time you copy the same file will be overwritten.

        Example:
           WindowsPathAndFileName =  'C:\\Users\\hgee\\AppData\\Local\\Ixia\\IxNetwork\\data\\result\\DP.Rfc2544Tput\\9e1a1f04-fca5-42a8-b3f3-74e5d165e68c\\Run0001\\TestReport.pdf'
           localPath = 'C:\\Results'
        """
        import datetime

        self.ixnObj.logInfo('\ncopyFileWindowsToLocalWindows: From: %s to %s\n' % (windowsPathAndFileName, localPath))
        self.ixnObj.logInfo('\nYou need to manually remove the saved copy in: %s' % windowsPathAndFileName)
        fileName = windowsPathAndFileName.split('\\')[-1]
        if renameDestinationFile:
            fileName = renameDestinationFile

        fileName = fileName.replace(' ', '_')
        if includeTimestamp:
            currentTimestamp = datetime.datetime.now().strftime('%H%M%S')
            tempFileName = fileName.split('.')
            if len(tempFileName) > 1:
                extension = fileName.split('.')[-1]
                fileName = tempFileName[0]+'_' + currentTimestamp + '.' + extension
            else:
                fileName = tempFileName[0]+'_' + currentTimestamp

        destinationPath = localPath+'\\'+fileName
        response = self.ixnObj.post(self.ixnObj.sessionUrl+'/operations/copyfile',
                             data={"arg1": windowsPathAndFileName, "arg2": destinationPath})

    def copyFileLinuxToLocalLinux(self, linuxApiServerPathAndFileName, localPath, renameDestinationFile=None,
                                  includeTimestamp=False, linuxApiServerPathExtension=None):
        """
        Description
            Copy files from Linux API Server to local Linux filesystem.
            The filename to be copied will remain the same filename unless you set renameDestinationFile
            to something you otherwise preferred.

            You could also include a timestamp for the destination file.

        Parameters
            linuxApiServerPathAndFileName: (str): The full path and filename to retrieve.
            linuxApiServerPathExtension: (str): In a situation such as packet capture for Linux API server only, the 
                                                captured file is saved at 'captures/<temp folder>/file.
                                                Value example: 'captures/packetCaptureFolder/port2_HW.cap'
                                                
            localPath: (str): The Linux destination path to put the file to.
            renameDestinationFile: (str): You could rename the destination file.
            includeTimestamp: (bool):  If False, each time you copy the same file will be overwritten.

        Syntax
            post: /api/v1/sessions/1/ixnetwork/operations/copyfile
            data: {'arg1': '/root/.local/share/Ixia/sdmStreamManager/common/bgpExportedConfigFile',
                   'arg2': '/api/v1/sessions/1/ixnetwork/files/'+fileName'}
        """
        import datetime

        self.ixnObj.logInfo('\ncopyFileLinuxToLocalLinux: From: %s to %s\n' % (linuxApiServerPathAndFileName, localPath))

        fileName = linuxApiServerPathAndFileName.split('/')[-1]
        fileName = fileName.replace(' ', '_')
         
        destinationPath = self.ixnObj.sessionUrl.split(self.ixnObj.httpHeader)[1]
        destinationPath = destinationPath + '/files/' + fileName
        currentTimestamp = datetime.datetime.now().strftime('%H%M%S')

        # Step 1 of 3:
        url = self.ixnObj.sessionUrl+'/operations/copyfile'
        response = self.ixnObj.post(url, data={"arg1": linuxApiServerPathAndFileName, "arg2": destinationPath})

        # Step 2 of 3:
        if linuxApiServerPathExtension:
            # Situations like packet capturing puts the captured file in 'captures/<temp folder>/'
            fileName = linuxApiServerPathExtension

        response = self.ixnObj.get(self.ixnObj.sessionUrl+'/files?filename=%s' % (fileName), stream=True, ignoreError=True)

        if response.status_code == 200:
            if renameDestinationFile is not None:
                fileName = renameDestinationFile

            if linuxApiServerPathExtension:
                # This extension means that it has an extended path: captures/<temp folder>/fileToGet
                fileName = linuxApiServerPathExtension.split('/')[-1]

            contents = response.raw.read()

            if includeTimestamp:
                if linuxApiServerPathAndFileNameAsIs:
                    fileName = fileName.split('/')[-1]

                tempFileName = fileName.split('.')
                if len(tempFileName) > 1:
                    extension = fileName.split('.')[-1]
                    fileName = tempFileName[0]+'_' + currentTimestamp + '.' + extension
                else:
                    fileName = tempFileName[0]+'_' + currentTimestamp

                localPath = localPath+'/'+fileName
            else:
                localPath = localPath+'/'+fileName

            # Step 3 of 3:
            self.ixnObj.logInfo('\ncopyFileLinuxToLocalLinux: %s' % localPath)
            with open(localPath, 'wb') as downloadedFileContents:
                downloadedFileContents.write(contents)

            self.ixnObj.logInfo('\nA copy of your saved file/report is in:\n\t%s' % (linuxApiServerPathAndFileName))
        else:
            self.ixnObj.logInfo('\ncopyFileLinuxToLocalLinux Error: Failed to download file from Linux API Server.')

    def convertIxncfgToJson(self, ixncfgFile, destinationPath):
        """
        Description
            This function takes the input .ixncfg config file to be loaded and then convert it
            to json format. The filename will be the same as the input .ixncfg filename, but the
            extension will be .json.  The converted .json file will be saved in the path
            variable destinationPath.

        Parameters
            ixncfgFile: (str): The binary IxNetwork .ixncfg file.
            destinationPath: (str): The destination path to save the .json config file.
        """
        self.loadConfigFile(ixncfgFile)
        filename = ixncfgFile.split('/')[-1]
        match = re.match('(.*).ixncfg', filename)
        if  match:
            filename = match.group(1)

        jsonFilename = destinationPath+'/'+filename+'.json'
        self.exportJsonConfigFile(jsonFilename)

    def importJsonConfigObj(self, dataObj, option='modify', silentMode=False, timeout=90):
        """
        Description
            For newConfig:
                This is equivalent to loading a saved .ixncfg file.
                To use this API, your script should have read a JSON config into an object variable.
                Then pass in the json object to the data parameter.

            For modify:
                Import the modified JSON data object to make a configuration modification on the API server.
                Supports one xpath at a time.
                    Example: {"xpath": "/traffic/trafficItem[1]",
                              "enabled": True,
                              "name": "Topo-BGP"}

        Parameters
            data: (json object): The JSON config object.
            option: (str): newConfig|modify
            silentMode: (bool): If True, don't display REST API command on stdout.
            timeout: (int): The timeout value to declare as failed.

        Note
            arg2 value must be a string of JSON data: '{"xpath": "/traffic/trafficItem[1]", "enabled": false}'
        """
        if option is 'modify':
            arg3 = False

        if option is 'newConfig':
            arg3 = True

        dataReformatted = {"arg1": "{0}/ixnetwork/resourceManager".format(self.ixnObj.headlessSessionId),
                           "arg2": json.dumps(dataObj),
                           "arg3": arg3}

        url = self.ixnObj.sessionUrl+'/resourceManager/operations/importconfig'
        response = self.ixnObj.post(url, data=dataReformatted, silentMode=silentMode)
        response = self.ixnObj.waitForComplete(response, url+'/'+response.json()['id'], silentMode=False, timeout=timeout)
        if response.json()['result'] != []:
            if option == 'modify':
                errorFlag = 0
                for errorMsg in response.json()['result']:
                    self.ixnObj.logError('JSON Import: %s' % errorMsg, timestamp=False)
                    errorFlag = 1

                if errorFlag:
                    raise IxNetRestApiException('\nimportJsonConfigObj Error')
        else:
            self.ixnObj.logInfo('importJsonConfigObj: No error in JSON import')


    def importJsonConfigFile(self, jsonFileName, option='modify'):
        """
        Description
            To import a JSON config file to IxNetwork.
            You could state it to import as a modified config or creating a new config.

            The benefit of importing an actual JSON config file is so you could manually use
            IxNetwork Resource Manager to edit any part of the JSON config and add to the
            current configuration

        Parameters
            jsonFileName: (json object): The JSON config file. Could include absolute path also.
            option: (str): newConfig|modify
        """
        if option is 'modify':
            arg3 = False
        if option is 'newConfig':
            arg3 = True

        fileName = jsonFileName.split('/')[-1]
        uploadFile = self.ixnObj.sessionUrl+'/files?filename='+fileName

        if self.ixnObj.serverOs == 'linux':
            headers = {'content-type': 'application/octet-stream', 'x-api-key': self.ixnObj.apiKey}
        else:
            headers = {'content-type': 'application/octet-stream'}

        # 1> Upload the config file to the server and give it any name you want for the filename
        self.ixnObj.logInfo('Uploading file to server: %s' % uploadFile)
        with open(jsonFileName, mode='rb') as file:
            configContents = file.read()
            configContents = io.BytesIO(configContents)
            response = self.ixnObj.post(uploadFile, data=configContents, noDataJsonDumps=True,
                                        headers=headers, silentMode=False)

        # 2> Tell IxNetwork to import the JSON config file
        data = {"arg1": "{0}/ixnetwork/resourceManager".format(self.ixnObj.headlessSessionId),
                "arg2": "{0}/ixnetwork/files/{1}".format(self.ixnObj.headlessSessionId, fileName),
                "arg3": arg3}

        url = self.ixnObj.sessionUrl+'/resourceManager/operations/importconfigfile'
        response = self.ixnObj.post(url, data=data)
        self.ixnObj.waitForComplete(response, url+'/'+response.json()['id'], silentMode=False, timeout=300)

    def exportJsonConfigFile(self, jsonFileName, xpathList=None):
        """
        Description
            Export the current configuration to a JSON format config file and copy it to local filesystem.

        Parameters
            jsonFileName: (str): The JSON config file name to create. Could include absolute path also.

            xpathList:  <list> 
                        To get entire configuration = ['/descendant-or-self::*']
                        To get code fragments such as /vport = ['/vport/descendant-or-self::*']

        Requirements
            self.ixnObj.waitForComplete()
            self.copyFileLinuxToLocalLinux()
            self.copyFileWindowsToLocalLinux()
            self.jsonReadConfig()
            self.jsonWriteToFile()

        Syntax
            POST /api/v1/sessions/{id}/ixnetwork/resourceManager/operations/exportconfigfile
            DATA = {'arg1': '/api/v1/sessions/{id}/ixnetwork/resourceManager',
                    'arg2': ['/descendant-or-self::*'],
                    'arg3': True,
                    'arg4': 'json',
                    'arg5': '/api/v1/sessions/{id}/ixnetwork/files/'+fileName
                   }

        Example
            restObj.exportJsonConfigFile(jsonFileName='/path/exportedJsonConfig.json')
        
        """
        if xpathList == None:
            xpathList = ['/descendant-or-self::*']

        jsonFileNameTemp = jsonFileName.split('/')
        if jsonFileNameTemp[0] == '':
            jsonFileNameTemp.pop(0)

        if len(jsonFileNameTemp) > 1:
            destinationPath = '/'
            destinationPath = destinationPath + '/'.join(jsonFileNameTemp[:-1])
        else:
            destinationPath = os.getcwd()

        self.ixnObj.logInfo('Storing the exported file to: %s' % destinationPath)

        fileName = jsonFileNameTemp[-1]
        # sessionId example: /api/v1/sessions/{id}/ixnetwork
        sessionId = self.ixnObj.sessionUrl.split(self.ixnObj.httpHeader)[1]

        data = {'arg1': sessionId+"/resourceManager",
                'arg2': xpathList,
                'arg3': True,
                'arg4': 'json',
                'arg5': sessionId+'/files/'+fileName
        }

        url = self.ixnObj.sessionUrl+'/resourceManager/operations/exportconfigfile'
        response = self.ixnObj.post(url, data=data)
        self.ixnObj.waitForComplete(response, url+'/'+response.json()['id'], silentMode=False)

        response = self.ixnObj.get(self.ixnObj.sessionUrl+'/files')
        absolutePath = response.json()['absolute']

        if self.ixnObj.serverOs in ['windows', 'windowsConnectionMgr']:
            absolutePath = absolutePath.replace('\\', '\\\\')
            absolutePath = absolutePath + '\\\\'+fileName

        if self.ixnObj.serverOs == 'linux':
            absolutePath = absolutePath+'/'+fileName

        if self.ixnObj.serverOs in ['windows', 'windowsConnectionMgr']:
            self.copyFileWindowsToLocalLinux(windowsPathAndFileName=absolutePath,
                                             localPath=destinationPath,
                                             renameDestinationFile=None,
                                             includeTimestamp=False)

        if self.ixnObj.serverOs == 'linux':
            self.copyFileLinuxToLocalLinux(linuxApiServerPathAndFileName=absolutePath,
                                           localPath=destinationPath,
                                           renameDestinationFile=None,
                                           includeTimestamp=False)
            
        # Indent the serialized json config file
        jsonObj = self.jsonReadConfig(jsonFileName)
        self.jsonWriteToFile(jsonObj, jsonFileName)

    def exportJsonConfigToDict(self, xpathList=None):
        """
        Description
            Export the current configuration to a JSON config format and convert to a
            Python Dict.

        Parameter
            xpathList:  To get entire configuration = ['/descendant-or-self::*']
                        To get code fragments such as /vport = ['/vport/descendant-or-self::*']

        Return
            JSON config in a dictionary format.
        """
        if xpathList == None:
            xpathList = ['/descendant-or-self::*']
        
        data = {'arg1': self.ixnObj.apiSessionId+"/resourceManager",
                'arg2': xpathList,
                'arg3': True,
                'arg4': 'json'
        }
        url = self.ixnObj.sessionUrl+'/resourceManager/operations/exportconfig'
        response = self.ixnObj.post(url, data=data)
        response = self.ixnObj.waitForComplete(response, url+'/'+response.json()['id'], silentMode=False)
        return json.loads(response.json()['result'])

    def getJsonConfigPortList(self, jsonData):
        """
        Description
            Read an exported json data and create a list of all the vports from the json configuration.

        Parameter
            jsonData: (json object): The json data after calling: jsonData = jsonReadConfig(jsonConfigFile)
        """
        portList = []
        for vport in jsonData['vport']:
            # /availableHardware/chassis[@alias = '172.28.95.60']/card[1]/port[2]"
            connectedTo = vport['connectedTo']
            match = re.match("/availableHardware/.*'([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)']/card\[([0-9]+)]/port\[([0-9]+)", connectedTo)
            portList.append([match.group(1), match.group(2), match.group(3)])
        return portList

    def jsonReadConfig(self, jsonFile):
        """
        Description
           Read the input json file.
        
        Parameter
           jsonFile: (json object): The json file to read.
        """
        if os.path.isfile(jsonFile) == False:
            raise IxNetRestApiException("JSON param file doesn't exists: %s" % jsonFile)

        with open(jsonFile.strip()) as inFile:
            jsonData = json.load(inFile)
        return jsonData

    def jsonWriteToFile(self, dataObj, jsonFile, sortKeys=False):
        """
        Description
           Write data to a json file.
        
        Parameters
           dataObj: (json object): The json object containing the data.
           jsonFile (str): The the destination json file to write the json data.
           sortKeys: (bool): To sort the json object keys.
        """
        self.ixnObj.logInfo('jsonWriteToFile ...')
        with open(jsonFile, 'w') as outFile:
            json.dump(dataObj, outFile, sort_keys=sortKeys, indent=4)

    def jsonPrettyprint(self,data, sortKeys=False, **kwargs):
        """
        Description
           Display the JSON data in human readable format with indentations.
        """
        self.ixnObj.logInfo('\nimportJsonConfigObj pretty print:', timestamp=False)
        self.ixnObj.logInfo('\n\n{0}'.format(json.dumps(data, indent=4, sort_keys=sortKeys)), timestamp=False)

    def collectDiagnostics(self, diagZipFilename='ixiaDiagnostics.zip', localPath=None):
        """
        Description
           Collect diagnostics for debugging.
        
        Parameter
           diagZipFileName: <str>: The diagnostic filename to name with .zip extension.
           localPath: <str>: The local destination where you want to put the collected diag file.
        """
        if localPath is None:
            localPath = '.'

        url = self.ixnObj.sessionUrl+'/operations/collectlogs'
        data = {'arg1': self.ixnObj.headlessSessionId+'/'+diagZipFilename}
        response = self.ixnObj.post(url, data=data)
        self.ixnObj.waitForComplete(response, url+'/'+response.json()['id'], silentMode=False, timeout=900)
        response = self.ixnObj.get(self.ixnObj.sessionUrl+'/files')
        absolutePath = response.json()['absolute']

        if self.ixnObj.serverOs in ['windows', 'windowsConnectionMgr']:
            absolutePath = absolutePath.replace('/', '\\')
            self.copyFileWindowsToLocalLinux(windowsPathAndFileName=absolutePath+'\\'+diagZipFilename, localPath=localPath)

        if self.ixnObj.serverOs == 'linux':
            self.copyFileLinuxToLocalLinux(linuxApiServerPathAndFileName=absolutePath+'/'+diagZipFilename, localPath=localPath)

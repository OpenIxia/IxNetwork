import re, os, json
from IxNetRestApi import IxNetRestApiException

class FileMgmt(object):
    def __init__(self, ixnObj):
        self.ixnObj = ixnObj

    def loadConfigFile(self, configFile):
        """
        Description
            Load a saved config file from a Linux machine.

        Parameter
            configFile: The full path including the saved config filename.
        """
        if os.path.exists(configFile) is False:
            raise IxNetRestApiException("Config file doesn't exists: %s" % configFile)

        if self.ixnObj.apiServerPlatform == 'linux':
            octetStreamHeader = {'content-type': 'application/octet-stream', 'x-api-key': self.ixnObj.apiKey}
        else:
            octetStreamHeader = self.ixnObj.jsonHeader

        # 1> Read the config file
        self.ixnObj.logInfo('\nReading saved config file')
        with open(configFile, mode='rb') as file:
            configContents = file.read()

        fileName = configFile.split('/')[-1]

        # 2> Upload it to the server and give it any name you want for the filename
        uploadFile = self.ixnObj.sessionUrl+'/files?filename='+fileName
        self.ixnObj.logInfo('\nUploading file to server: %s' % uploadFile)
        response = self.ixnObj.post(uploadFile, data=configContents, noDataJsonDumps=True, headers=octetStreamHeader, silentMode=True)

        # 3> Set the payload to load the given filename:  /api/v1/sessions/1/ixnetwork/files/ospfNgpf_8.10.ixncfg
        payload = {'arg1': '/api/v1/sessions/1/ixnetwork/files/%s' % fileName}

        loadConfigUrl = self.ixnObj.sessionUrl+'/operations/loadconfig'

        # 4> Tell the server to load the config file
        response = self.ixnObj.post(loadConfigUrl, data=payload, headers=octetStreamHeader)
        if self.ixnObj.waitForComplete(response, loadConfigUrl+'/'+response.json()['id'], timeout=140) == 1:
            raise IxNetRestApiException

    def copyFileWindowsToRemoteWindows(self, windowsPathAndFileName, localPath, renameDestinationFile=None, includeTimestamp=False):
        """
        Description
            Copy files from the IxNetwork API Server c: drive to local Linux filesystem.
            The filename to be copied will remain the same filename unless you set renameDestinationFile to something you otherwise preferred.
            You could also include a timestamp for the destination file.

        Parameters
            windowsPathAndFileName: The full path and filename to retrieve from Windows API server.
            localPath: The remote Windows destination path to put the file to.
            renameDestinationFile: You could rename the destination file.
            includeTimestamp: True|False.  If False, each time you copy the same file will be overwritten.
        """
        import datetime

        self.ixnObj.logInfo('\ncopyFileWindowsToRemoteWindows: From: %s to %s\n' % (windowsPathAndFileName, localPath))
        windowsPathAndFileName = windowsPathAndFileName.replace('\\', '\\\\')
        fileName = windowsPathAndFileName.split('\\')[-1]
        fileName = fileName.replace(' ', '_')
        # Default location: "C:\\Users\\<user name>\\AppData\\Local\\sdmStreamManager\\common"
        destinationPath = '/api/v1/sessions/1/ixnetwork/files/'+fileName
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
            windowsPathAndFileName: The full path and filename to retrieve from Windows client.
            localPath: The Linux destination path to put the file to.
            renameDestinationFile: You could rename the destination file.
            includeTimestamp: True|False.  If False, each time you copy the same file will be overwritten.

        Syntax
            post: /api/v0/sessions/1/ixnetwork/operations/copyfile
            data: {'arg1': windowsPathAndFileName, 'arg2': '/api/v1/sessions/1/ixnetwork/files/'+fileName'}

            Note:
               To get the Windows path dynamically:

        """
        import datetime

        self.ixnObj.logInfo('\ncopyFileWindowsToLocalLinux: From: %s to %s\n' % (windowsPathAndFileName, localPath))
        fileName = windowsPathAndFileName.split('\\')[-1]
        fileName = fileName.replace(' ', '_')
        destinationPath = '/api/v1/sessions/1/ixnetwork/files/'+fileName
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

    def copyFileWindowsToLocalWindows(self, windowsPathAndFileName, localPath, renameDestinationFile=None, includeTimestamp=False):
        """
        Description
            Copy files from the Windows IxNetwork API Server to a local c: drive destination.
            The filename to be copied will remain the same filename unless you set renameDestinationFile to something you otherwise preferred.
            You could include a timestamp for the destination file.

        Parameters
            windowsPathAndFileName: The full path and filename to retrieve from Windows client.
            localPath: The Windows local filesystem. Ex: C:\\Results.
            renameDestinationFile: You could name the destination file.
            includeTimestamp: True|False.  If False, each time you copy the same file will be overwritten.

        Example:  WindowsPathAndFileName =  'C:\\Users\\hgee\\AppData\\Local\\Ixia\\IxNetwork\\data\\result\\DP.Rfc2544Tput\\9e1a1f04-fca5-42a8-b3f3-74e5d165e68c\\Run0001\\TestReport.pdf'
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

    def convertIxncfgToJson(self, ixncfgFile, destinationPath):
        """
        Description
            This function takes the input .ixncfg config file to be loaded and then convert it
            to json format. The filename will be the same as the input .ixncfg filename, but the
            extension will be .json.  The converted .json file will be saved in the path
            variable destinationPath.

        Parameter
            ixncfgFile: The binary IxNetwork .ixncfg file.
            destinationPath: The destination path to save the .json config file.
        """
        self.loadConfigFile(ixncfgFile)
        filename = ixncfgFile.split('/')[-1]
        match = re.match('(.*).ixncfg', filename)
        if  match:
            filename = match.group(1)

        jsonFilename = destinationPath+'/'+filename+'.json'
        self.exportJsonConfigFile(jsonFilename)

    def importJsonConfigObj(self, dataObj, type='modify'):
        """
        Description
            For newConfig:
                This is an equivalent to loading a saved .ixncfg file.
                To use this API, your script should have read a JSON config into an object variable.
                Then pass in the json object to the data parameter.

            For modify:
                Import the modified JSON data object to make a configuration modification on the API server.
                Supports one xpath at a time.
                    Example: {"xpath": "/traffic/trafficItem[1]",
                              "enabled": True,
                              "name": "Topo-BGP"}

        Parameter
            data: The JSON config object.
            type: newConfig|modify

        Note
            arg2 value must be a string of JSON data: '{"xpath": "/traffic/trafficItem[1]", "enabled": false}'
        """
        if type is 'modify':
            arg3 = False
            silentMode = False
        if type is 'newConfig':
            arg3 = True
            silentMode = True

        dataReformatted = {"arg1": "/api/v1/sessions/1/ixnetwork/resourceManager",
                           "arg2": json.dumps(dataObj),
                           "arg3": arg3}
        url = self.ixnObj.sessionUrl+'/resourceManager/operations/importconfig'
        response = self.ixnObj.post(url, data=dataReformatted, silentMode=silentMode)
        if self.ixnObj.waitForComplete(response, url+'/'+response.json()['id']) == 1:
            raise IxNetRestApiException

    def importJsonConfigFile(self, jsonFileName, type='modify'):
        """
        Description
            To import a JSON config file to IxNetwork.
            You could state it to import as a modified config or creating a new config.

            The benefit of importing an actual JSON config file is so you could manually use
            IxNetwork Resource Manager to edit any part of the JSON config and add to the
            current configuration

        Parameters
            jsonFileName: The JSON config file. Could include absolute path also.
            type: newConfig|modify
        """

        if type is 'modify':
            arg3 = False
        if type is 'newConfig':
            arg3 = True

        # 1> Read the config file
        self.ixnObj.logInfo('\nReading saved config file')
        with open(jsonFileName, mode='r') as file:
            configContents = file.read()

        fileName = jsonFileName.split('/')[-1]

        # 2> Upload it to the server and give it any name you want for the filename
        if self.ixnObj.apiServerPlatform == 'linux':
            octetStreamHeader = {'content-type': 'application/octet-stream', 'x-api-key': self.ixnObj.apiKey}
        else:
            octetStreamHeader = self.ixnObj.jsonHeader

        uploadFile = self.ixnObj.sessionUrl+'/files?filename='+fileName
        self.ixnObj.logInfo('\nUploading file to server:', uploadFile)
        response = self.ixnObj.post(uploadFile, data=configContents, noDataJsonDumps=True, headers=octetStreamHeader, silentMode=True)

        # 3> Tell IxNetwork to import the JSON config file
        data = {"arg1": "/api/v1/sessions/1/ixnetwork/resourceManager",
                "arg2": "/api/v1/sessions/1/ixnetwork/files/{0}".format(fileName),
                "arg3": arg3}
        url = self.ixnObj.sessionUrl+'/resourceManager/operations/importconfigfile'
        response = self.ixnObj.post(url, data=data)
        if self.ixnObj.waitForComplete(response, url+'/'+response.json()['id']) == 1:
            raise IxNetRestApiException

    def exportJsonConfigFile(self, jsonFileName):
        """
        Description
            Export the current configuration to a JSON format config file.

        Parameters
            jsonFileName: The JSON config file name to create. Could include absolute path also.

        Example
            restObj.exportJsonConfigFile(jsonFileName='/path/exportedJsonConfig.json')
        """
        jsonFileNameTemp = jsonFileName.split('/')
        if jsonFileNameTemp[0] == '':
            jsonFileNameTemp.pop(0)

        if len(jsonFileNameTemp) > 1:
            destinationPath = '/'
            destinationPath = destinationPath + '/'.join(jsonFileNameTemp[:-1])
        else:
            #localPath = '.'
            destinationPath = '.'

        fileName = jsonFileNameTemp[-1]
        data = {'arg1': "/api/v1/sessions/1/ixnetwork/resourceManager",
                'arg2': ['/descendant-or-self::*'],
                'arg3': True,
                'arg4': 'json',
                'arg5': '/api/v1/sessions/1/ixnetwork/files/'+fileName
        }
        url = self.ixnObj.sessionUrl+'/resourceManager/operations/exportconfigfile'
        response = self.ixnObj.post(url, data=data)
        if self.ixnObj.waitForComplete(response, url+'/'+response.json()['id']) == 1:
            raise IxNetRestApiException

        response = self.ixnObj.get(self.ixnObj.sessionUrl+'/files')
        absolutePath = response.json()['absolute']
        self.ixnObj.logInfo('Storing the exported file to: %s' % destinationPath)
        self.copyFileWindowsToLocalLinux(absolutePath.replace('\\', '\\\\')+'\\\\'+fileName,
                                        localPath=destinationPath,
                                        renameDestinationFile=None,
                                        includeTimestamp=False)

        # Indent the serialized json config file
        jsonObj = self.jsonReadConfig(jsonFileName)
        self.jsonWriteToFile(jsonObj, jsonFileName)

    def exportJsonConfigToDict(self):
        """
        Description
            Export the current configuration to a JSON config format and convert to a
            Python Dict.

        Return
            JSON config in a dictionary format.
        """
        data = {'arg1': "/api/v1/sessions/1/ixnetwork/resourceManager",
                'arg2': ['/descendant-or-self::*'],
                'arg3': True,
                'arg4': 'json'
        }
        url = self.ixnObj.sessionUrl+'/resourceManager/operations/exportconfig'
        response = self.ixnObj.post(url, data=data)
        if self.ixnObj.waitForComplete(response, url+'/'+response.json()['id']) == 1:
            raise IxNetRestApiException
        return json.loads(response.json()['result'])

    def getJsonConfigPortList(self, jsonData):
        """
        Description
            Read an exported json data and create a list of all the vports from the json configuration.

        Parameter
            jsonData: The json data after calling: jsonData = jsonReadConfig(jsonConfigFile)
        """
        portList = []
        for vport in jsonData['vport']:
            # /availableHardware/chassis[@alias = '172.28.95.60']/card[1]/port[2]"
            connectedTo = vport['connectedTo']
            match = re.match("/availableHardware/.*'([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)']/card\[([0-9]+)]/port\[([0-9]+)", connectedTo)
            portList.append([match.group(1), match.group(2), match.group(3)])
        return portList

    def jsonAssignPorts(self, jsonObject, portList):
        """
        Description
            Reassign ports.  Will remove the existing JSON config datas: availableHardware, cardId, portId.
            Then recreate JSON datas for availableHardware based on the portList input.

        Parameters
            jsonObject: The JSON config object.
            portList: Example:
                        portList = [[ixChassisIp, '1', '1'], [ixChassisIp, '2', '1']]
        """
        # Since it is reassigning ports, remove existing chassis's and add what users want.
        jsonObject.pop("availableHardware")
        jsonObject.update({"availableHardware": {
                            "xpath": "/availableHardware",
                            "chassis": []
                        }})

        ixChassisId = 1
        chassisIpList = []
        vportId = 1
        for ports in portList:
            ixChassisIp = ports[0]
            cardId = ports[1]
            portId = ports[2]
            if ixChassisIp not in chassisIpList:
                jsonObject["availableHardware"]["chassis"].insert(0, {"xpath": "/availableHardware/chassis[{0}]".format(ixChassisId),
                                                                        "hostname": ixChassisIp,
                                                                        "card": []
                                                                    })
            cardList = []
            if cardId not in cardList:
                # If card doesn't exist in list, create a new card.
                jsonObject["availableHardware"]["chassis"][0]["card"].insert(0, {"xpath": "/availableHardware/chassis[@alias = {0}/card[{1}]".format(ixChassisIp, cardId)})
                jsonObject["availableHardware"]["chassis"][0]["card"][0].update({"port": []})
                cardList.append(cardId)
            self.ixnObj.logInfo('\njsonAssignPorts: %s %s %s' % (ixChassisIp, cardId, portId))
            jsonObject["availableHardware"]["chassis"][0]["card"][0]["port"].insert(0, {"xpath": "/availableHardware/chassis[@alias = {0}/card[{1}]/port[{2}]".format(ixChassisIp, cardId, portId)})
            jsonObject["vport"][vportId-1].update({"connectedTo": "/availableHardware/chassis[@alias = {0}]/card[{1}]/port[{2}]".format(ixChassisIp, cardId, portId),
                                            "xpath": "/vport[{0}]".format(vportId)
                                          })
            vportId += 1
            ixChassisId += 1
        self.ixnObj.logInfo('\nImporting port mapping to IxNetwork')
        self.ixnObj.logInfo('Ports rebooting ...')
        self.importJsonConfigObj(dataObj=jsonObject, type='newConfig')

    def jsonReadConfig(self, jsonFile):
        #if os.path.exists(jsonFile) is False:
        #    raise IxNetRestApiException("JSON file doesn't exists: %s" % jsonFile)
        with open(jsonFile.strip()) as inFile:
            jsonData = json.load(inFile)
        return jsonData

    @staticmethod
    def jsonWriteToFile(dataObj, jsonFile, sortKeys=False):
        print('\njsonWriteToFile ...')
        with open(jsonFile, 'w') as outFile:
            json.dump(dataObj, outFile, sort_keys=sortKeys, indent=4)

    @staticmethod
    def jsonPrettyprint(data, sortKeys=False):
        print('\n', json.dumps(data, indent=4, sort_keys=sortKeys))

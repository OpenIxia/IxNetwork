import re
import os
import json
import time

from IxNetRestApi import IxNetRestApiException
from ixnetwork_restpy.files import Files
import datetime


class FileMgmt(object):
    def __init__(self, ixnObj=None):
        """
        Description
           Initialize default attributes.

        Parameter
           ixnObj: (Object): The parent object.
        """
        self.ixnObj = ixnObj
        self.ixNetwork = ixnObj.ixNetwork

    def setMainObject(self, mainObject):
        """
        Description
           For Robot support only. Setting the parent object.

        Parameter
           mainObject: (Object): The parent object.
        """
        self.ixnObj = mainObject

    def loadConfigFile(self, configFile, localFile=True, portList=None):
        """
        Description
            Load a saved config file.

        Parameters
            configFile: (str): The full path including the saved config filename.
                               If the config file is in a Windows filesystem, the format is
                               c:\\path\\bgp.ixncfg
                               If you are executing the script from Linux and the config file is in
                               local Linux filesystem, the format is /path/bgp.ixncfg and
                               localFile=True.

            localFile: (bool): For Windows API server and Connection Mgr running on a Windows
            server only. Set to False if the config file is in the Windows API server filesystem.
        """

        self.ixnObj.logInfo("Loading Config File {}".format(configFile))
        try:
            self.ixNetwork.LoadConfig(Files(configFile, local_file=localFile))
            if portList is not None:
                vportList = self.ixNetwork.Vport.find()
                chassisIp = portList[0][0]
                connectedChassis = self.ixNetwork.AvailableHardware.Chassis.find()
                if chassisIp != connectedChassis.Hostname:
                    self.ixNetwork.AvailableHardware.Chassis.find().remove()
                    self.ixNetwork.AvailableHardware.Chassis.add(Hostname=chassisIp)
                for port, vport in zip(portList, vportList):
                    vport.update(Location=';'.join(port))

        except Exception as err:
            self.ixnObj.logInfo("Error with Load config {}".format(err))
            raise Exception("Failed to load config file {} ".format(configFile))

    def copyFileWindowsToRemoteWindows(self, windowsPathAndFileName, localPath,
                                       renameDestinationFile=None, includeTimestamp=False):
        """
        Description
            Copy files from the IxNetwork API Server c: drive to local Linux filesystem.
            The filename to be copied will remain the same filename unless you  set
            renameDestinationFile to something you otherwise preferred. You could also include a
            timestamp for the destination file.

        Parameters
            windowsPathAndFileName: (str): The full path and filename to retrieve from Windows API
            server.
            localPath: (str): The remote Windows destination path to put the file to.
            renameDestinationFile: (str): You could rename the destination file.
            includeTimestamp: (bool):  If False, each time you copy the same file will be
            overwritten.
        """
        self.ixnObj.logInfo('\n copyFileWindowsToRemoteWindows: From: %s to %s\n' %
                            (windowsPathAndFileName, localPath))
        fileName = windowsPathAndFileName.split('\\')[-1]
        fileName = fileName.replace(' ', '_')

        if renameDestinationFile:
            fileName = renameDestinationFile

        if includeTimestamp:
            fileName = self._addTimestampToFile(fileName)

        destinationPath = localPath + '\\' + fileName

        try:
            self.ixNetwork.CopyFile(windowsPathAndFileName, destinationPath)
        except Exception as err:
            self.ixnObj.logInfo("Error with file transfer {}".format(err))
            raise Exception("Copy File from {} to {} Failed".format(windowsPathAndFileName,
                                                                    destinationPath))

    def copyFileWindowsToLocalLinux(self, windowsPathAndFileName, localPath,
                                    renameDestinationFile=None, includeTimestamp=False):
        """
        Description
            Copy files from the IxNetwork API Server c: drive to local Linux filesystem.
            The filename to be copied will remain the same filename unless you set
            renameDestinationFile to something you otherwise preferred. You could also include a
            timestamp for the destination file.

        Parameters
            windowsPathAndFileName: (str): The full path and filename to retrieve from Windows
            client.
            localPath: (str): The Linux destination path to put the file to.
            renameDestinationFile: (str): You could rename the destination file.
            includeTimestamp: (bool): If False, each time you copy the same file will be
                                       overwritten.
        """

        self.ixnObj.logInfo('\n copyFileWindowsToLocalLinux: From: %s to %s\n' %
                            (windowsPathAndFileName, localPath))
        fileName = windowsPathAndFileName.split('\\')[-1]
        fileName = fileName.replace(' ', '_')

        if renameDestinationFile:
            fileName = renameDestinationFile

        if includeTimestamp:
            fileName = self._addTimestampToFile(fileName)

        destinationPath = localPath + '/' + fileName

        try:
            self.ixNetwork.CopyFile(windowsPathAndFileName, destinationPath)
        except Exception as err:
            self.ixnObj.logInfo("Error with file transfer {}".format(err))
            raise Exception("\n copyFileWindowsToLocalLinux Error: Failed to download file from "
                            "IxNetwork API Server ")

    def copyFileWindowsToLocalWindows(self, windowsPathAndFileName, localPath,
                                      renameDestinationFile=None, includeTimestamp=False):
        """
        Description
            Copy files from the Windows IxNetwork API Server to a local c: drive destination.
            The filename to be copied will remain the same filename unless you set
            renameDestinationFile to something you otherwise preferred. You could include a
            timestamp for the destination file.

        Parameters
            windowsPathAndFileName: (str): The full path and filename to retrieve from Windows
                                          client.
            localPath: (str): The Windows local filesystem. Ex: C:\\Results.
            renameDestinationFile: (str): You could name the destination file.
            includeTimestamp: (bool):  If False, each time you copy the same file will be
                                       overwritten.

        Example:
           WindowsPathAndFileName =  'C:\\Users\\hgee\\AppData\\Local\\Ixia\\IxNetwork\\data\\result
                    \\DP.Rfc2544Tput\\9e1a1f04-fca5-42a8-b3f3-74e5d165e68c\\Run0001\\TestReport.pdf'
           localPath = 'C:\\Results'
        """
        self.ixnObj.logInfo('\n copyFileWindowsToLocalWindows: From: %s to %s\n\n' %
                            (windowsPathAndFileName, localPath))
        fileName = windowsPathAndFileName.split('\\')[-1]
        fileName = fileName.replace(' ', '_')
        if renameDestinationFile:
            fileName = renameDestinationFile

        if includeTimestamp:
            fileName = self._addTimestampToFile(fileName)

        destinationPath = localPath + '\\' + fileName
        self.ixnObj.logInfo('Copying from {} -> {}'.format(windowsPathAndFileName, destinationPath))
        self.ixNetwork.CopyFile(windowsPathAndFileName, destinationPath)

    def _addTimestampToFile(self, filename):
        """
        Function used internally by API rfc2544_quicktest

        :param filename: filename for which timestamp to be added
        """
        currentTimestamp = datetime.datetime.now().strftime('%H%M%S')
        if '\\' in filename:
            filename = filename.split('\\')[-1]

        if '/' in filename:
            filename = filename.split('/')[-1]

        newFilename = filename.split('.')[0]
        newFileExtension = filename.split('.')[1]
        newFileWithTimestamp = '{}_{}.{}'.format(newFilename, currentTimestamp, newFileExtension)
        return newFileWithTimestamp

    def copyFileLinuxToLocalLinux(self, linuxApiServerPathAndFileName, localPath,
                                  renameDestinationFile=None, includeTimestamp=False,
                                  linuxApiServerPathExtension=None):
        """
        Description
            Copy files from Linux API Server to local Linux filesystem. The filename to be copied
            will remain the same filename unless you set renameDestinationFile to something you
            otherwise preferred.
            You could also include a timestamp for the destination file.

        Parameters
            linuxApiServerPathAndFileName: (str): The full path and filename to retrieve.
            linuxApiServerPathExtension: (str): Not using in Resrpy
            localPath: (str): The Linux destination path to put the file to.
            renameDestinationFile: (str): You could rename the destination file.
            includeTimestamp: (bool):  If False, each time you copy the same file will be
            overwritten.
        """

        self.ixnObj.logInfo('\n copyFileLinuxToLocalLinux: From: %s to %s\n' %
                            (linuxApiServerPathAndFileName, localPath))

        fileName = linuxApiServerPathAndFileName.split('/')[-1]
        fileName = fileName.replace(' ', '_')

        if renameDestinationFile:
            fileName = renameDestinationFile

        if includeTimestamp:
            fileName = self._addTimestampToFile(fileName)

        destinationPath = localPath + '/' + fileName

        try:
            self.ixNetwork.CopyFile(linuxApiServerPathAndFileName, destinationPath)
        except Exception as err:
            self.ixnObj.logInfo("Error with file transfer {}".format(err))
            raise Exception("\n copyFileLinuxToLocalLinux Error: Failed to download file from "
                            "IxNetwork API Server ")

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
        self.ixnObj.logInfo("convertIxncfgToJson")
        self.loadConfigFile(ixncfgFile)
        filename = re.findall(r'[^\/|\\]+(?=\.)', ixncfgFile)[0]

        if self.ixnObj.serverOs in ['windows', 'windowsConnectionMgr']:
            jsonFilename = destinationPath + '\\' + filename + '.json'
            destinationPath = jsonFilename.replace('\\', '\\\\')

        if self.ixnObj.serverOs == 'linux':
            destinationPath = destinationPath+'/'+filename + '.json'

        self.exportJsonConfigFile(destinationPath)

    def importJsonConfigObj(self, dataObj, option='modify', silentMode=False, timeout=90):
        """
        Description
            For newConfig:
                This is equivalent to loading a saved .ixncfg file.
                To use this API, your script should have read a JSON config into an object variable.
                Then pass in the json object to the data parameter.

            For modify:
                Import the modified JSON data object to make a configuration modification
                 on the API server.
                Supports one xpath at a time.
                    Example: {"xpath": "/traffic/trafficItem[1]",
                              "enabled": True,
                              "name": "Topo-BGP"}

        Parameters
            data: (json object): The JSON config object.
            option: (str): newConfig|modify
            silentMode: (bool): Not required in Restpy
            timeout: (int): Not required in Restpy

        Note
            arg2 value must be a string of JSON data: '{"xpath": "/traffic/trafficItem[1]",
                                                        "enabled": false}'
        """
        if option == 'modify':
            arg3 = False

        if option == 'newConfig':
            arg3 = True

        try:
            self.ixNetwork.ResourceManager.ImportConfig(Arg2=json.dumps(dataObj), Arg3=arg3)
        except Exception as e:
            print(e)
            raise Exception('\nimportJsonConfigObj Error')

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
        if option == 'modify':
            arg3 = False
        if option == 'newConfig':
            arg3 = True

        try:
            self.ixNetwork.ResourceManager.ImportConfigFile(Arg2=Files(jsonFileName), Arg3=arg3)
        except Exception as err:
            self.ixnObj.logInfo("Error with importJsonConfig {}".format(err))
            raise Exception('\nimportJsonConfigObj Error')

    def exportJsonConfigFile(self, jsonFileName, xpathList=None):
        """
        Description
            Export the current configuration to a JSON format config file and copy it to local
            filesystem.

        Parameters
            jsonFileName: (str): The JSON config file name to create. Could include absolute path
            also.

            xpathList:  <list>
                        To get entire configuration = ['/descendant-or-self::*']
                        To get code fragments such as /vport = ['/vport/descendant-or-self::*']

        Requirements
            self.ixnObj.waitForComplete()
            self.copyFileLinuxToLocalLinux()
            self.copyFileWindowsToLocalLinux()
            self.jsonReadConfig()
            self.jsonWriteToFile()

        Example
            restObj.exportJsonConfigFile(jsonFileName='/path/exportedJsonConfig.json')

        """
        if xpathList is None:
            xpathList = ['/descendant-or-self::*']

        self.ixnObj.logInfo('Storing the exported file to: %s' % jsonFileName)

        try:
            ret = self.ixNetwork.ResourceManager.ExportConfig(Arg2=xpathList, Arg3=True,
                                                              Arg4='json')
            convStrToDict = json.loads(ret)
            with open(jsonFileName, 'w') as fp:
                json.dump(convStrToDict, fp)
        except Exception as err:
            raise Exception("Failed Exporting Configuration {}".format(err))

        # Indent the serialized json config file
        jsonObj = self.jsonReadConfig(jsonFileName)
        self.jsonWriteToFile(jsonObj, jsonFileName)

    def exportJsonConfigToDict(self, xpathList=None):
        """
        Description
            Export the current configuration to a JSON config format and convert to a Python Dict.

        Parameter
            xpathList:  To get entire configuration = ['/descendant-or-self::*']
                        To get code fragments such as /vport = ['/vport/descendant-or-self::*']

        Return
            JSON config in a dictionary format.
        """
        if xpathList is None:
            xpathList = ['/descendant-or-self::*']
        try:
            ret = self.ixNetwork.ResourceManager.ExportConfig(Arg2=xpathList, Arg3=True,
                                                              Arg4='json')
            return json.loads(ret)
        except Exception as err:
            raise Exception("Failed Exporting Configuration {}".format(err))

    def getJsonConfigPortList(self, jsonData):
        """
        Description
            Read an exported json data and create a list of all the vports from the json
            configuration.

        Parameter
            jsonData: (json object): The json data after calling: jsonData = jsonReadConfig(
            jsonConfigFile)
        """
        portList = []
        for vport in jsonData['vport']:
            # /availableHardware/chassis[@alias = '172.28.95.60']/card[1]/port[2]"
            connectedTo = vport['connectedTo']
            match = re.match(
                "/availableHardware/.*'([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)']/card\[([0-9]+)]/port\[([0-9]+)",
                connectedTo)
            portList.append([match.group(1), match.group(2), match.group(3)])
        return portList

    def jsonReadConfig(self, jsonFile):
        """
        Description
           Read the input json file.

        Parameter
           jsonFile: (json object): The json file to read.
        """
        if not os.path.isfile(jsonFile):
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

    def jsonPrettyprint(self, data, sortKeys=False, **kwargs):
        """
        Description
           Display the JSON data in human readable format with indentations.
        """
        self.ixnObj.logInfo('\nimportJsonConfigObj pretty print:', timestamp=False)
        self.ixnObj.logInfo('\n\n{0}'.format(json.dumps(data, indent=4, sort_keys=sortKeys)),
                            timestamp=False)

    def collectDiagnostics(self, diagZipFilename='ixiaDiagnostics.zip', localPath=None):
        """
        Description
           Collect diagnostics for debugging.

        Parameter
           diagZipFileName: <str>: The diagnostic filename to name with .zip extension.
           localPath: <str>: The local destination where you want to put the collected diag file.
        """

        try:
            self.ixNetwork.CollectLogs(Arg1=Files(diagZipFilename, local_file=True))
        except Exception as err:
            raise Exception("Failed Creating Diag logs {}".format(err))

        if localPath:
            try:
                self.ixNetwork.CopyFile(Files(diagZipFilename, local_file=True),
                                        localPath + "\\" + diagZipFilename)
            except Exception as e:
                print(e)
                self.ixNetwork.CopyFile(Files(diagZipFilename, local_file=True),
                                        localPath + "/" + diagZipFilename)

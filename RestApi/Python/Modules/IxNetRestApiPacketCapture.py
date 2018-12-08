import sys, re 
from IxNetRestApiFileMgmt import FileMgmt
from IxNetRestApiPortMgmt import PortMgmt
from IxNetRestApi import IxNetRestApiException

class PacketCapture(object):
    """
    ixnObj: The main connection object
    portObj: The port object

    """
    def __init__(self, ixnObj=None, portMgmtObj=None):
        """
        Parameters
            ixnObj: The main ixnObj object
            portMgmtObj: (Optional):  The PortMgmt object.
                         If you already have the portMgmt object, then pass it in. 
                         Otherwise, leave portMgmtObj=None

        Example:
            trafficObj = Traffic(mainObj)
            portMgmtObj = PortMgmt(mainObj)
            captureObj = PacketCapture(mainObj, portMgmtObj)
            captureObj.packetCaptureConfigPortMode(port=[ixChassisIp, '2', '1'], enableControlPlane=False, enableDataPlane=True)
            trafficObj.startTraffic()  <-- Make sure traffic is running in continuous mode
            captureObj.packetCaptureStart()
            time.sleep(10)
            captureObj.packetCaptureStop()
            trafficObj.stopTraffic()

            pktCaptureObj.getCapFile(port=[ixChassisIp, '2', '1'], typeOfCapture='data', saveToTempLocation='c:\\Results',
                                     localLinuxLocation='.', appendToSavedCapturedFile=None)

            pktCaptureObj.packetCaptureGetCurrentPackets(getUpToPacketNumber=5, capturePacketsToFile=True,
                                                         getSavedCapturedDotCapFile=True)

            captureObj.packetCaptureClearTabs()
        """
        self.ixnObj = ixnObj
        if portMgmtObj:
            self.portMgmtObj = portMgmtObj
        else:
            self.portMgmtObj = PortMgmt(ixnObj)

        self.enableControlPlane = False
        self.enableDataPlane = False

    def setMainObject(self, mainObject):
        # For Python Robot Framework support
        self.ixnObj = mainObject
        self.portMgmtObj.setMainObject(mainObject)

    def packetCaptureConfigPortMode(self, port, portRxMode='capture', enableControlPlane=True, enableDataPlane=True):
        """
        Description
           Enable|Disable port capturing for control plane and data plane.

           Values are true or false
              -softwareEnabled == Control Plane
              -hardwareEnabled == Data Plane

        Parameters
            port: <list>:  [ixChassisIp, '1', '3'] => [ixChasssisIp, str(cardNumber), str(portNumber)]
            portRxMode: <str>: capture|captureAndMeasure
            enableControlPlane: <bool>
            enableDataPlane: <bool>
        """
        if enableControlPlane == True:
            self.enableControlPlane = True
        if enableDataPlane == True:
            self.enableDataPlane = True

        self.captureRxPort = port
        vport = self.portMgmtObj.getVports([port])[0]
        self.ixnObj.patch(self.ixnObj.httpHeader+vport, data={'rxMode': portRxMode})
        self.ixnObj.patch(self.ixnObj.httpHeader+vport+'/capture', data={'softwareEnabled': enableControlPlane,
                                                                         'hardwareEnabled': enableDataPlane})

    def packetCaptureStart(self):
        """
        Start packet capturing
        """
        response = self.ixnObj.post(self.ixnObj.sessionUrl+'/operations/startcapture')
        self.ixnObj.waitForComplete(response, self.ixnObj.sessionUrl+'/operations/startcapture/'+response.json()['id'])

    def packetCaptureStop(self):
        """
        Stop packet capturing
        """
        response = self.ixnObj.post(self.ixnObj.sessionUrl+'/operations/stopcapture')
        self.ixnObj.waitForComplete(response, self.ixnObj.sessionUrl+'/operations/stopcapture/'+response.json()['id'])

    def packetCaptureClearTabs(self):
        """
        Remove all captured tabs on Windows IxNetwork GUI
        """
        response = self.ixnObj.post(self.ixnObj.sessionUrl+'/operations/closeAllTabs')
        self.ixnObj.waitForComplete(response, self.ixnObj.sessionUrl+'/operations/closeAllTabs/'+response.json()['id'])

    def packetCaptureGetCurrentPackets(self, getUpToPacketNumber=20, capturePacketsToFile=True):
        """
        Description
           Packet Capturing in wireshark style details. By default, it saved 7209 packet counts.
           It takes a long time to save all the packet header details into a file. 
           This API will default saving 20 packet counts. You could increase the packet count.

        Parameters
            getUpToPacketNumber: None|The last packet number to get. 
                                 Always starts at 1. If you state 10, then this function will get 1-10 packets.
            capturePacketsToFile: True|False
        """
        import subprocess, time

        if capturePacketsToFile:
            timestamp = int(time.time())
            if self.enableDataPlane:
                packetCaptureFilenameData = 'packetCaptureForData_'+str(timestamp)
                subprocess.call(['touch', packetCaptureFilenameData])

            if self.enableControlPlane:
                packetCaptureFilenameControl = 'packetCaptureForControl_'+str(timestamp)
                subprocess.call(['touch', packetCaptureFilenameControl])

            if self.enableDataPlane == False and self.enableControlPlane == False:
                raise IxNetRestApiException('\nPacketCapture Error: You must enable one of the options: enableDataPlane|enableControlPlane')
        
        vport = self.portMgmtObj.getVports([self.captureRxPort])[0]
        response = self.ixnObj.get(self.ixnObj.httpHeader+vport+'/capture')
        totalDataCapturedPackets = response.json()['dataPacketCounter']
        totalControlCapturedPackets = response.json()['controlPacketCounter']

        if type(totalDataCapturedPackets) != int:
            totalDataCapturedPackets = 0
        else:
            if getUpToPacketNumber != None:
                totalDataCapturedPackets = getUpToPacketNumber

        if type(totalControlCapturedPackets) != int:
            totalControlCapturedPackets = 0
        else:
            if getUpToPacketNumber != None:
                totalControlCapturedPackets = getUpToPacketNumber

        for eachTypeOfCaptures, totalCapturedPackets in zip(('data', 'control'), (totalDataCapturedPackets, totalControlCapturedPackets)):
            self.ixnObj.logInfo('Getting captured packets for capture type: {0}'.format(eachTypeOfCaptures))

            if capturePacketsToFile and int(totalCapturedPackets) != 0:
                timestamp = int(time.time())
                if self.enableDataPlane:
                    packetCaptureFilenameData = 'packetCaptureForData_'+str(timestamp)
                    subprocess.call(['touch', packetCaptureFilenameData])

                if self.enableControlPlane:
                    packetCaptureFilenameControl = 'packetCaptureForControl_'+str(timestamp)
                    subprocess.call(['touch', packetCaptureFilenameControl])

            for packetIndex in range(1, int(totalCapturedPackets)):
                self.ixnObj.logInfo('Getting captured packet index number: {}/{}'.format(packetIndex, getUpToPacketNumber))

                if self.enableDataPlane and eachTypeOfCaptures == 'data':
                    data = {'arg1': vport+'/capture/currentPacket', 'arg2': packetIndex}
                    response = self.ixnObj.post(self.ixnObj.sessionUrl+'/vport/capture/currentPacket/operations/getpacketfromdatacapture',
                                                data=data, silentMode=False)
                    self.ixnObj.waitForComplete(response, self.ixnObj.sessionUrl+'/vport/capture/currentPacket/operations/getpacketfromdatacapture/'+response.json()['id'])

                if self.enableControlPlane and eachTypeOfCaptures == 'control':
                    data = {'arg1': vport+'/capture/currentPacket', 'arg2': packetIndex}
                    response = self.ixnObj.post(self.ixnObj.sessionUrl+'/vport/capture/currentPacket/operations/getpacketfromcontrolcapture',
                                                data=data, silentMode=False)

                    self.ixnObj.waitForComplete(response, self.ixnObj.sessionUrl+'/vport/capture/currentPacket/operations/getpacketfromcontrolcapture/'+response.json()['id'])

                response = self.ixnObj.get(self.ixnObj.httpHeader+vport+'/capture/currentPacket/stack', silentMode=False)

                for eachStack in response.json():
                    displayName = eachStack['displayName']
                    stackIdObject = eachStack['links'][0]['href']
                    self.ixnObj.logInfo('\nStack: %s' % displayName)
                    if capturePacketsToFile:
                        if eachTypeOfCaptures == 'data':
                            with open(packetCaptureFilenameData, 'a') as packetCaptureFile:
                                packetCaptureFile.write('\nStack: %s\n' % displayName)

                        if eachTypeOfCaptures == 'control':
                            with open(packetCaptureFilenameControl, 'a') as packetCaptureFile:
                                packetCaptureFile.write('\nStack: %s\n' % displayName)

                    response = self.ixnObj.get(self.ixnObj.httpHeader+stackIdObject+'/field', silentMode=False)
                    for eachField in response.json():
                        fieldId = eachField['id']
                        fieldName = eachField['displayName']
                        fieldValue = eachField['fieldValue']
                        self.ixnObj.logInfo('\t{0}: {1}: {2}'.format(fieldId, fieldName, fieldValue))

                        if capturePacketsToFile:
                            if eachTypeOfCaptures == 'data':
                                with open(packetCaptureFilenameData, 'a') as packetCaptureFile:
                                    packetCaptureFile.write('\t{0}: {1}: {2}\n'.format(fieldId, fieldName, fieldValue))

                            if eachTypeOfCaptures == 'control':
                                with open(packetCaptureFilenameControl, 'a') as packetCaptureFile:
                                    packetCaptureFile.write('\t{0}: {1}: {2}\n'.format(fieldId, fieldName, fieldValue))

    def getCapFile(self, port, typeOfCapture='data', saveToTempLocation='c:\\Temp', localLinuxLocation='.', appendToSavedCapturedFile=None):
        """
        Get the latest captured .cap file from ReST API server to local Linux drive.

        Parameters
            port: Format:[IxiaIpAddress, slotNumber, cardNumber]
                  Example: [ixChassisIp, '2', '1']

            typeOfCapture: data|control

            saveToTempLocation: For Windows:
                                    Where to temporary save the .cap file on the ReST API server: 
                                    Provide any path with double backslashes: C:\\Temp.
                                    The folder will be created if it doesn't exists.

                                For Linux, value= 'linux'.
 
            localLinuxLocation: Where to save the .cap file on the local Linux machine.

            appendToSavedCapturedFile: Add a text string to the captured file.

        Example:
            captureObj.getCapFile([ixChassisIp, '2', '1'], 'control', 'c:\\Temp', '/home/hgee/test')

        Syntaxes:
               PATCH: /vport/2
               DATA: {'rxMode': 'captureAndMeasure'}

               PATCH: /vport/2/capture
               DATA: {'softwareEnabled': False, 'hardwareEnabled': True}
 
               # Set traffic item to send continuous packets
               PATCH: /traffic/trafficItem/1/configElement/<id>/transmissionControl
               DATA: {'type': 'continuous'}

               POST: /traffic/trafficItem/operations/generate
               DATA: {"arg1": ["/api/v1/sessions/<id>/ixnetwork/traffic/trafficItem/1"]}

               POST: /traffic/operations/apply
               DATA: {"arg1": "/api/v1/sessions/<id>/ixnetwork/traffic"}

               POST: /traffic/operations/start
               DATA: {"arg1": "https://192.168.70.12/api/v1/sessions/<id>/ixnetwork/traffic"}

               Start continuous traffic

               POST: /ixnetwork/operations/startcapture
               POST: /ixnetwork/operations/stopcapture
               POST: /ixnetwork/operations/savecapturefiles
               DATA: {"arg1": "packetCaptureFolder"}  <-- This could be any name.  Just a temporary folder to store the captured file.

               Wait for the /operations/savecapturefiles/<id> to complete.  May take up to a minute or more.

               For Windows API server:
                  POST: /ixnetwork/operations/copyfile
                  DATA: {"arg1": "c:\\Results\\port2_HW.cap", "arg2": "/api/v1/sessions/1/ixnetwork/files/port2_HW.cap"}
                  GET: /ixnetwork/files?filename=port2_HW.cap

               For Linux API server:
                  POST: /ixnetwork/operations/copyfile
                  DATA: {"arg1": "captures/packetCaptureFolder/port2_HW.cap", "arg2": "/api/v1/sessions/<id>/ixnetwork/files/port2_HW.cap"}
                  GET: /ixnetwork/files?filename=captures/packetCaptureFolder/port2_HW.cap
        """
        
        # For Linux API server
        if '\\' not in saveToTempLocation:
            # For Linux API server, need to give a name for a temporary folder
            saveToTempLocation = 'packetCaptureFolder'

            # For Linux API server, must get the vport name and cannot modify the vport name.
            vport = self.portMgmtObj.getVports([port])[0]
            response = self.ixnObj.get(self.ixnObj.httpHeader + vport)
            vportName = response.json()['name']

            vportName = vportName.replace('/', '_')
            vportName = vportName.replace(' ', '_')
            self.ixnObj.logInfo('vportName: {}'.format(vportName))

        if appendToSavedCapturedFile != None:
            data = {'arg1': saveToTempLocation, 'arg2': appendToSavedCapturedFile}
        else:
            data = {'arg1': saveToTempLocation}

        response = self.ixnObj.post(self.ixnObj.sessionUrl+'/operations/savecapturefiles', data=data)
        self.ixnObj.waitForComplete(response, self.ixnObj.httpHeader+ response.json()['url'], timeout=300)

        if typeOfCapture == 'control':
            if '\\' not in saveToTempLocation:
                # For Linux
                capFileToGet = '/home/ixia_apps/web/platform/apps-resources/ixnetworkweb/configs/captures/{0}/{1}_SW.cap'.format(
                    saveToTempLocation, vportName)
            else:
                # For Windows
                capFileToGet = saveToTempLocation+'\\'+port[1]+'-'+port[2]+'_SW.cap'

        if typeOfCapture == 'data':
            if '\\' not in saveToTempLocation:
                # For Linux
                capFileToGet = '/home/ixia_apps/web/platform/apps-resources/ixnetworkweb/configs/captures/{0}/{1}_HW.cap'.format(
                    saveToTempLocation, vportName)
            else:
                capFileToGet = saveToTempLocation+'\\'+port[1]+'-'+port[2]+'_HW.cap'

        fileMgmtObj = FileMgmt(self.ixnObj)

        if self.ixnObj.serverOs in ['windows', 'windowsConnectionMgr']:
            fileMgmtObj.copyFileWindowsToLocalLinux(windowsPathAndFileName=capFileToGet, localPath=localLinuxLocation,
                                                    renameDestinationFile=None)
        if self.ixnObj.serverOs == 'linux':
            # Parse out captures/packetCaptureFolder/<vportName>_HW.cap
            match = re.search('.*(captures.*)', capFileToGet)
            pathExtension = match.group(1)

            fileMgmtObj.copyFileLinuxToLocalLinux(linuxApiServerPathAndFileName=capFileToGet, localPath=localLinuxLocation,
                                                  renameDestinationFile=None, linuxApiServerPathExtension=pathExtension)
            

import sys
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
        self.ixnObj.post(self.ixnObj.sessionUrl+'/operations/startcapture')

    def packetCaptureStop(self):
        """
        Stop packet capturing
        """
        self.ixnObj.post(self.ixnObj.sessionUrl+'/operations/stopcapture')

    def packetCaptureClearTabs(self):
        """
        Remove all captured tabs on Windows IxNetwork GUI
        """
        self.ixnObj.post(self.ixnObj.sessionUrl+'/operations/closeAllTabs')

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
            self.ixnObj.logInfo('Getting captured packets for: %s totalCapturedPackets:%s' % (eachTypeOfCaptures, totalCapturedPackets))

            if capturePacketsToFile and int(totalCapturedPackets) != 0:
                timestamp = int(time.time())
                if self.enableDataPlane:
                    packetCaptureFilenameData = 'packetCaptureForData_'+str(timestamp)
                    subprocess.call(['touch', packetCaptureFilenameData])
                if self.enableControlPlane:
                    packetCaptureFilenameControl = 'packetCaptureForControl_'+str(timestamp)
                    subprocess.call(['touch', packetCaptureFilenameControl])

            for packetIndex in range(1, int(totalCapturedPackets)):
                if self.enableDataPlane and eachTypeOfCaptures == 'data':
                    data = {'arg1': vport+'/capture/currentPacket', 'arg2': packetIndex}
                    response = self.ixnObj.post(self.ixnObj.sessionUrl+'/vport/capture/currentPacket/operations/getpacketfromdatacapture',
                                                data=data, silentMode=True)
                if self.enableControlPlane and eachTypeOfCaptures == 'control':
                    data = {'arg1': vport+'/capture/currentPacket', 'arg2': packetIndex}
                    response = self.ixnObj.post(self.ixnObj.sessionUrl+'/vport/capture/currentPacket/operations/getpacketfromcontrolcapture',
                                                data=data, silentMode=True)

                response = self.ixnObj.get(self.ixnObj.httpHeader+vport+'/capture/currentPacket/stack', silentMode=True)
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

                    response = self.ixnObj.get(self.ixnObj.httpHeader+stackIdObject+'/field', silentMode=True)
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
            saveToTempLocation: Where to temporary save the .cap file on the ReST API server: C:\\Temp
                                The folder will be created if it doesn't exists.
            localLinuxLocation: Where to save the .cap file on the Linux machine.
            appendToSavedCapturedFile: Add a text string to the captured file.

        Example:
            captureObj.getCapFile([ixChassisIp, '2', '1'], 'control', 'c:\\Temp', '/home/hgee/test')
        """
        if appendToSavedCapturedFile != None:
            data = {'arg1': saveToTempLocation, 'arg2': appendToSavedCapturedFile}
        else:
            data = {'arg1': saveToTempLocation}
        self.ixnObj.post(self.ixnObj.sessionUrl+'/operations/savecapture', data=data)

        if typeOfCapture == 'control':
            capFileToGet = saveToTempLocation+'\\'+port[1]+'-'+port[2]+'_SW.cap'
        if typeOfCapture == 'data':
            capFileToGet = saveToTempLocation+'\\'+port[1]+'-'+port[2]+'_HW.cap'

        fileMgmtObj = FileMgmt(self.ixnObj)

        if self.ixnObj.serverOs in ['windows', 'windowsConnectionMgr']:
            fileMgmtObj.copyFileWindowsToLocalLinux(windowsPathAndFileName=capFileToGet, localPath=localLinuxLocation,
                                                    renameDestinationFile=None)
        if self.ixnObj.serverOs == 'linux':
            fileMgmtObj.copyFileLinuxToLocalLinux(linuxApiServerPathAndFileName=capFileToGet, localPath=localLinuxLocation,
                                                  renameDestinationFile=None)

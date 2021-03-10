import time
from IxNetRestApiPortMgmt import PortMgmt
from IxNetRestApi import IxNetRestApiException
from ixnetwork_restpy.files import Files


class PacketCapture(object):
    """
    ixnObj: The main connection object
    portObj: The port object

    """
    def __init__(self, ixnObj=None, portMgmtObj=None):
        """
        Parameters
            ixnObj: The main ixnObj object
            portMgmtObj: (Optional):  The PortMgmt object. If you already have the portMgmt
            object, then pass it in.
                         Otherwise, leave portMgmtObj=None
        Example:
            trafficObj = Traffic(mainObj)
            portMgmtObj = PortMgmt(mainObj)
            captureObj = PacketCapture(mainObj, portMgmtObj)
            captureObj.packetCaptureConfigPortMode(port=[ixChassisIp, '2', '1'],
            enableControlPlane=False, enableDataPlane=True)
            trafficObj.startTraffic()  <-- Make sure traffic is running in continuous mode
            captureObj.packetCaptureStart()
            time.sleep(10)
            captureObj.packetCaptureStop()
            trafficObj.stopTraffic()

            pktCaptureObj.getCapFile(port=[ixChassisIp, '2', '1'], typeOfCapture='data',
            saveToTempLocation='c:\\Results', localLinuxLocation='.',
            appendToSavedCapturedFile=None)

            pktCaptureObj.packetCaptureGetCurrentPackets(getUpToPacketNumber=5,
            capturePacketsToFile=True, getSavedCapturedDotCapFile=True)

            captureObj.packetCaptureClearTabs()
        """
        self.ixnObj = ixnObj
        self.ixNetwork = ixnObj.ixNetwork
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

    def packetCaptureConfigPortMode(self,
                                    port,
                                    portRxMode='capture',
                                    enableControlPlane=True,
                                    enableDataPlane=True):
        """
        Description
           Enable|Disable port capturing for control plane and data plane.

           Values are true or false
              -softwareEnabled == Control Plane
              -hardwareEnabled == Data Plane

        Parameters
            port: <list>:[ixChassisIp, '1', '3'] => [ixChasssisIp, str(cardNumber), str(portNumber)]
            portRxMode: <str>: capture|captureAndMeasure
            enableControlPlane: <bool>
            enableDataPlane: <bool>
        """
        self.ixnObj.logInfo("Configuring and enable control/data plane capture")
        if enableControlPlane:
            self.enableControlPlane = True
        if enableDataPlane:
            self.enableDataPlane = True

        self.captureRxPort = port
        vport = self.portMgmtObj.getVports([port])[0]
        vport.RxMode = portRxMode

        vport.Capture.SoftwareEnabled = enableControlPlane
        vport.Capture.HardwareEnabled = enableDataPlane

    def packetCaptureStart(self):
        """
        Start packet capturing
        """
        try:
            self.ixNetwork.StartCapture()
        except Exception as err:
            self.ixnObj.logInfo("Error {} ".format(err))
            raise Exception('\n Failed to start captures')

    def packetCaptureStop(self):
        """
        Stop packet capturing
        """
        try:
            self.ixNetwork.StopCapture()
        except Exception as err:
            self.ixnObj.logInfo("Error {} ".format(err))
            raise Exception('\n Failed to stop captures')

    def packetCaptureClearTabs(self):
        """
        Remove all captured tabs on Windows IxNetwork GUI
        """
        try:
            self.ixNetwork.CloseAllTabs()
        except Exception as err:
            self.ixnObj.logInfo("Error {} ".format(err))
            raise Exception('\n Failed closing all tabs')

    def packetCaptureGetCurrentPackets(self, getUpToPacketNumber=20, capturePacketsToFile=True):
        """
        Description
           Packet Capturing in wireshark style details. By default, it saved 7209 packet counts.
           It takes a long time to save all the packet header details into a file.
           This API will default saving 20 packet counts. You could increase the packet count.

        Parameters
            getUpToPacketNumber: None|The last packet number to get. Always starts at 1.
                                 If you state 10, then this function will get 1-10 packets.
            capturePacketsToFile: True|False
        """

        if capturePacketsToFile:
            timestamp = int(time.time())
            if self.enableDataPlane:
                packetCaptureFilenameData = 'packetCaptureForData_'+str(timestamp)

            if self.enableControlPlane:
                packetCaptureFilenameControl = 'packetCaptureForControl_'+str(timestamp)

            if not self.enableDataPlane and not self.enableControlPlane:
                raise IxNetRestApiException('\n PacketCapture Error: You must enable one of the '
                                            'options: enableDataPlane|enableControlPlane')

        vport = self.portMgmtObj.getVports([self.captureRxPort])[0]
        totalDataCapturedPackets = vport.Capture.DataPacketCounter
        totalControlCapturedPackets = vport.Capture.ControlPacketCounter

        if type(totalDataCapturedPackets) != int:
            totalDataCapturedPackets = 0
        else:
            if getUpToPacketNumber is not None:
                totalDataCapturedPackets = getUpToPacketNumber

        if type(totalControlCapturedPackets) != int:
            totalControlCapturedPackets = 0
        else:
            if getUpToPacketNumber is not None:
                totalControlCapturedPackets = getUpToPacketNumber

        for eachTypeOfCaptures, totalCapturedPackets in \
                zip(('data', 'control'), (totalDataCapturedPackets, totalControlCapturedPackets)):
            self.ixnObj.logInfo(
                'Getting captured packets for capture type: {0}'.format(eachTypeOfCaptures))

            if capturePacketsToFile and int(totalCapturedPackets) != 0:
                timestamp = int(time.time())
                if self.enableDataPlane:
                    packetCaptureFilenameData = 'packetCaptureForData_'+str(timestamp)

                if self.enableControlPlane:
                    packetCaptureFilenameControl = 'packetCaptureForControl_'+str(timestamp)

            for packetIndex in range(1, int(totalCapturedPackets)):
                self.ixnObj.logInfo('Getting captured packet index number: {}/{}'.
                                    format(packetIndex, getUpToPacketNumber))

                if self.enableDataPlane and eachTypeOfCaptures == 'data':
                    vport.Capture.CurrentPacket.GetPacketFromDataCapture(Arg2=packetIndex)

                if self.enableControlPlane and eachTypeOfCaptures == 'control':
                    vport.Capture.CurrentPacket.GetPacketFromControlCapture(Arg2=packetIndex)

                stackObj = vport.Capture.CurrentPacket.Stack.find()

                for eachStack in stackObj:
                    displayName = eachStack.DisplayName
                    self.ixnObj.logInfo('\n Stack: %s' % displayName)
                    if capturePacketsToFile:
                        if eachTypeOfCaptures == 'data':
                            with open(packetCaptureFilenameData, 'a') as packetCaptureFile:
                                packetCaptureFile.write('\n Stack: %s\n' % displayName)

                        if eachTypeOfCaptures == 'control':
                            with open(packetCaptureFilenameControl, 'a') as packetCaptureFile:
                                packetCaptureFile.write('\n Stack: %s\n' % displayName)

                    for eachFieldObj in eachStack.Field.find():
                        fieldId = eachFieldObj.href.split('/')[-1]
                        fieldName = eachFieldObj.DisplayName
                        fieldValue = eachFieldObj.FieldValue
                        self.ixnObj.logInfo(
                            '\t{0}: {1}: {2}'.format(fieldId, fieldName, fieldValue))

                        if capturePacketsToFile:
                            if eachTypeOfCaptures == 'data':
                                with open(packetCaptureFilenameData, 'a') as packetCaptureFile:
                                    packetCaptureFile.write(
                                        '\t{0}: {1}: {2}\n'.format(fieldId, fieldName, fieldValue))

                            if eachTypeOfCaptures == 'control':
                                with open(packetCaptureFilenameControl, 'a') as packetCaptureFile:
                                    packetCaptureFile.write(
                                        '\t{0}: {1}: {2}\n'.format(fieldId, fieldName, fieldValue))

    def packetCaptureGetCurrentPacketsHex(self, getUpToPacketNumber=10):
        """
        Description
           Returns captured packets in hex format.
           This API will default return 20 packet hex. You could increase the packet count.

        Parameters
            getUpToPacketNumber: None|The last packet number to get.
                                 Always starts at 1. If you state 10,
                                 then this function will get 1-10 packets.

        Return
            capturedData:  dictionary.   key is 'data' and/or 'control'
                capturedData['data']  is dictionary of packet hex data for Data Capture Buffer
                capturedData['control']  is dictionary of packet hex data for Control Capture Buffer
        """

        vport = self.portMgmtObj.getVports([self.captureRxPort])[0]
        totalDataCapturedPackets = vport.Capture.DataPacketCounter
        totalControlCapturedPackets = vport.Capture.ControlPacketCounter

        if type(totalDataCapturedPackets) != int:
            totalDataCapturedPackets = 0
        else:
            if getUpToPacketNumber is not None:
                totalDataCapturedPackets = getUpToPacketNumber

        if type(totalControlCapturedPackets) != int:
            totalControlCapturedPackets = 0
        else:
            if getUpToPacketNumber is not None:
                totalControlCapturedPackets = getUpToPacketNumber

        capturedData = {}
        for eachTypeOfCaptures, totalCapturedPackets in \
                zip(('data', 'control'), (totalDataCapturedPackets, totalControlCapturedPackets)):
            self.ixnObj.logInfo(
                'Getting captured packets for capture type: {0}'.format(eachTypeOfCaptures))

            capturedData[eachTypeOfCaptures] = {}
            for packetIndex in range(1, int(totalCapturedPackets)):
                self.ixnObj.logInfo('Getting captured packet index number: {}/{}'. format(
                    packetIndex, getUpToPacketNumber))

                if totalDataCapturedPackets > 0:
                    vport.Capture.CurrentPacket.GetPacketFromDataCapture(Arg2=packetIndex)

                if totalControlCapturedPackets > 0:
                    vport.Capture.CurrentPacket.GetPacketFromControlCapture(Arg2=packetIndex)

                packetHex = vport.Capture.CurrentPacket.PacketHex
                capturedData[eachTypeOfCaptures][packetIndex] = packetHex
            return capturedData

    def getCapFile(self, port, typeOfCapture='data', saveToTempLocation='c:\\Temp',
                   localLinuxLocation='.', appendToSavedCapturedFile=None):
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

               DATA: {"arg1": "packetCaptureFolder"}  <-- This could be any name.
                                                Just a temporary folder to store the captured file.

               Wait for the /operations/savecapturefiles/<id> to complete.
                            May take up to a minute or more.

               For Windows API server:

                  DATA: {"arg1": "c:\\Results\\port2_HW.cap",
                         "arg2": "/api/v1/sessions/1/ixnetwork/files/port2_HW.cap"}

               For Linux API server:

                  DATA: {"arg1": "captures/packetCaptureFolder/port2_HW.cap",
                         "arg2": "/api/v1/sessions/<id>/ixnetwork/files/port2_HW.cap"}

        """

        vport = self.portMgmtObj.getVports([port])[0]
        vportName = vport.Name

        if appendToSavedCapturedFile is not None:
            self.ixNetwork.SaveCaptureFiles(Arg1=saveToTempLocation, Arg2=appendToSavedCapturedFile)
        else:
            self.ixNetwork.SaveCaptureFiles(Arg1=saveToTempLocation)

        # example capfilePathName: 'c:\\Results\\1-7-2_HW.cap'
        if typeOfCapture == 'control':
            if self.ixnObj.serverOs in ['windows', 'windowsConnectionMgr']:
                capFileToGet = saveToTempLocation + "\\" + vportName + "_SW.cap"
                filename = vportName + "_HW.cap"
            else:
                capFileToGet = saveToTempLocation + "/" + vportName + "_SW.cap"
                filename = vportName + "_HW.cap"

        if typeOfCapture == 'data':
            if self.ixnObj.serverOs in ['windows', 'windowsConnectionMgr']:
                capFileToGet = saveToTempLocation + "\\" + vportName + "_HW.cap"
                filename = vportName + "_HW.cap"
            else:
                capFileToGet = saveToTempLocation + "/" + vportName + "_HW.cap"
                filename = vportName + "_HW.cap"

        try:
            self.ixNetwork.CopyFile(Files(capFileToGet, local_file=False),
                                    localLinuxLocation + "\\" + filename + ".cap")
        except Exception as err:
            self.ixnObj.logInfo("Error {} ".format(err))
            self.ixNetwork.CopyFile(Files(capFileToGet, local_file=False),
                                    localLinuxLocation + "/" + filename + ".cap")

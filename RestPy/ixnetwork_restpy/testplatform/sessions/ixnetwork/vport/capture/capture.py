from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Capture(Base):
	"""The Capture class encapsulates a required capture node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Capture property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'capture'

	def __init__(self, parent):
		super(Capture, self).__init__(parent)

	@property
	def CurrentPacket(self):
		"""An instance of the CurrentPacket class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.capture.currentpacket.currentpacket.CurrentPacket)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.capture.currentpacket.currentpacket import CurrentPacket
		return CurrentPacket(self)._select()

	@property
	def Filter(self):
		"""An instance of the Filter class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.capture.filter.filter.Filter)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.capture.filter.filter import Filter
		return Filter(self)._select()

	@property
	def FilterPallette(self):
		"""An instance of the FilterPallette class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.capture.filterpallette.filterpallette.FilterPallette)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.capture.filterpallette.filterpallette import FilterPallette
		return FilterPallette(self)._select()

	@property
	def Trigger(self):
		"""An instance of the Trigger class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.capture.trigger.trigger.Trigger)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.capture.trigger.trigger import Trigger
		return Trigger(self)._select()

	@property
	def AfterTriggerFilter(self):
		"""Controls the capture of data after triggering when operating in triggered mode.

		Returns:
			str(captureAfterTriggerAll|captureAfterTriggerConditionFilter|captureAfterTriggerFilter)
		"""
		return self._get_attribute('afterTriggerFilter')
	@AfterTriggerFilter.setter
	def AfterTriggerFilter(self, value):
		self._set_attribute('afterTriggerFilter', value)

	@property
	def BeforeTriggerFilter(self):
		"""Controls the capture of data prior to triggering when operating in triggered mode

		Returns:
			str(captureBeforeTriggerAll|captureBeforeTriggerFilter|captureBeforeTriggerNone)
		"""
		return self._get_attribute('beforeTriggerFilter')
	@BeforeTriggerFilter.setter
	def BeforeTriggerFilter(self, value):
		self._set_attribute('beforeTriggerFilter', value)

	@property
	def CaptureMode(self):
		"""Controls whether data capture is performed in a continuous or triggered mode.

		Returns:
			str(captureContinuousMode|captureTriggerMode)
		"""
		return self._get_attribute('captureMode')
	@CaptureMode.setter
	def CaptureMode(self, value):
		self._set_attribute('captureMode', value)

	@property
	def ContinuousFilters(self):
		"""Controls the circular buffer behaviour: continuous capture of all received packets or continuous capture of received packets which match the filter conditions applied.

		Returns:
			str(captureContinuousAll|captureContinuousFilter)
		"""
		return self._get_attribute('continuousFilters')
	@ContinuousFilters.setter
	def ContinuousFilters(self, value):
		self._set_attribute('continuousFilters', value)

	@property
	def ControlActiveCapture(self):
		"""The name of the active control capture (if any).The active control capture is the last one made on the port by default; but the user can change it using this attribute.

		Returns:
			str
		"""
		return self._get_attribute('controlActiveCapture')
	@ControlActiveCapture.setter
	def ControlActiveCapture(self, value):
		self._set_attribute('controlActiveCapture', value)

	@property
	def ControlBufferBehaviour(self):
		"""Sets the control capture buffer behavior.

		Returns:
			str(bufferAfterStopCircular|bufferAfterStopNonCircular|bufferLiveCircular|bufferLiveNonCircular)
		"""
		return self._get_attribute('controlBufferBehaviour')
	@ControlBufferBehaviour.setter
	def ControlBufferBehaviour(self, value):
		self._set_attribute('controlBufferBehaviour', value)

	@property
	def ControlBufferSize(self):
		"""Sets the size(%) of the ports memory used by the control capture.

		Returns:
			number
		"""
		return self._get_attribute('controlBufferSize')
	@ControlBufferSize.setter
	def ControlBufferSize(self, value):
		self._set_attribute('controlBufferSize', value)

	@property
	def ControlCaptureFilter(self):
		"""Controls the dividing line within the capture buffer between before trigger dataand post trigger data. This control is only useful in triggered mode.

		Returns:
			str
		"""
		return self._get_attribute('controlCaptureFilter')
	@ControlCaptureFilter.setter
	def ControlCaptureFilter(self, value):
		self._set_attribute('controlCaptureFilter', value)

	@property
	def ControlCaptureState(self):
		"""Current state of the control capture (if there are packets uploading in GUI or not).

		Returns:
			str(notReady|ready)
		"""
		return self._get_attribute('controlCaptureState')

	@property
	def ControlCaptureTrigger(self):
		"""This is the control Trigger string.

		Returns:
			str
		"""
		return self._get_attribute('controlCaptureTrigger')
	@ControlCaptureTrigger.setter
	def ControlCaptureTrigger(self, value):
		self._set_attribute('controlCaptureTrigger', value)

	@property
	def ControlCapturedPacketCounter(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('controlCapturedPacketCounter')

	@property
	def ControlCaptures(self):
		"""The list of control captures which are available for the port.

		Returns:
			str
		"""
		return self._get_attribute('controlCaptures')

	@property
	def ControlDecodeAsCurrentFilter(self):
		"""The control capture decode as filter used by last decode as operation (if any).

		Returns:
			str
		"""
		return self._get_attribute('controlDecodeAsCurrentFilter')

	@property
	def ControlInterfaceType(self):
		"""Enables control capture on the desired interfaces.

		Returns:
			str(anyInterface|specificInterface)
		"""
		return self._get_attribute('controlInterfaceType')
	@ControlInterfaceType.setter
	def ControlInterfaceType(self, value):
		self._set_attribute('controlInterfaceType', value)

	@property
	def ControlPacketCounter(self):
		"""Shows the number of control capture packets.

		Returns:
			number
		"""
		return self._get_attribute('controlPacketCounter')

	@property
	def ControlSliceSize(self):
		"""Sets the size of the control capture slices.

		Returns:
			number
		"""
		return self._get_attribute('controlSliceSize')
	@ControlSliceSize.setter
	def ControlSliceSize(self, value):
		self._set_attribute('controlSliceSize', value)

	@property
	def DataActiveCapture(self):
		"""The name of the active data capture (if any). The active data capture is the last one made on the port by default; but the user can change it using this attribute.

		Returns:
			str
		"""
		return self._get_attribute('dataActiveCapture')
	@DataActiveCapture.setter
	def DataActiveCapture(self, value):
		self._set_attribute('dataActiveCapture', value)

	@property
	def DataCaptureState(self):
		"""Current state of the data capture; ready if all packets have been uploaded on client or notReady if packet uploading is in progress.

		Returns:
			str(notReady|ready)
		"""
		return self._get_attribute('dataCaptureState')

	@property
	def DataCapturedPacketCounter(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('dataCapturedPacketCounter')

	@property
	def DataCaptures(self):
		"""The list of data captures which are available for the port.

		Returns:
			str
		"""
		return self._get_attribute('dataCaptures')

	@property
	def DataDecodeAsCurrentFilter(self):
		"""The data capture decode as filter used by last decode as operation (if any).

		Returns:
			str
		"""
		return self._get_attribute('dataDecodeAsCurrentFilter')

	@property
	def DataPacketCounter(self):
		"""Shows the number of data capture packets.

		Returns:
			number
		"""
		return self._get_attribute('dataPacketCounter')

	@property
	def DataReceiveTimestamp(self):
		"""Controls whether the data capture packets timestamp are using the chassis UTC time or the HW timestamp.

		Returns:
			str(chassisUtcTime|hwTimestamp)
		"""
		return self._get_attribute('dataReceiveTimestamp')
	@DataReceiveTimestamp.setter
	def DataReceiveTimestamp(self, value):
		self._set_attribute('dataReceiveTimestamp', value)

	@property
	def DecodeAsLinkProtocols(self):
		"""List with link protocols available for capture decode as operation. Need to have an active capture to retrieve the property.

		Returns:
			list(str)
		"""
		return self._get_attribute('decodeAsLinkProtocols')

	@property
	def DecodeAsNetworkProtocols(self):
		"""List with network protocols available for capture decode as operation. Need to have an active capture to retrieve the property.

		Returns:
			list(str)
		"""
		return self._get_attribute('decodeAsNetworkProtocols')

	@property
	def DecodeAsTransportProtocols(self):
		"""List with transport protocols available for capture decode as operation. Need to have an active capture to retrieve the property.

		Returns:
			list(str)
		"""
		return self._get_attribute('decodeAsTransportProtocols')

	@property
	def DisplayFiltersControlCapture(self):
		"""Displays the packet filter set inside the control capture that is used to filter the already captured packets

		Returns:
			str
		"""
		return self._get_attribute('displayFiltersControlCapture')
	@DisplayFiltersControlCapture.setter
	def DisplayFiltersControlCapture(self, value):
		self._set_attribute('displayFiltersControlCapture', value)

	@property
	def DisplayFiltersDataCapture(self):
		"""Displays the packet filter set inside the data capture that is used to filter the already captured packets

		Returns:
			str
		"""
		return self._get_attribute('displayFiltersDataCapture')
	@DisplayFiltersDataCapture.setter
	def DisplayFiltersDataCapture(self, value):
		self._set_attribute('displayFiltersDataCapture', value)

	@property
	def HardwareEnabled(self):
		"""If true, enables the capture of data plane traffic. Note that in order for data traffic to be captured, the vport attritbute -rxMode must be set to capture.

		Returns:
			bool
		"""
		return self._get_attribute('hardwareEnabled')
	@HardwareEnabled.setter
	def HardwareEnabled(self, value):
		self._set_attribute('hardwareEnabled', value)

	@property
	def IsCaptureRunning(self):
		"""Indicates if the capture is running.

		Returns:
			bool
		"""
		return self._get_attribute('isCaptureRunning')

	@property
	def IsControlCaptureRunning(self):
		"""Indicates if the control capture is running.

		Returns:
			bool
		"""
		return self._get_attribute('isControlCaptureRunning')

	@property
	def IsDataCaptureRunning(self):
		"""Indicates if the data capture is running.

		Returns:
			bool
		"""
		return self._get_attribute('isDataCaptureRunning')

	@property
	def SliceSize(self):
		"""The size of the capture slice.

		Returns:
			number
		"""
		return self._get_attribute('sliceSize')
	@SliceSize.setter
	def SliceSize(self, value):
		self._set_attribute('sliceSize', value)

	@property
	def SoftwareEnabled(self):
		"""If true, enables the capture of control plane traffic. Note that in order for data traffic to be captured, the vport attritbute -rxMode must be set to capture.

		Returns:
			bool
		"""
		return self._get_attribute('softwareEnabled')
	@SoftwareEnabled.setter
	def SoftwareEnabled(self, value):
		self._set_attribute('softwareEnabled', value)

	@property
	def TriggerPosition(self):
		"""Controls the dividing line within the capture buffer between before trigger data and post trigger data. This control is only useful in triggered mode.

		Returns:
			number
		"""
		return self._get_attribute('triggerPosition')
	@TriggerPosition.setter
	def TriggerPosition(self, value):
		self._set_attribute('triggerPosition', value)

	def DecodeAsApply(self, Arg2, Arg3, Arg4, Arg5):
		"""Executes the decodeAsApply operation on the server.

		The command forces a re-dissection of all packets based on a filter condition. (similar with Decode As from Wireshark)

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=capture)): The method internally set Arg1 to the current href for this instance
			Arg2 (str(control|data)): The capture type, could be either control or data.
			Arg3 (str(link|network|transport)): Specifies the network layer at witch the command should take place.
			Arg4 (number): Could be the TCP port for Transport layer (either source or destination), IP protocol for Network layer or Ethertype for Link layer.
			Arg5 (str): The protocol name to re-dissect as.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('DecodeAsApply', payload=locals(), response_object=None)

	def DecodeAsApply(self, Arg2, Arg3, Arg4, Arg5, Arg6, Arg7):
		"""Executes the decodeAsApply operation on the server.

		The command forces a re-dissection of all packets based on a filter condition. (similar with Decode As from Wireshark)

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=capture)): The method internally set Arg1 to the current href for this instance
			Arg2 (str(control|data)): The capture type, could be either control or data.
			Arg3 (str(transport)): The transport layer.
			Arg4 (number): The TCP source port.
			Arg5 (str(transport)): The transport layer.
			Arg6 (number): The TCP destination port.
			Arg7 (str): The protocol name to re-dissect as.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('DecodeAsApply', payload=locals(), response_object=None)

	def DecodeAsClear(self, Arg2):
		"""Executes the decodeAsClear operation on the server.

		The command clears the dissection filter set by DecodeAsApply command.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=capture)): The method internally set Arg1 to the current href for this instance
			Arg2 (str(control|data)): The capture type, could be either control or data.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('DecodeAsClear', payload=locals(), response_object=None)

	def MergeCapture(self, Arg2, Arg3, Arg4, Arg5):
		"""Executes the mergeCapture operation on the server.

		The command merges to online captures.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=capture)): The method internally set Arg1 to the current href for this instance
			Arg2 (str(control|data)): The capture type, could be either control or data.
			Arg3 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=capture)): The capture object of a port.
			Arg4 (str(control|data)): The capture type, could be either control or data.
			Arg5 (str): The full path where the resulted merged capture will be saved, the result capture name needs to contain extension also.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('MergeCapture', payload=locals(), response_object=None)

	def MergeCapture(self, Arg2, Arg3, Arg4):
		"""Executes the mergeCapture operation on the server.

		The command merges an online capture file with an offline one.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=capture)): The method internally set Arg1 to the current href for this instance
			Arg2 (str(control|data)): The capture type, could be either control or data.
			Arg3 (str): The full path of the offline capture.
			Arg4 (str): The full path where the resulted merged capture will be saved, the result capture name needs to contain extension also.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('MergeCapture', payload=locals(), response_object=None)

	def Start(self):
		"""Executes the start operation on the server.

		This command starts the capture process for a port or group of ports.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=capture)): The method internally set Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Start', payload=locals(), response_object=None)

	def Start(self, Arg2):
		"""Executes the start operation on the server.

		The command starts the capture porcess for the specified port.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=capture)): The method internally set Arg1 to the current href for this instance
			Arg2 (str(allTraffic|controlTraffic|dataTraffic)): The type of the capture that should be started.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Start', payload=locals(), response_object=None)

	def Stop(self):
		"""Executes the stop operation on the server.

		This command stops captures for the specified capture configuration.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=capture)): The method internally set Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Stop', payload=locals(), response_object=None)

	def Stop(self, Arg2):
		"""Executes the stop operation on the server.

		The command stops the capture on a port.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=capture)): The method internally set Arg1 to the current href for this instance
			Arg2 (str(allTraffic|controlTraffic|dataTraffic)): The capture type.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Stop', payload=locals(), response_object=None)

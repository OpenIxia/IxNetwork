
# Copyright 1997 - 2018 by IXIA Keysight
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
    
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
		"""

		Returns:
			str(captureAfterTriggerAll|captureAfterTriggerConditionFilter|captureAfterTriggerFilter)
		"""
		return self._get_attribute('afterTriggerFilter')
	@AfterTriggerFilter.setter
	def AfterTriggerFilter(self, value):
		self._set_attribute('afterTriggerFilter', value)

	@property
	def BeforeTriggerFilter(self):
		"""

		Returns:
			str(captureBeforeTriggerAll|captureBeforeTriggerFilter|captureBeforeTriggerNone)
		"""
		return self._get_attribute('beforeTriggerFilter')
	@BeforeTriggerFilter.setter
	def BeforeTriggerFilter(self, value):
		self._set_attribute('beforeTriggerFilter', value)

	@property
	def CaptureMode(self):
		"""

		Returns:
			str(captureContinuousMode|captureTriggerMode)
		"""
		return self._get_attribute('captureMode')
	@CaptureMode.setter
	def CaptureMode(self, value):
		self._set_attribute('captureMode', value)

	@property
	def ContinuousFilters(self):
		"""

		Returns:
			str(captureContinuousAll|captureContinuousFilter)
		"""
		return self._get_attribute('continuousFilters')
	@ContinuousFilters.setter
	def ContinuousFilters(self, value):
		self._set_attribute('continuousFilters', value)

	@property
	def ControlActiveCapture(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('controlActiveCapture')
	@ControlActiveCapture.setter
	def ControlActiveCapture(self, value):
		self._set_attribute('controlActiveCapture', value)

	@property
	def ControlBufferBehaviour(self):
		"""

		Returns:
			str(bufferAfterStopCircular|bufferAfterStopNonCircular|bufferLiveCircular|bufferLiveNonCircular)
		"""
		return self._get_attribute('controlBufferBehaviour')
	@ControlBufferBehaviour.setter
	def ControlBufferBehaviour(self, value):
		self._set_attribute('controlBufferBehaviour', value)

	@property
	def ControlBufferSize(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('controlBufferSize')
	@ControlBufferSize.setter
	def ControlBufferSize(self, value):
		self._set_attribute('controlBufferSize', value)

	@property
	def ControlCaptureFilter(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('controlCaptureFilter')
	@ControlCaptureFilter.setter
	def ControlCaptureFilter(self, value):
		self._set_attribute('controlCaptureFilter', value)

	@property
	def ControlCaptureState(self):
		"""

		Returns:
			str(notReady|ready)
		"""
		return self._get_attribute('controlCaptureState')

	@property
	def ControlCaptureTrigger(self):
		"""

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
		"""

		Returns:
			str
		"""
		return self._get_attribute('controlCaptures')

	@property
	def ControlDecodeAsCurrentFilter(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('controlDecodeAsCurrentFilter')

	@property
	def ControlInterfaceType(self):
		"""

		Returns:
			str(anyInterface|specificInterface)
		"""
		return self._get_attribute('controlInterfaceType')
	@ControlInterfaceType.setter
	def ControlInterfaceType(self, value):
		self._set_attribute('controlInterfaceType', value)

	@property
	def ControlPacketCounter(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('controlPacketCounter')

	@property
	def ControlSliceSize(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('controlSliceSize')
	@ControlSliceSize.setter
	def ControlSliceSize(self, value):
		self._set_attribute('controlSliceSize', value)

	@property
	def DataActiveCapture(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('dataActiveCapture')
	@DataActiveCapture.setter
	def DataActiveCapture(self, value):
		self._set_attribute('dataActiveCapture', value)

	@property
	def DataCaptureState(self):
		"""

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
		"""

		Returns:
			str
		"""
		return self._get_attribute('dataCaptures')

	@property
	def DataDecodeAsCurrentFilter(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('dataDecodeAsCurrentFilter')

	@property
	def DataPacketCounter(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('dataPacketCounter')

	@property
	def DataReceiveTimestamp(self):
		"""

		Returns:
			str(chassisUtcTime|hwTimestamp)
		"""
		return self._get_attribute('dataReceiveTimestamp')
	@DataReceiveTimestamp.setter
	def DataReceiveTimestamp(self, value):
		self._set_attribute('dataReceiveTimestamp', value)

	@property
	def DecodeAsLinkProtocols(self):
		"""

		Returns:
			list(str)
		"""
		return self._get_attribute('decodeAsLinkProtocols')

	@property
	def DecodeAsNetworkProtocols(self):
		"""

		Returns:
			list(str)
		"""
		return self._get_attribute('decodeAsNetworkProtocols')

	@property
	def DecodeAsTransportProtocols(self):
		"""

		Returns:
			list(str)
		"""
		return self._get_attribute('decodeAsTransportProtocols')

	@property
	def DisplayFiltersControlCapture(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('displayFiltersControlCapture')
	@DisplayFiltersControlCapture.setter
	def DisplayFiltersControlCapture(self, value):
		self._set_attribute('displayFiltersControlCapture', value)

	@property
	def DisplayFiltersDataCapture(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('displayFiltersDataCapture')
	@DisplayFiltersDataCapture.setter
	def DisplayFiltersDataCapture(self, value):
		self._set_attribute('displayFiltersDataCapture', value)

	@property
	def HardwareEnabled(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('hardwareEnabled')
	@HardwareEnabled.setter
	def HardwareEnabled(self, value):
		self._set_attribute('hardwareEnabled', value)

	@property
	def IsCaptureRunning(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isCaptureRunning')

	@property
	def IsControlCaptureRunning(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isControlCaptureRunning')

	@property
	def IsDataCaptureRunning(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isDataCaptureRunning')

	@property
	def SliceSize(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('sliceSize')
	@SliceSize.setter
	def SliceSize(self, value):
		self._set_attribute('sliceSize', value)

	@property
	def SoftwareEnabled(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('softwareEnabled')
	@SoftwareEnabled.setter
	def SoftwareEnabled(self, value):
		self._set_attribute('softwareEnabled', value)

	@property
	def TriggerPosition(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('triggerPosition')
	@TriggerPosition.setter
	def TriggerPosition(self, value):
		self._set_attribute('triggerPosition', value)

	def DecodeAsApply(self, Arg2, Arg3, Arg4, Arg5):
		"""Executes the decodeAsApply operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=capture)): The method internally sets Arg1 to the current href for this instance
			Arg2 (str(control|data)): 
			Arg3 (str(link|network|transport)): 
			Arg4 (number): 
			Arg5 (str): 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('DecodeAsApply', payload=locals(), response_object=None)

	def DecodeAsApply(self, Arg2, Arg3, Arg4, Arg5, Arg6, Arg7):
		"""Executes the decodeAsApply operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=capture)): The method internally sets Arg1 to the current href for this instance
			Arg2 (str(control|data)): 
			Arg3 (str(transport)): 
			Arg4 (number): 
			Arg5 (str(transport)): 
			Arg6 (number): 
			Arg7 (str): 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('DecodeAsApply', payload=locals(), response_object=None)

	def DecodeAsClear(self, Arg2):
		"""Executes the decodeAsClear operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=capture)): The method internally sets Arg1 to the current href for this instance
			Arg2 (str(control|data)): 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('DecodeAsClear', payload=locals(), response_object=None)

	def MergeCapture(self, Arg2, Arg3, Arg4, Arg5):
		"""Executes the mergeCapture operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=capture)): The method internally sets Arg1 to the current href for this instance
			Arg2 (str(control|data)): 
			Arg3 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=capture)): 
			Arg4 (str(control|data)): 
			Arg5 (str): 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('MergeCapture', payload=locals(), response_object=None)

	def MergeCapture(self, Arg2, Arg3, Arg4):
		"""Executes the mergeCapture operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=capture)): The method internally sets Arg1 to the current href for this instance
			Arg2 (str(control|data)): 
			Arg3 (str): 
			Arg4 (str): 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('MergeCapture', payload=locals(), response_object=None)

	def Start(self):
		"""Executes the start operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=capture)): The method internally sets Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Start', payload=locals(), response_object=None)

	def Start(self, Arg2):
		"""Executes the start operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=capture)): The method internally sets Arg1 to the current href for this instance
			Arg2 (str(allTraffic|controlTraffic|dataTraffic)): 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Start', payload=locals(), response_object=None)

	def Stop(self):
		"""Executes the stop operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=capture)): The method internally sets Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Stop', payload=locals(), response_object=None)

	def Stop(self, Arg2):
		"""Executes the stop operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=capture)): The method internally sets Arg1 to the current href for this instance
			Arg2 (str(allTraffic|controlTraffic|dataTraffic)): 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Stop', payload=locals(), response_object=None)

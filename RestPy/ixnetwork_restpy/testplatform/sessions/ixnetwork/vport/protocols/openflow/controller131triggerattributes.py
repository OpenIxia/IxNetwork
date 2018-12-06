
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


class Controller131TriggerAttributes(Base):
	"""The Controller131TriggerAttributes class encapsulates a required controller131TriggerAttributes node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Controller131TriggerAttributes property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'controller131TriggerAttributes'

	def __init__(self, parent):
		super(Controller131TriggerAttributes, self).__init__(parent)

	@property
	def EnableSendTriggerMeterConfigStatsLearnedInformation(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableSendTriggerMeterConfigStatsLearnedInformation')
	@EnableSendTriggerMeterConfigStatsLearnedInformation.setter
	def EnableSendTriggerMeterConfigStatsLearnedInformation(self, value):
		self._set_attribute('enableSendTriggerMeterConfigStatsLearnedInformation', value)

	@property
	def EnableSendTriggerMeterFeatureStatsLearnedInformation(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableSendTriggerMeterFeatureStatsLearnedInformation')
	@EnableSendTriggerMeterFeatureStatsLearnedInformation.setter
	def EnableSendTriggerMeterFeatureStatsLearnedInformation(self, value):
		self._set_attribute('enableSendTriggerMeterFeatureStatsLearnedInformation', value)

	@property
	def EnableSendTriggerMeterStatLearnedInformation(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableSendTriggerMeterStatLearnedInformation')
	@EnableSendTriggerMeterStatLearnedInformation.setter
	def EnableSendTriggerMeterStatLearnedInformation(self, value):
		self._set_attribute('enableSendTriggerMeterStatLearnedInformation', value)

	@property
	def FlowStatOutGroup(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('flowStatOutGroup')
	@FlowStatOutGroup.setter
	def FlowStatOutGroup(self, value):
		self._set_attribute('flowStatOutGroup', value)

	@property
	def FlowStatOutGroupInputMode(self):
		"""

		Returns:
			str(allGroups|anyGroup|outGroupCustom)
		"""
		return self._get_attribute('flowStatOutGroupInputMode')
	@FlowStatOutGroupInputMode.setter
	def FlowStatOutGroupInputMode(self, value):
		self._set_attribute('flowStatOutGroupInputMode', value)

	@property
	def FlowStatOutPort(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('flowStatOutPort')
	@FlowStatOutPort.setter
	def FlowStatOutPort(self, value):
		self._set_attribute('flowStatOutPort', value)

	@property
	def FlowStatOutPortInputMode(self):
		"""

		Returns:
			str(ofppInPort|ofppNormal|ofppFlood|ofppAll|ofppController|ofppLocal|ofppAny|outPortCustom)
		"""
		return self._get_attribute('flowStatOutPortInputMode')
	@FlowStatOutPortInputMode.setter
	def FlowStatOutPortInputMode(self, value):
		self._set_attribute('flowStatOutPortInputMode', value)

	@property
	def FlowStatTableId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('flowStatTableId')
	@FlowStatTableId.setter
	def FlowStatTableId(self, value):
		self._set_attribute('flowStatTableId', value)

	@property
	def FlowStatTableIdInputMode(self):
		"""

		Returns:
			str(allTables|emergency|custom)
		"""
		return self._get_attribute('flowStatTableIdInputMode')
	@FlowStatTableIdInputMode.setter
	def FlowStatTableIdInputMode(self, value):
		self._set_attribute('flowStatTableIdInputMode', value)

	@property
	def IsMeterConfigStatLearnedInformationRefreshed(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isMeterConfigStatLearnedInformationRefreshed')

	@property
	def IsMeterFeatureStatLearnedInformationRefreshed(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isMeterFeatureStatLearnedInformationRefreshed')

	@property
	def IsMeterStatLearnedInformationRefreshed(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isMeterStatLearnedInformationRefreshed')

	@property
	def MeterConfigStatMeterId(self):
		"""

		Returns:
			str(ofpmController|ofpmSlowPath|ofpmAll|manual)
		"""
		return self._get_attribute('meterConfigStatMeterId')
	@MeterConfigStatMeterId.setter
	def MeterConfigStatMeterId(self, value):
		self._set_attribute('meterConfigStatMeterId', value)

	@property
	def MeterConfigStatMeterNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('meterConfigStatMeterNumber')
	@MeterConfigStatMeterNumber.setter
	def MeterConfigStatMeterNumber(self, value):
		self._set_attribute('meterConfigStatMeterNumber', value)

	@property
	def MeterConfigStatResponseTimeOut(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('meterConfigStatResponseTimeOut')
	@MeterConfigStatResponseTimeOut.setter
	def MeterConfigStatResponseTimeOut(self, value):
		self._set_attribute('meterConfigStatResponseTimeOut', value)

	@property
	def MeterFeatureStatResponseTimeOut(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('meterFeatureStatResponseTimeOut')
	@MeterFeatureStatResponseTimeOut.setter
	def MeterFeatureStatResponseTimeOut(self, value):
		self._set_attribute('meterFeatureStatResponseTimeOut', value)

	@property
	def MeterStatMeterId(self):
		"""

		Returns:
			str(ofpmController|ofpmSlowPath|ofpmAll|manual)
		"""
		return self._get_attribute('meterStatMeterId')
	@MeterStatMeterId.setter
	def MeterStatMeterId(self, value):
		self._set_attribute('meterStatMeterId', value)

	@property
	def MeterStatMeterNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('meterStatMeterNumber')
	@MeterStatMeterNumber.setter
	def MeterStatMeterNumber(self, value):
		self._set_attribute('meterStatMeterNumber', value)

	@property
	def MeterStatResponseTimeOut(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('meterStatResponseTimeOut')
	@MeterStatResponseTimeOut.setter
	def MeterStatResponseTimeOut(self, value):
		self._set_attribute('meterStatResponseTimeOut', value)

	@property
	def PortStatPortNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('portStatPortNumber')
	@PortStatPortNumber.setter
	def PortStatPortNumber(self, value):
		self._set_attribute('portStatPortNumber', value)

	@property
	def PortStatPortNumberInputMode(self):
		"""

		Returns:
			str(ofppAny|portNumberCustom)
		"""
		return self._get_attribute('portStatPortNumberInputMode')
	@PortStatPortNumberInputMode.setter
	def PortStatPortNumberInputMode(self, value):
		self._set_attribute('portStatPortNumberInputMode', value)

	@property
	def QueueConfigPortNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('queueConfigPortNumber')
	@QueueConfigPortNumber.setter
	def QueueConfigPortNumber(self, value):
		self._set_attribute('queueConfigPortNumber', value)

	@property
	def QueueConfigPortNumberInputMode(self):
		"""

		Returns:
			str(ofppAny|portNumberCustom)
		"""
		return self._get_attribute('queueConfigPortNumberInputMode')
	@QueueConfigPortNumberInputMode.setter
	def QueueConfigPortNumberInputMode(self, value):
		self._set_attribute('queueConfigPortNumberInputMode', value)

	@property
	def QueueStatPortNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('queueStatPortNumber')
	@QueueStatPortNumber.setter
	def QueueStatPortNumber(self, value):
		self._set_attribute('queueStatPortNumber', value)

	@property
	def QueueStatPortNumberInputMode(self):
		"""

		Returns:
			str(ofppAll|ofppAny|portNumberCustom)
		"""
		return self._get_attribute('queueStatPortNumberInputMode')
	@QueueStatPortNumberInputMode.setter
	def QueueStatPortNumberInputMode(self, value):
		self._set_attribute('queueStatPortNumberInputMode', value)

	@property
	def VendorMessageExperimenterType(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('vendorMessageExperimenterType')
	@VendorMessageExperimenterType.setter
	def VendorMessageExperimenterType(self, value):
		self._set_attribute('vendorMessageExperimenterType', value)

	@property
	def VendorStatExperimenterType(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('vendorStatExperimenterType')
	@VendorStatExperimenterType.setter
	def VendorStatExperimenterType(self, value):
		self._set_attribute('vendorStatExperimenterType', value)

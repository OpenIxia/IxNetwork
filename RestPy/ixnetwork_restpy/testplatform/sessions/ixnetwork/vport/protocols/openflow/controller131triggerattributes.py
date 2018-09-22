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
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('enableSendTriggerMeterConfigStatsLearnedInformation')
	@EnableSendTriggerMeterConfigStatsLearnedInformation.setter
	def EnableSendTriggerMeterConfigStatsLearnedInformation(self, value):
		self._set_attribute('enableSendTriggerMeterConfigStatsLearnedInformation', value)

	@property
	def EnableSendTriggerMeterFeatureStatsLearnedInformation(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('enableSendTriggerMeterFeatureStatsLearnedInformation')
	@EnableSendTriggerMeterFeatureStatsLearnedInformation.setter
	def EnableSendTriggerMeterFeatureStatsLearnedInformation(self, value):
		self._set_attribute('enableSendTriggerMeterFeatureStatsLearnedInformation', value)

	@property
	def EnableSendTriggerMeterStatLearnedInformation(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('enableSendTriggerMeterStatLearnedInformation')
	@EnableSendTriggerMeterStatLearnedInformation.setter
	def EnableSendTriggerMeterStatLearnedInformation(self, value):
		self._set_attribute('enableSendTriggerMeterStatLearnedInformation', value)

	@property
	def FlowStatOutGroup(self):
		"""The out group used.

		Returns:
			number
		"""
		return self._get_attribute('flowStatOutGroup')
	@FlowStatOutGroup.setter
	def FlowStatOutGroup(self, value):
		self._set_attribute('flowStatOutGroup', value)

	@property
	def FlowStatOutGroupInputMode(self):
		"""The input mode of the out group.

		Returns:
			str(allGroups|anyGroup|outGroupCustom)
		"""
		return self._get_attribute('flowStatOutGroupInputMode')
	@FlowStatOutGroupInputMode.setter
	def FlowStatOutGroupInputMode(self, value):
		self._set_attribute('flowStatOutGroupInputMode', value)

	@property
	def FlowStatOutPort(self):
		"""Specifies the Output port number.

		Returns:
			number
		"""
		return self._get_attribute('flowStatOutPort')
	@FlowStatOutPort.setter
	def FlowStatOutPort(self, value):
		self._set_attribute('flowStatOutPort', value)

	@property
	def FlowStatOutPortInputMode(self):
		"""The output port used.

		Returns:
			str(ofppInPort|ofppNormal|ofppFlood|ofppAll|ofppController|ofppLocal|ofppAny|outPortCustom)
		"""
		return self._get_attribute('flowStatOutPortInputMode')
	@FlowStatOutPortInputMode.setter
	def FlowStatOutPortInputMode(self, value):
		self._set_attribute('flowStatOutPortInputMode', value)

	@property
	def FlowStatTableId(self):
		"""The identifier of the table.

		Returns:
			number
		"""
		return self._get_attribute('flowStatTableId')
	@FlowStatTableId.setter
	def FlowStatTableId(self, value):
		self._set_attribute('flowStatTableId', value)

	@property
	def FlowStatTableIdInputMode(self):
		"""The identifier of the table.

		Returns:
			str(allTables|emergency|custom)
		"""
		return self._get_attribute('flowStatTableIdInputMode')
	@FlowStatTableIdInputMode.setter
	def FlowStatTableIdInputMode(self, value):
		self._set_attribute('flowStatTableIdInputMode', value)

	@property
	def IsMeterConfigStatLearnedInformationRefreshed(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('isMeterConfigStatLearnedInformationRefreshed')

	@property
	def IsMeterFeatureStatLearnedInformationRefreshed(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('isMeterFeatureStatLearnedInformationRefreshed')

	@property
	def IsMeterStatLearnedInformationRefreshed(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('isMeterStatLearnedInformationRefreshed')

	@property
	def MeterConfigStatMeterId(self):
		"""NOT DEFINED

		Returns:
			str(ofpmController|ofpmSlowPath|ofpmAll|manual)
		"""
		return self._get_attribute('meterConfigStatMeterId')
	@MeterConfigStatMeterId.setter
	def MeterConfigStatMeterId(self, value):
		self._set_attribute('meterConfigStatMeterId', value)

	@property
	def MeterConfigStatMeterNumber(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('meterConfigStatMeterNumber')
	@MeterConfigStatMeterNumber.setter
	def MeterConfigStatMeterNumber(self, value):
		self._set_attribute('meterConfigStatMeterNumber', value)

	@property
	def MeterConfigStatResponseTimeOut(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('meterConfigStatResponseTimeOut')
	@MeterConfigStatResponseTimeOut.setter
	def MeterConfigStatResponseTimeOut(self, value):
		self._set_attribute('meterConfigStatResponseTimeOut', value)

	@property
	def MeterFeatureStatResponseTimeOut(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('meterFeatureStatResponseTimeOut')
	@MeterFeatureStatResponseTimeOut.setter
	def MeterFeatureStatResponseTimeOut(self, value):
		self._set_attribute('meterFeatureStatResponseTimeOut', value)

	@property
	def MeterStatMeterId(self):
		"""NOT DEFINED

		Returns:
			str(ofpmController|ofpmSlowPath|ofpmAll|manual)
		"""
		return self._get_attribute('meterStatMeterId')
	@MeterStatMeterId.setter
	def MeterStatMeterId(self, value):
		self._set_attribute('meterStatMeterId', value)

	@property
	def MeterStatMeterNumber(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('meterStatMeterNumber')
	@MeterStatMeterNumber.setter
	def MeterStatMeterNumber(self, value):
		self._set_attribute('meterStatMeterNumber', value)

	@property
	def MeterStatResponseTimeOut(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('meterStatResponseTimeOut')
	@MeterStatResponseTimeOut.setter
	def MeterStatResponseTimeOut(self, value):
		self._set_attribute('meterStatResponseTimeOut', value)

	@property
	def PortStatPortNumber(self):
		"""The port number for port stat learned information.

		Returns:
			number
		"""
		return self._get_attribute('portStatPortNumber')
	@PortStatPortNumber.setter
	def PortStatPortNumber(self, value):
		self._set_attribute('portStatPortNumber', value)

	@property
	def PortStatPortNumberInputMode(self):
		"""The input mode of port number for port stat learned information.

		Returns:
			str(ofppAny|portNumberCustom)
		"""
		return self._get_attribute('portStatPortNumberInputMode')
	@PortStatPortNumberInputMode.setter
	def PortStatPortNumberInputMode(self, value):
		self._set_attribute('portStatPortNumberInputMode', value)

	@property
	def QueueConfigPortNumber(self):
		"""The port number for queue config learned information.

		Returns:
			number
		"""
		return self._get_attribute('queueConfigPortNumber')
	@QueueConfigPortNumber.setter
	def QueueConfigPortNumber(self, value):
		self._set_attribute('queueConfigPortNumber', value)

	@property
	def QueueConfigPortNumberInputMode(self):
		"""The input mode of port number for queue config learned information.

		Returns:
			str(ofppAny|portNumberCustom)
		"""
		return self._get_attribute('queueConfigPortNumberInputMode')
	@QueueConfigPortNumberInputMode.setter
	def QueueConfigPortNumberInputMode(self, value):
		self._set_attribute('queueConfigPortNumberInputMode', value)

	@property
	def QueueStatPortNumber(self):
		"""The port number for queue statistics learned information.

		Returns:
			number
		"""
		return self._get_attribute('queueStatPortNumber')
	@QueueStatPortNumber.setter
	def QueueStatPortNumber(self, value):
		self._set_attribute('queueStatPortNumber', value)

	@property
	def QueueStatPortNumberInputMode(self):
		"""The input mode of port number for queue statistics learned information.

		Returns:
			str(ofppAll|ofppAny|portNumberCustom)
		"""
		return self._get_attribute('queueStatPortNumberInputMode')
	@QueueStatPortNumberInputMode.setter
	def QueueStatPortNumberInputMode(self, value):
		self._set_attribute('queueStatPortNumberInputMode', value)

	@property
	def VendorMessageExperimenterType(self):
		"""Experimenter type for Vendor Message.

		Returns:
			number
		"""
		return self._get_attribute('vendorMessageExperimenterType')
	@VendorMessageExperimenterType.setter
	def VendorMessageExperimenterType(self, value):
		self._set_attribute('vendorMessageExperimenterType', value)

	@property
	def VendorStatExperimenterType(self):
		"""Experimenter type for Vendor stat.

		Returns:
			number
		"""
		return self._get_attribute('vendorStatExperimenterType')
	@VendorStatExperimenterType.setter
	def VendorStatExperimenterType(self, value):
		self._set_attribute('vendorStatExperimenterType', value)

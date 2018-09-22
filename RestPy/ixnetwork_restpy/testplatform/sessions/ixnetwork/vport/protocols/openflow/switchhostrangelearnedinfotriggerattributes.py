from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class SwitchHostRangeLearnedInfoTriggerAttributes(Base):
	"""The SwitchHostRangeLearnedInfoTriggerAttributes class encapsulates a required switchHostRangeLearnedInfoTriggerAttributes node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the SwitchHostRangeLearnedInfoTriggerAttributes property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'switchHostRangeLearnedInfoTriggerAttributes'

	def __init__(self, parent):
		super(SwitchHostRangeLearnedInfoTriggerAttributes, self).__init__(parent)

	@property
	def CustomPacket(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('customPacket')
	@CustomPacket.setter
	def CustomPacket(self, value):
		self._set_attribute('customPacket', value)

	@property
	def DestinationCustom(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('destinationCustom')
	@DestinationCustom.setter
	def DestinationCustom(self, value):
		self._set_attribute('destinationCustom', value)

	@property
	def DestinationCustomIpv4Address(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('destinationCustomIpv4Address')
	@DestinationCustomIpv4Address.setter
	def DestinationCustomIpv4Address(self, value):
		self._set_attribute('destinationCustomIpv4Address', value)

	@property
	def DestinationCustomIpv4AddressStep(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('destinationCustomIpv4AddressStep')
	@DestinationCustomIpv4AddressStep.setter
	def DestinationCustomIpv4AddressStep(self, value):
		self._set_attribute('destinationCustomIpv4AddressStep', value)

	@property
	def DestinationCustomMacAddress(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('destinationCustomMacAddress')
	@DestinationCustomMacAddress.setter
	def DestinationCustomMacAddress(self, value):
		self._set_attribute('destinationCustomMacAddress', value)

	@property
	def DestinationCustomMacAddressStep(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('destinationCustomMacAddressStep')
	@DestinationCustomMacAddressStep.setter
	def DestinationCustomMacAddressStep(self, value):
		self._set_attribute('destinationCustomMacAddressStep', value)

	@property
	def DestinationHostList(self):
		"""NOT DEFINED

		Returns:
			list(str[None|/api/v1/sessions/1/ixnetwork/vport?deepchild=switchHostRanges])
		"""
		return self._get_attribute('destinationHostList')
	@DestinationHostList.setter
	def DestinationHostList(self, value):
		self._set_attribute('destinationHostList', value)

	@property
	def MeshingType(self):
		"""NOT DEFINED

		Returns:
			str(fullyMesh)
		"""
		return self._get_attribute('meshingType')
	@MeshingType.setter
	def MeshingType(self, value):
		self._set_attribute('meshingType', value)

	@property
	def PacketType(self):
		"""NOT DEFINED

		Returns:
			str(arp|ping|custom)
		"""
		return self._get_attribute('packetType')
	@PacketType.setter
	def PacketType(self, value):
		self._set_attribute('packetType', value)

	@property
	def PeriodIntervalInMs(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('periodIntervalInMs')
	@PeriodIntervalInMs.setter
	def PeriodIntervalInMs(self, value):
		self._set_attribute('periodIntervalInMs', value)

	@property
	def Periodic(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('periodic')
	@Periodic.setter
	def Periodic(self, value):
		self._set_attribute('periodic', value)

	@property
	def PeriodicIterationNumber(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('periodicIterationNumber')
	@PeriodicIterationNumber.setter
	def PeriodicIterationNumber(self, value):
		self._set_attribute('periodicIterationNumber', value)

	@property
	def ResponseTimeout(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('responseTimeout')
	@ResponseTimeout.setter
	def ResponseTimeout(self, value):
		self._set_attribute('responseTimeout', value)

	@property
	def SourceHostList(self):
		"""NOT DEFINED

		Returns:
			list(str[None|/api/v1/sessions/1/ixnetwork/vport?deepchild=switchHostRanges])
		"""
		return self._get_attribute('sourceHostList')
	@SourceHostList.setter
	def SourceHostList(self, value):
		self._set_attribute('sourceHostList', value)
